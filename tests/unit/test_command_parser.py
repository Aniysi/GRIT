from src.cli.command_parser import CLICommandParser, CLICommandType, ParsedCLICommand

import pytest

@pytest.fixture
def parser():
    return CLICommandParser()

def test_parse_empty(parser):
    result = parser.parse("")
    assert result.command_type == CLICommandType.REGULAR
    assert result.content == ""

def test_parse_quit(parser):
    result = parser.parse("/quit")
    assert result.command_type == CLICommandType.QUIT

def test_parse_exec(parser):
    result = parser.parse("/exec")
    assert result.command_type == CLICommandType.EXEC

def test_parse_fix(parser):
    result = parser.parse("/fix")
    assert result.command_type == CLICommandType.FIX

def test_parse_refine(parser):
    result = parser.parse("/refine improve the command")
    assert result.command_type == CLICommandType.REFINE
    assert result.content == "improve the command"

def test_parse_refine_strip(parser):
    result = parser.parse("/refine    add more tests   ")
    assert result.command_type == CLICommandType.REFINE
    assert result.content == "add more tests"

def test_parse_commit(parser):
    result = parser.parse("/commit")
    assert result.command_type == CLICommandType.COMMIT

def test_parse_regular(parser):
    result = parser.parse("just a normal request")
    assert result.command_type == CLICommandType.REGULAR
    assert result.content == "just a normal request"

def test_parse_case_insensitive(parser):
    result = parser.parse("/QuIt")
    assert result.command_type == CLICommandType.QUIT