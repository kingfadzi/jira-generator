"""
Setup Component Mapping for Jira Projects.

Updates component_mapping table to link applications to real Jira projects.
Removes fake Jira entries and inserts real project mappings.
"""

import os
import logging
import psycopg2
from typing import Dict, List

logger = logging.getLogger(__name__)

# Real Jira projects we created
JIRA_PROJECTS = [
    {"key": "DEVEX", "name": "Developer Experience"},
    {"key": "TECHCON", "name": "Technology Consolidation"},
    {"key": "AIOPS", "name": "AI Operations"},
    {"key": "GOV", "name": "Governance & Compliance"},
    {"key": "DATA", "name": "Data & Analytics"},
]


def get_db_connection():
    """Get database connection from environment."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "lct_data"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )


def get_jira_url() -> str:
    """Get Jira base URL from environment."""
    return os.getenv("JIRA_URL", "http://localhost:8080")


def delete_fake_jira_mappings(cursor) -> int:
    """Delete existing Jira mappings from component_mapping."""
    cursor.execute("""
        DELETE FROM component_mapping
        WHERE mapping_type = 'work_management'
          AND tool_type = 'Jira'
    """)
    return cursor.rowcount


def get_applications(cursor) -> List[Dict]:
    """Get all applications from source_data.component_mapping."""
    cursor.execute("""
        SELECT component_id, identifier, component_name
        FROM source_data.component_mapping
        WHERE mapping_type = 'it_business_application'
        ORDER BY component_id
    """)

    return [
        {"component_id": row[0], "identifier": row[1], "name": row[2]}
        for row in cursor.fetchall()
    ]


def insert_jira_mappings(cursor, applications: List[Dict], jira_url: str) -> int:
    """Insert Jira project mappings for applications."""
    inserted = 0

    for i, app in enumerate(applications):
        # Round-robin assignment to projects
        project = JIRA_PROJECTS[i % len(JIRA_PROJECTS)]

        cursor.execute(
            """
            INSERT INTO component_mapping (
                component_id,
                component_name,
                mapping_type,
                tool_type,
                name,
                identifier,
                project_key,
                instance_url,
                web_url
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
            (
                app["component_id"],
                app["name"],
                "work_management",
                "Jira",
                f"{app['name']} - {project['key']}",
                f"{app['identifier']}-{project['key']}",
                project["key"],
                jira_url,
                f"{jira_url}/projects/{project['key']}",
            ),
        )
        inserted += 1

    return inserted


def setup_component_mapping() -> Dict:
    """
    Setup component_mapping with real Jira projects.

    Returns:
        Dict with results
    """
    jira_url = get_jira_url()
    conn = get_db_connection()

    try:
        cursor = conn.cursor()

        # Delete fake Jira mappings
        deleted = delete_fake_jira_mappings(cursor)
        logger.info(f"Deleted {deleted} fake Jira mappings")

        # Get applications
        applications = get_applications(cursor)
        logger.info(f"Found {len(applications)} applications")

        # Insert real mappings
        inserted = insert_jira_mappings(cursor, applications, jira_url)
        logger.info(f"Inserted {inserted} Jira mappings")

        conn.commit()

        return {
            "deleted": deleted,
            "applications": len(applications),
            "inserted": inserted,
            "jira_url": jira_url,
        }

    except Exception as e:
        conn.rollback()
        logger.error(f"Failed to setup component mapping: {e}")
        raise
    finally:
        conn.close()


def print_mapping_summary(result: Dict):
    """Print summary of component mapping setup."""
    print("\n" + "=" * 60)
    print("COMPONENT MAPPING SETUP SUMMARY")
    print("=" * 60)

    print(f"\nJira URL: {result['jira_url']}")
    print(f"\nDeleted fake mappings: {result['deleted']}")
    print(f"Applications found: {result['applications']}")
    print(f"Mappings inserted: {result['inserted']}")

    print("\nProject distribution (round-robin):")
    for i, project in enumerate(JIRA_PROJECTS):
        count = (result["applications"] + len(JIRA_PROJECTS) - 1 - i) // len(
            JIRA_PROJECTS
        )
        print(f"  {project['key']}: {count} apps")

    print("=" * 60 + "\n")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("Setting up component mapping...")
    result = setup_component_mapping()
    print_mapping_summary(result)
