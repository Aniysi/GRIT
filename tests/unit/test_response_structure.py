import pytest
from plugin.utils.ResponseStructure import Response

class TestResponseStructure:
    def setup_method(self):
        # Basic response for testing
        self.basic_response = Response(
            explanation="This is a git commit command",
            command="git commit -m Initial commit"
        )

    def test_response_creation(self):
        assert self.basic_response.explanation == "This is a git commit command"
        assert self.basic_response.command == "git commit -m Initial commit"

    def test_to_json(self):
        json_str = self.basic_response.toJson()
        assert '"explanation": "This is a git commit command"' in json_str
        assert '"command": "git commit -m Initial commit"' in json_str

    def test_get_cmd_string_basic(self):
        response = Response(
            explanation="Basic command",
            command="git status"
        )
        assert response.getCmdString() == "git status"

    def test_get_cmd_string_with_flag_value(self):
        response = Response(
            explanation="Command with flag and value",
            command="git commit --since=1 week ago"
        )
        assert response.getCmdString() == 'git commit --since="1 week ago"'

    def test_get_cmd_string_with_pretty_format_flag(self):
        response = Response(
            explanation="Command git log with pretty format flag and value",
            command="git commit --pretty=format:%an <%h>"
        )
        assert response.getCmdString() == 'git commit --pretty="format:%an <%h>"'