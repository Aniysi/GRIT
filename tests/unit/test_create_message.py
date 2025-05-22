import pytest
from plugin.commands.CreateMessage import CreateMessage, Role

class TestCreateMessage:
    def setup_method(self):
        self.prompt = "Test prompt"
        self.context = "Test context with np.float64"
    
    def test_constructor_missing_required_params(self):
        with pytest.raises(TypeError):
            CreateMessage()
        with pytest.raises(TypeError):
            CreateMessage(Role.user)

    def test_constructor_invalid_role_type(self):
        with pytest.raises(TypeError):
            CreateMessage("invalid_role", self.prompt)

    def test_create_system_message_without_context(self):
        message = CreateMessage(Role.system, self.prompt)
        result = message.execute()
        
        assert result["role"] == "system"
        assert result["content"] == "Test prompt/no_think"

    def test_create_user_message_without_context(self):
        message = CreateMessage(Role.user, self.prompt)
        result = message.execute()
        
        assert result["role"] == "user"
        assert result["content"] == "Test prompt/no_think"

    def test_create_assistant_message_without_context(self):
        message = CreateMessage(Role.assistant, self.prompt)
        result = message.execute()
        
        assert result["role"] == "assistant"
        assert result["content"] == "Test prompt/no_think"

    def test_create_message_with_context(self):
        message = CreateMessage(Role.user, self.prompt, self.context)
        result = message.execute()
        
        assert result["role"] == "user"
        assert "Context:\nTest context with " in result["content"]
        assert "Query:\nTest prompt" in result["content"]
        assert "np.float64" not in result["content"]

    def test_create_message_with_empty_context(self):
        message = CreateMessage(Role.user, self.prompt, "")
        result = message.execute()
        
        assert result["role"] == "user"
        assert result["content"] == "Test prompt/no_think"