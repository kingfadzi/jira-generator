"""
Setup Jira Projects.

Creates the projects defined in data/projects.py.
"""

import logging
from typing import List, Dict

from .jira_client import JiraClient
from .data.projects import PROJECTS

logger = logging.getLogger(__name__)


def setup_projects(client: JiraClient) -> List[Dict]:
    """
    Create all projects defined in PROJECTS.

    Args:
        client: JiraClient instance

    Returns:
        List of created/existing project data
    """
    results = []

    for project_def in PROJECTS:
        logger.info(f"Setting up project: {project_def['key']} - {project_def['name']}")

        try:
            project = client.create_project(
                key=project_def["key"],
                name=project_def["name"],
                description=project_def.get("description"),
                lead=project_def.get("lead"),
                project_type="software",
            )
            results.append(
                {
                    "key": project_def["key"],
                    "name": project_def["name"],
                    "status": "created" if project else "exists",
                    "project": project,
                }
            )
        except Exception as e:
            logger.error(f"Failed to create project {project_def['key']}: {e}")
            results.append(
                {
                    "key": project_def["key"],
                    "name": project_def["name"],
                    "status": "error",
                    "error": str(e),
                }
            )

    return results


def verify_projects(client: JiraClient) -> Dict:
    """
    Verify all required projects exist.

    Returns:
        Dict with verification results
    """
    results = {
        "all_exist": True,
        "projects": [],
    }

    for project_def in PROJECTS:
        exists = client.project_exists(project_def["key"])
        results["projects"].append(
            {
                "key": project_def["key"],
                "name": project_def["name"],
                "exists": exists,
            }
        )
        if not exists:
            results["all_exist"] = False

    return results


def print_project_summary(results: List[Dict]):
    """Print summary of project setup."""
    print("\n" + "=" * 60)
    print("PROJECT SETUP SUMMARY")
    print("=" * 60)

    created = [r for r in results if r["status"] == "created"]
    existing = [r for r in results if r["status"] == "exists"]
    errors = [r for r in results if r["status"] == "error"]

    print(f"\nCreated: {len(created)}")
    for r in created:
        print(f"  + {r['key']} - {r['name']}")

    print(f"\nAlready existed: {len(existing)}")
    for r in existing:
        print(f"  = {r['key']} - {r['name']}")

    if errors:
        print(f"\nErrors: {len(errors)}")
        for r in errors:
            print(f"  ! {r['key']} - {r['name']}: {r['error']}")

    print("=" * 60 + "\n")


if __name__ == "__main__":
    # Allow running standalone for testing
    logging.basicConfig(level=logging.INFO)

    client = JiraClient()
    print("Testing Jira connection...")
    user = client.test_connection()
    print(f"Connected as: {user.get('displayName', user.get('name', 'unknown'))}")

    print("\nSetting up projects...")
    results = setup_projects(client)
    print_project_summary(results)
