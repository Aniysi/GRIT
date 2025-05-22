import pytest
from unittest.mock import patch, MagicMock
from plugin.commands.QueryLLM import QueryLLM
from plugin.utils.ResponseStructure import Response
from plugin.commands.CreateMessage import CreateMessage, Role
from plugin.utils.config import config

class TestQueryLLM:
    def setup_method(self):
        # Setup test data
        self.model = config.model_name
        self.messages = [
            {"role": "system", "content": "You are a git command helper"},
            {"role": "user", "content": "How do I commit changes?"}
        ]
        self.query_llm = QueryLLM(self.model, self.messages)

        # Expected response from LLM
        self.expected_json = {
            "explanation": "To commit changes in git, use git commit command",
            "command": "git commit -m 'your message'"
        }

    @patch('ollama.chat')
    def test_successful_query(self, mock_chat):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.message.content = Response(
            explanation="To commit changes in git, use git commit command",
            command="git commit -m 'your message'"
        ).model_dump_json()
        mock_chat.return_value = mock_response

        # Execute query
        result = self.query_llm.execute()

        # Verify chat was called with correct parameters
        mock_chat.assert_called_once_with(
            model=self.model,
            messages=self.messages,
            format=Response.model_json_schema()
        )

        # Verify response
        assert isinstance(result, Response)
        assert result.explanation == "To commit changes in git, use git commit command"
        assert result.command == "git commit -m 'your message'"

    @patch('ollama.chat')
    def test_invalid_response_format(self, mock_chat):
        # Setup mock response with invalid format
        mock_response = MagicMock()
        mock_response.message.content = '{"invalid": "format"}'
        mock_chat.return_value = mock_response

        # Test invalid response raises validation error
        with pytest.raises(ValueError):
            self.query_llm.execute()

    def test_empty_messages(self):
        # Test with empty messages list
        with pytest.raises(ValueError):
            QueryLLM(self.model, [])