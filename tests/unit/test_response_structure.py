import pytest
from pydantic import ValidationError

from src.domain.response_structure import (
    Mode, CommitMsg, Questions, CommitResponse, GitCommand,
    ImpactAnalisys, Status, ConflictResolutionResponse
)

def test_commit_msg_str():
    msg = CommitMsg(title="Fix bug", body="Fixed a bug in the system.")
    assert str(msg) == "Commit title: Fix bug\nCommit body: Fixed a bug in the system."

def test_questions_str_with_questions():
    q = Questions(questions=["What is your name?", "How old are you?"])
    expected = "Domande per l'utente:\n1. What is your name?\n2. How old are you?"
    assert str(q) == expected

def test_questions_str_empty():
    q = Questions(questions=[])
    assert str(q) == "Nessuna domanda disponibile."

def test_commit_response_commit_mode():
    commit = CommitMsg(title="Add feature", body="Added a new feature.")
    resp = CommitResponse(mode=Mode.COMMIT, commit=commit)
    assert str(resp) == str(commit)

def test_commit_response_question_mode():
    questions = Questions(questions=["Why did you change this?"])
    resp = CommitResponse(mode=Mode.QUESTION, questions=questions)
    assert str(resp) == str(questions)

def test_git_command_str():
    cmd = GitCommand(explanation="Initialize repo", command="git init")
    assert str(cmd) == "Explanation: Initialize repo\nCommand: git init"

def test_impact_analisys_str():
    ia = ImpactAnalisys(analisys="Low risk", rating=7)
    assert str(ia) == "Safety esteem: 7\nImpact anlisys: Low risk"

def test_impact_analisys_rating_bounds():
    ImpactAnalisys(analisys="Test", rating=1)
    ImpactAnalisys(analisys="Test", rating=10)
    with pytest.raises(ValidationError):
        ImpactAnalisys(analisys="Test", rating=0)
    with pytest.raises(ValidationError):
        ImpactAnalisys(analisys="Test", rating=11)

def test_conflict_resolution_response_resolved():
    resp = ConflictResolutionResponse(status=Status.RESOLVED, content="Merged", reason=None)
    assert resp.status == Status.RESOLVED
    assert resp.content == "Merged"
    assert resp.reason is None

def test_conflict_resolution_response_unresolved():
    resp = ConflictResolutionResponse(status=Status.UNRESOLVED, content=None, reason="Manual intervention required")
    assert resp.status == Status.UNRESOLVED
    assert resp.content is None
    assert resp.reason == "Manual intervention required"