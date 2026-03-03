import pytest
import json
import csv
import tempfile
import os
from datetime import datetime, timezone
from branches_cleanup.branch_report import BranchInfo, BranchReport


@pytest.fixture
def sample_branches():
    return [
        BranchInfo(
            name="main",
            last_commit_date=datetime.now(timezone.utc).isoformat(),
            days_old=0,
            last_commit_sha="abc123",
            is_merged=False,
            should_delete=False,
        ),
        BranchInfo(
            name="feature/old",
            last_commit_date="2025-01-01T00:00:00+00:00",
            days_old=61,
            last_commit_sha="def456",
            is_merged=True,
            should_delete=True,
        ),
    ]


def test_branch_info_initialization(sample_branches):
    assert sample_branches[0].name == "main"
    assert sample_branches[0].days_old == 0
    assert sample_branches[1].is_merged is True


def test_report_csv_roundtrip(sample_branches):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        filepath = f.name
    
    try:
        report = BranchReport(sample_branches)
        report.save_csv(filepath)
        
        loaded_report = BranchReport.load_csv(filepath)
        assert len(loaded_report.branches) == 2
        assert loaded_report.branches[0].name == "main"
        assert loaded_report.branches[1].should_delete is True
    finally:
        os.unlink(filepath)


def test_report_json_roundtrip(sample_branches):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        filepath = f.name
    
    try:
        report = BranchReport(sample_branches)
        report.save_json(filepath)
        
        loaded_report = BranchReport.load_json(filepath)
        assert len(loaded_report.branches) == 2
        assert loaded_report.branches[0].name == "main"
        assert loaded_report.branches[1].is_merged is True
    finally:
        os.unlink(filepath)


def test_report_print(sample_branches, capsys):
    report = BranchReport(sample_branches)
    report.print_report()
    captured = capsys.readouterr()
    assert "main" in captured.out
    assert "feature/old" in captured.out
    assert "2 branches" in captured.out
