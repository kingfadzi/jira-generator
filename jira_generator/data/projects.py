"""
Jira Project Definitions.

Projects to create in Jira for LCT testing.
"""

# Projects aligned with Strategic Objectives
PROJECTS = [
    {
        "key": "DEVEX",
        "name": "Developer Experience",
        "description": "Streamline Developer Experience initiatives",
        "lead": None,  # Uses current user
    },
    {
        "key": "TECHCON",
        "name": "Technology Consolidation",
        "description": "Consolidate Technology Platforms initiatives",
        "lead": None,
    },
    {
        "key": "AIOPS",
        "name": "AI Operations",
        "description": "AI-Powered Operations initiatives",
        "lead": None,
    },
    {
        "key": "GOV",
        "name": "Governance & Compliance",
        "description": "Automate Governance & Compliance initiatives",
        "lead": None,
    },
    {
        "key": "DATA",
        "name": "Data & Analytics",
        "description": "Accelerate Data-Driven Decisions initiatives",
        "lead": None,
    },
]

# Mapping of Strategic Objective to Project
STRATEGIC_OBJ_TO_PROJECT = {
    "Streamline Developer Experience": "DEVEX",
    "Consolidate Technology Platforms": "TECHCON",
    "AI-Powered Operations": "AIOPS",
    "Automate Governance & Compliance": "GOV",
    "Accelerate Data-Driven Decisions": "DATA",
}
