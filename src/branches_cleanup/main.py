import argparse
import sys
from .report_gen import generate_report
from .cli import main as delete_branches


def main():
    """Main entry point for branches cleanup tool."""
    parser = argparse.ArgumentParser(
        description="GitHub Branch Cleanup Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a branch report with metadata
  python -m branches_cleanup report --owner USER --repo REPO --token TOKEN

  # Delete branches based on criteria
  python -m branches_cleanup delete --owner USER --repo REPO --token TOKEN --pattern "feature/.*"

  # Interactive mode (menu-driven)
  python -m branches_cleanup
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Report generation subcommand
    report_parser = subparsers.add_parser(
        "report", help="Generate a branch metadata report"
    )
    report_parser.add_argument("--owner", required=True, help="Repository owner")
    report_parser.add_argument("--repo", required=True, help="Repository name")
    report_parser.add_argument("--token", help="GitHub personal access token")
    report_parser.add_argument(
        "--output",
        default="branches_report.csv",
        help="Output file (supports .csv and .json)",
    )
    report_parser.add_argument(
        "--min-age",
        type=int,
        default=30,
        help="Mark branches older than this (days) for deletion",
    )
    report_parser.add_argument(
        "--include-merged",
        action="store_true",
        help="Mark merged branches for deletion",
    )

    # Delete branches subcommand
    delete_parser = subparsers.add_parser("delete", help="Delete branches")
    delete_parser.add_argument("--owner", required=True, help="Repository owner")
    delete_parser.add_argument("--repo", required=True, help="Repository name")
    delete_parser.add_argument("--token", help="GitHub personal access token")
    delete_parser.add_argument(
        "--pattern",
        help="Regular expression to match branch names for deletion",
    )
    delete_parser.add_argument(
        "--branch",
        action="append",
        help="Specific branch name to delete (can be specified multiple times)",
    )

    args = parser.parse_args()

    # If no command provided, show interactive menu
    if not args.command:
        show_interactive_menu()
        return

    # Handle commands
    if args.command == "report":
        report_args = [
            "--owner", args.owner,
            "--repo", args.repo,
        ]
        if args.token:
            report_args.extend(["--token", args.token])
        if args.output != "branches_report.csv":
            report_args.extend(["--output", args.output])
        if args.min_age != 30:
            report_args.extend(["--min-age", str(args.min_age)])
        if args.include_merged:
            report_args.append("--include-merged")
        generate_report(report_args)

    elif args.command == "delete":
        delete_args = [
            "--owner", args.owner,
            "--repo", args.repo,
        ]
        if args.token:
            delete_args.extend(["--token", args.token])
        if args.pattern:
            delete_args.extend(["--pattern", args.pattern])
        if args.branch:
            for branch in args.branch:
                delete_args.extend(["--branch", branch])
        delete_branches(delete_args)


def show_interactive_menu():
    """Show interactive menu for user to choose action."""
    print("\n" + "=" * 70)
    print("  GitHub Branch Cleanup Tool")
    print("=" * 70)
    print("\nChoose an action:\n")
    print("  1. Generate branch metadata report")
    print("  2. Delete branches (with confirmation)")
    print("  3. Exit")
    print()

    choice = input("Enter your choice (1-3): ").strip()

    if choice == "1":
        print("\n--- Generate Branch Report ---\n")
        owner = input("GitHub owner/organization: ").strip()
        repo = input("Repository name: ").strip()
        token = input("GitHub token (or press Enter to use GITHUB_TOKEN env): ").strip()
        output = input("Output file [branches_report.csv]: ").strip() or "branches_report.csv"
        min_age = input("Min age in days to mark for deletion [30]: ").strip() or "30"
        include_merged = input("Include merged branches for deletion? (y/n) [n]: ").strip().lower() == "y"

        report_args = ["--owner", owner, "--repo", repo, "--output", output, "--min-age", min_age]
        if token:
            report_args.extend(["--token", token])
        if include_merged:
            report_args.append("--include-merged")

        generate_report(report_args)

    elif choice == "2":
        print("\n--- Delete Branches ---\n")
        owner = input("GitHub owner/organization: ").strip()
        repo = input("Repository name: ").strip()
        token = input("GitHub token (or press Enter to use GITHUB_TOKEN env): ").strip()
        pattern = input("Branch pattern (regex, or press Enter to skip): ").strip()
        print("Note: You can specify multiple branches, one per line. Leave blank when done.")
        branches = []
        while True:
            branch = input("Branch name (or press Enter to finish): ").strip()
            if not branch:
                break
            branches.append(branch)

        delete_args = ["--owner", owner, "--repo", repo]
        if token:
            delete_args.extend(["--token", token])
        if pattern:
            delete_args.extend(["--pattern", pattern])
        for branch in branches:
            delete_args.extend(["--branch", branch])

        delete_branches(delete_args)

    elif choice == "3":
        print("Goodbye!")
        sys.exit(0)

    else:
        print("Invalid choice. Please try again.")
        show_interactive_menu()


if __name__ == "__main__":
    main()
