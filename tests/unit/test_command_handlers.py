import pytest
from unittest.mock import MagicMock, patch
from src.application.cli_command_handlers.command_handlers import (
    QuitHandler, ExecHandler, RefineCmdHandler, FixHandler,
    RegularHandler, CommitHandler, RefineCommitHandler
)

import warnings
warnings.filterwarnings("ignore")

# QuitHandler
def test_quit_handler():
    mock_io = MagicMock()
    handler = QuitHandler(mock_io)
    result = handler.handle("any", {})
    mock_io.display_message.assert_called_once_with("[yellow]Program terminated.[/yellow]")
    assert result is False

# ExecHandler - success
@patch("src.application.cli_command_handlers.command_handlers.subprocess.run")
def test_exec_handler_success(mock_run):
    mock_io = MagicMock()
    handler = ExecHandler(mock_io)
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = "ok"
    mock_run.return_value.stderr = ""
    context = {"last_generated_command": "echo ok"}
    result = handler.handle("", context)
    mock_io.display_success.assert_called_once()
    mock_io.display_output.assert_called_once_with("ok")
    assert context["last_execution_success"] is True
    assert result is True

# ExecHandler - no command
def test_exec_handler_no_command():
    mock_io = MagicMock()
    handler = ExecHandler(mock_io)
    context = {}
    result = handler.handle("", context)
    mock_io.display_error.assert_called_once()
    assert result is True

# RefineCmdHandler
def test_refine_cmd_handler():
    mock_llm = MagicMock()
    mock_chat = MagicMock()
    mock_io = MagicMock()
    handler = RefineCmdHandler(mock_llm, mock_chat, mock_io)
    context = {"last_generated_command": "ls"}
    mock_llm.generate_structured_response.return_value = MagicMock(command="ls -l")
    result = handler.handle("add -l", context)
    mock_chat.add_user_message.assert_called()
    mock_io.display_message.assert_called()
    assert context["last_generated_command"] == "ls -l"
    assert result is True

def test_refine_cmd_handler_no_content():
    mock_llm = MagicMock()
    mock_chat = MagicMock()
    mock_io = MagicMock()
    handler = RefineCmdHandler(mock_llm, mock_chat, mock_io)
    context = {"last_generated_command": "ls"}
    result = handler.handle("", context)
    mock_io.display_error.assert_called_once()
    assert result is True

def test_refine_cmd_handler_no_last_command():
    mock_llm = MagicMock()
    mock_chat = MagicMock()
    mock_io = MagicMock()
    handler = RefineCmdHandler(mock_llm, mock_chat, mock_io)
    context = {}
    result = handler.handle("add -l", context)
    mock_io.display_error.assert_called_once()
    assert result is True

# FixHandler
def test_fix_handler():
    mock_llm = MagicMock()
    mock_chat = MagicMock()
    mock_io = MagicMock()
    handler = FixHandler(mock_llm, mock_chat, mock_io)
    context = {
        "last_execution_error": "fail",
        "last_generated_command": "ls",
        "last_execution_success": False
    }
    mock_llm.generate_structured_response.return_value = MagicMock(command="ls -l")
    result = handler.handle("", context)
    mock_chat.add_user_message.assert_called()
    mock_io.display_message.assert_called()
    assert context["last_generated_command"] == "ls -l"
    assert context["last_execution_error"] is None
    assert result is True

def test_fix_handler_no_error():
    mock_llm = MagicMock()
    mock_chat = MagicMock()
    mock_io = MagicMock()
    handler = FixHandler(mock_llm, mock_chat, mock_io)
    context = {"last_execution_success": True}
    result = handler.handle("", context)
    mock_io.display_error.assert_called_once()
    assert result is True

# RegularHandler
@patch("src.application.cli_command_handlers.command_handlers.load_config")
def test_regular_handler(mock_load_config):
    mock_llm = MagicMock()
    mock_chat = MagicMock()
    mock_io = MagicMock()
    mock_context_builder = MagicMock()
    handler = RegularHandler(mock_llm, mock_chat, mock_io, mock_context_builder)
    mock_load_config.return_value = {"embedding-model": "model"}
    mock_llm.generate_structured_response.return_value = MagicMock(command="ls")
    context = {}
    result = handler.handle("list files", context)
    mock_chat.add_user_message.assert_called_once_with("list files")
    mock_chat.add_context_message.assert_called()
    mock_llm.generate_structured_response.assert_called()
    mock_io.display_output.assert_called()
    mock_chat.add_assistant_message.assert_called()
    assert context["last_generated_command"] == "ls"
    assert result is True

# CommitHandler
@patch("src.application.cli_command_handlers.command_handlers.create_custom_commit")
def test_commit_handler_success(mock_create_commit):
    mock_create_commit.return_value = True
    mock_io = MagicMock()
    handler = CommitHandler(mock_io)
    commit = {"commit_title": "t", "commit_body": "b"}
    result = handler.handle("", commit)
    mock_io.display_success.assert_called_once()
    assert result is False

@patch("src.application.cli_command_handlers.command_handlers.create_custom_commit")
def test_commit_handler_fail(mock_create_commit):
    mock_create_commit.return_value = False
    mock_io = MagicMock()
    handler = CommitHandler(mock_io)
    commit = {"commit_title": "t", "commit_body": "b"}
    result = handler.handle("", commit)
    mock_io.display_error.assert_called_once()
    assert result is False

# RefineCommitHandler
def test_refine_commit_handler():
    mock_llm = MagicMock()
    mock_chat = MagicMock()
    mock_io = MagicMock()
    handler = RefineCommitHandler(mock_llm, mock_chat, mock_io)
    commit = {"commit_title": "t", "commit_body": "b"}
    result = handler.handle("fix typo", commit)
    mock_chat.add_user_message.assert_called()
    assert result is True

def test_refine_commit_handler_no_content():
    mock_llm = MagicMock()
    mock_chat = MagicMock()
    mock_io = MagicMock()
    handler = RefineCommitHandler(mock_llm, mock_chat, mock_io)
    commit = {"commit_title": "t", "commit_body": "b"}
    result = handler.handle("", commit)
    mock_io.display_error.assert_called_once()
    assert result is True