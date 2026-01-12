"""
Setup Feature Fix Versions.

Assigns existing Features to unreleased fix versions (round-robin).
"""

import logging
from typing import Dict, List

from .jira_client import JiraClient
from .data.projects import PROJECTS

logger = logging.getLogger(__name__)

UNRELEASED_VERSIONS = ["v2.0.0", "v2.1.0", "v3.0.0"]


class FeatureVersionAssigner:
    """Assigns fix versions to Features."""

    def __init__(self, client: JiraClient):
        self.client = client
        self.stats = {"updated": 0, "skipped": 0, "errors": 0}

    def get_features(self, project_key: str) -> List[Dict]:
        """Get all Features without fix versions."""
        jql = f"project = {project_key} AND issuetype = Feature AND fixVersion is EMPTY"
        return self.client.search_issues(jql, fields="key,summary", max_results=500)

    def assign_versions(self) -> Dict:
        """Assign fix versions to Features across all projects."""
        results = {"projects": []}

        for project in PROJECTS:
            project_key = project["key"]
            logger.info(f"Processing {project_key}...")

            features = self.get_features(project_key)
            if not features:
                logger.info(f"  No Features without fix versions in {project_key}")
                results["projects"].append(
                    {
                        "key": project_key,
                        "features_updated": 0,
                    }
                )
                continue

            project_result = {"key": project_key, "features_updated": 0}

            for i, feature in enumerate(features):
                version = UNRELEASED_VERSIONS[i % len(UNRELEASED_VERSIONS)]
                try:
                    self.client.set_fix_version(feature["key"], version)
                    self.stats["updated"] += 1
                    project_result["features_updated"] += 1
                    logger.info(f"  {feature['key']} -> {version}")
                except Exception as e:
                    logger.error(f"  Failed to update {feature['key']}: {e}")
                    self.stats["errors"] += 1

            results["projects"].append(project_result)

        results["stats"] = self.stats
        return results


def setup_feature_versions(client: JiraClient) -> Dict:
    """Assign fix versions to Features."""
    assigner = FeatureVersionAssigner(client)
    return assigner.assign_versions()


def print_feature_version_summary(result: Dict):
    """Print summary."""
    print("\n" + "=" * 60)
    print("FEATURE VERSION ASSIGNMENT SUMMARY")
    print("=" * 60)

    stats = result.get("stats", {})
    print(f"\nUpdated: {stats.get('updated', 0)}")
    print(f"Errors:  {stats.get('errors', 0)}")

    print("\nBy Project:")
    for p in result.get("projects", []):
        print(f"  - {p['key']}: {p['features_updated']} features")

    print("=" * 60 + "\n")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    client = JiraClient()
    print("Testing Jira connection...")
    user = client.test_connection()
    print(f"Connected as: {user.get('displayName', user.get('name', 'unknown'))}")

    print("\nAssigning fix versions to Features...")
    result = setup_feature_versions(client)
    print_feature_version_summary(result)
