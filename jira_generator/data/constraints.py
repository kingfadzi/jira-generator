"""
Sample Constraint Issues.

Constraints linked to Business Outcomes or Features for governance testing.
"""

# Sample constraints across different guilds and materiality levels
CONSTRAINTS = [
    # =========================================================================
    # Security Guild Constraints
    # =========================================================================
    {
        'summary': 'WAF rules must be configured before production deployment',
        'description': 'Web Application Firewall rules are required for all internet-facing services to protect against OWASP Top 10 vulnerabilities.',
        'guild': 'Security',
        'risk_materiality': 'Critical',
        'mitigation_plan': 'Configure WAF rules in CloudFlare/AWS WAF. Rules must cover SQL injection, XSS, and path traversal. Security team to validate configuration.',
        'status': 'Identified',
        'blocks': {
            'project': 'DEVEX',
            'type': 'Business Outcome',
            'summary': 'On-Demand Environment Provisioning',
        },
    },
    {
        'summary': 'Penetration testing must be completed for new APIs',
        'description': 'All externally exposed APIs require penetration testing before production release.',
        'guild': 'Security',
        'risk_materiality': 'High',
        'mitigation_plan': 'Engage security team for pen test. Estimated 2-week engagement. All critical/high findings must be remediated before go-live.',
        'status': 'In Progress',
        'blocks': {
            'project': 'DEVEX',
            'type': 'Feature',
            'summary': 'Environment request portal',
        },
    },
    {
        'summary': 'Secrets rotation policy must be implemented',
        'description': 'All secrets and API keys must have automated rotation with maximum 90-day lifetime.',
        'guild': 'Security',
        'risk_materiality': 'High',
        'mitigation_plan': 'Integrate with HashiCorp Vault for dynamic secrets. Configure rotation schedule for all credentials.',
        'status': 'Identified',
        'blocks': {
            'project': 'DEVEX',
            'type': 'Feature',
            'summary': 'Secrets injection automation',
        },
    },
    {
        'summary': 'Zero trust network policies required',
        'description': 'Service-to-service communication must use mTLS and explicit network policies.',
        'guild': 'Security',
        'risk_materiality': 'Critical',
        'mitigation_plan': 'Implement Istio service mesh with strict mTLS. Define NetworkPolicies for all Kubernetes namespaces.',
        'status': 'Identified',
        'blocks': {
            'project': 'TECHCON',
            'type': 'Feature',
            'summary': 'Service mesh adoption',
        },
    },

    # =========================================================================
    # Data Guild Constraints
    # =========================================================================
    {
        'summary': 'PII encryption must be enabled for all customer data',
        'description': 'All personally identifiable information must be encrypted at rest and in transit per GDPR requirements.',
        'guild': 'Data',
        'risk_materiality': 'Critical',
        'mitigation_plan': 'Enable TDE for databases. Implement field-level encryption for PII columns. Update data classification tags.',
        'status': 'In Progress',
        'blocks': {
            'project': 'DEVEX',
            'type': 'Feature',
            'summary': 'Data masking for non-prod',
        },
    },
    {
        'summary': 'Data retention policy must be documented and enforced',
        'description': 'All data stores must have documented retention policies with automated purge procedures.',
        'guild': 'Data',
        'risk_materiality': 'High',
        'mitigation_plan': 'Define retention periods per data classification. Implement lifecycle policies in S3/database. Create audit trail for deletions.',
        'status': 'Identified',
        'blocks': {
            'project': 'DATA',
            'type': 'Business Outcome',
            'summary': 'Unified Data Lake',
        },
    },
    {
        'summary': 'Data lineage must be captured for regulatory reporting',
        'description': 'End-to-end data lineage required for all data used in financial and regulatory reports.',
        'guild': 'Data',
        'risk_materiality': 'High',
        'mitigation_plan': 'Integrate OpenLineage with data pipelines. Configure automatic lineage capture in Spark/Airflow jobs.',
        'status': 'Identified',
        'blocks': {
            'project': 'DATA',
            'type': 'Feature',
            'summary': 'Data lineage visualization',
        },
    },
    {
        'summary': 'GDPR right-to-deletion workflow required',
        'description': 'Must support automated data subject deletion requests within 30-day SLA.',
        'guild': 'Data',
        'risk_materiality': 'Critical',
        'mitigation_plan': 'Build deletion workflow in ServiceNow. Create data discovery scripts for all data stores. Test deletion completeness.',
        'status': 'Ready for Review',
        'blocks': {
            'project': 'GOV',
            'type': 'Feature',
            'summary': 'Exception management portal',
        },
    },

    # =========================================================================
    # Operations Guild Constraints
    # =========================================================================
    {
        'summary': 'Runbook documentation required for incident response',
        'description': 'All production services must have runbooks covering common failure scenarios and recovery procedures.',
        'guild': 'Operations',
        'risk_materiality': 'Medium',
        'mitigation_plan': 'Create runbook templates. Document top 10 incident scenarios per service. Link runbooks to PagerDuty alerts.',
        'status': 'In Progress',
        'blocks': {
            'project': 'AIOPS',
            'type': 'Feature',
            'summary': 'Runbook automation library',
        },
    },
    {
        'summary': 'DR failover must be tested quarterly',
        'description': 'Disaster recovery procedures must be validated through quarterly failover tests.',
        'guild': 'Operations',
        'risk_materiality': 'High',
        'mitigation_plan': 'Schedule Q1 DR test. Define success criteria (RTO < 4hr, RPO < 1hr). Document lessons learned.',
        'status': 'Identified',
        'blocks': {
            'project': 'AIOPS',
            'type': 'Business Outcome',
            'summary': 'Auto-Remediation',
        },
    },
    {
        'summary': 'SLOs must be defined and monitored',
        'description': 'All Tier 1 services must have defined SLOs with automated alerting on budget burn.',
        'guild': 'Operations',
        'risk_materiality': 'Medium',
        'mitigation_plan': 'Define availability and latency SLOs. Configure SLO dashboards in Grafana. Set up burn-rate alerts.',
        'status': 'In Progress',
        'blocks': {
            'project': 'TECHCON',
            'type': 'Feature',
            'summary': 'Single pane of glass dashboard',
        },
    },
    {
        'summary': 'Capacity planning review required before launch',
        'description': 'Load testing and capacity analysis must be completed for expected peak traffic.',
        'guild': 'Operations',
        'risk_materiality': 'High',
        'mitigation_plan': 'Run load tests at 2x expected peak. Document resource requirements. Configure auto-scaling policies.',
        'status': 'Identified',
        'blocks': {
            'project': 'AIOPS',
            'type': 'Feature',
            'summary': 'Demand forecasting models',
        },
    },

    # =========================================================================
    # Enterprise Architecture Guild Constraints
    # =========================================================================
    {
        'summary': 'Architecture review required for new service',
        'description': 'All new services must pass EA review board for alignment with strategic patterns.',
        'guild': 'Enterprise Architecture',
        'risk_materiality': 'Medium',
        'mitigation_plan': 'Submit ADR to EA review board. Address feedback on technology choices. Update architecture diagrams.',
        'status': 'In Progress',
        'blocks': {
            'project': 'DEVEX',
            'type': 'Business Outcome',
            'summary': 'Pipeline Standardization',
        },
    },
    {
        'summary': 'API versioning strategy must follow standards',
        'description': 'All APIs must implement semantic versioning with backward compatibility guarantees.',
        'guild': 'Enterprise Architecture',
        'risk_materiality': 'Medium',
        'mitigation_plan': 'Implement URL-based versioning (v1, v2). Document deprecation policy. Add version headers to responses.',
        'status': 'Ready for Review',
        'blocks': {
            'project': 'TECHCON',
            'type': 'Feature',
            'summary': 'Strategic DB engine selection',
        },
    },
    {
        'summary': 'Technology stack must be on approved list',
        'description': 'All technology choices must be from the approved technology radar.',
        'guild': 'Enterprise Architecture',
        'risk_materiality': 'Low',
        'mitigation_plan': 'Review tech choices against radar. Submit exception request for any non-standard technologies.',
        'status': 'Identified',
        'blocks': {
            'project': 'DATA',
            'type': 'Feature',
            'summary': 'Lakehouse architecture',
        },
    },
    {
        'summary': 'Integration patterns must use event-driven architecture',
        'description': 'New integrations should prefer async event-driven patterns over synchronous API calls.',
        'guild': 'Enterprise Architecture',
        'risk_materiality': 'Medium',
        'mitigation_plan': 'Design event schema. Set up Kafka topics. Implement consumer groups with proper error handling.',
        'status': 'Identified',
        'blocks': {
            'project': 'DATA',
            'type': 'Feature',
            'summary': 'Real-time ingestion pipelines',
        },
    },

    # =========================================================================
    # Cross-Guild Constraints (Multiple concerns)
    # =========================================================================
    {
        'summary': 'Production deployment requires change approval',
        'description': 'All production deployments must have approved change request with rollback plan.',
        'guild': 'Operations',
        'risk_materiality': 'High',
        'mitigation_plan': 'Create CR in ServiceNow. Document deployment steps and rollback procedure. Get CAB approval.',
        'status': 'Identified',
        'blocks': {
            'project': 'GOV',
            'type': 'Business Outcome',
            'summary': 'Deployment Governance Gates',
        },
    },
    {
        'summary': 'Compliance evidence must be collected before release',
        'description': 'SOX-relevant applications must have compliance evidence uploaded before production deployment.',
        'guild': 'Security',
        'risk_materiality': 'Critical',
        'mitigation_plan': 'Complete control attestations. Upload evidence to GRC portal. Get compliance officer sign-off.',
        'status': 'In Progress',
        'blocks': {
            'project': 'GOV',
            'type': 'Business Outcome',
            'summary': 'Continuous Evidence Collection',
        },
    },
]


def get_constraints_by_guild(guild: str):
    """Get constraints for a specific guild."""
    return [c for c in CONSTRAINTS if c['guild'] == guild]


def get_constraints_by_status(status: str):
    """Get constraints by status."""
    return [c for c in CONSTRAINTS if c['status'] == status]


def get_constraints_by_materiality(materiality: str):
    """Get constraints by risk materiality."""
    return [c for c in CONSTRAINTS if c['risk_materiality'] == materiality]


def get_constraints_for_project(project_key: str):
    """Get constraints that block items in a specific project."""
    return [c for c in CONSTRAINTS if c['blocks']['project'] == project_key]


def count_constraints():
    """Count constraints by various dimensions."""
    return {
        'total': len(CONSTRAINTS),
        'by_guild': {
            'Security': len(get_constraints_by_guild('Security')),
            'Data': len(get_constraints_by_guild('Data')),
            'Operations': len(get_constraints_by_guild('Operations')),
            'Enterprise Architecture': len(get_constraints_by_guild('Enterprise Architecture')),
        },
        'by_status': {
            'Identified': len(get_constraints_by_status('Identified')),
            'In Progress': len(get_constraints_by_status('In Progress')),
            'Ready for Review': len(get_constraints_by_status('Ready for Review')),
            'Closed': len(get_constraints_by_status('Closed')),
        },
        'by_materiality': {
            'Critical': len(get_constraints_by_materiality('Critical')),
            'High': len(get_constraints_by_materiality('High')),
            'Medium': len(get_constraints_by_materiality('Medium')),
            'Low': len(get_constraints_by_materiality('Low')),
        },
    }
