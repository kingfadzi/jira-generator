# Jira Generator

Populates Jira Data Center with governance test data for LCT migration planning.

## Installation

```bash
git clone https://github.com/kingfadzi/jira-generator.git
cd jira-generator
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Jira credentials
```

## Configuration

```bash
# .env file
JIRA_URL=http://your-jira:8080
JIRA_USER=admin
JIRA_TOKEN=your-pat-token
JIRA_VERIFY_SSL=false

# Database (for component-mapping feature)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=lct_data
DB_USER=postgres
DB_PASSWORD=postgres
```

## Usage

```bash
# Full setup
python run.py --all

# Individual phases
python run.py --projects
python run.py --hierarchy
python run.py --constraints
python run.py --versions
python run.py --feature-versions
python run.py --component-mapping

# Teardown
python run.py --teardown         # Delete issues, keep projects
python run.py --teardown-all     # Delete everything

# Rebuild (teardown + setup)
python run.py --rebuild
python run.py --rebuild -f       # Skip confirmation

# Preview
python run.py --dry-run --all
```

Alternative module invocation:
```bash
python -m jira_generator.main --all
```

## What Gets Created

| Type | Count |
|------|-------|
| Projects | 5 (DEVEX, TECHCON, AIOPS, GOV, DATA) |
| Strategic Objectives | 5 |
| Portfolio Epics | 15 |
| Business Outcomes | 40 |
| Features | 120 |
| Constraints | 18 |

## Prerequisites

- Jira Data Center with Advanced Roadmaps
- Issue types: Strategic Objective, Portfolio Epic, Business Outcome, Feature, Constraint
- "LCT Governance Scheme" assigned to projects
- Parent Link field (customfield_10108) for hierarchy

## Project Structure

```
jira-generator/
├── run.py                  # Entry point
├── requirements.txt
├── .env.example
├── README.md
└── jira_generator/
    ├── __init__.py
    ├── config.py           # Configuration & constants
    ├── jira_client.py      # Jira REST API client
    ├── main.py             # CLI orchestrator
    ├── data/
    │   ├── projects.py     # Project definitions
    │   ├── hierarchy.py    # Strategic hierarchy data
    │   └── constraints.py  # Constraint definitions
    ├── setup_projects.py
    ├── setup_issue_types.py
    ├── setup_custom_fields.py
    ├── setup_hierarchy.py
    ├── setup_constraints.py
    ├── setup_versions.py
    ├── setup_feature_versions.py
    ├── setup_component_mapping.py
    └── teardown.py
```

## Related Repositories

- [lean-migration](https://github.com/kingfadzi/lean-migration) - Core lineage migration & validation
- [tech-stack-generator](https://github.com/kingfadzi/tech-stack-generator) - Tech stack analysis & enrichment
