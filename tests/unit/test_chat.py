import pytest
from src.domain.chat import ChatSession, ChatMessage, Role

class DummyDiff:
    def __str__(self):
        return "diff --git a/file.txt b/file.txt"

def test_chat_message_to_dict():
    msg = ChatMessage(role=Role.user, content="Hello")
    d = msg.to_dict()
    assert d["role"] == "user"
    assert d["content"] == "Hello"

def test_chat_session_add_and_pop():
    session = ChatSession()
    session.add_user_message("Hi")
    session.add_system_message("System msg")
    session.add_assistant_message("Assistant msg")
    assert len(session._messages) == 3
    last = session.pop_last_message()
    assert last._content == "Assistant msg"
    assert len(session._messages) == 2

def test_chat_session_clear():
    session = ChatSession()
    session.add_user_message("Hi")
    session.clear_messages()
    assert session._messages == []

def test_add_first_message():
    session = ChatSession()
    session.add_first_message("First system message")
    assert session._messages[0]._role == Role.system
    assert session._messages[0]._content == "First system message"

def test_add_diff_message():
    session = ChatSession()
    diff = DummyDiff()
    session.add_diff_message(diff)
    assert "Git diff" in session._messages[0]._content
    assert "diff --git" in session._messages[0]._content

def test_add_context_message():
    session = ChatSession()
    session.add_context_message("context", "query")
    assert "Here are some examples:" in session._messages[0]._content
    assert "context" in session._messages[0]._content
    assert "query" in session._messages[0]._content

def test_to_dict_list():
    session = ChatSession()
    session.add_user_message("Hi")
    session.add_system_message("Sys")
    dicts = session.to_dict_list()
    assert dicts[0]["role"] == "user"
    assert dicts[1]["role"] == "system"