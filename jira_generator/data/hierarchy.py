"""
Full Jira Hierarchy Data.

Strategic Objectives -> Portfolio Epics -> Business Outcomes -> Features
"""

HIERARCHY = [
    # =========================================================================
    # 1. Streamline Developer Experience
    # =========================================================================
    {
        "strategic_objective": {
            "summary": "Streamline Developer Experience",
            "description": "Reduce friction in the software delivery lifecycle - faster onboarding, self-service infrastructure, automated compliance gates, and unified toolchain",
            "project": "DEVEX",
        },
        "portfolio_epics": [
            {
                "summary": "Self-Service Infrastructure",
                "description": "Enable developers to provision and manage infrastructure on-demand",
                "business_outcomes": [
                    {
                        "summary": "On-Demand Environment Provisioning",
                        "description": "Developers can spin up environments in minutes without tickets",
                        "features": [
                            {
                                "summary": "Infrastructure-as-Code templates",
                                "description": "Terraform/Pulumi templates for common architectures",
                            },
                            {
                                "summary": "Environment request portal",
                                "description": "Self-service UI for environment provisioning",
                            },
                            {
                                "summary": "Auto-teardown for idle environments",
                                "description": "Cost savings through automatic cleanup of unused resources",
                            },
                        ],
                    },
                    {
                        "summary": "Developer Cloud Workspaces",
                        "description": "Cloud-based development environments for consistent tooling",
                        "features": [
                            {
                                "summary": "Cloud IDE provisioning",
                                "description": "VS Code Server or GitHub Codespaces integration",
                            },
                            {
                                "summary": "Pre-configured dev containers",
                                "description": "Standardized development containers per stack",
                            },
                            {
                                "summary": "Secrets injection automation",
                                "description": "Secure secrets management for dev environments",
                            },
                        ],
                    },
                    {
                        "summary": "Database Self-Service",
                        "description": "On-demand database provisioning and data management",
                        "features": [
                            {
                                "summary": "On-demand database cloning",
                                "description": "Clone production databases for testing",
                            },
                            {
                                "summary": "Data masking for non-prod",
                                "description": "Automatic PII masking in non-production environments",
                            },
                            {
                                "summary": "Schema migration automation",
                                "description": "Automated database schema deployments",
                            },
                        ],
                    },
                ],
            },
            {
                "summary": "Unified CI/CD Platform",
                "description": "Standardized build, test, and deployment pipelines",
                "business_outcomes": [
                    {
                        "summary": "Pipeline Standardization",
                        "description": "Golden path CI/CD templates for all teams",
                        "features": [
                            {
                                "summary": "Golden pipeline templates",
                                "description": "Reusable pipeline templates for common patterns",
                            },
                            {
                                "summary": "Build time optimization",
                                "description": "Caching, parallelization, and incremental builds",
                            },
                            {
                                "summary": "Artifact management consolidation",
                                "description": "Single artifact repository (Nexus/Artifactory)",
                            },
                        ],
                    },
                    {
                        "summary": "Automated Quality Gates",
                        "description": "Shift-left quality enforcement in pipelines",
                        "features": [
                            {
                                "summary": "SAST/DAST integration",
                                "description": "Security scanning in CI pipelines",
                            },
                            {
                                "summary": "Test coverage enforcement",
                                "description": "Minimum coverage thresholds per project",
                            },
                            {
                                "summary": "Performance regression detection",
                                "description": "Automated performance benchmarking",
                            },
                        ],
                    },
                    {
                        "summary": "Progressive Delivery",
                        "description": "Safe rollout strategies for deployments",
                        "features": [
                            {
                                "summary": "Feature flag platform",
                                "description": "LaunchDarkly/Split integration for feature toggles",
                            },
                            {
                                "summary": "Canary deployment automation",
                                "description": "Gradual rollout with automatic rollback",
                            },
                            {
                                "summary": "Rollback automation",
                                "description": "One-click rollback for failed deployments",
                            },
                        ],
                    },
                ],
            },
            {
                "summary": "Developer Onboarding & Enablement",
                "description": "Fast-track new developers to productivity",
                "business_outcomes": [
                    {
                        "summary": "Day-1 Productivity",
                        "description": "New developers productive within first day",
                        "features": [
                            {
                                "summary": "Automated access provisioning",
                                "description": "JIT access to required systems on hire",
                            },
                            {
                                "summary": "Onboarding checklist automation",
                                "description": "Guided setup with progress tracking",
                            },
                            {
                                "summary": "Starter project templates",
                                "description": "Cookiecutter templates for new services",
                            },
                        ],
                    },
                    {
                        "summary": "Inner Source Program",
                        "description": "Foster code reuse and collaboration across teams",
                        "features": [
                            {
                                "summary": "Internal package registry",
                                "description": "Private npm/PyPI for shared libraries",
                            },
                            {
                                "summary": "Shared component library",
                                "description": "UI component library for frontend consistency",
                            },
                            {
                                "summary": "Contribution guidelines & tooling",
                                "description": "PR templates, code owners, review automation",
                            },
                        ],
                    },
                ],
            },
        ],
    },
    # =========================================================================
    # 2. Consolidate Technology Platforms
    # =========================================================================
    {
        "strategic_objective": {
            "summary": "Consolidate Technology Platforms",
            "description": "Reduce tech sprawl by rationalizing redundant systems, standardizing on strategic platforms, and eliminating shadow IT",
            "project": "TECHCON",
        },
        "portfolio_epics": [
            {
                "summary": "Application Rationalization",
                "description": "Reduce application portfolio complexity",
                "business_outcomes": [
                    {
                        "summary": "Portfolio Assessment",
                        "description": "Complete visibility into application landscape",
                        "features": [
                            {
                                "summary": "Application inventory discovery",
                                "description": "Automated discovery of all applications",
                            },
                            {
                                "summary": "TCO analysis tooling",
                                "description": "Total cost of ownership calculator",
                            },
                            {
                                "summary": "Redundancy identification",
                                "description": "Find duplicate/overlapping applications",
                            },
                        ],
                    },
                    {
                        "summary": "Sunset Legacy Systems",
                        "description": "Retire end-of-life applications",
                        "features": [
                            {
                                "summary": "Decommission roadmap planning",
                                "description": "Phased retirement schedules",
                            },
                            {
                                "summary": "Data migration execution",
                                "description": "Safe data extraction and archival",
                            },
                            {
                                "summary": "Consumer cutover coordination",
                                "description": "Stakeholder communication and transition",
                            },
                        ],
                    },
                    {
                        "summary": "Build vs Buy Framework",
                        "description": "Decision framework for new capabilities",
                        "features": [
                            {
                                "summary": "Vendor evaluation criteria",
                                "description": "Standardized RFP scoring matrix",
                            },
                            {
                                "summary": "Total cost modeling",
                                "description": "5-year TCO comparison templates",
                            },
                            {
                                "summary": "Strategic vendor partnerships",
                                "description": "Preferred vendor program",
                            },
                        ],
                    },
                ],
            },
            {
                "summary": "Infrastructure Standardization",
                "description": "Converge on strategic infrastructure platforms",
                "business_outcomes": [
                    {
                        "summary": "Cloud Landing Zone",
                        "description": "Standardized cloud foundation",
                        "features": [
                            {
                                "summary": "Account/subscription structure",
                                "description": "Multi-account strategy with guardrails",
                            },
                            {
                                "summary": "Network topology standards",
                                "description": "Hub-spoke network architecture",
                            },
                            {
                                "summary": "Tagging & cost allocation",
                                "description": "Mandatory tagging for cost attribution",
                            },
                        ],
                    },
                    {
                        "summary": "Container Platform Consolidation",
                        "description": "Single Kubernetes platform",
                        "features": [
                            {
                                "summary": "Kubernetes cluster standards",
                                "description": "EKS/AKS/GKE configuration baseline",
                            },
                            {
                                "summary": "Service mesh adoption",
                                "description": "Istio/Linkerd for service-to-service",
                            },
                            {
                                "summary": "Image registry consolidation",
                                "description": "Single container registry with scanning",
                            },
                        ],
                    },
                    {
                        "summary": "Database Platform Reduction",
                        "description": "Reduce database engine sprawl",
                        "features": [
                            {
                                "summary": "Strategic DB engine selection",
                                "description": "PostgreSQL, MongoDB, Redis as standards",
                            },
                            {
                                "summary": "Migration path tooling",
                                "description": "Database migration automation",
                            },
                            {
                                "summary": "DBA self-service portal",
                                "description": "Self-service database provisioning",
                            },
                        ],
                    },
                ],
            },
            {
                "summary": "Toolchain Consolidation",
                "description": "Reduce tool sprawl across SDLC",
                "business_outcomes": [
                    {
                        "summary": "ITSM Unification",
                        "description": "Single IT Service Management platform",
                        "features": [
                            {
                                "summary": "ServiceNow single instance",
                                "description": "Consolidate to one SNOW instance",
                            },
                            {
                                "summary": "CMDB data quality program",
                                "description": "Automated CMDB reconciliation",
                            },
                            {
                                "summary": "Workflow standardization",
                                "description": "Common change/incident workflows",
                            },
                        ],
                    },
                    {
                        "summary": "Observability Stack Convergence",
                        "description": "Unified monitoring and logging",
                        "features": [
                            {
                                "summary": "Monitoring tool reduction",
                                "description": "Converge from 5+ tools to 1-2",
                            },
                            {
                                "summary": "Single pane of glass dashboard",
                                "description": "Unified operations dashboard",
                            },
                            {
                                "summary": "Alert routing consolidation",
                                "description": "Single alert management system",
                            },
                        ],
                    },
                ],
            },
        ],
    },
    # =========================================================================
    # 3. AI-Powered Operations
    # =========================================================================
    {
        "strategic_objective": {
            "summary": "AI-Powered Operations",
            "description": "Embed AI/ML into operational processes - predictive incident detection, automated remediation, intelligent capacity planning, and AIOps",
            "project": "AIOPS",
        },
        "portfolio_epics": [
            {
                "summary": "Predictive Incident Management",
                "description": "Detect and prevent incidents before impact",
                "business_outcomes": [
                    {
                        "summary": "Anomaly Detection",
                        "description": "ML-based detection of abnormal patterns",
                        "features": [
                            {
                                "summary": "ML-based threshold tuning",
                                "description": "Dynamic thresholds based on patterns",
                            },
                            {
                                "summary": "Log pattern recognition",
                                "description": "NLP for log anomaly detection",
                            },
                            {
                                "summary": "Metric correlation engine",
                                "description": "Cross-metric anomaly correlation",
                            },
                        ],
                    },
                    {
                        "summary": "Predictive Alerting",
                        "description": "Alert before failures occur",
                        "features": [
                            {
                                "summary": "Failure prediction models",
                                "description": "Time-series forecasting for failures",
                            },
                            {
                                "summary": "Alert noise reduction",
                                "description": "ML-based alert deduplication",
                            },
                            {
                                "summary": "Incident probability scoring",
                                "description": "Risk scores for potential incidents",
                            },
                        ],
                    },
                    {
                        "summary": "Root Cause Analysis Automation",
                        "description": "Accelerate incident diagnosis",
                        "features": [
                            {
                                "summary": "Topology-aware diagnostics",
                                "description": "Service map-based root cause",
                            },
                            {
                                "summary": "Change correlation analysis",
                                "description": "Link incidents to recent changes",
                            },
                            {
                                "summary": "Suggested remediation engine",
                                "description": "AI-recommended fix actions",
                            },
                        ],
                    },
                ],
            },
            {
                "summary": "Intelligent Automation",
                "description": "AI-driven operational automation",
                "business_outcomes": [
                    {
                        "summary": "Auto-Remediation",
                        "description": "Self-healing infrastructure",
                        "features": [
                            {
                                "summary": "Runbook automation library",
                                "description": "Codified remediation procedures",
                            },
                            {
                                "summary": "Self-healing infrastructure",
                                "description": "Automatic recovery actions",
                            },
                            {
                                "summary": "Automated rollback triggers",
                                "description": "ML-triggered deployment rollbacks",
                            },
                        ],
                    },
                    {
                        "summary": "Capacity Intelligence",
                        "description": "Smart resource management",
                        "features": [
                            {
                                "summary": "Demand forecasting models",
                                "description": "Predict capacity needs",
                            },
                            {
                                "summary": "Auto-scaling optimization",
                                "description": "ML-tuned scaling policies",
                            },
                            {
                                "summary": "Cost anomaly detection",
                                "description": "Alert on unexpected spend",
                            },
                        ],
                    },
                    {
                        "summary": "ChatOps & Virtual SRE",
                        "description": "Conversational operations",
                        "features": [
                            {
                                "summary": "Slack/Teams bot integration",
                                "description": "ChatOps command interface",
                            },
                            {
                                "summary": "Natural language incident queries",
                                "description": "Ask questions about incidents",
                            },
                            {
                                "summary": "Automated status communications",
                                "description": "AI-generated status updates",
                            },
                        ],
                    },
                ],
            },
            {
                "summary": "Knowledge & Learning Systems",
                "description": "Capture and leverage operational knowledge",
                "business_outcomes": [
                    {
                        "summary": "Operational Knowledge Base",
                        "description": "Centralized ops knowledge",
                        "features": [
                            {
                                "summary": "Incident pattern library",
                                "description": "Searchable incident history",
                            },
                            {
                                "summary": "Auto-generated runbooks",
                                "description": "ML-suggested procedures",
                            },
                            {
                                "summary": "Tribal knowledge capture",
                                "description": "Document expert knowledge",
                            },
                        ],
                    },
                    {
                        "summary": "Continuous Learning Pipeline",
                        "description": "Models that improve over time",
                        "features": [
                            {
                                "summary": "Model retraining automation",
                                "description": "Scheduled model updates",
                            },
                            {
                                "summary": "Feedback loop integration",
                                "description": "Operator feedback for learning",
                            },
                            {
                                "summary": "Drift detection & alerting",
                                "description": "Detect model degradation",
                            },
                        ],
                    },
                ],
            },
        ],
    },
    # =========================================================================
    # 4. Automate Governance & Compliance
    # =========================================================================
    {
        "strategic_objective": {
            "summary": "Automate Governance & Compliance",
            "description": "Shift compliance left with policy-as-code, automated evidence collection, and continuous control monitoring - eliminate manual audit burden",
            "project": "GOV",
        },
        "portfolio_epics": [
            {
                "summary": "Policy-as-Code Platform",
                "description": "Codified governance policies",
                "business_outcomes": [
                    {
                        "summary": "Preventive Controls",
                        "description": "Block non-compliant changes before deployment",
                        "features": [
                            {
                                "summary": "OPA/Rego policy library",
                                "description": "Reusable policy definitions",
                            },
                            {
                                "summary": "Pre-commit policy hooks",
                                "description": "Developer-time policy checks",
                            },
                            {
                                "summary": "Infrastructure policy scanning",
                                "description": "IaC compliance validation",
                            },
                        ],
                    },
                    {
                        "summary": "Deployment Governance Gates",
                        "description": "Risk-based deployment approval",
                        "features": [
                            {
                                "summary": "Risk-based gate automation",
                                "description": "Auto-approve low-risk changes",
                            },
                            {
                                "summary": "Approval workflow engine",
                                "description": "Configurable approval chains",
                            },
                            {
                                "summary": "Environment promotion rules",
                                "description": "Stage-gate requirements",
                            },
                        ],
                    },
                    {
                        "summary": "Policy Drift Detection",
                        "description": "Continuous compliance monitoring",
                        "features": [
                            {
                                "summary": "Continuous compliance scanning",
                                "description": "24/7 policy violation detection",
                            },
                            {
                                "summary": "Auto-remediation workflows",
                                "description": "Automatic drift correction",
                            },
                            {
                                "summary": "Exception management portal",
                                "description": "Managed policy exceptions",
                            },
                        ],
                    },
                ],
            },
            {
                "summary": "Evidence Automation",
                "description": "Automated compliance evidence lifecycle",
                "business_outcomes": [
                    {
                        "summary": "Continuous Evidence Collection",
                        "description": "Always audit-ready",
                        "features": [
                            {
                                "summary": "Control-to-evidence mapping",
                                "description": "Link controls to evidence sources",
                            },
                            {
                                "summary": "API-based evidence capture",
                                "description": "Automated evidence pull from tools",
                            },
                            {
                                "summary": "Immutable evidence repository",
                                "description": "Tamper-proof evidence storage",
                            },
                        ],
                    },
                    {
                        "summary": "Audit-Ready Reporting",
                        "description": "On-demand compliance reports",
                        "features": [
                            {
                                "summary": "SOX control dashboards",
                                "description": "Real-time SOX compliance view",
                            },
                            {
                                "summary": "PCI-DSS report automation",
                                "description": "Auto-generated PCI reports",
                            },
                            {
                                "summary": "On-demand auditor access",
                                "description": "Self-service auditor portal",
                            },
                        ],
                    },
                    {
                        "summary": "Evidence Lifecycle Management",
                        "description": "Track evidence freshness",
                        "features": [
                            {
                                "summary": "TTL-based expiry tracking",
                                "description": "Evidence expiration alerts",
                            },
                            {
                                "summary": "Renewal notification workflows",
                                "description": "Proactive renewal reminders",
                            },
                            {
                                "summary": "Historical evidence archive",
                                "description": "Long-term evidence retention",
                            },
                        ],
                    },
                ],
            },
            {
                "summary": "Risk & Control Management",
                "description": "Enterprise risk visibility",
                "business_outcomes": [
                    {
                        "summary": "Control Framework Automation",
                        "description": "Dynamic control requirements",
                        "features": [
                            {
                                "summary": "Control requirement engine",
                                "description": "Risk-based control calculation",
                            },
                            {
                                "summary": "Risk profile questionnaire",
                                "description": "Self-service risk assessment",
                            },
                            {
                                "summary": "Guild-based control ownership",
                                "description": "Clear control accountability",
                            },
                        ],
                    },
                    {
                        "summary": "Risk Visibility & Escalation",
                        "description": "Enterprise risk transparency",
                        "features": [
                            {
                                "summary": "Risk materiality scoring",
                                "description": "Quantified risk assessment",
                            },
                            {
                                "summary": "Constraint tracking workflows",
                                "description": "Jira-based constraint management",
                            },
                            {
                                "summary": "Executive risk dashboards",
                                "description": "Board-level risk reporting",
                            },
                        ],
                    },
                ],
            },
        ],
    },
    # =========================================================================
    # 5. Accelerate Data-Driven Decisions
    # =========================================================================
    {
        "strategic_objective": {
            "summary": "Accelerate Data-Driven Decisions",
            "description": "Democratize data access with self-service analytics, real-time dashboards, and embedded ML insights across business functions",
            "project": "DATA",
        },
        "portfolio_epics": [
            {
                "summary": "Enterprise Data Platform",
                "description": "Unified data foundation",
                "business_outcomes": [
                    {
                        "summary": "Unified Data Lake",
                        "description": "Single source of truth for analytics",
                        "features": [
                            {
                                "summary": "Lakehouse architecture",
                                "description": "Delta Lake/Iceberg implementation",
                            },
                            {
                                "summary": "Real-time ingestion pipelines",
                                "description": "Streaming data integration",
                            },
                            {
                                "summary": "Data quality framework",
                                "description": "Automated data validation",
                            },
                        ],
                    },
                    {
                        "summary": "Data Catalog & Discovery",
                        "description": "Find and understand data assets",
                        "features": [
                            {
                                "summary": "Metadata harvesting automation",
                                "description": "Auto-catalog new datasets",
                            },
                            {
                                "summary": "Business glossary management",
                                "description": "Common business definitions",
                            },
                            {
                                "summary": "Data lineage visualization",
                                "description": "End-to-end data flow tracking",
                            },
                        ],
                    },
                    {
                        "summary": "Data Mesh Enablement",
                        "description": "Decentralized data ownership",
                        "features": [
                            {
                                "summary": "Domain ownership model",
                                "description": "Domain-oriented data teams",
                            },
                            {
                                "summary": "Data product templates",
                                "description": "Standardized data product creation",
                            },
                            {
                                "summary": "Federated governance",
                                "description": "Centralized standards, local execution",
                            },
                        ],
                    },
                ],
            },
            {
                "summary": "Self-Service Analytics",
                "description": "Empower business users with data",
                "business_outcomes": [
                    {
                        "summary": "Democratized Reporting",
                        "description": "Anyone can build reports",
                        "features": [
                            {
                                "summary": "Semantic layer",
                                "description": "Business-friendly metrics store",
                            },
                            {
                                "summary": "Self-service dashboard builder",
                                "description": "Drag-and-drop report creation",
                            },
                            {
                                "summary": "Natural language queries",
                                "description": "Ask questions in plain English",
                            },
                        ],
                    },
                    {
                        "summary": "Real-Time Insights",
                        "description": "Live operational intelligence",
                        "features": [
                            {
                                "summary": "Streaming analytics platform",
                                "description": "Real-time event processing",
                            },
                            {
                                "summary": "Live operational dashboards",
                                "description": "Sub-second dashboard refresh",
                            },
                            {
                                "summary": "Alert-driven insights",
                                "description": "Proactive anomaly notifications",
                            },
                        ],
                    },
                    {
                        "summary": "Embedded Analytics",
                        "description": "Analytics in applications",
                        "features": [
                            {
                                "summary": "Application-embedded charts",
                                "description": "In-app visualizations",
                            },
                            {
                                "summary": "API-first analytics",
                                "description": "Analytics as a service",
                            },
                            {
                                "summary": "White-label reporting",
                                "description": "Customer-facing analytics",
                            },
                        ],
                    },
                ],
            },
            {
                "summary": "ML Democratization",
                "description": "Make ML accessible to all",
                "business_outcomes": [
                    {
                        "summary": "Citizen Data Science",
                        "description": "Non-experts can build models",
                        "features": [
                            {
                                "summary": "AutoML platform",
                                "description": "Automated model training",
                            },
                            {
                                "summary": "No-code model builder",
                                "description": "Visual ML pipeline creation",
                            },
                            {
                                "summary": "Model marketplace",
                                "description": "Pre-built model catalog",
                            },
                        ],
                    },
                    {
                        "summary": "Production ML Platform",
                        "description": "Enterprise MLOps",
                        "features": [
                            {
                                "summary": "Feature store",
                                "description": "Centralized feature management",
                            },
                            {
                                "summary": "Model registry & versioning",
                                "description": "Model lifecycle management",
                            },
                            {
                                "summary": "A/B testing infrastructure",
                                "description": "Model experimentation platform",
                            },
                        ],
                    },
                ],
            },
        ],
    },
]


def get_all_strategic_objectives():
    """Get list of all strategic objectives."""
    return [h["strategic_objective"] for h in HIERARCHY]


def get_hierarchy_for_project(project_key: str):
    """Get hierarchy data for a specific project."""
    for h in HIERARCHY:
        if h["strategic_objective"]["project"] == project_key:
            return h
    return None


def count_items():
    """Count all items in hierarchy."""
    counts = {
        "strategic_objectives": 0,
        "portfolio_epics": 0,
        "business_outcomes": 0,
        "features": 0,
    }

    for h in HIERARCHY:
        counts["strategic_objectives"] += 1
        for pe in h["portfolio_epics"]:
            counts["portfolio_epics"] += 1
            for bo in pe["business_outcomes"]:
                counts["business_outcomes"] += 1
                counts["features"] += len(bo["features"])

    return counts
