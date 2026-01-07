"""
Setup Jira Issue Types.

Creates the Constraint issue type and verifies hierarchy issue types exist.
"""
import logging
from typing import List, Dict, Optional

from .jira_client import JiraClient
from .config import CONSTRAINT_ISSUE_TYPE, ISSUE_TYPE_NAMES

logger = logging.getLogger(__name__)


def setup_constraint_issue_type(client: JiraClient) -> Dict:
    """
    Create the Constraint issue type.

    Args:
        client: JiraClient instance

    Returns:
        Dict with issue type data or error
    """
    logger.info("Setting up Constraint issue type...")

    try:
        issue_type = client.create_issue_type(
            name=CONSTRAINT_ISSUE_TYPE['name'],
            description=CONSTRAINT_ISSUE_TYPE['description'],
            type=CONSTRAINT_ISSUE_TYPE['type'],
        )
        return {
            'name': CONSTRAINT_ISSUE_TYPE['name'],
            'status': 'created' if issue_type else 'exists',
            'issue_type': issue_type,
        }
    except Exception as e:
        logger.error(f"Failed to create Constraint issue type: {e}")
        return {
            'name': CONSTRAINT_ISSUE_TYPE['name'],
            'status': 'error',
            'error': str(e),
        }


def verify_hierarchy_issue_types(client: JiraClient) -> Dict:
    """
    Verify that all hierarchy issue types exist.

    These should be pre-configured in Jira with Advanced Roadmaps:
    - Strategic Objective
    - Portfolio Epic
    - Business Outcome
    - Feature
    - Story

    Returns:
        Dict with verification results
    """
    results = {
        'all_exist': True,
        'issue_types': [],
        'missing': [],
    }

    for key, name in ISSUE_TYPE_NAMES.items():
        if key == 'constraint':
            continue  # Skip constraint, we create it ourselves

        exists = client.issue_type_exists(name)
        results['issue_types'].append({
            'key': key,
            'name': name,
            'exists': exists,
        })
        if not exists:
            results['all_exist'] = False
            results['missing'].append(name)

    return results


def get_issue_type_id(client: JiraClient, name: str) -> Optional[str]:
    """Get the ID of an issue type by name."""
    issue_type = client.get_issue_type_by_name(name)
    return issue_type['id'] if issue_type else None


def list_all_issue_types(client: JiraClient) -> List[Dict]:
    """List all issue types in Jira."""
    return client.get_issue_types()


def print_issue_type_summary(constraint_result: Dict, hierarchy_result: Dict):
    """Print summary of issue type setup."""
    print("\n" + "=" * 60)
    print("ISSUE TYPE SETUP SUMMARY")
    print("=" * 60)

    # Constraint issue type
    print("\nConstraint Issue Type:")
    if constraint_result['status'] == 'created':
        print(f"  + Created: {constraint_result['name']}")
    elif constraint_result['status'] == 'exists':
        print(f"  = Already exists: {constraint_result['name']}")
    else:
        print(f"  ! Error: {constraint_result.get('error', 'Unknown error')}")

    # Hierarchy issue types
    print("\nHierarchy Issue Types:")
    for it in hierarchy_result['issue_types']:
        status = "OK" if it['exists'] else "MISSING"
        symbol = "+" if it['exists'] else "!"
        print(f"  {symbol} {it['name']}: {status}")

    if hierarchy_result['missing']:
        print(f"\n  WARNING: Missing issue types: {', '.join(hierarchy_result['missing'])}")
        print("  These must be created manually in Jira Admin or via Advanced Roadmaps setup.")

    print("=" * 60 + "\n")


if __name__ == '__main__':
    # Allow running standalone for testing
    logging.basicConfig(level=logging.INFO)

    client = JiraClient()
    print("Testing Jira connection...")
    user = client.test_connection()
    print(f"Connected as: {user.get('displayName', user.get('name', 'unknown'))}")

    print("\nSetting up issue types...")
    constraint_result = setup_constraint_issue_type(client)
    hierarchy_result = verify_hierarchy_issue_types(client)
    print_issue_type_summary(constraint_result, hierarchy_result)

    print("\nAll available issue types:")
    for it in list_all_issue_types(client):
        print(f"  - {it['name']} (id: {it['id']})")
