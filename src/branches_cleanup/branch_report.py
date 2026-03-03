import csv
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional


@dataclass
class BranchInfo:
    """Data class to represent a branch with metadata."""
    name: str
    last_commit_date: str
    days_old: int
    last_commit_sha: str
    is_merged: bool
    should_delete: bool = False

    def to_dict(self):
        return asdict(self)


class BranchReport:
    def __init__(self, branches: List[BranchInfo]):
        self.branches = branches

    def save_csv(self, filepath: str) -> None:
        """Save branch report to CSV file."""
        if not self.branches:
            return
        
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "name",
                    "last_commit_date",
                    "days_old",
                    "last_commit_sha",
                    "is_merged",
                    "should_delete",
                ],
            )
            writer.writeheader()
            for branch in self.branches:
                writer.writerow(branch.to_dict())

    def save_json(self, filepath: str) -> None:
        """Save branch report to JSON file."""
        data = [b.to_dict() for b in self.branches]
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load_csv(cls, filepath: str) -> "BranchReport":
        """Load branch report from CSV file."""
        branches = []
        with open(filepath, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                branch = BranchInfo(
                    name=row["name"],
                    last_commit_date=row["last_commit_date"],
                    days_old=int(row["days_old"]),
                    last_commit_sha=row["last_commit_sha"],
                    is_merged=row["is_merged"].lower() == "true",
                    should_delete=row["should_delete"].lower() == "true",
                )
                branches.append(branch)
        return cls(branches)

    @classmethod
    def load_json(cls, filepath: str) -> "BranchReport":
        """Load branch report from JSON file."""
        with open(filepath, "r") as f:
            data = json.load(f)
        branches = [BranchInfo(**item) for item in data]
        return cls(branches)

    def print_report(self) -> None:
        """Print branch report to console."""
        print(f"{'Branch':<40} {'Age (days)':<15} {'Merged':<10} {'Delete':<10}")
        print("-" * 75)
        for branch in self.branches:
            print(
                f"{branch.name:<40} {branch.days_old:<15} "
                f"{str(branch.is_merged):<10} {str(branch.should_delete):<10}"
            )
        print(f"\nTotal: {len(self.branches)} branches")
        to_delete = sum(1 for b in self.branches if b.should_delete)
        print(f"Marked for deletion: {to_delete}")
