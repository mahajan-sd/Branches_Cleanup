import pytest
import branches_cleanup.cli as cli


def test_no_token(monkeypatch, capsys):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    with pytest.raises(SystemExit):
        cli.main(["--owner", "o", "--repo", "r"])
    captured = capsys.readouterr()
    assert "Error: GitHub token" in captured.err


def test_abort(monkeypatch, capsys):
    # simulate listing and filtering
    class DummyClient:
        def list_branches(self, o, r):
            return ["b1"]

        def filter_branches(self, branches, pattern=None, names=None):
            return ["b1"]

    monkeypatch.setattr(cli, "GitHubClient", lambda token: DummyClient())
    monkeypatch.setattr("builtins.input", lambda prompt: "n")
    cli.main(["--owner","o","--repo","r","--token","t"])
    captured = capsys.readouterr()
    assert "Aborted" in captured.out
