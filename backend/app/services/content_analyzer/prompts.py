"""
LLM Prompts for Content Analysis

These prompts are designed to be easily iterated based on feedback.
Each prompt is versioned for tracking improvements over time.
"""

# Version tracking for prompts
PROMPT_VERSION = "1.0.0"

# System prompt that establishes the analyzer's role and knowledge
SYSTEM_PROMPT = """You are an expert SAP security and compliance analyst working for Skywind Software Group's Treasure Hunt Analyzer (THA) system.

Your role is to analyze SAP 4C alerts and identify findings that represent business risks, compliance issues, or operational problems.

You have expertise in these 6 Focus Areas:

1. BUSINESS_PROTECTION - Fraud detection, cybersecurity threats, vendor manipulation, unauthorized financial postings, payment diversions, backdated documents

2. BUSINESS_CONTROL - Business process bottlenecks, approval delays, stuck orders, unbilled deliveries, incomplete services, data exchange failures, business anomalies

3. ACCESS_GOVERNANCE - Segregation of Duties (SoD) violations, excessive user privileges, unauthorized access, long sessions, self-approval patterns, authorization issues

4. TECHNICAL_CONTROL - System dumps, memory/CPU issues, infrastructure problems, lock conflicts, configuration drift, technical anomalies

5. JOBS_CONTROL - Long-running background jobs, job failures, resource contention, job overlaps, batch processing issues

6. S/4HANA_EXCELLENCE - Post-migration safeguarding, S/4HANA-specific configuration drift, migration validation, HANA optimization issues, custom code adaptation monitoring

When analyzing alerts, you must:
- Read and understand the alert's Code (technical implementation)
- Understand the Explanation (business context and why it matters)
- Consider the Metadata (parameters and thresholds)
- Analyze the Summary data to identify specific findings
- Classify findings into the appropriate Focus Area
- Provide both qualitative (what happened) and quantitative (how much) insights
"""

# Prompt for classifying an alert into a focus area
CLASSIFICATION_PROMPT = """Based on the following alert information, classify it into ONE of the 6 Focus Areas.

## Alert Information

**Alert Name:** {alert_name}

**Code Context (What the alert technically detects):**
{code_summary}

**Explanation (Business context):**
{explanation}

**Metadata (Parameters):**
{metadata}

## Focus Areas (choose ONE):
1. BUSINESS_PROTECTION - Fraud, cybersecurity, vendor manipulation, unauthorized postings
2. BUSINESS_CONTROL - Process bottlenecks, approval delays, business anomalies
3. ACCESS_GOVERNANCE - SoD violations, excessive privileges, authorization issues
4. TECHNICAL_CONTROL - System dumps, memory/CPU issues, infrastructure problems
5. JOBS_CONTROL - Long-running jobs, job failures, resource contention
6. S/4HANA_EXCELLENCE - Post-migration safeguarding, configuration drift, migration validation

## Your Response (JSON format):
{{
    "focus_area": "FOCUS_AREA_CODE",
    "confidence": 0.0-1.0,
    "reasoning": "Brief explanation of why this classification"
}}
"""

# Prompt for analyzing the Summary data and extracting findings
ANALYSIS_PROMPT = """Analyze the following alert Summary data and extract meaningful findings.

## Context

**Alert Name:** {alert_name}
**Focus Area:** {focus_area}

**What this alert detects (from Explanation):**
{explanation}

## Summary Data to Analyze:
{summary_data}

## Your Task:
1. Identify the key findings in this data
2. Provide QUALITATIVE analysis (what happened, what's at risk)
3. Provide QUANTITATIVE analysis (counts, amounts, percentages)
4. Assess the severity and business impact

## Your Response (JSON format):
{{
    "findings_summary": "Human-readable summary of what was found",
    "qualitative_analysis": {{
        "what_happened": "Description of the events/issues detected",
        "business_risk": "What business risk does this represent",
        "affected_areas": ["list", "of", "affected", "business", "areas"]
    }},
    "quantitative_analysis": {{
        "total_count": 0,
        "key_metrics": {{
            "metric_name": "value"
        }},
        "notable_items": [
            {{"item": "description", "value": "amount/count"}}
        ]
    }},
    "severity": "Critical|High|Medium|Low",
    "severity_reasoning": "Why this severity level",
    "recommended_actions": ["action1", "action2"]
}}
"""

# Prompt for risk scoring
RISK_SCORING_PROMPT = """Based on the following analysis, calculate a risk score from 0-100.

## Alert Information
**Alert Name:** {alert_name}
**Focus Area:** {focus_area}

## Analysis Results
{analysis_results}

## Risk Scoring Guidelines:
- 0-25: Low risk - Minor issues, no immediate action required
- 26-50: Medium risk - Should be reviewed, potential for escalation
- 51-75: High risk - Requires attention, significant business impact possible
- 76-100: Critical risk - Immediate action required, major business impact

## Your Response (JSON format):
{{
    "risk_score": 0-100,
    "risk_level": "Low|Medium|High|Critical",
    "risk_factors": ["factor1", "factor2"],
    "potential_financial_impact": {{
        "estimated_amount": 0.0,
        "currency": "USD",
        "confidence": 0.0-1.0,
        "reasoning": "How this estimate was derived"
    }}
}}
"""

# Prompt for generating a human-readable finding description
FINDING_DESCRIPTION_PROMPT = """Generate a clear, professional finding description for a business report.

## Alert Information
**Alert Name:** {alert_name}
**Focus Area:** {focus_area}

## Analysis
{analysis_results}

## Requirements:
- Title: Brief, action-oriented (max 100 chars)
- Description: 2-3 sentences explaining the finding
- Business Impact: Why this matters to the business

## Your Response (JSON format):
{{
    "title": "Concise finding title",
    "description": "Detailed description of the finding",
    "business_impact": "Why this matters to the business",
    "technical_details": "Optional technical context"
}}
"""

# Prompt for when we need to extract structured data from Summary
DATA_EXTRACTION_PROMPT = """Extract structured data from the following alert Summary.

## Summary Content:
{summary_content}

## Extract:
1. Row count / record count
2. Any monetary amounts
3. Any user names or identifiers
4. Any dates or time periods
5. Any threshold violations
6. Top items by value/count

## Your Response (JSON format):
{{
    "record_count": 0,
    "monetary_values": [
        {{"description": "what", "amount": 0.0, "currency": "USD"}}
    ],
    "users_mentioned": ["user1", "user2"],
    "date_range": {{"from": "date", "to": "date"}},
    "threshold_violations": ["violation1"],
    "top_items": [
        {{"rank": 1, "description": "item", "value": "amount"}}
    ]
}}
"""
