import pytest
from unittest.mock import MagicMock, patch
from src.infrastructure.git_service.git_diff import Diff

@patch("src.infrastructure.git_service.git_diff.Repo")
def test_diff_init_success(mock_repo):
    mock_repo.return_value.git_dir = "some/.git"
    d = Diff()
    assert d.repo is mock_repo.return_value

@patch("src.infrastructure.git_service.git_diff.Repo")
def test_diff_init_fail(mock_repo):
    mock_repo.return_value.git_dir = None
    with pytest.raises(ValueError):
        Diff()

@patch("src.infrastructure.git_service.git_diff.Repo")
def test_get_staged_diff_success(mock_repo):
    repo = mock_repo.return_value
    repo.git.diff.side_effect = ["file1.py\nfile2.py", "diff content"]
    d = Diff()
    result = d.get_staged_diff()
    assert result == "diff content"
    assert repo.git.diff.call_count == 2

@patch("src.infrastructure.git_service.git_diff.Repo")
def test_get_staged_diff_no_files(mock_repo):
    repo = mock_repo.return_value
    repo.git.diff.return_value = ""
    d = Diff()
    with pytest.raises(ValueError, match="No files are currently staged"):
        d.get_staged_diff()

@patch("src.infrastructure.git_service.git_diff.os.path.isfile")
@patch("src.infrastructure.git_service.git_diff.Repo")
def test_get_file_diff_success(mock_repo, mock_isfile):
    mock_isfile.return_value = True
    repo = mock_repo.return_value
    repo.git.diff.return_value = "file diff"
    d = Diff()
    result = d.get_file_diff("file1.py", "HEAD")
    assert result == "file diff"
    repo.git.diff.assert_called_once_with("HEAD", "--cached", "file1.py")

@patch("src.infrastructure.git_service.git_diff.os.path.isfile")
@patch("src.infrastructure.git_service.git_diff.Repo")
def test_get_file_diff_file_not_exist(mock_repo, mock_isfile):
    mock_isfile.return_value = False
    d = Diff()
    with pytest.raises(ValueError, match="does not exist or is not a valid file"):
        d.get_file_diff("file1.py", "HEAD")