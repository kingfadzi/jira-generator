"""
Jira Data Center Configuration.

All Jira connection settings and constants.
"""
import os
import sys
from pathlib import Path

# Load .env from project root
try:
    from dotenv import load_dotenv
    project_root = Path(__file__).resolve().parent.parent
    env_path = project_root / '.env'
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass


def get_required_env(var_name: str) -> str:
    """Get required environment variable or raise clear error."""
    value = os.getenv(var_name)
    if value is None:
        print(f"\n{'='*80}", file=sys.stderr)
        print(f"ERROR: Missing required environment variable: {var_name}", file=sys.stderr)
        print(f"{'='*80}", file=sys.stderr)
        print("\nJira configuration is required. Please set environment variables:", file=sys.stderr)
        print("  - JIRA_URL (Jira Data Center base URL)", file=sys.stderr)
        print("  - JIRA_USER (Jira username)", file=sys.stderr)
        print("  - JIRA_TOKEN (Personal Access Token)", file=sys.stderr)
        print("\nOption 1: Add to .env file:", file=sys.stderr)
        print("  JIRA_URL=https://jira.company.com", file=sys.stderr)
        print("  JIRA_USER=admin", file=sys.stderr)
        print("  JIRA_TOKEN=your-pat-token", file=sys.stderr)
        print("\nOption 2: Export environment variables:", file=sys.stderr)
        print("  export JIRA_URL=https://jira.company.com", file=sys.stderr)
        print("  export JIRA_USER=admin", file=sys.stderr)
        print("  export JIRA_TOKEN=your-pat-token", file=sys.stderr)
        print(f"\n{'='*80}\n", file=sys.stderr)
        sys.exit(1)
    return value


# Jira Connection Settings
JIRA_CONFIG = {
    'base_url': os.getenv('JIRA_URL', ''),
    'username': os.getenv('JIRA_USER', ''),
    'token': os.getenv('JIRA_TOKEN', ''),
    'verify_ssl': os.getenv('JIRA_VERIFY_SSL', 'true').lower() == 'true',
}

# API paths for Jira Data Center (API v2)
API_PATHS = {
    'project': '/rest/api/2/project',
    'issue': '/rest/api/2/issue',
    'issue_type': '/rest/api/2/issuetype',
    'field': '/rest/api/2/field',
    'status': '/rest/api/2/status',
    'workflow': '/rest/api/2/workflow',
    'issue_link': '/rest/api/2/issueLink',
    'issue_link_type': '/rest/api/2/issueLinkType',
    'version': '/rest/api/2/version',
    'search': '/rest/api/2/search',
    'myself': '/rest/api/2/myself',
}

# Constraint Issue Type Configuration
CONSTRAINT_ISSUE_TYPE = {
    'name': 'Constraint',
    'description': 'Governance constraint that blocks deployment until resolved',
    'type': 'standard',  # standard, subtask
}

# Constraint Workflow
CONSTRAINT_WORKFLOW = {
    'name': 'Constraint Workflow',
    'statuses': [
        {'name': 'Identified', 'category': 'new'},
        {'name': 'In Progress', 'category': 'indeterminate'},
        {'name': 'Ready for Review', 'category': 'indeterminate'},
        {'name': 'Closed', 'category': 'done'},
    ],
    'transitions': [
        {'from': 'Identified', 'to': 'In Progress', 'name': 'Start Work'},
        {'from': 'In Progress', 'to': 'Ready for Review', 'name': 'Submit for Review'},
        {'from': 'Ready for Review', 'to': 'Closed', 'name': 'Approve & Close'},
        {'from': 'Ready for Review', 'to': 'In Progress', 'name': 'Reject'},
        {'from': 'In Progress', 'to': 'Identified', 'name': 'Stop Work'},
    ],
}

# Custom Fields for Constraints
CONSTRAINT_CUSTOM_FIELDS = {
    'risk_materiality': {
        'name': 'Risk Materiality',
        'description': 'The materiality level of the risk',
        'type': 'com.atlassian.jira.plugin.system.customfieldtypes:select',
        'options': ['Low', 'Medium', 'High', 'Critical'],
    },
    'mitigation_plan': {
        'name': 'Mitigation Plan',
        'description': 'Description of how the risk will be mitigated',
        'type': 'com.atlassian.jira.plugin.system.customfieldtypes:textarea',
    },
    'guild': {
        'name': 'Guild',
        'description': 'The responsible guild for this constraint',
        'type': 'com.atlassian.jira.plugin.system.customfieldtypes:select',
        'options': ['Security', 'Data', 'Operations', 'Enterprise Architecture'],
    },
}

# Issue Link Types
ISSUE_LINK_TYPES = {
    'blocks': {
        'name': 'Blocks',
        'inward': 'is blocked by',
        'outward': 'blocks',
    },
}

# Hierarchy Level Mapping (for Advanced Roadmaps)
HIERARCHY_LEVELS = {
    'strategic_objective': 1,
    'portfolio_epic': 2,
    'business_outcome': 3,
    'feature': 4,
    'story': 5,
}

# Issue Type Names (must exist in Jira or be created)
# These map to the actual issue types in Jira Advanced Roadmaps
ISSUE_TYPE_NAMES = {
    'strategic_objective': 'Strategic Objective',
    'portfolio_epic': 'Portfolio Epic',
    'business_outcome': 'Business Outcome',
    'feature': 'Feature',
    'story': 'Story',
    'constraint': 'Constraint',
}
