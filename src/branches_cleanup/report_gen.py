import argparse
import os
import sys
from .github_client import GitHubClient
from .branch_report import BranchReport


def generate_report(argv=None):
    """Generate a report of all branches with metadata."""
    parser = argparse.ArgumentParser(
        description="Generate branch metadata report from a GitHub repo"
    )
    parser.add_argument("--owner", required=True, help="Repository owner")
    parser.add_argument("--repo", required=True, help="Repository name")
    parser.add_argument("--token", help="GitHub personal access token")
    parser.add_argument(
        "--output",
        default="branches_report.csv",
        help="Output file (supports .csv and .json)",
    )
    parser.add_argument(
        "--min-age",
        type=int,
        default=30,
        help="Mark branches older than this (days) for deletion",
    )
    parser.add_argument(
        "--include-merged",
        action="store_true",
        help="Mark merged branches for deletion",
    )
    args = parser.parse_args(argv)

    token = args.token or os.getenv("GITHUB_TOKEN")
    if not token:
        print(
            "Error: GitHub token must be provided via --token or GITHUB_TOKEN env",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Fetching branch info from {args.owner}/{args.repo}...")
    client = GitHubClient(token)
    branches = client.get_all_branches_info(args.owner, args.repo)
    print(f"Found {len(branches)} branches")

    # Mark branches for deletion based on criteria
    for branch in branches:
        should_delete = False
        if branch.days_old > args.min_age:
            should_delete = True
        if args.include_merged and branch.is_merged:
            should_delete = True
        branch.should_delete = should_delete

    report = BranchReport(branches)
    
    # Save to file
    if args.output.endswith(".json"):
        report.save_json(args.output)
    else:
        report.save_csv(args.output)
    
    print(f"\nReport saved to {args.output}")
    print("\n" + "=" * 75)
    report.print_report()


if __name__ == "__main__":
    generate_report()
