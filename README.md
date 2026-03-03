# Branches Cleanup

This project provides a CLI utility to delete branches from a GitHub repository using the GitHub API.

## Features

- **List branches** in a repository
- **Fetch branch metadata** (commit date, age, merge status)
- **Generate reports** (CSV/JSON) with branch information and auto-delete flags
- **Delete branches** matching a pattern or explicit names
- **Uses GitHub API** with personal access tokens for authentication

## Getting Started

### Prerequisites

- Python 3.10+
- A GitHub personal access token with `repo` scope

### Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Usage

#### Interactive Mode (Recommended)

Run the tool without arguments to get an interactive menu:

```bash
python -m branches_cleanup
```

This will guide you through:
1. Generating a branch report
2. Deleting branches with confirmation
3. Exiting

#### Command-Line Mode

##### 1. Generate Branch Report

##### 1. Generate Branch Report

```bash
python -m branches_cleanup report \
    --owner OWNER --repo REPO \
    --token <TOKEN> \
    --output branches_report.csv \
    --min-age 30 \
    --include-merged
```

Options:

- `--owner`: GitHub account or organization
- `--repo`: Repository name
- `--token`: Personal access token (or set `GITHUB_TOKEN` environment variable)
- `--output`: Output file path (supports `.csv` or `.json`, default: `branches_report.csv`)
- `--min-age`: Mark branches older than this many days for deletion (default: 30)
- `--include-merged`: Also mark merged branches for deletion

**Output format:**  
The report CSV/JSON contains:
- `name`: Branch name
- `last_commit_date`: ISO timestamp of last commit
- `days_old`: Age of the branch in days
- `last_commit_sha`: Commit hash
- `is_merged`: Whether the branch is merged into main
- `should_delete`: Flag indicating if it should be deleted

##### 2. Delete Branches

```bash
python -m branches_cleanup delete \
    --owner OWNER --repo REPO \
    --token <TOKEN> \
    --pattern "feature/.*"
```

Or delete specific branches:

```bash
python -m branches_cleanup delete \
    --owner OWNER --repo REPO \
    --token <TOKEN> \
    --branch "old-feature-1" \
    --branch "old-feature-2"
```

The tool will prompt for confirmation before deleting any branches.

### Testing

```bash
pip install -r requirements-dev.txt
pytest
```
