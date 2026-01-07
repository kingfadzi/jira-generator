"""
Teardown Jira Test Data.

Deletes all test issues and optionally projects created by the setup scripts.
"""
import logging
from typing import List, Dict

from .jira_client import JiraClient
from .config import ISSUE_TYPE_NAMES
from .data.projects import PROJECTS

logger = logging.getLogger(__name__)


class JiraTeardown:
    """Handles deletion of test data from Jira."""

    def __init__(self, client: JiraClient):
        self.client = client
        self.stats = {
            'issues_deleted': 0,
            'issues_failed': 0,
            'projects_deleted': 0,
            'projects_failed': 0,
        }

    def delete_all_issues_in_project(self, project_key: str) -> int:
        """
        Delete all issues in a project.

        Args:
            project_key: Project key

        Returns:
            Number of issues deleted
        """
        deleted = 0
        # Get all issues in batches
        start_at = 0
        batch_size = 50

        while True:
            jql = f'project = {project_key} ORDER BY created DESC'
            try:
                issues = self.client.search_issues(
                    jql,
                    fields='key',
                    max_results=batch_size
                )
            except Exception as e:
                logger.error(f"Failed to search issues in {project_key}: {e}")
                break

            if not issues:
                break

            for issue in issues:
                issue_key = issue.get('key')
                try:
                    self.client.delete(f"/rest/api/2/issue/{issue_key}")
                    logger.info(f"Deleted: {issue_key}")
                    deleted += 1
                    self.stats['issues_deleted'] += 1
                except Exception as e:
                    logger.error(f"Failed to delete {issue_key}: {e}")
                    self.stats['issues_failed'] += 1

            # If we got fewer than batch_size, we're done
            if len(issues) < batch_size:
                break

        return deleted

    def delete_project(self, project_key: str) -> bool:
        """
        Delete a project.

        Args:
            project_key: Project key

        Returns:
            True if deleted successfully
        """
        try:
            # First delete all issues
            logger.info(f"Deleting all issues in {project_key}...")
            deleted_count = self.delete_all_issues_in_project(project_key)
            logger.info(f"Deleted {deleted_count} issues from {project_key}")

            # Then delete the project
            logger.info(f"Deleting project {project_key}...")
            self.client.delete(f"/rest/api/2/project/{project_key}")
            logger.info(f"Deleted project: {project_key}")
            self.stats['projects_deleted'] += 1
            return True

        except Exception as e:
            logger.error(f"Failed to delete project {project_key}: {e}")
            self.stats['projects_failed'] += 1
            return False

    def teardown_issues_only(self) -> Dict:
        """
        Delete all issues in LCT projects but keep projects.

        Returns:
            Dict with results
        """
        results = {
            'projects_cleaned': [],
            'issues_deleted': 0,
        }

        for project in PROJECTS:
            project_key = project['key']
            logger.info(f"\nCleaning project: {project_key}")

            # Check if project exists
            if not self.client.project_exists(project_key):
                logger.info(f"Project {project_key} does not exist, skipping")
                continue

            deleted = self.delete_all_issues_in_project(project_key)
            results['projects_cleaned'].append({
                'key': project_key,
                'issues_deleted': deleted,
            })
            results['issues_deleted'] += deleted

        results['stats'] = self.stats
        return results

    def teardown_all(self) -> Dict:
        """
        Delete all LCT projects and their issues.

        Returns:
            Dict with results
        """
        results = {
            'projects_deleted': [],
            'projects_failed': [],
        }

        for project in PROJECTS:
            project_key = project['key']
            logger.info(f"\nDeleting project: {project_key}")

            # Check if project exists
            if not self.client.project_exists(project_key):
                logger.info(f"Project {project_key} does not exist, skipping")
                continue

            if self.delete_project(project_key):
                results['projects_deleted'].append(project_key)
            else:
                results['projects_failed'].append(project_key)

        results['stats'] = self.stats
        return results


def teardown_issues(client: JiraClient) -> Dict:
    """Delete all issues but keep projects."""
    teardown = JiraTeardown(client)
    return teardown.teardown_issues_only()


def teardown_all(client: JiraClient) -> Dict:
    """Delete all projects and issues."""
    teardown = JiraTeardown(client)
    return teardown.teardown_all()


def print_teardown_summary(result: Dict, include_projects: bool = False):
    """Print summary of teardown."""
    print("\n" + "=" * 60)
    print("TEARDOWN SUMMARY")
    print("=" * 60)

    stats = result.get('stats', {})

    print(f"\nIssues:")
    print(f"  Deleted: {stats.get('issues_deleted', 0)}")
    print(f"  Failed:  {stats.get('issues_failed', 0)}")

    if include_projects:
        print(f"\nProjects:")
        print(f"  Deleted: {stats.get('projects_deleted', 0)}")
        print(f"  Failed:  {stats.get('projects_failed', 0)}")

        if result.get('projects_deleted'):
            print("\n  Deleted projects:")
            for p in result['projects_deleted']:
                print(f"    - {p}")

        if result.get('projects_failed'):
            print("\n  Failed to delete:")
            for p in result['projects_failed']:
                print(f"    - {p}")
    else:
        if result.get('projects_cleaned'):
            print("\n  Cleaned projects:")
            for p in result['projects_cleaned']:
                print(f"    - {p['key']}: {p['issues_deleted']} issues deleted")

    print("=" * 60 + "\n")


if __name__ == '__main__':
    import argparse

    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description='Teardown Jira test data')
    parser.add_argument('--issues-only', action='store_true',
                        help='Delete issues only, keep projects')
    parser.add_argument('--all', action='store_true',
                        help='Delete everything including projects')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview without making changes')

    args = parser.parse_args()

    if not args.issues_only and not args.all:
        parser.print_help()
        print("\nError: Specify --issues-only or --all")
        exit(1)

    client = JiraClient(dry_run=args.dry_run)

    print("Testing Jira connection...")
    user = client.test_connection()
    print(f"Connected as: {user.get('displayName', user.get('name', 'unknown'))}")

    if args.dry_run:
        print("\n*** DRY RUN MODE ***\n")

    if args.all:
        print("\nWARNING: This will delete ALL LCT projects and issues!")
        confirm = input("Type 'DELETE' to confirm: ")
        if confirm != 'DELETE':
            print("Aborted.")
            exit(0)
        result = teardown_all(client)
        print_teardown_summary(result, include_projects=True)
    else:
        print("\nDeleting all issues (keeping projects)...")
        result = teardown_issues(client)
        print_teardown_summary(result, include_projects=False)
