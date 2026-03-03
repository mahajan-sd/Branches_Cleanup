import pytest
from branches_cleanup.github_client import GitHubClient


class DummyRepo:
    def __init__(self, branches):
        self._branches = branches

    def get_branches(self):
        class Branch:
            def __init__(self, name):
                self.name = name

        return [Branch(n) for n in self._branches]

    def get_git_ref(self, ref):
        class Ref:
            def __init__(self, name):
                self.name = name

            def delete(self):
                if "fail" in self.name:
                    raise Exception("delete error")

        return Ref(ref)


class DummyGH:
    def __init__(self, repo):
        self._repo = repo

    def get_repo(self, full_name):
        return self._repo


@pytest.fixture
def client(monkeypatch):
    dummy = GitHubClient("token")
    monkeypatch.setattr(dummy, "_gh", DummyGH(DummyRepo(["main", "feature/x"])))
    return dummy


def test_list_branches(client):
    assert client.list_branches("o", "r") == ["main", "feature/x"]


def test_filter_branches_pattern(client):
    result = client.filter_branches(["a", "b1", "b2"], pattern="b")
    assert result == ["b1", "b2"]


def test_filter_branches_names(client):
    result = client.filter_branches(["a", "b1", "b2"], names=["b2"]) 
    assert result == ["b2"]


def test_delete_branch_success(client):
    client.delete_branch("o", "r", "main")  # no exception


def test_delete_branch_failure(client):
    with pytest.raises(Exception):
        client.delete_branch("o", "r", "fail")
