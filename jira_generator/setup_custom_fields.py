"""
Setup Jira Custom Fields.

Creates custom fields for Constraint issues:
- Risk Materiality (select)
- Mitigation Plan (textarea)
- Guild (select)
"""
import logging
from typing import List, Dict, Optional

from .jira_client import JiraClient
from .config import CONSTRAINT_CUSTOM_FIELDS

logger = logging.getLogger(__name__)


# Field type to searcher mapping for Jira Data Center
# Note: Select fields don't need a searcher specified in DC - it auto-detects
FIELD_TYPE_SEARCHERS = {
    'com.atlassian.jira.plugin.system.customfieldtypes:textarea': 'com.atlassian.jira.plugin.system.customfieldtypes:textsearcher',
    'com.atlassian.jira.plugin.system.customfieldtypes:textfield': 'com.atlassian.jira.plugin.system.customfieldtypes:textsearcher',
    # Select fields - don't specify searcher, let Jira auto-detect
}


def setup_custom_fields(client: JiraClient) -> List[Dict]:
    """
    Create all custom fields defined in CONSTRAINT_CUSTOM_FIELDS.

    Args:
        client: JiraClient instance

    Returns:
        List of created/existing field data
    """
    results = []

    for field_key, field_def in CONSTRAINT_CUSTOM_FIELDS.items():
        logger.info(f"Setting up custom field: {field_def['name']}")

        try:
            # Get appropriate searcher for field type
            searcher_key = FIELD_TYPE_SEARCHERS.get(field_def['type'])

            field = client.create_custom_field(
                name=field_def['name'],
                description=field_def['description'],
                field_type=field_def['type'],
                searcher_key=searcher_key,
            )

            result = {
                'key': field_key,
                'name': field_def['name'],
                'type': field_def['type'],
                'status': 'created' if field else 'exists',
                'field': field,
            }

            # Note: Setting up select options requires additional API calls
            # that depend on the field context. This is typically done in Jira Admin UI.
            if 'options' in field_def:
                result['options_note'] = f"Options to configure manually: {field_def['options']}"

            results.append(result)

        except Exception as e:
            logger.error(f"Failed to create field {field_def['name']}: {e}")
            results.append({
                'key': field_key,
                'name': field_def['name'],
                'status': 'error',
                'error': str(e),
            })

    return results


def verify_custom_fields(client: JiraClient) -> Dict:
    """
    Verify all required custom fields exist.

    Returns:
        Dict with verification results
    """
    results = {
        'all_exist': True,
        'fields': [],
        'missing': [],
    }

    for field_key, field_def in CONSTRAINT_CUSTOM_FIELDS.items():
        field = client.get_custom_field_by_name(field_def['name'])
        exists = field is not None
        results['fields'].append({
            'key': field_key,
            'name': field_def['name'],
            'exists': exists,
            'field_id': field['id'] if field else None,
        })
        if not exists:
            results['all_exist'] = False
            results['missing'].append(field_def['name'])

    return results


def get_custom_field_id(client: JiraClient, name: str) -> Optional[str]:
    """Get the ID of a custom field by name."""
    field = client.get_custom_field_by_name(name)
    return field['id'] if field else None


def list_custom_fields(client: JiraClient) -> List[Dict]:
    """List all custom fields in Jira."""
    all_fields = client.get_fields()
    return [f for f in all_fields if f.get('custom', False)]


def print_custom_field_summary(results: List[Dict]):
    """Print summary of custom field setup."""
    print("\n" + "=" * 60)
    print("CUSTOM FIELD SETUP SUMMARY")
    print("=" * 60)

    created = [r for r in results if r['status'] == 'created']
    existing = [r for r in results if r['status'] == 'exists']
    errors = [r for r in results if r['status'] == 'error']

    print(f"\nCreated: {len(created)}")
    for r in created:
        print(f"  + {r['name']} ({r['type']})")
        if 'options_note' in r:
            print(f"    Note: {r['options_note']}")

    print(f"\nAlready existed: {len(existing)}")
    for r in existing:
        print(f"  = {r['name']}")

    if errors:
        print(f"\nErrors: {len(errors)}")
        for r in errors:
            print(f"  ! {r['name']}: {r['error']}")

    print("\n" + "-" * 60)
    print("IMPORTANT: For select fields, you must configure options manually:")
    print("-" * 60)
    for field_key, field_def in CONSTRAINT_CUSTOM_FIELDS.items():
        if 'options' in field_def:
            print(f"\n  {field_def['name']}:")
            for opt in field_def['options']:
                print(f"    - {opt}")

    print("\n  Go to Jira Admin > Issues > Custom Fields > [Field] > Configure")
    print("  to add these options to each select field.")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    # Allow running standalone for testing
    logging.basicConfig(level=logging.INFO)

    client = JiraClient()
    print("Testing Jira connection...")
    user = client.test_connection()
    print(f"Connected as: {user.get('displayName', user.get('name', 'unknown'))}")

    print("\nSetting up custom fields...")
    results = setup_custom_fields(client)
    print_custom_field_summary(results)

    print("\nVerifying custom fields...")
    verification = verify_custom_fields(client)
    print(f"All fields exist: {verification['all_exist']}")
    if verification['missing']:
        print(f"Missing: {verification['missing']}")
