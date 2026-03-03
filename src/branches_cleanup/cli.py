import argparse
import os
import sys
from .github_client import GitHubClient


def main(argv=None):
    parser = argparse.ArgumentParser(description="Delete branches from a GitHub repo")
    parser.add_argument("--owner", required=True, help="Repository owner")
    parser.add_argument("--repo", required=True, help="Repository name")
    parser.add_argument("--token", help="GitHub personal access token")
    parser.add_argument(
        "--pattern",
        help="regular expression to match branch names for deletion",
    )
    parser.add_argument(
        "--branch",
        action="append",
        help="specific branch name to delete (can be specified multiple times)",
    )
    args = parser.parse_args(argv)

    token = args.token or os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GitHub token must be provided via --token or GITHUB_TOKEN env", file=sys.stderr)
        sys.exit(1)

    client = GitHubClient(token)
    branches = client.list_branches(args.owner, args.repo)
    to_delete = client.filter_branches(branches, pattern=args.pattern, names=args.branch)

    if not to_delete:
        print("No branches matched criteria. Nothing to delete.")
        return

    print("Branches that will be deleted:")
    for b in to_delete:
        print("  ", b)
    confirm = input("Proceed? [y/N]: ")
    if confirm.lower() != "y":
        print("Aborted.")
        return

    for b in to_delete:
        try:
            client.delete_branch(args.owner, args.repo, b)
            print(f"Deleted {b}")
        except Exception as e:
            print(f"Failed to delete {b}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
