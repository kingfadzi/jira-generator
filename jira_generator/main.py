#!/usr/bin/env python3
"""
Jira Data Center Population Script.

Main CLI orchestrator for setting up Jira test data.

Usage:
    python -m jira.main --help
    python -m jira.main --dry-run --all
    python -m jira.main --projects
    python -m jira.main --hierarchy
    python -m jira.main --constraints
"""

import argparse
import logging
import sys

from .jira_client import JiraClient
from .config import JIRA_CONFIG, get_required_env
from .data.hierarchy import count_items
from .data.constraints import count_constraints
from .data.projects import PROJECTS

from .setup_projects import setup_projects, print_project_summary
from .setup_issue_types import (
    setup_constraint_issue_type,
    verify_hierarchy_issue_types,
    print_issue_type_summary,
)
from .setup_custom_fields import setup_custom_fields, print_custom_field_summary
from .setup_hierarchy import setup_hierarchy, print_hierarchy_summary
from .setup_constraints import setup_constraints, print_constraint_summary
from .setup_versions import setup_versions, print_version_summary
from .setup_feature_versions import (
    setup_feature_versions,
    print_feature_version_summary,
)
from .setup_component_mapping import setup_component_mapping, print_mapping_summary
from .teardown import teardown_issues, teardown_all, print_teardown_summary


def setup_logging(verbose: bool = False):
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # Reduce noise from requests library
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)


def print_banner():
    """Print welcome banner."""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║          JIRA DATA CENTER POPULATION SCRIPT                   ║
║                                                               ║
║  Creates test data for LCT governance testing                 ║
╚═══════════════════════════════════════════════════════════════╝
""")


def print_config_summary():
    """Print configuration summary."""
    print("Configuration:")
    print("-" * 40)
    url = JIRA_CONFIG.get("base_url", "NOT SET")
    user = JIRA_CONFIG.get("username", "NOT SET")
    token = JIRA_CONFIG.get("token", "")
    token_display = f"{token[:8]}..." if len(token) > 8 else "NOT SET"

    print(f"  JIRA_URL:   {url}")
    print(f"  JIRA_USER:  {user}")
    print(f"  JIRA_TOKEN: {token_display}")
    print()


def print_data_summary():
    """Print summary of data to be created."""
    print("Data to Create:")
    print("-" * 40)

    print(f"  Projects: {len(PROJECTS)}")
    for p in PROJECTS:
        print(f"    - {p['key']}: {p['name']}")

    hierarchy = count_items()
    print("\n  Hierarchy:")
    print(f"    - Strategic Objectives: {hierarchy['strategic_objectives']}")
    print(f"    - Portfolio Epics:      {hierarchy['portfolio_epics']}")
    print(f"    - Business Outcomes:    {hierarchy['business_outcomes']}")
    print(f"    - Features:             {hierarchy['features']}")

    constraints = count_constraints()
    print(f"\n  Constraints: {constraints['total']}")
    print("    By Guild:")
    for guild, count in constraints["by_guild"].items():
        print(f"      - {guild}: {count}")

    print()


def test_connection(client: JiraClient) -> bool:
    """Test Jira connection."""
    print("Testing Jira connection...")
    try:
        user = client.test_connection()
        display_name = user.get("displayName", user.get("name", "unknown"))
        print(f"  Connected as: {display_name}")
        print(f"  Email: {user.get('emailAddress', 'N/A')}")
        print()
        return True
    except Exception as e:
        print(f"  ERROR: Failed to connect to Jira: {e}")
        print()
        return False


def run_projects(client: JiraClient):
    """Create projects."""
    print("\n" + "=" * 60)
    print("PHASE 1: CREATING PROJECTS")
    print("=" * 60)
    results = setup_projects(client)
    print_project_summary(results)
    return results


def run_issue_types(client: JiraClient):
    """Create/verify issue types."""
    print("\n" + "=" * 60)
    print("PHASE 2: SETTING UP ISSUE TYPES")
    print("=" * 60)
    constraint_result = setup_constraint_issue_type(client)
    hierarchy_result = verify_hierarchy_issue_types(client)
    print_issue_type_summary(constraint_result, hierarchy_result)
    return constraint_result, hierarchy_result


def run_custom_fields(client: JiraClient):
    """Create custom fields."""
    print("\n" + "=" * 60)
    print("PHASE 3: CREATING CUSTOM FIELDS")
    print("=" * 60)
    results = setup_custom_fields(client)
    print_custom_field_summary(results)
    return results


def run_hierarchy(client: JiraClient):
    """Create hierarchy."""
    print("\n" + "=" * 60)
    print("PHASE 4: CREATING HIERARCHY")
    print("=" * 60)
    print("This may take a few minutes...")
    results = setup_hierarchy(client)
    print_hierarchy_summary(results)
    return results


def run_versions(client: JiraClient):
    """Create fix versions."""
    print("\n" + "=" * 60)
    print("PHASE 5: CREATING FIX VERSIONS")
    print("=" * 60)
    results = setup_versions(client)
    print_version_summary(results)
    return results


def run_feature_versions(client: JiraClient):
    """Assign fix versions to Features."""
    print("\n" + "=" * 60)
    print("PHASE 5b: ASSIGNING FEATURE VERSIONS")
    print("=" * 60)
    results = setup_feature_versions(client)
    print_feature_version_summary(results)
    return results


def run_constraints(client: JiraClient):
    """Create constraints."""
    print("\n" + "=" * 60)
    print("PHASE 6: CREATING CONSTRAINTS")
    print("=" * 60)
    results = setup_constraints(client)
    print_constraint_summary(results)
    return results


def run_component_mapping():
    """Update component_mapping table."""
    print("\n" + "=" * 60)
    print("PHASE 7: UPDATING COMPONENT MAPPING")
    print("=" * 60)
    results = setup_component_mapping()
    print_mapping_summary(results)
    return results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Populate Jira Data Center with LCT test data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m jira.main --dry-run --all    Preview all changes
  python -m jira.main --projects         Create projects only
  python -m jira.main --issue-types      Create Constraint issue type
  python -m jira.main --fields           Create custom fields
  python -m jira.main --hierarchy        Create full hierarchy
  python -m jira.main --constraints      Create constraint issues
  python -m jira.main --all              Run full setup

  python -m jira.main --teardown         Delete all issues (keep projects)
  python -m jira.main --teardown-all     Delete everything including projects
  python -m jira.main --rebuild          Teardown + full setup

Environment Variables:
  JIRA_URL    Jira Data Center base URL
  JIRA_USER   Jira username
  JIRA_TOKEN  Personal Access Token
        """,
    )

    parser.add_argument(
        "--dry-run", action="store_true", help="Preview changes without making them"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    # Phase selection
    parser.add_argument("--all", action="store_true", help="Run all setup phases")
    parser.add_argument("--projects", action="store_true", help="Create Jira projects")
    parser.add_argument(
        "--issue-types", action="store_true", help="Create Constraint issue type"
    )
    parser.add_argument("--fields", action="store_true", help="Create custom fields")
    parser.add_argument(
        "--hierarchy",
        action="store_true",
        help="Create full hierarchy (SO->PE->BO->Feature)",
    )
    parser.add_argument("--versions", action="store_true", help="Create fix versions")
    parser.add_argument(
        "--feature-versions",
        action="store_true",
        help="Assign Features to fix versions",
    )
    parser.add_argument(
        "--constraints", action="store_true", help="Create Constraint issues"
    )
    parser.add_argument(
        "--component-mapping",
        action="store_true",
        help="Update component_mapping table with Jira projects",
    )

    # Teardown options
    parser.add_argument(
        "--teardown", action="store_true", help="Delete all issues but keep projects"
    )
    parser.add_argument(
        "--teardown-all",
        action="store_true",
        help="Delete everything including projects",
    )
    parser.add_argument(
        "--rebuild", action="store_true", help="Teardown issues then run full setup"
    )

    # Utility
    parser.add_argument(
        "--test-connection", action="store_true", help="Test Jira connection only"
    )
    parser.add_argument(
        "--show-config", action="store_true", help="Show configuration and data summary"
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Skip confirmation prompts for destructive operations",
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    # Print banner
    print_banner()

    # Show config if requested
    if args.show_config:
        print_config_summary()
        print_data_summary()
        return 0

    # Validate that at least one action is requested
    actions = [
        args.all,
        args.projects,
        args.issue_types,
        args.fields,
        args.hierarchy,
        args.versions,
        args.feature_versions,
        args.constraints,
        args.component_mapping,
        args.test_connection,
        args.teardown,
        args.teardown_all,
        args.rebuild,
    ]
    if not any(actions):
        parser.print_help()
        print("\nError: No action specified. Use --all or specify individual phases.")
        return 1

    # Validate environment (will exit if missing)
    try:
        if not JIRA_CONFIG.get("base_url"):
            get_required_env("JIRA_URL")
        if not JIRA_CONFIG.get("username"):
            get_required_env("JIRA_USER")
        if not JIRA_CONFIG.get("token"):
            get_required_env("JIRA_TOKEN")
    except SystemExit:
        return 1

    # Print config
    print_config_summary()

    if args.dry_run:
        print("*** DRY RUN MODE - No changes will be made ***\n")

    # Create client
    client = JiraClient(dry_run=args.dry_run)

    # Test connection
    if not test_connection(client):
        return 1

    if args.test_connection:
        print("Connection test successful!")
        return 0

    # Print data summary
    print_data_summary()

    # Handle teardown operations
    try:
        if args.teardown or args.teardown_all or args.rebuild:
            include_projects = args.teardown_all

            if include_projects:
                print("\n" + "=" * 60)
                print("WARNING: DESTRUCTIVE OPERATION")
                print("=" * 60)
                print("\nThis will DELETE all LCT projects and their issues:")
                for p in PROJECTS:
                    print(f"  - {p['key']}: {p['name']}")

                if not args.force and not args.dry_run:
                    confirm = input("\nType 'DELETE' to confirm: ")
                    if confirm != "DELETE":
                        print("Aborted.")
                        return 0
            else:
                print("\n" + "=" * 60)
                print("TEARDOWN: Deleting all issues (keeping projects)")
                print("=" * 60)

                if not args.force and not args.dry_run:
                    confirm = input("\nType 'yes' to confirm: ")
                    if confirm.lower() != "yes":
                        print("Aborted.")
                        return 0

            if include_projects:
                result = teardown_all(client)
                print_teardown_summary(result, include_projects=True)
            else:
                result = teardown_issues(client)
                print_teardown_summary(result, include_projects=False)

            # If just teardown (not rebuild), we're done
            if not args.rebuild:
                return 0

            print("\n" + "=" * 60)
            print("REBUILD: Running full setup")
            print("=" * 60)

    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        return 130

    # Run requested phases
    try:
        if args.all or args.rebuild or args.projects:
            run_projects(client)

        if args.all or args.rebuild or args.issue_types:
            run_issue_types(client)

        if args.all or args.rebuild or args.fields:
            run_custom_fields(client)

        if args.all or args.rebuild or args.hierarchy:
            run_hierarchy(client)

        if args.all or args.rebuild or args.versions:
            run_versions(client)

        if args.all or args.rebuild or args.feature_versions:
            run_feature_versions(client)

        if args.all or args.rebuild or args.constraints:
            run_constraints(client)

        if args.all or args.rebuild or args.component_mapping:
            run_component_mapping()

    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        return 130
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return 1

    print("\n" + "=" * 60)
    print("SETUP COMPLETE")
    print("=" * 60)

    if args.dry_run:
        print("\nThis was a dry run. Re-run without --dry-run to apply changes.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
