"""
Setup Jira Fix Versions.

Creates fix versions for each project.
"""

import logging
from typing import Dict

from .jira_client import JiraClient
from .data.projects import PROJECTS

logger = logging.getLogger(__name__)

# Versions to create per project
VERSIONS = [
    {"name": "v1.0.0", "released": True, "description": "Initial release"},
    {"name": "v1.1.0", "released": True, "description": "Bug fixes and improvements"},
    {"name": "v2.0.0", "released": False, "description": "Current development sprint"},
    {"name": "v2.1.0", "released": False, "description": "Next planned release"},
    {"name": "v3.0.0", "released": False, "description": "Future major release"},
]


class VersionBuilder:
    """Builds fix versions for Jira projects."""

    def __init__(self, client: JiraClient):
        self.client = client
        self.stats = {
            "created": 0,
            "exists": 0,
            "errors": 0,
        }

    def create_version(self, project_key: str, version_data: Dict) -> Dict:
        """Create a single version in a project."""
        try:
            version = self.client.create_version(
                project_key=project_key,
                name=version_data["name"],
                description=version_data.get("description", ""),
                released=version_data.get("released", False),
            )

            if version:
                # Check if it was created or already existed
                if version.get("id"):
                    self.stats["created"] += 1
                else:
                    self.stats["exists"] += 1

            return version

        except Exception as e:
            logger.error(
                f"Failed to create version {version_data['name']} in {project_key}: {e}"
            )
            self.stats["errors"] += 1
            return None

    def build_versions(self) -> Dict:
        """Create all versions for all projects."""
        results = {
            "projects": [],
        }

        for project in PROJECTS:
            project_key = project["key"]
            logger.info(f"Creating versions for {project_key}...")

            project_result = {
                "key": project_key,
                "versions": [],
            }

            for version_data in VERSIONS:
                version = self.create_version(project_key, version_data)
                if version:
                    project_result["versions"].append(
                        {
                            "name": version_data["name"],
                            "released": version_data["released"],
                        }
                    )

            results["projects"].append(project_result)

        results["stats"] = self.stats
        return results


def setup_versions(client: JiraClient) -> Dict:
    """Create all fix versions."""
    builder = VersionBuilder(client)
    return builder.build_versions()


def print_version_summary(result: Dict):
    """Print summary of version setup."""
    print("\n" + "=" * 60)
    print("VERSION SETUP SUMMARY")
    print("=" * 60)

    stats = result.get("stats", {})
    print(f"\nCreated: {stats.get('created', 0)}")
    print(f"Existed: {stats.get('exists', 0)}")
    print(f"Errors:  {stats.get('errors', 0)}")

    print(f"\nVersions per project: {len(VERSIONS)}")
    for v in VERSIONS:
        status = "released" if v["released"] else "unreleased"
        print(f"  - {v['name']} ({status})")

    print(f"\nProjects: {len(result.get('projects', []))}")
    for p in result.get("projects", []):
        print(f"  - {p['key']}: {len(p['versions'])} versions")

    print("=" * 60 + "\n")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    client = JiraClient()
    print("Testing Jira connection...")
    user = client.test_connection()
    print(f"Connected as: {user.get('displayName', user.get('name', 'unknown'))}")

    print("\nSetting up versions...")
    result = setup_versions(client)
    print_version_summary(result)
