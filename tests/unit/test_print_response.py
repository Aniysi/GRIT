import pytest
from unittest.mock import patch
from io import StringIO
from plugin.commands.PrintResponse import PrintResponse
from plugin.utils.ResponseStructure import Response
from colorama import Fore, Style

class TestPrintResponse:
    def setup_method(self):
        # Sample response for testing
        self.response = Response(
            explanation="This command will show the git status",
            command="git status"
        )
        self.print_response = PrintResponse(self.response)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_simple_response(self, mock_stdout):
        # Execute the print command
        self.print_response.execute()
        
        # Get the printed output
        output = mock_stdout.getvalue()
        
        # Check if all parts are present in the output
        expected_output = Fore.GREEN + "LLM: " + Style.RESET_ALL + "This command will show the git status" + "\n\n\nCommand:  git status\n"
        assert expected_output in output

    def test_invalid_response_type(self):
        # Test with invalid response type
        with pytest.raises(TypeError):
            PrintResponse("not a response object")

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_complex_command(self, mock_stdout):
        # Test with a more complex response
        complex_response = Response(
            explanation="This command will commit with a message",
            command='git commit --message="Initial commit"'
        )
        printer = PrintResponse(complex_response)
        printer.execute()
        
        output = mock_stdout.getvalue()
        assert 'git commit --message="Initial commit"' in output
        assert "This command will commit with a message" in output

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_response_with_special_chars(self, mock_stdout):
        # Test with special characters in the response
        special_response = Response(
            explanation="Test with special chars: àèìòù",
            command="git log --pretty=format:'%h - %an, %ar : %s'"
        )
        printer = PrintResponse(special_response)
        printer.execute()
        
        output = mock_stdout.getvalue()
        assert "Test with special chars: àèìòù" in output
        assert "git log --pretty=format:'%h - %an, %ar : %s'" in output