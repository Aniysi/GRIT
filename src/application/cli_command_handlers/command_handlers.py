from abc import ABC, abstractmethod
from cli.user_io import UserIO
from domain.chat import ChatSession
from infrastructure.llm.llm_client import LLMClient
from application.rag.rag_context_builder import RAGContextBuilder
from config.config import load_config
from domain.response_structure import GitCommand
from domain.response_structure import CommitMsg
from infrastructure.git_service.git_repository import create_custom_commit


import subprocess
import sys
import os

class CommandHandler(ABC):
    @abstractmethod
    def handle(self, content: str, context: dict) -> bool:
        """Returns True if conversation should continue, False if should exit"""
        pass

class QuitHandler(CommandHandler):
    def __init__(self, user_io: UserIO):
        self._user_io = user_io
        
    def handle(self, content: str, context: dict) -> bool:
        self._user_io.display_message("[yellow]👋 Programma terminato.[/yellow]")
        return False
    

class ExecHandler(CommandHandler):
    def __init__(self, user_io: UserIO):
        self._user_io = user_io
        
    def handle(self, content: str, context: dict) -> bool:
        last_command = context.get('last_generated_command')
        if not last_command:
            self._user_io.display_error("Nessun comando da eseguire. Genera prima un comando.")
            return True
            
        try:
            result = subprocess.run(
                last_command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                shell=True,
                text=True,
                env={**os.environ, 'GIT_PAGER': 'cat'},
                timeout=60
            )
            
            if result.returncode == 0:
                self._user_io.display_success("Comando eseguito con successo!")
                if result.stdout:
                    self._user_io.display_output(result.stdout)
                context['last_execution_success'] = True
                context['last_execution_error'] = None
            else:
                self._user_io.display_error(f"Comando fallito con codice {result.returncode}")
                if result.stderr:
                    self._user_io.display_error(result.stderr)
                context['last_execution_success'] = False
                context['last_execution_error'] = result.stderr
                
        except subprocess.TimeoutExpired:
            self._user_io.display_error("Comando interrotto per timeout")
            context['last_execution_success'] = False
            context['last_execution_error'] = "Timeout expired"
        except Exception as e:
            self._user_io.display_error(f"Errore nell'esecuzione: {str(e)}")
            context['last_execution_success'] = False
            context['last_execution_error'] = str(e)
            
        return True

class RefineCmdHandler(CommandHandler):
    def __init__(self, llm_client: LLMClient, chat_session: ChatSession, user_io: UserIO):
        self._llm_client = llm_client
        self._chat_session = chat_session
        self._user_io = user_io
        
    def handle(self, content: str, context: dict) -> bool:
        if not content:
            self._user_io.display_error("Specifica le correzioni da applicare dopo /refine")
            return True
            
        last_command = context.get('last_generated_command')
        if not last_command:
            self._user_io.display_error("Nessun comando da raffinare. Genera prima un comando.")
            return True
            
        # Add refinement request to chat
        refinement_message = f"Correct command '{last_command}' applying the following changes: {content}"
        self._chat_session.add_user_message(refinement_message)
        
        # Generate refined command
        response = self._llm_client.generate_structured_response(self._chat_session, GitCommand)
        refined_command = str(response)
        
        # Display command and add it to conversation context
        self._user_io.display_message(f"[green]Comando raffinato:[/green]\n{refined_command}")
        self._chat_session.add_assistant_message(refined_command)
        context['last_generated_command'] = response.command
        
        return True

class FixHandler(CommandHandler):
    def __init__(self, llm_client: LLMClient, chat_session: ChatSession, user_io: UserIO):
        self._llm_client = llm_client
        self._chat_session = chat_session
        self._user_io = user_io
        
    def handle(self, content: str, context: dict) -> bool:
        last_error = context.get('last_execution_error')
        last_command = context.get('last_generated_command')
        
        if not last_error or context.get('last_execution_success', True):
            self._user_io.display_error("Nessun errore da correggere. Esegui prima un comando che fallisce.")
            return True
            
        # Add fix request to chat
        fix_message = f"The command '{last_command}' failed with the following error: {last_error}. Correct the given git command."
        self._chat_session.add_user_message(fix_message)
        
        # Generate fixed command
        response = self._llm_client.generate_structured_response(self._chat_session, GitCommand)
        fixed_command = str(response)
        
        # Display command and add it to conversation context
        self._user_io.display_message(f"[green]Comando corretto:[/green] {fixed_command}")
        self._chat_session.add_assistant_message(fixed_command)
        context['last_generated_command'] = response.command
        context['last_execution_error'] = None  # Reset error
        
        return True

class RegularHandler(CommandHandler):
    def __init__(self, llm_client: LLMClient, chat_session: ChatSession, user_io: UserIO, context_builder: RAGContextBuilder):
        self._llm_client = llm_client
        self._chat_session = chat_session
        self._user_io = user_io
        self._context_builder = context_builder
        
    def handle(self, content: str, context: dict) -> bool:
        if not content:
            return True
            
        # Get config 
        config=load_config()

        # Get context true hybrid search
        self._chat_session.add_user_message(content)
        rag_context = self._context_builder.build_context(content, config["embedding-model"])
        self._chat_session.add_context_message(rag_context, content)
        
        # Get llm generated command
        response = self._llm_client.generate_structured_response(self._chat_session, GitCommand)
        generated_command = str(response)
        
        # Display command and add it to conversation context
        self._user_io.display_message(f"[green]Comando suggerito:[/green]\n{generated_command}")
        self._chat_session.add_assistant_message(generated_command)
        context['last_generated_command'] = response.command
        return True
    
class CommitHandler(CommandHandler):
    def __init__(self, user_io):
        self._user_io = user_io

    def handle(self, content: str, commit: dict):
        if (create_custom_commit(commit['commit_title'], commit['commit_body'])):
            self._user_io.display_success("Commit succesfull!")
        else:
            self._user_io.display_error("Unable to commit changes")
        return False
    
class RefineCommitHandler(CommandHandler):
    def __init__(self, llm_client: LLMClient, chat_session: ChatSession, user_io: UserIO):
        self._llm_client = llm_client
        self._chat_session = chat_session
        self._user_io = user_io
    
    def handle(self, content: str, commit: dict):
        if not content:
            self._user_io.display_error("Specify your corrections after /refine")
            return True
        
        correction_msg = f"""
        You previously produced the following commit message:

        Commit title: {commit['commit_title']}
        Commit body {commit['commit_body']}

        Now apply the following correction to the commit message:

        **{content}**
        """ 

        # Add chat message to chat session
        self._chat_session.add_user_message(correction_msg)

        return True
    
        

