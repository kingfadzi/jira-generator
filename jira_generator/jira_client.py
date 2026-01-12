"""
Jira Data Center REST API Client.

Provides methods for interacting with Jira Data Center v9.x REST API.
"""

import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin
import logging

from .config import JIRA_CONFIG, API_PATHS

logger = logging.getLogger(__name__)


class JiraClient:
    """REST API client for Jira Data Center."""

    def __init__(
        self,
        base_url: str = None,
        username: str = None,
        token: str = None,
        verify_ssl: bool = True,
        dry_run: bool = False,
    ):
        """
        Initialize Jira client.

        Args:
            base_url: Jira base URL (e.g., https://jira.company.com)
            username: Jira username
            token: Personal Access Token
            verify_ssl: Whether to verify SSL certificates
            dry_run: If True, don't make actual API calls
        """
        self.base_url = (base_url or JIRA_CONFIG["base_url"]).rstrip("/")
        self.username = username or JIRA_CONFIG["username"]
        self.token = token or JIRA_CONFIG["token"]
        self.verify_ssl = (
            verify_ssl if verify_ssl is not None else JIRA_CONFIG["verify_ssl"]
        )
        self.dry_run = dry_run

        self.session = requests.Session()
        # Jira Data Center uses Bearer token authentication for PATs
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )
        self.session.verify = self.verify_ssl

        # Cache for lookups
        self._issue_type_cache: Dict[str, Dict] = {}
        self._project_cache: Dict[str, Dict] = {}
        self._field_cache: Dict[str, Dict] = {}
        self._link_type_cache: Dict[str, Dict] = {}

    def _url(self, path: str) -> str:
        """Build full URL from path."""
        return urljoin(self.base_url, path)

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        """Make HTTP request to Jira API."""
        url = self._url(path)

        if self.dry_run and method.upper() != "GET":
            logger.info(f"[DRY RUN] {method.upper()} {url}")
            if "json" in kwargs:
                logger.info(f"[DRY RUN] Payload: {kwargs['json']}")
            # Return mock response for dry run
            mock_response = requests.Response()
            mock_response.status_code = 200
            mock_response._content = b"{}"
            return mock_response

        response = self.session.request(method, url, **kwargs)

        if not response.ok:
            logger.error(f"Jira API error: {response.status_code} {response.text}")
            response.raise_for_status()

        return response

    def get(self, path: str, **kwargs) -> Dict:
        """GET request."""
        response = self._request("GET", path, **kwargs)
        return response.json() if response.content else {}

    def post(self, path: str, data: Dict = None, **kwargs) -> Dict:
        """POST request."""
        response = self._request("POST", path, json=data, **kwargs)
        return response.json() if response.content else {}

    def put(self, path: str, data: Dict = None, **kwargs) -> Dict:
        """PUT request."""
        response = self._request("PUT", path, json=data, **kwargs)
        return response.json() if response.content else {}

    def delete(self, path: str, **kwargs) -> bool:
        """DELETE request."""
        self._request("DELETE", path, **kwargs)
        return True

    # =========================================================================
    # Connection Test
    # =========================================================================

    def test_connection(self) -> Dict:
        """Test connection to Jira and return current user info."""
        return self.get(API_PATHS["myself"])

    # =========================================================================
    # Projects
    # =========================================================================

    def get_project(self, project_key: str) -> Optional[Dict]:
        """Get project by key."""
        if project_key in self._project_cache:
            return self._project_cache[project_key]

        try:
            project = self.get(f"{API_PATHS['project']}/{project_key}")
            self._project_cache[project_key] = project
            return project
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise

    def project_exists(self, project_key: str) -> bool:
        """Check if project exists."""
        return self.get_project(project_key) is not None

    def create_project(
        self,
        key: str,
        name: str,
        project_type: str = "software",
        lead: str = None,
        description: str = None,
    ) -> Dict:
        """
        Create a new project.

        Args:
            key: Project key (e.g., 'CORE')
            name: Project name
            project_type: 'software' or 'business'
            lead: Project lead username (defaults to current user)
            description: Project description
        """
        if self.project_exists(key):
            logger.info(f"Project {key} already exists, skipping creation")
            return self.get_project(key)

        payload = {
            "key": key,
            "name": name,
            "projectTypeKey": project_type,
            "lead": lead or self.username,
        }
        if description:
            payload["description"] = description

        logger.info(f"Creating project: {key} - {name}")
        project = self.post(API_PATHS["project"], payload)
        self._project_cache[key] = project
        return project

    def get_all_projects(self) -> List[Dict]:
        """Get all projects."""
        return self.get(API_PATHS["project"])

    # =========================================================================
    # Issue Types
    # =========================================================================

    def get_issue_types(self) -> List[Dict]:
        """Get all issue types."""
        return self.get(API_PATHS["issue_type"])

    def get_issue_type_by_name(self, name: str) -> Optional[Dict]:
        """Get issue type by name."""
        if name in self._issue_type_cache:
            return self._issue_type_cache[name]

        issue_types = self.get_issue_types()
        for it in issue_types:
            self._issue_type_cache[it["name"]] = it
            if it["name"] == name:
                return it
        return None

    def issue_type_exists(self, name: str) -> bool:
        """Check if issue type exists."""
        return self.get_issue_type_by_name(name) is not None

    def create_issue_type(
        self, name: str, description: str = None, type: str = "standard"
    ) -> Dict:
        """
        Create a new issue type.

        Args:
            name: Issue type name
            description: Description
            type: 'standard' or 'subtask'
        """
        if self.issue_type_exists(name):
            logger.info(f"Issue type '{name}' already exists, skipping creation")
            return self.get_issue_type_by_name(name)

        payload = {
            "name": name,
            "description": description or f"{name} issue type",
            "type": type,
        }

        logger.info(f"Creating issue type: {name}")
        issue_type = self.post(API_PATHS["issue_type"], payload)
        self._issue_type_cache[name] = issue_type
        return issue_type

    # =========================================================================
    # Custom Fields
    # =========================================================================

    def get_fields(self) -> List[Dict]:
        """Get all fields (system and custom)."""
        return self.get(API_PATHS["field"])

    def get_custom_field_by_name(self, name: str) -> Optional[Dict]:
        """Get custom field by name."""
        if name in self._field_cache:
            return self._field_cache[name]

        fields = self.get_fields()
        for field in fields:
            if field.get("custom", False):
                self._field_cache[field["name"]] = field
                if field["name"] == name:
                    return field
        return None

    def custom_field_exists(self, name: str) -> bool:
        """Check if custom field exists."""
        return self.get_custom_field_by_name(name) is not None

    def create_custom_field(
        self, name: str, description: str, field_type: str, searcher_key: str = None
    ) -> Dict:
        """
        Create a custom field.

        Args:
            name: Field name
            description: Field description
            field_type: Field type (e.g., 'com.atlassian.jira.plugin.system.customfieldtypes:select')
            searcher_key: Searcher type for the field
        """
        if self.custom_field_exists(name):
            logger.info(f"Custom field '{name}' already exists, skipping creation")
            return self.get_custom_field_by_name(name)

        payload = {
            "name": name,
            "description": description,
            "type": field_type,
        }
        if searcher_key:
            payload["searcherKey"] = searcher_key

        logger.info(f"Creating custom field: {name}")
        field = self.post(API_PATHS["field"], payload)
        self._field_cache[name] = field
        return field

    # =========================================================================
    # Versions (Fix Versions)
    # =========================================================================

    def get_project_versions(self, project_key: str) -> List[Dict]:
        """Get all versions for a project."""
        return self.get(f"{API_PATHS['project']}/{project_key}/versions")

    def get_version_by_name(self, project_key: str, name: str) -> Optional[Dict]:
        """Get version by name within a project."""
        versions = self.get_project_versions(project_key)
        for v in versions:
            if v["name"] == name:
                return v
        return None

    def create_version(
        self,
        project_key: str,
        name: str,
        description: str = None,
        released: bool = False,
        start_date: str = None,
        release_date: str = None,
    ) -> Dict:
        """
        Create a version (Fix Version) in a project.

        Args:
            project_key: Project key
            name: Version name (e.g., 'v1.0.0')
            description: Version description
            released: Whether the version is released
            start_date: Start date (YYYY-MM-DD)
            release_date: Release date (YYYY-MM-DD)
        """
        existing = self.get_version_by_name(project_key, name)
        if existing:
            logger.info(f"Version '{name}' already exists in {project_key}, skipping")
            return existing

        payload = {
            "project": project_key,
            "name": name,
            "released": released,
        }
        if description:
            payload["description"] = description
        if start_date:
            payload["startDate"] = start_date
        if release_date:
            payload["releaseDate"] = release_date

        logger.info(f"Creating version: {project_key}/{name}")
        return self.post(API_PATHS["version"], payload)

    # =========================================================================
    # Issues
    # =========================================================================

    def get_issue(self, issue_key: str, fields: str = "*all") -> Optional[Dict]:
        """Get issue by key."""
        try:
            return self.get(
                f"{API_PATHS['issue']}/{issue_key}", params={"fields": fields}
            )
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise

    def issue_exists(self, issue_key: str) -> bool:
        """Check if issue exists."""
        return self.get_issue(issue_key) is not None

    def create_issue(
        self,
        project_key: str,
        issue_type: str,
        summary: str,
        description: str = None,
        parent_key: str = None,
        fix_versions: List[str] = None,
        custom_fields: Dict[str, Any] = None,
        labels: List[str] = None,
    ) -> Dict:
        """
        Create an issue.

        Args:
            project_key: Project key
            issue_type: Issue type name
            summary: Issue summary
            description: Issue description
            parent_key: Parent issue key (for hierarchy)
            fix_versions: List of fix version names
            custom_fields: Dict of custom field name -> value
            labels: List of labels
        """
        fields = {
            "project": {"key": project_key},
            "issuetype": {"name": issue_type},
            "summary": summary,
        }

        if description:
            fields["description"] = description

        if parent_key:
            # Use Parent Link (customfield_10108) for Advanced Roadmaps hierarchy
            # Not the standard 'parent' field which is for sub-tasks only
            fields["customfield_10108"] = parent_key

        if fix_versions:
            fields["fixVersions"] = [{"name": v} for v in fix_versions]

        # Note: Labels field may not be on all screens, so we skip it
        # If labels are needed, add them to the screen in Jira Admin
        # if labels:
        #     fields['labels'] = labels

        if custom_fields:
            for field_name, value in custom_fields.items():
                field = self.get_custom_field_by_name(field_name)
                if field:
                    field_id = field["id"]
                    # Handle select fields
                    if isinstance(value, str) and "select" in field.get(
                        "schema", {}
                    ).get("type", ""):
                        fields[field_id] = {"value": value}
                    else:
                        fields[field_id] = value

        logger.info(f"Creating issue: [{project_key}] {issue_type} - {summary}")
        return self.post(API_PATHS["issue"], {"fields": fields})

    def search_issues(
        self,
        jql: str,
        fields: str = "key,summary,issuetype,status",
        max_results: int = 100,
    ) -> List[Dict]:
        """
        Search issues using JQL.

        Args:
            jql: JQL query string
            fields: Comma-separated list of fields to return
            max_results: Maximum number of results
        """
        payload = {
            "jql": jql,
            "fields": fields.split(",") if isinstance(fields, str) else fields,
            "maxResults": max_results,
        }
        result = self.post(API_PATHS["search"], payload)
        return result.get("issues", [])

    def find_issue_by_summary(
        self, project_key: str, summary: str, issue_type: str = None
    ) -> Optional[Dict]:
        """Find an issue by its summary in a project."""
        # Escape special JQL characters in summary
        escaped_summary = summary.replace('"', '\\"')
        jql = f'project = {project_key} AND summary ~ "{escaped_summary}"'
        if issue_type:
            jql += f' AND issuetype = "{issue_type}"'

        issues = self.search_issues(jql)
        # Find exact match
        for issue in issues:
            if issue["fields"]["summary"] == summary:
                return issue
        return None

    # =========================================================================
    # Issue Links
    # =========================================================================

    def get_issue_link_types(self) -> List[Dict]:
        """Get all issue link types."""
        result = self.get(API_PATHS["issue_link_type"])
        return result.get("issueLinkTypes", [])

    def get_link_type_by_name(self, name: str) -> Optional[Dict]:
        """Get issue link type by name."""
        if name in self._link_type_cache:
            return self._link_type_cache[name]

        link_types = self.get_issue_link_types()
        for lt in link_types:
            self._link_type_cache[lt["name"]] = lt
            if lt["name"] == name:
                return lt
        return None

    def create_issue_link(
        self, inward_issue: str, outward_issue: str, link_type: str = "Blocks"
    ) -> bool:
        """
        Create a link between two issues.

        Args:
            inward_issue: The issue that is blocked (e.g., 'PROJ-123')
            outward_issue: The issue that blocks (e.g., 'PROJ-456')
            link_type: Link type name (default: 'Blocks')
        """
        link_type_obj = self.get_link_type_by_name(link_type)
        if not link_type_obj:
            logger.error(f"Link type '{link_type}' not found")
            return False

        payload = {
            "type": {"name": link_type},
            "inwardIssue": {"key": inward_issue},
            "outwardIssue": {"key": outward_issue},
        }

        logger.info(f"Creating link: {outward_issue} blocks {inward_issue}")
        self.post(API_PATHS["issue_link"], payload)
        return True

    # =========================================================================
    # Workflow & Status (limited in REST API)
    # =========================================================================

    def get_statuses(self) -> List[Dict]:
        """Get all statuses."""
        return self.get(API_PATHS["status"])

    def get_status_by_name(self, name: str) -> Optional[Dict]:
        """Get status by name."""
        statuses = self.get_statuses()
        for s in statuses:
            if s["name"] == name:
                return s
        return None

    def transition_issue(self, issue_key: str, transition_name: str) -> bool:
        """
        Transition an issue to a new status.

        Args:
            issue_key: Issue key
            transition_name: Name of the transition to execute
        """
        # Get available transitions
        transitions = self.get(f"{API_PATHS['issue']}/{issue_key}/transitions")

        for t in transitions.get("transitions", []):
            if t["name"] == transition_name:
                self.post(
                    f"{API_PATHS['issue']}/{issue_key}/transitions",
                    {"transition": {"id": t["id"]}},
                )
                logger.info(f"Transitioned {issue_key} via '{transition_name}'")
                return True

        logger.warning(f"Transition '{transition_name}' not found for {issue_key}")
        return False

    def update_issue(self, issue_key: str, fields: Dict) -> Dict:
        """
        Update an issue's fields.

        Args:
            issue_key: Issue key
            fields: Dict of field name -> value
        """
        logger.info(f"Updating issue: {issue_key}")
        return self.put(f"{API_PATHS['issue']}/{issue_key}", {"fields": fields})

    def set_fix_version(self, issue_key: str, version_name: str) -> Dict:
        """Set fix version on an issue."""
        return self.update_issue(issue_key, {"fixVersions": [{"name": version_name}]})

    # =========================================================================
    # Screens
    # =========================================================================

    def get_screens(self) -> List[Dict]:
        """
        Get all screens.

        Returns:
            List of screen objects with id and name
        """
        try:
            result = self.get("/rest/api/2/screens")
            # Handle both list response and paginated response
            if isinstance(result, list):
                return result
            return result.get("values", [])
        except requests.HTTPError as e:
            logger.error(f"Failed to get screens: {e}")
            return []

    def get_project_screens(self, project_key: str) -> List[Dict]:
        """
        Get all screens for a project by matching screen name prefix.

        Args:
            project_key: Project key (e.g., 'TECHCON')

        Returns:
            List of matching screen objects
        """
        all_screens = self.get_screens()
        prefix = f"{project_key}:"
        return [s for s in all_screens if s.get("name", "").startswith(prefix)]

    def get_screen_tabs(self, screen_id: int) -> List[Dict]:
        """
        Get all tabs for a screen.

        Args:
            screen_id: Screen ID

        Returns:
            List of tab objects with id and name
        """
        try:
            return self.get(f"/rest/api/2/screens/{screen_id}/tabs")
        except requests.HTTPError as e:
            logger.error(f"Failed to get tabs for screen {screen_id}: {e}")
            return []

    def add_field_to_screen(self, screen_id: int, field_id: str) -> bool:
        """
        Add a field to a screen.

        Args:
            screen_id: Screen ID (e.g., 1 for Default Screen)
            field_id: Field ID (e.g., 'customfield_10212')

        Returns:
            True if successful or field already on screen
        """
        # Get the first tab ID for this screen
        tabs = self.get_screen_tabs(screen_id)
        if not tabs:
            logger.error(f"No tabs found for screen {screen_id}")
            return False

        tab_id = tabs[0]["id"]

        try:
            self.post(f"/rest/api/2/screens/{screen_id}/tabs/{tab_id}/fields", {"fieldId": field_id})
            logger.info(f"Added {field_id} to screen {screen_id}")
            return True
        except requests.HTTPError as e:
            if e.response.status_code == 400 and "already" in e.response.text.lower():
                logger.info(f"Field {field_id} already on screen {screen_id}")
                return True
            logger.error(f"Failed to add {field_id} to screen {screen_id}: {e}")
            return False
