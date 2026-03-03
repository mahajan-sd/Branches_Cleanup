import re
from datetime import datetime
from github import Github
from typing import List, Optional
from .branch_report import BranchInfo


class GitHubClient:
    def __init__(self, token: str):
        self._gh = Github(token)

    def list_branches(self, owner: str, repo: str) -> List[str]:
        """Return names of branches in the given repository."""
        repository = self._gh.get_repo(f"{owner}/{repo}")
        return [b.name for b in repository.get_branches()]

    def delete_branch(self, owner: str, repo: str, branch: str) -> None:
        """Delete a single branch (must not be default)."""
        repository = self._gh.get_repo(f"{owner}/{repo}")
        ref = repository.get_git_ref(f"heads/{branch}")
        ref.delete()

    def filter_branches(
        self,
        branches: List[str],
        pattern: Optional[str] = None,
        names: Optional[List[str]] = None,
    ) -> List[str]:
        """Return subset of branch names matching pattern or in names list."""
        if pattern:
            regex = re.compile(pattern)
            branches = [b for b in branches if regex.search(b)]
        if names:
            branches = [b for b in branches if b in names]
        return branches

    def get_branch_info(self, owner: str, repo: str, branch_name: str) -> BranchInfo:
        """Fetch detailed metadata for a single branch."""
        repository = self._gh.get_repo(f"{owner}/{repo}")
        branch = repository.get_branch(branch_name)
        
        # Get commit date
        commit = branch.commit
        last_commit_date = commit.commit.author.date
        last_commit_sha = commit.sha
        
        # Calculate age in days
        days_old = (datetime.now(last_commit_date.tzinfo) - last_commit_date).days
        
        # Check if merged
        default_branch = repository.default_branch
        is_merged = False
        try:
            if branch_name != default_branch:
                # Check if this branch is in the default branch's history
                merge_base = repository.get_commit(
                    repository.compare(default_branch, branch_name).merge_base.sha
                )
                is_merged = merge_base.sha == commit.sha
        except Exception:
            is_merged = False
        
        return BranchInfo(
            name=branch_name,
            last_commit_date=last_commit_date.isoformat(),
            days_old=days_old,
            last_commit_sha=last_commit_sha,
            is_merged=is_merged,
            should_delete=False,
        )

    def get_all_branches_info(self, owner: str, repo: str) -> List[BranchInfo]:
        """Fetch metadata for all branches in repo."""
        branches = self.list_branches(owner, repo)
        return [self.get_branch_info(owner, repo, b) for b in branches]
