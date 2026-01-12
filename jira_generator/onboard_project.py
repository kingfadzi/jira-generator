"""
Onboard a Jira Project for LCT Governance.

Sets up a project with the required custom fields on all its screens.

Usage:
    python -m jira_generator.onboard_project TECHCON
    python -m jira_generator.onboard_project TECHCON AIOPS DATA
"""

import argparse
import logging
import sys
from typing import List, Dict

from .jira_client import JiraClient
from .config import STORY_TRIGGER_FIELDS

logger = logging.getLogger(__name__)


def get_trigger_field_ids(client: JiraClient) -> Dict[str, str]:
    """
    Get the field IDs for all trigger fields.

    Returns:
        Dict mapping field name to field ID
    """
    field_ids = {}
    for field_key, field_def in STORY_TRIGGER_FIELDS.items():
        field = client.get_custom_field_by_name(field_def["name"])
        if field:
            field_ids[field_def["name"]] = field["id"]
        else:
            logger.warning(f"Field '{field_def['name']}' not found in Jira")
    return field_ids


def onboard_project(client: JiraClient, project_key: str) -> Dict:
    """
    Onboard a single project by adding trigger fields to its screens.

    Args:
        client: JiraClient instance
        project_key: Project key (e.g., 'TECHCON')

    Returns:
        Dict with results
    """
    result = {
        "project": project_key,
        "screens_found": 0,
        "screens_updated": [],
        "fields_added": 0,
        "errors": [],
    }

    # Verify project exists
    project = client.get_project(project_key)
    if not project:
        result["errors"].append(f"Project '{project_key}' not found")
        return result

    logger.info(f"Onboarding project: {project_key} - {project.get('name', '')}")

    # Get trigger field IDs
    field_ids = get_trigger_field_ids(client)
    if not field_ids:
        result["errors"].append("No trigger fields found in Jira. Run setup_custom_fields first.")
        return result

    logger.info(f"Found {len(field_ids)} trigger fields to add")

    # Get project screens
    screens = client.get_project_screens(project_key)
    result["screens_found"] = len(screens)

    if not screens:
        result["errors"].append(
            f"No screens found for project '{project_key}'. "
            f"Screens should be named like '{project_key}: ...'"
        )
        return result

    logger.info(f"Found {len(screens)} screens for {project_key}")

    # Add fields to each screen
    for screen in screens:
        screen_id = screen.get("id")
        screen_name = screen.get("name", f"Screen {screen_id}")

        logger.info(f"Processing screen: {screen_name}")

        fields_added_to_screen = 0
        for field_name, field_id in field_ids.items():
            if client.add_field_to_screen(screen_id, field_id):
                fields_added_to_screen += 1

        result["screens_updated"].append({
            "id": screen_id,
            "name": screen_name,
            "fields_added": fields_added_to_screen,
        })
        result["fields_added"] += fields_added_to_screen

    return result


def onboard_projects(client: JiraClient, project_keys: List[str]) -> List[Dict]:
    """
    Onboard multiple projects.

    Args:
        client: JiraClient instance
        project_keys: List of project keys

    Returns:
        List of result dicts
    """
    results = []
    for project_key in project_keys:
        result = onboard_project(client, project_key.upper())
        results.append(result)
    return results


def print_onboard_summary(results: List[Dict]):
    """Print summary of onboarding results."""
    print("\n" + "=" * 60)
    print("PROJECT ONBOARDING SUMMARY")
    print("=" * 60)

    for result in results:
        project = result["project"]
        print(f"\n{project}:")

        if result["errors"]:
            for error in result["errors"]:
                print(f"  ERROR: {error}")
            continue

        print(f"  Screens found: {result['screens_found']}")
        print(f"  Total fields added: {result['fields_added']}")

        for screen in result["screens_updated"]:
            status = "updated" if screen["fields_added"] > 0 else "no changes"
            print(f"    - {screen['name']}: {status}")

    print("\n" + "=" * 60)

    # Summary counts
    total_projects = len(results)
    successful = len([r for r in results if not r["errors"]])
    failed = total_projects - successful

    print(f"\nProjects processed: {total_projects}")
    print(f"  Successful: {successful}")
    if failed:
        print(f"  Failed: {failed}")
    print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Onboard Jira projects for LCT governance"
    )
    parser.add_argument(
        "projects",
        nargs="+",
        help="Project keys to onboard (e.g., TECHCON AIOPS DATA)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(levelname)s: %(message)s",
    )

    # Initialize client
    client = JiraClient(dry_run=args.dry_run)

    # Test connection
    print("Connecting to Jira...")
    try:
        user = client.test_connection()
        print(f"Connected as: {user.get('displayName', user.get('name', 'unknown'))}")
    except Exception as e:
        print(f"ERROR: Failed to connect to Jira: {e}")
        sys.exit(1)

    if args.dry_run:
        print("\n[DRY RUN MODE - No changes will be made]\n")

    # Onboard projects
    print(f"\nOnboarding {len(args.projects)} project(s)...")
    results = onboard_projects(client, args.projects)

    # Print summary
    print_onboard_summary(results)

    # Exit with error code if any failures
    if any(r["errors"] for r in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
