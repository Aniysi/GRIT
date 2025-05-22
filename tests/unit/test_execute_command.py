from plugin.commands.ExecuteCommand import ExecuteCommand
from plugin.utils.ResponseStructure import Response

import pytest
from unittest.mock import patch, MagicMock
import subprocess
import os
from io import StringIO

class TestExecuteCommand:
    def setup_method(self):
        # Create a mock Response object
        self.mock_response = MagicMock(spec=Response)
        self.mock_response.getCmdString.return_value = "git status"
        self.execute_command = ExecuteCommand(self.mock_response)

    @patch('subprocess.run')
    def test_successful_command_with_output(self, mock_run):
        # Setup mock subprocess.run
        mock_process = MagicMock()
        mock_process.stdout = "On branch main\nYour branch is up to date."
        mock_process.stderr = ""
        mock_run.return_value = mock_process

        # Execute command
        result = self.execute_command.execute()

        # Verify subprocess.run was called correctly
        mock_run.assert_called_once_with(
            "git status",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True,
            env={**os.environ, 'GIT_PAGER': 'cat'}
        )
        assert result.stdout == "On branch main\nYour branch is up to date."
        assert result.stderr == ""

    @patch('subprocess.run')
    @patch('sys.stderr', new_callable=StringIO)
    def test_command_with_error(self, mock_stderr, mock_run):
        # Setup mock subprocess.run with error
        mock_process = MagicMock()
        mock_process.stdout = ""
        mock_process.stderr = "fatal: not a git repository"
        mock_run.return_value = mock_process

        # Execute command
        self.execute_command.execute()

        # Verify the command was called correctly
        mock_run.assert_called_once_with(
            "git status",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True,
            env={**os.environ, 'GIT_PAGER': 'cat'}
        )

        # Verify error was printed to stderr
        assert "fatal: not a git repository" in mock_stderr.getvalue()

    @patch('subprocess.run')
    @patch('sys.stderr', new_callable=StringIO)
    def test_command_raises_exception(self, mock_stderr, mock_run):
        # Setup mock to raise an exception
        mock_run.side_effect = Exception("Command failed")

        # Test that system exit is called
        with pytest.raises(SystemExit) as exc_info:
            self.execute_command.execute()
        
        assert "An exception has occurred: " in mock_stderr.getvalue()
        assert exc_info.value.code == 1

    def test_invalid_command_type(self):
        # Test constructor with invalid command type
        with pytest.raises(TypeError):
            ExecuteCommand("invalid command")