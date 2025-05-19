import pytest
from unittest.mock import patch
from plugin.commands.GetInput import GetInput

class TestGetInput:
    
    def setup_method(self):
        self.get_input = GetInput()

    @patch('builtins.input', return_value='test query')
    def test_execute_normal_input(self, mock_input):
        result = self.get_input.execute()
        assert result == 'test query'

    @patch('builtins.input', return_value='/quit')
    def test_execute_quit_command(self, mock_input):
        with pytest.raises(SystemExit) as e:
            self.get_input.execute()
        assert e.value.code == 0