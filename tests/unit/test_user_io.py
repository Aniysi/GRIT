import pytest
from unittest.mock import patch, MagicMock
from src.cli.user_io import UserIO

@patch("src.cli.user_io.console.input")
def test_ask_query(mock_input):
    mock_input.return_value = "test input"
    ui = UserIO()
    result = ui.ask_query()
    assert result == "test input"

@patch("src.cli.user_io.console.print")
def test_display_message(mock_print):
    ui = UserIO()
    ui.display_message("hello")
    mock_print.assert_called_once_with("hello")

@patch("src.cli.user_io.console.print")
def test_display_error(mock_print):
    ui = UserIO()
    ui.display_error("error!")
    mock_print.assert_called_once()
    assert "[red]❌ error![/red]" in str(mock_print.call_args)

@patch("src.cli.user_io.console.print")
def test_display_success(mock_print):
    ui = UserIO()
    ui.display_success("ok!")
    mock_print.assert_called_once()
    assert "[green]ok![/green]" in str(mock_print.call_args)

@patch("src.cli.user_io.console.print")
def test_display_output(mock_print):
    ui = UserIO()
    ui.display_output("output")
    args, kwargs = mock_print.call_args
    panel = args[0]
    assert hasattr(panel, "renderable")
    assert "output" in panel.renderable
    assert panel.title == "Output"

@patch("src.cli.user_io.console.print")
def test_display_question(mock_print):
    ui = UserIO()
    ui.display_question("question?")
    args, kwargs = mock_print.call_args
    panel = args[0]
    assert hasattr(panel, "renderable")
    assert "question?" in panel.renderable

@patch("src.cli.user_io.console.print")
def test_display_cmd_help(mock_print):
    ui = UserIO()
    ui.display_cmd_help()
    args, kwargs = mock_print.call_args
    panel = args[0]
    assert hasattr(panel, "renderable")
    assert "Available commands" in panel.renderable

@patch("src.cli.user_io.console.print")
def test_display_commit_help(mock_print):
    ui = UserIO()
    ui.display_commit_help()
    args, kwargs = mock_print.call_args
    panel = args[0]
    assert hasattr(panel, "renderable")
    assert "Available commands" in panel.renderable