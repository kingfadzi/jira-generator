"""
Setup Jira Constraint Issues.

Creates Constraint issues and links them to Business Outcomes or Features.
"""

import logging
from typing import List, Dict, Optional

from .jira_client import JiraClient
from .config import ISSUE_TYPE_NAMES, CONSTRAINT_CUSTOM_FIELDS
from .data.constraints import CONSTRAINTS, count_constraints

logger = logging.getLogger(__name__)


class ConstraintBuilder:
    """Builds Constraint issues and links them to hierarchy items."""

    def __init__(self, client: JiraClient):
        self.client = client
        self.created_constraints: List[Dict] = []
        self.stats = {
            "created": 0,
            "exists": 0,
            "errors": 0,
            "links_created": 0,
            "links_failed": 0,
        }
        # Cache for custom field IDs
        self._field_id_cache: Dict[str, str] = {}

    def _get_custom_field_id(self, field_name: str) -> Optional[str]:
        """Get custom field ID by name, with caching."""
        if field_name in self._field_id_cache:
            return self._field_id_cache[field_name]

        field = self.client.get_custom_field_by_name(field_name)
        if field:
            self._field_id_cache[field_name] = field["id"]
            return field["id"]
        return None

    def _find_target_issue(
        self, project_key: str, issue_type: str, summary: str
    ) -> Optional[Dict]:
        """Find the target issue (BO or Feature) to link to."""
        # Map friendly type names to issue type names
        type_mapping = {
            "Business Outcome": ISSUE_TYPE_NAMES["business_outcome"],
            "Feature": ISSUE_TYPE_NAMES["feature"],
        }
        jira_issue_type = type_mapping.get(issue_type, issue_type)

        return self.client.find_issue_by_summary(project_key, summary, jira_issue_type)

    def create_constraint(self, constraint_data: Dict) -> Optional[Dict]:
        """
        Create a single Constraint issue.

        Args:
            constraint_data: Dict with constraint definition from data/constraints.py

        Returns:
            Created issue data or None on failure
        """
        project_key = constraint_data["blocks"]["project"]
        summary = constraint_data["summary"]

        # Check if constraint already exists
        existing = self.client.find_issue_by_summary(
            project_key, summary, ISSUE_TYPE_NAMES["constraint"]
        )
        if existing:
            logger.info(
                f"Constraint already exists: {existing.get('key')} - {summary[:40]}..."
            )
            self.stats["exists"] += 1
            return existing

        # Build custom fields
        custom_fields = {}

        # Note: Select fields (Risk Materiality, Guild) require options to be configured
        # in Jira Admin first. Skip them for now and only use text fields.

        # Mitigation Plan (textarea - works without options)
        mp_field = CONSTRAINT_CUSTOM_FIELDS.get("mitigation_plan", {})
        if mp_field:
            custom_fields[mp_field["name"]] = constraint_data.get("mitigation_plan", "")

        # Skip select fields until options are configured:
        # - Risk Materiality: needs options (Low, Medium, High, Critical)
        # - Guild: needs options (Security, Data, Operations, Enterprise Architecture)
        # These can be added later via Jira Admin > Custom Fields > Configure

        try:
            issue = self.client.create_issue(
                project_key=project_key,
                issue_type=ISSUE_TYPE_NAMES["constraint"],
                summary=summary,
                description=constraint_data.get("description", ""),
                custom_fields=custom_fields,
                labels=[
                    "constraint",
                    f"guild-{constraint_data.get('guild', 'unknown').lower().replace(' ', '-')}",
                ],
            )

            if issue:
                self.stats["created"] += 1
                self.created_constraints.append(
                    {
                        "key": issue.get("key"),
                        "summary": summary,
                        "guild": constraint_data.get("guild"),
                        "materiality": constraint_data.get("risk_materiality"),
                        "blocks": constraint_data["blocks"],
                    }
                )

                # Transition to appropriate status if not 'Identified' (default)
                target_status = constraint_data.get("status", "Identified")
                if target_status != "Identified":
                    self._transition_to_status(issue.get("key"), target_status)

            return issue

        except Exception as e:
            logger.error(f"Failed to create constraint '{summary[:40]}...': {e}")
            self.stats["errors"] += 1
            return None

    def _transition_to_status(self, issue_key: str, target_status: str):
        """Transition an issue to the target status."""
        # Define transition paths from 'Identified'
        transition_paths = {
            "In Progress": ["Start Work"],
            "Ready for Review": ["Start Work", "Submit for Review"],
            "Closed": ["Start Work", "Submit for Review", "Approve & Close"],
        }

        transitions = transition_paths.get(target_status, [])
        for transition_name in transitions:
            try:
                self.client.transition_issue(issue_key, transition_name)
            except Exception as e:
                logger.warning(
                    f"Failed to transition {issue_key} via '{transition_name}': {e}"
                )
                break

    def link_constraint_to_target(
        self, constraint_key: str, constraint_data: Dict
    ) -> bool:
        """
        Create a 'blocks' link from Constraint to target BO/Feature.

        Args:
            constraint_key: The Constraint issue key
            constraint_data: Dict with constraint definition

        Returns:
            True if link created successfully
        """
        blocks_info = constraint_data["blocks"]
        project_key = blocks_info["project"]
        target_type = blocks_info["type"]
        target_summary = blocks_info["summary"]

        # Find the target issue
        target_issue = self._find_target_issue(project_key, target_type, target_summary)
        if not target_issue:
            logger.warning(
                f"Target not found: {target_type} '{target_summary}' in {project_key}"
            )
            self.stats["links_failed"] += 1
            return False

        target_key = target_issue.get("key")

        try:
            # Create link: Constraint blocks Target
            # In Jira link terms: outward (Constraint) blocks inward (Target)
            self.client.create_issue_link(
                inward_issue=target_key,  # The blocked issue
                outward_issue=constraint_key,  # The blocking issue
                link_type="Blocks",
            )
            self.stats["links_created"] += 1
            logger.info(f"Linked: {constraint_key} blocks {target_key}")
            return True

        except Exception as e:
            logger.error(f"Failed to link {constraint_key} -> {target_key}: {e}")
            self.stats["links_failed"] += 1
            return False

    def build_constraints(self) -> Dict:
        """
        Create all constraints and link them to targets.

        Returns:
            Dict with results and statistics
        """
        result = {
            "constraints": [],
        }

        for constraint_data in CONSTRAINTS:
            logger.info(f"Creating Constraint: {constraint_data['summary'][:50]}...")

            # Create the constraint issue
            issue = self.create_constraint(constraint_data)

            if issue:
                constraint_key = issue.get("key")
                if constraint_key:
                    # Link to target BO or Feature
                    self.link_constraint_to_target(constraint_key, constraint_data)

                    result["constraints"].append(
                        {
                            "key": constraint_key,
                            "summary": constraint_data["summary"],
                            "guild": constraint_data.get("guild"),
                            "status": constraint_data.get("status"),
                            "blocks": f"{constraint_data['blocks']['type']}: {constraint_data['blocks']['summary']}",
                        }
                    )

        result["stats"] = self.stats
        return result


def setup_constraints(client: JiraClient) -> Dict:
    """
    Create all constraints in Jira.

    Args:
        client: JiraClient instance

    Returns:
        Dict with results and statistics
    """
    builder = ConstraintBuilder(client)
    return builder.build_constraints()


def print_constraint_summary(result: Dict):
    """Print summary of constraint setup."""
    print("\n" + "=" * 60)
    print("CONSTRAINT SETUP SUMMARY")
    print("=" * 60)

    expected = count_constraints()
    stats = result.get("stats", {})

    print(f"\nExpected: {expected['total']}")
    print(f"Created:  {stats.get('created', 0)}")
    print(f"Existed:  {stats.get('exists', 0)}")
    print(f"Errors:   {stats.get('errors', 0)}")

    print("\nLinks:")
    print(f"  Created: {stats.get('links_created', 0)}")
    print(f"  Failed:  {stats.get('links_failed', 0)}")

    print("\nBy Guild (expected):")
    for guild, count in expected["by_guild"].items():
        print(f"  {guild}: {count}")

    print("\nBy Status (expected):")
    for status, count in expected["by_status"].items():
        print(f"  {status}: {count}")

    print("\nBy Materiality (expected):")
    for mat, count in expected["by_materiality"].items():
        print(f"  {mat}: {count}")

    print("\nCreated Constraints:")
    print("-" * 40)
    for c in result.get("constraints", [])[:10]:
        print(f"  {c.get('key', 'N/A')}: [{c.get('guild')}] {c['summary'][:35]}...")
        print(f"    Blocks: {c.get('blocks', 'N/A')[:45]}...")

    total = len(result.get("constraints", []))
    if total > 10:
        print(f"  ... and {total - 10} more")

    print("=" * 60 + "\n")


if __name__ == "__main__":
    # Allow running standalone for testing
    logging.basicConfig(level=logging.INFO)

    client = JiraClient()
    print("Testing Jira connection...")
    user = client.test_connection()
    print(f"Connected as: {user.get('displayName', user.get('name', 'unknown'))}")

    print(f"\nExpected constraints to create: {count_constraints()['total']}")

    print("\nSetting up constraints...")
    result = setup_constraints(client)
    print_constraint_summary(result)
