"""
Setup Jira Hierarchy.

Creates the full hierarchy structure:
Strategic Objectives -> Portfolio Epics -> Business Outcomes -> Features
"""
import logging
from typing import List, Dict, Optional

from .jira_client import JiraClient
from .config import ISSUE_TYPE_NAMES
from .data.hierarchy import HIERARCHY, count_items

logger = logging.getLogger(__name__)


class HierarchyBuilder:
    """Builds the Jira issue hierarchy."""

    def __init__(self, client: JiraClient):
        self.client = client
        self.created_issues: Dict[str, Dict] = {}  # key -> issue data
        self.stats = {
            'strategic_objectives': {'created': 0, 'exists': 0, 'errors': 0},
            'portfolio_epics': {'created': 0, 'exists': 0, 'errors': 0},
            'business_outcomes': {'created': 0, 'exists': 0, 'errors': 0},
            'features': {'created': 0, 'exists': 0, 'errors': 0},
        }

    def _make_key(self, project: str, issue_type: str, summary: str) -> str:
        """Create a unique key for tracking created issues."""
        return f"{project}:{issue_type}:{summary}"

    def _find_or_create_issue(self, project_key: str, issue_type: str, summary: str,
                               description: str = None, parent_key: str = None,
                               labels: List[str] = None) -> Optional[Dict]:
        """Find existing issue or create new one."""
        # Check cache first
        cache_key = self._make_key(project_key, issue_type, summary)
        if cache_key in self.created_issues:
            return self.created_issues[cache_key]

        # Search for existing issue
        existing = self.client.find_issue_by_summary(project_key, summary, issue_type)
        if existing:
            self.created_issues[cache_key] = existing
            return existing

        # Create new issue
        try:
            issue = self.client.create_issue(
                project_key=project_key,
                issue_type=issue_type,
                summary=summary,
                description=description,
                parent_key=parent_key,
                labels=labels,
            )
            self.created_issues[cache_key] = issue
            return issue
        except Exception as e:
            logger.error(f"Failed to create {issue_type} '{summary}': {e}")
            return None

    def create_strategic_objective(self, project_key: str, summary: str,
                                    description: str = None) -> Optional[Dict]:
        """Create a Strategic Objective issue."""
        issue_type = ISSUE_TYPE_NAMES['strategic_objective']
        issue = self._find_or_create_issue(
            project_key=project_key,
            issue_type=issue_type,
            summary=summary,
            description=description,
            labels=['strategic-objective'],
        )

        if issue:
            if 'key' in issue:  # New issue created
                self.stats['strategic_objectives']['created'] += 1
            else:
                self.stats['strategic_objectives']['exists'] += 1
        else:
            self.stats['strategic_objectives']['errors'] += 1

        return issue

    def create_portfolio_epic(self, project_key: str, summary: str,
                               parent_key: str, description: str = None) -> Optional[Dict]:
        """Create a Portfolio Epic issue."""
        issue_type = ISSUE_TYPE_NAMES['portfolio_epic']
        issue = self._find_or_create_issue(
            project_key=project_key,
            issue_type=issue_type,
            summary=summary,
            description=description,
            parent_key=parent_key,
            labels=['portfolio-epic'],
        )

        if issue:
            if 'key' in issue:
                self.stats['portfolio_epics']['created'] += 1
            else:
                self.stats['portfolio_epics']['exists'] += 1
        else:
            self.stats['portfolio_epics']['errors'] += 1

        return issue

    def create_business_outcome(self, project_key: str, summary: str,
                                 parent_key: str, description: str = None) -> Optional[Dict]:
        """Create a Business Outcome issue."""
        issue_type = ISSUE_TYPE_NAMES['business_outcome']
        issue = self._find_or_create_issue(
            project_key=project_key,
            issue_type=issue_type,
            summary=summary,
            description=description,
            parent_key=parent_key,
            labels=['business-outcome'],
        )

        if issue:
            if 'key' in issue:
                self.stats['business_outcomes']['created'] += 1
            else:
                self.stats['business_outcomes']['exists'] += 1
        else:
            self.stats['business_outcomes']['errors'] += 1

        return issue

    def create_feature(self, project_key: str, summary: str,
                       parent_key: str, description: str = None) -> Optional[Dict]:
        """Create a Feature issue."""
        issue_type = ISSUE_TYPE_NAMES['feature']
        issue = self._find_or_create_issue(
            project_key=project_key,
            issue_type=issue_type,
            summary=summary,
            description=description,
            parent_key=parent_key,
            labels=['feature'],
        )

        if issue:
            if 'key' in issue:
                self.stats['features']['created'] += 1
            else:
                self.stats['features']['exists'] += 1
        else:
            self.stats['features']['errors'] += 1

        return issue

    def build_hierarchy(self) -> Dict:
        """
        Build the complete hierarchy from HIERARCHY data.

        Returns:
            Dict with created issue keys organized by hierarchy level
        """
        result = {
            'strategic_objectives': [],
            'portfolio_epics': [],
            'business_outcomes': [],
            'features': [],
        }

        for strat_obj_data in HIERARCHY:
            so = strat_obj_data['strategic_objective']
            project_key = so['project']

            logger.info(f"Creating Strategic Objective: {so['summary']}")

            # Create Strategic Objective
            so_issue = self.create_strategic_objective(
                project_key=project_key,
                summary=so['summary'],
                description=so.get('description'),
            )

            if not so_issue:
                logger.error(f"Failed to create SO: {so['summary']}, skipping children")
                continue

            so_key = so_issue.get('key')
            result['strategic_objectives'].append({
                'key': so_key,
                'summary': so['summary'],
                'project': project_key,
            })

            # Create Portfolio Epics under this SO
            for pe_data in strat_obj_data['portfolio_epics']:
                logger.info(f"  Creating Portfolio Epic: {pe_data['summary']}")

                pe_issue = self.create_portfolio_epic(
                    project_key=project_key,
                    summary=pe_data['summary'],
                    parent_key=so_key,
                    description=pe_data.get('description'),
                )

                if not pe_issue:
                    logger.error(f"  Failed to create PE: {pe_data['summary']}, skipping children")
                    continue

                pe_key = pe_issue.get('key')
                result['portfolio_epics'].append({
                    'key': pe_key,
                    'summary': pe_data['summary'],
                    'parent': so_key,
                })

                # Create Business Outcomes under this PE
                for bo_data in pe_data['business_outcomes']:
                    logger.info(f"    Creating Business Outcome: {bo_data['summary']}")

                    bo_issue = self.create_business_outcome(
                        project_key=project_key,
                        summary=bo_data['summary'],
                        parent_key=pe_key,
                        description=bo_data.get('description'),
                    )

                    if not bo_issue:
                        logger.error(f"    Failed to create BO: {bo_data['summary']}, skipping children")
                        continue

                    bo_key = bo_issue.get('key')
                    result['business_outcomes'].append({
                        'key': bo_key,
                        'summary': bo_data['summary'],
                        'parent': pe_key,
                    })

                    # Create Features under this BO
                    for feature_data in bo_data['features']:
                        logger.info(f"      Creating Feature: {feature_data['summary']}")

                        feature_issue = self.create_feature(
                            project_key=project_key,
                            summary=feature_data['summary'],
                            parent_key=bo_key,
                            description=feature_data.get('description'),
                        )

                        if feature_issue:
                            result['features'].append({
                                'key': feature_issue.get('key'),
                                'summary': feature_data['summary'],
                                'parent': bo_key,
                            })

        return result


def setup_hierarchy(client: JiraClient) -> Dict:
    """
    Create the full hierarchy in Jira.

    Args:
        client: JiraClient instance

    Returns:
        Dict with results and statistics
    """
    builder = HierarchyBuilder(client)
    result = builder.build_hierarchy()
    result['stats'] = builder.stats
    return result


def print_hierarchy_summary(result: Dict):
    """Print summary of hierarchy setup."""
    print("\n" + "=" * 60)
    print("HIERARCHY SETUP SUMMARY")
    print("=" * 60)

    expected = count_items()
    stats = result.get('stats', {})

    print("\nExpected vs Actual:")
    print("-" * 40)

    for level, expected_count in expected.items():
        level_stats = stats.get(level, {})
        created = level_stats.get('created', 0)
        exists = level_stats.get('exists', 0)
        errors = level_stats.get('errors', 0)
        total = created + exists

        print(f"  {level}:")
        print(f"    Expected: {expected_count}")
        print(f"    Created:  {created}")
        print(f"    Existed:  {exists}")
        print(f"    Errors:   {errors}")
        print(f"    Total:    {total}")

    print("\nCreated Issues by Level:")
    print("-" * 40)

    for level in ['strategic_objectives', 'portfolio_epics', 'business_outcomes', 'features']:
        items = result.get(level, [])
        print(f"\n  {level.replace('_', ' ').title()} ({len(items)}):")
        for item in items[:5]:  # Show first 5
            print(f"    - {item.get('key', 'N/A')}: {item['summary'][:40]}...")
        if len(items) > 5:
            print(f"    ... and {len(items) - 5} more")

    print("=" * 60 + "\n")


if __name__ == '__main__':
    # Allow running standalone for testing
    logging.basicConfig(level=logging.INFO)

    client = JiraClient()
    print("Testing Jira connection...")
    user = client.test_connection()
    print(f"Connected as: {user.get('displayName', user.get('name', 'unknown'))}")

    print(f"\nExpected items to create:")
    for level, count in count_items().items():
        print(f"  {level}: {count}")

    print("\nSetting up hierarchy...")
    result = setup_hierarchy(client)
    print_hierarchy_summary(result)
