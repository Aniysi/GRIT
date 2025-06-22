import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path

import src.infrastructure.git_service.git_repository as git_repo

@patch("src.infrastructure.git_service.git_repository.Repo")
def test_get_remote_head_hash_success(mock_repo):
    mock_repo.return_value.git_dir = "some/.git"
    mock_repo.return_value.git.rev_parse.return_value = "abc123"
    assert git_repo.get_remote_head_hash("repo") == "abc123"

@patch("src.infrastructure.git_service.git_repository.Repo")
def test_get_remote_head_hash_fail(mock_repo):
    mock_repo.return_value.git_dir = None
    with pytest.raises(ValueError):
        git_repo.get_remote_head_hash("repo")

@patch("src.infrastructure.git_service.git_repository.Repo")
def test_get_file_annotate_success(mock_repo):
    mock_repo.return_value.git_dir = "some/.git"
    mock_repo.return_value.git.annotate.return_value = "annotate output"
    assert git_repo.get_file_annotate("hash", Path("file.py"), "repo") == "annotate output"

@patch("src.infrastructure.git_service.git_repository.Repo")
def test_get_file_annotate_fail(mock_repo):
    mock_repo.return_value.git_dir = "some/.git"
    mock_repo.return_value.git.annotate.side_effect = Exception("fail")
    with pytest.raises(ValueError):
        git_repo.get_file_annotate("hash", Path("file.py"), "repo")

@patch("src.infrastructure.git_service.git_repository.Repo")
def test_get_file_from_hash_success(mock_repo):
    mock_repo.return_value.git_dir = "some/.git"
    mock_repo.return_value.git.show.return_value = "file content"
    assert git_repo.get_file_from_hash("hash", Path("file.py"), "repo") == "file content"

@patch("src.infrastructure.git_service.git_repository.Repo")
def test_get_file_from_hash_fail(mock_repo):
    mock_repo.return_value.git_dir = "some/.git"
    mock_repo.return_value.git.show.side_effect = Exception("fail")
    with pytest.raises(ValueError):
        git_repo.get_file_from_hash("hash", Path("file.py"), "repo")

@patch("src.infrastructure.git_service.git_repository.Repo")
def test_create_custom_commit_success(mock_repo):
    mock_repo.return_value.git_dir = "some/.git"
    mock_repo.return_value.index.commit.return_value = True
    assert git_repo.create_custom_commit("title", "body", "repo")

@patch("src.infrastructure.git_service.git_repository.Repo")
def test_create_custom_commit_fail(mock_repo):
    mock_repo.return_value.git_dir = "some/.git"
    mock_repo.return_value.index.commit.side_effect = Exception("fail")
    with pytest.raises(ValueError):
        git_repo.create_custom_commit("title", "body", "repo")

@patch("src.infrastructure.git_service.git_repository.Path")
@patch("src.infrastructure.git_service.git_repository.Repo")
def test_get_conflicted_files_file(mock_repo, mock_path):
    # Simula file in conflitto
    mock_path.return_value.is_file.return_value = True
    mock_path.return_value.is_absolute.return_value = True
    mock_path.return_value.relative_to.return_value = Path("file.py")
    repo = mock_repo.return_value
    repo.git_dir = "some/.git"
    repo.git.ls_files.return_value = "C\tfile.py"
    repo.working_dir = "repo"
    result = git_repo.get_conflicted_files("file.py")
    assert isinstance(result, list)

@patch("src.infrastructure.git_service.git_repository.Path")
@patch("src.infrastructure.git_service.git_repository.Repo")
def test_get_conflicted_files_dir(mock_repo, mock_path):
    # Simula directory con file in conflitto
    mock_path.return_value.is_file.return_value = False
    mock_path.return_value.is_dir.return_value = True
    mock_path.return_value.is_absolute.return_value = True
    repo = mock_repo.return_value
    repo.git_dir = "some/.git"
    repo.git.ls_files.return_value = "C\tfile1.py\nC\tfile2.py"
    repo.working_dir = "repo"
    result = git_repo.get_conflicted_files("repo")
    assert isinstance(result, list)

@patch("src.infrastructure.git_service.git_repository.Repo")
def test_git_add_to_staging_success(mock_repo):
    mock_repo.return_value.git_dir = "some/.git"
    assert git_repo.git_add_to_staging(Path("file.py"), "repo")

@patch("src.infrastructure.git_service.git_repository.Repo")
def test_git_add_to_staging_fail(mock_repo):
    mock_repo.return_value.git_dir = "some/.git"
    mock_repo.return_value.git.add.side_effect = Exception("fail")
    with pytest.raises(ValueError):
        git_repo.git_add_to_staging(Path("file.py"), "repo")