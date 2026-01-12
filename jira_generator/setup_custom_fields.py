"""
Setup Jira Custom Fields.

Creates custom fields for Constraint issues:
- Risk Materiality (select)
- Mitigation Plan (textarea)
- Guild (select)

Creates custom fields for Story risk triggers:
- Risk: External Boundary (select)
- Risk: Sensitive Data (select)
- Risk: Security Controls (select)
- Risk: ML/AI Model Change (select)
- Risk: Critical Logic (select)
"""

import logging
from typing import List, Dict, Optional

from .jira_client import JiraClient
from .config import CONSTRAINT_CUSTOM_FIELDS, STORY_TRIGGER_FIELDS

logger = logging.getLogger(__name__)


# Field type to searcher mapping for Jira Data Center
# Note: Select fields don't need a searcher specified in DC - it auto-detects
FIELD_TYPE_SEARCHERS = {
    "com.atlassian.jira.plugin.system.customfieldtypes:textarea": "com.atlassian.jira.plugin.system.customfieldtypes:textsearcher",
    "com.atlassian.jira.plugin.system.customfieldtypes:textfield": "com.atlassian.jira.plugin.system.customfieldtypes:textsearcher",
    # Select fields - don't specify searcher, let Jira auto-detect
}


def setup_custom_fields(client: JiraClient) -> List[Dict]:
    """
    Create all custom fields defined in CONSTRAINT_CUSTOM_FIELDS and STORY_TRIGGER_FIELDS.

    Args:
        client: JiraClient instance

    Returns:
        List of created/existing field data
    """
    results = []

    # Combine all field definitions
    all_fields = {**CONSTRAINT_CUSTOM_FIELDS, **STORY_TRIGGER_FIELDS}

    for field_key, field_def in all_fields.items():
        logger.info(f"Setting up custom field: {field_def['name']}")

        try:
            # Get appropriate searcher for field type
            searcher_key = FIELD_TYPE_SEARCHERS.get(field_def["type"])

            field = client.create_custom_field(
                name=field_def["name"],
                description=field_def["description"],
                field_type=field_def["type"],
                searcher_key=searcher_key,
            )

            result = {
                "key": field_key,
                "name": field_def["name"],
                "type": field_def["type"],
                "status": "created" if field else "exists",
                "field": field,
            }

            # Add field to Default Screen (ID: 1)
            if field:
                field_id = field.get("id")
                if field_id:
                    screen_added = client.add_field_to_screen(1, field_id)
                    result["added_to_screen"] = screen_added

            # Note about manual option configuration for select fields
            if "options" in field_def:
                result["options_note"] = (
                    f"Options to configure manually: {field_def['options']}"
                )

            results.append(result)

        except Exception as e:
            logger.error(f"Failed to create field {field_def['name']}: {e}")
            results.append(
                {
                    "key": field_key,
                    "name": field_def["name"],
                    "status": "error",
                    "error": str(e),
                }
            )

    return results


def verify_custom_fields(client: JiraClient) -> Dict:
    """
    Verify all required custom fields exist.

    Returns:
        Dict with verification results
    """
    results = {
        "all_exist": True,
        "fields": [],
        "missing": [],
    }

    # Combine all field definitions
    all_fields = {**CONSTRAINT_CUSTOM_FIELDS, **STORY_TRIGGER_FIELDS}

    for field_key, field_def in all_fields.items():
        field = client.get_custom_field_by_name(field_def["name"])
        exists = field is not None
        results["fields"].append(
            {
                "key": field_key,
                "name": field_def["name"],
                "exists": exists,
                "field_id": field["id"] if field else None,
            }
        )
        if not exists:
            results["all_exist"] = False
            results["missing"].append(field_def["name"])

    return results


def get_custom_field_id(client: JiraClient, name: str) -> Optional[str]:
    """Get the ID of a custom field by name."""
    field = client.get_custom_field_by_name(name)
    return field["id"] if field else None


def list_custom_fields(client: JiraClient) -> List[Dict]:
    """List all custom fields in Jira."""
    all_fields = client.get_fields()
    return [f for f in all_fields if f.get("custom", False)]


def print_custom_field_summary(results: List[Dict]):
    """Print summary of custom field setup."""
    print("\n" + "=" * 60)
    print("CUSTOM FIELD SETUP SUMMARY")
    print("=" * 60)

    created = [r for r in results if r["status"] == "created"]
    existing = [r for r in results if r["status"] == "exists"]
    errors = [r for r in results if r["status"] == "error"]

    print(f"\nCreated: {len(created)}")
    for r in created:
        screen_status = "added to Default Screen" if r.get("added_to_screen") else ""
        print(f"  + {r['name']} ({r['type']}) {screen_status}")

    print(f"\nAlready existed: {len(existing)}")
    for r in existing:
        screen_status = "added to Default Screen" if r.get("added_to_screen") else ""
        print(f"  = {r['name']} {screen_status}")

    if errors:
        print(f"\nErrors: {len(errors)}")
        for r in errors:
            print(f"  ! {r['name']}: {r['error']}")

    print("\n" + "-" * 60)
    print("MANUAL CONFIGURATION REQUIRED:")
    print("-" * 60)
    print("\n  For select fields, configure options in Jira Admin:")
    print("  Jira Admin > Issues > Custom Fields > [Field] > Configure contexts > Options")

    # Combine all field definitions
    all_fields = {**CONSTRAINT_CUSTOM_FIELDS, **STORY_TRIGGER_FIELDS}

    for field_key, field_def in all_fields.items():
        if "options" in field_def:
            print(f"\n  {field_def['name']}:")
            for opt in field_def["options"]:
                print(f"    - {opt}")

    print("\n  Fields have been added to the Default Screen automatically.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
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
    if verification["missing"]:
        print(f"Missing: {verification['missing']}")
