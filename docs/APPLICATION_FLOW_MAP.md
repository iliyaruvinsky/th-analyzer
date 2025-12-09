# THA Application Flow Map

> **Version:** 1.0 | **Created:** 2025-12-09
>
> This document provides a complete visual map of all application workflows and their associated artifacts.

---

## Quick Reference - File Locations

```
FRONTEND (React)         → frontend/src/
BACKEND API              → backend/app/api/
SERVICES                 → backend/app/services/
MODELS                   → backend/app/models/
SCHEMAS                  → backend/app/schemas/
DOCUMENTATION            → docs/
RULES                    → .claude/rules/
CONTEXT                  → docs/th-context/
```

---

## Master Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           THA - TREASURE HUNT ANALYZER                                   │
│                              Complete Application Flow                                   │
└─────────────────────────────────────────────────────────────────────────────────────────┘

                                    ┌─────────────┐
                                    │   USER      │
                                    └──────┬──────┘
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    │                      │                      │
                    ▼                      ▼                      ▼
         ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
         │  FLOW A: UPLOAD  │   │  FLOW B: CONTENT │   │  FLOW C: ALERT   │
         │  & BASIC ANALYSIS│   │  ANALYSIS (4C)   │   │  DASHBOARD       │
         └────────┬─────────┘   └────────┬─────────┘   └────────┬─────────┘
                  │                      │                      │
                  ▼                      ▼                      ▼
         ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
         │ Upload.tsx       │   │ AlertAnalysis.tsx│   │ Dashboard.tsx    │
         │ ingestion.py     │   │ content_analysis │   │ alert_dashboard  │
         │ parsers/*        │   │ ContentAnalyzer  │   │ .py              │
         └────────┬─────────┘   └────────┬─────────┘   └────────┬─────────┘
                  │                      │                      │
                  └──────────────────────┼──────────────────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │    DATABASE          │
                              │    (PostgreSQL)      │
                              │    20+ Tables        │
                              └──────────────────────┘
```

---

## FLOW A: File Upload & Basic Analysis

### Stage A1: File Upload

```
┌─────────────────────────────────────────────────────────────────────────┐
│ STAGE A1: FILE UPLOAD                                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────────────────┐  │
│  │   USER      │      │   FRONTEND  │      │        BACKEND          │  │
│  │   Uploads   │ ──▶  │   Upload    │ ──▶  │   POST /ingestion/      │  │
│  │   File      │      │   Page      │      │   upload                │  │
│  └─────────────┘      └─────────────┘      └─────────────────────────┘  │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│ ARTIFACTS:                                                               │
│                                                                          │
│ Frontend:                                                                │
│   • frontend/src/pages/Upload.tsx              [UI Component]            │
│   • frontend/src/services/api.ts               [API Client]              │
│     → uploadFile(), uploadMultipleFiles()                                │
│                                                                          │
│ Backend API:                                                             │
│   • backend/app/api/ingestion.py               [Route Handler]           │
│     → POST /upload                                                       │
│     → POST /upload-multiple                                              │
│     → GET /data-sources                                                  │
│                                                                          │
│ File Storage:                                                            │
│   • ./storage/uploads/                         [Local Files]             │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Stage A2: File Parsing

```
┌─────────────────────────────────────────────────────────────────────────┐
│ STAGE A2: FILE PARSING                                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────────────────┐  │
│  │  Uploaded   │      │   Parser    │      │      Extracted          │  │
│  │  File       │ ──▶  │   Factory   │ ──▶  │      Data               │  │
│  │  (PDF/XLSX) │      │             │      │                         │  │
│  └─────────────┘      └─────────────┘      └─────────────────────────┘  │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│ ARTIFACTS:                                                               │
│                                                                          │
│ Parser Factory:                                                          │
│   • backend/app/services/ingestion/parser_factory.py   [Router]          │
│     → Selects appropriate parser based on file type                      │
│                                                                          │
│ Parsers:                                                                 │
│   • backend/app/services/ingestion/csv_parser.py       [CSV]             │
│   • backend/app/services/ingestion/excel_parser_4c.py  [4C Alerts]       │
│   • backend/app/services/ingestion/excel_parser_soda.py [SoDA Reports]   │
│   • backend/app/services/ingestion/pdf_parser.py       [PDF]             │
│   • backend/app/services/ingestion/docx_parser.py      [DOCX]            │
│   • backend/app/services/ingestion/base_parser.py      [Base Class]      │
│                                                                          │
│ Data Saver:                                                              │
│   • backend/app/services/ingestion/data_saver.py       [DB Insert]       │
│                                                                          │
│ Models (Database):                                                       │
│   • backend/app/models/data_source.py                  [DataSource]      │
│   • backend/app/models/alert.py                        [Alert]           │
│   • backend/app/models/soda_report.py                  [SoDAReport]      │
│   • backend/app/models/finding.py                      [Finding]         │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Stage A3: Basic Analysis

```
┌─────────────────────────────────────────────────────────────────────────┐
│ STAGE A3: BASIC ANALYSIS (Classification + Risk Scoring)                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────────────────┐  │
│  │  Parsed     │      │  Analyzer   │      │   Classified            │  │
│  │  Findings   │ ──▶  │  Service    │ ──▶  │   Findings + Scores     │  │
│  └─────────────┘      └─────────────┘      └─────────────────────────┘  │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│ ARTIFACTS:                                                               │
│                                                                          │
│ Analysis API:                                                            │
│   • backend/app/api/analysis.py                [Route Handler]           │
│     → POST /run                                                          │
│     → GET /runs                                                          │
│     → GET /findings                                                      │
│                                                                          │
│ Analysis Services:                                                       │
│   • backend/app/services/analysis/analyzer.py  [Orchestrator]            │
│   • backend/app/services/analysis/classifier.py [Focus Area Classifier]  │
│     → FocusAreaClassifier                                                │
│     → IssueTypeClassifier                                                │
│   • backend/app/services/analysis/risk_scorer.py [Risk Scoring]          │
│     → SEVERITY_SCORES: {Critical:90, High:75, Medium:60, Low:50}         │
│                                                                          │
│ Hybrid Money Loss:                                                       │
│   • backend/app/services/hybrid_engine.py      [60% LLM + 40% ML]        │
│   • backend/app/services/llm_engine/money_loss_llm.py [LLM Estimates]    │
│   • backend/app/services/ml_engine/money_loss_ml.py   [ML Predictions]   │
│                                                                          │
│ Models:                                                                  │
│   • backend/app/models/focus_area.py           [6 Focus Areas]           │
│   • backend/app/models/issue_type.py           [Issue Types]             │
│   • backend/app/models/risk_assessment.py      [Risk Scores]             │
│   • backend/app/models/money_loss.py           [Financial Impact]        │
│   • backend/app/models/analysis_run.py         [Run Tracking]            │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## FLOW B: Content Analysis (4C Alerts)

### Stage B1: Alert Artifact Loading

```
┌─────────────────────────────────────────────────────────────────────────┐
│ STAGE B1: ALERT ARTIFACT LOADING                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Alert Directory Structure (4 Files):                                    │
│                                                                          │
│  docs/skywind-4c-alerts-output/{MODULE}/{ALERT_ID}/                      │
│      │                                                                   │
│      ├── Code_*.txt           → ABAP source code                         │
│      ├── Explanation_*.txt    → Business purpose (from Skywind)          │
│      ├── Metadata_*.xlsx      → Parameters, dates, settings              │
│      └── Summary_*.xlsx       → ACTUAL DATA (counts, amounts)            │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│ ARTIFACTS:                                                               │
│                                                                          │
│ Frontend:                                                                │
│   • frontend/src/pages/AlertAnalysis.tsx       [Analysis UI]             │
│   • frontend/src/pages/AlertAnalysis.css       [Styles]                  │
│                                                                          │
│ Backend API:                                                             │
│   • backend/app/api/content_analysis.py        [Route Handler]           │
│     → POST /analyze                                                      │
│     → POST /analyze-and-save                                             │
│     → GET /report/{alert_id}                                             │
│                                                                          │
│ Artifact Reader:                                                         │
│   • backend/app/services/content_analyzer/artifact_reader.py             │
│     → ArtifactReader class                                               │
│     → AlertArtifacts dataclass                                           │
│     → read_from_directory()                                              │
│                                                                          │
│ Sample Alert Directories:                                                │
│   • docs/skywind-4c-alerts-output/FI/200025_001372 - Rarely Used Vendors │
│   • docs/skywind-4c-alerts-output/SD/200025_001455 - Monthly returns...  │
│   • docs/skywind-4c-alerts-output/MM/200025_001397 - Inventory Count...  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Stage B2: Context Loading

```
┌─────────────────────────────────────────────────────────────────────────┐
│ STAGE B2: CONTEXT LOADING (TH Principles)                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────────────────┐  │
│  │  Context    │      │   Context   │      │   Loaded                │  │
│  │  Documents  │ ──▶  │   Loader    │ ──▶  │   Knowledge Base        │  │
│  └─────────────┘      └─────────────┘      └─────────────────────────┘  │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│ ARTIFACTS:                                                               │
│                                                                          │
│ Context Loader:                                                          │
│   • backend/app/services/content_analyzer/context_loader.py              │
│     → ContextLoader class                                                │
│     → load_all_context()                                                 │
│                                                                          │
│ Context Documents (Knowledge Base):                                      │
│   • docs/th-context/skywind-4c-knowledge.md    [4C Alert Knowledge]      │
│   • docs/th-context/soda-knowledge.md          [SoDA Report Knowledge]   │
│   • docs/th-context/treasure-hunt-principles.md [TH Methodology]         │
│   • docs/th-context/focus-areas.md             [6 Focus Areas]           │
│                                                                          │
│ Analysis Rules:                                                          │
│   • docs/th-context/analysis-rules/QUANTITATIVE_ALERT_WORKFLOW.md        │
│   • docs/th-context/analysis-rules/templates/quantitative-alert.yaml     │
│   • docs/th-context/analysis-rules/presentation-rules.yaml               │
│   • docs/th-context/analysis-rules/field-mappings/sd-fields.yaml         │
│                                                                          │
│ Scoring Rules:                                                           │
│   • docs/scoring-rules/BUSINESS_PROTECTION.md  [Severity: 90/75/60/50]   │
│                                                                          │
│ Claude Rules (Enforcement):                                              │
│   • .claude/rules/anti-hallucination-rules.md  [14 Critical Rules]       │
│   • .claude/rules/quantitative-alert-analysis.md [Analysis Rules]        │
│   • .claude/rules/llm-handover-maintenance.md  [Handover Rules]          │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Stage B3: LLM Classification

```
┌─────────────────────────────────────────────────────────────────────────┐
│ STAGE B3: LLM CLASSIFICATION                                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────────────────┐  │
│  │  Alert      │      │   LLM       │      │   Focus Area            │  │
│  │  Artifacts  │ ──▶  │   Classifier│ ──▶  │   + Confidence          │  │
│  └─────────────┘      └─────────────┘      └─────────────────────────┘  │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│ ARTIFACTS:                                                               │
│                                                                          │
│ LLM Classifier:                                                          │
│   • backend/app/services/content_analyzer/llm_classifier.py              │
│     → LLMClassifier class                                                │
│     → classify_focus_area()                                              │
│     → analyze_summary()                                                  │
│     → calculate_risk_score()                                             │
│     → analyze_without_llm() [Pattern-based fallback]                     │
│                                                                          │
│ Prompts:                                                                 │
│   • backend/app/services/content_analyzer/prompts.py                     │
│     → FOCUS_AREA_CLASSIFICATION_PROMPT                                   │
│     → SUMMARY_ANALYSIS_PROMPT                                            │
│     → RISK_SCORING_PROMPT                                                │
│                                                                          │
│ LLM Clients:                                                             │
│   • backend/app/services/llm_engine/llm_client.py                        │
│     → OpenAIClient                                                       │
│     → AnthropicClient                                                    │
│     → get_llm_client() factory                                           │
│                                                                          │
│ 6 Focus Areas (Classification Targets):                                  │
│   1. BUSINESS_PROTECTION  → Fraud detection, cybersecurity               │
│   2. BUSINESS_CONTROL     → Bottlenecks, anomalies                       │
│   3. ACCESS_GOVERNANCE    → SoD, authorization                           │
│   4. TECHNICAL_CONTROL    → Infrastructure issues                        │
│   5. JOBS_CONTROL         → Job performance                              │
│   6. S4HANA_EXCELLENCE    → Migration safeguarding                       │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Stage B4: Scoring Engine

```
┌─────────────────────────────────────────────────────────────────────────┐
│ STAGE B4: SCORING ENGINE                                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────────────────┐  │
│  │ Classified  │      │  Scoring    │      │   Risk Score (0-100)    │  │
│  │ Finding     │ ──▶  │  Engine     │ ──▶  │   + Severity Level      │  │
│  └─────────────┘      └─────────────┘      └─────────────────────────┘  │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│ ARTIFACTS:                                                               │
│                                                                          │
│ Scoring Engine:                                                          │
│   • backend/app/services/content_analyzer/scoring_engine.py              │
│     → ScoringEngine class                                                │
│     → calculate_score()                                                  │
│     → SEVERITY_BASE_SCORES: {CRITICAL:90, HIGH:75, MEDIUM:60, LOW:50}    │
│                                                                          │
│ Scoring Components:                                                      │
│   • Qualitative Score (QualitativeScore dataclass)                       │
│     → severity                                                           │
│     → severity_reasoning                                                 │
│     → risk_factors                                                       │
│                                                                          │
│   • Quantitative Score (QuantitativeScore dataclass)                     │
│     → total_count                                                        │
│     → monetary_amount                                                    │
│     → currency                                                           │
│     → key_metrics                                                        │
│     → notable_items                                                      │
│                                                                          │
│   • Combined Score (CombinedScore dataclass)                             │
│     → risk_score (0-100)                                                 │
│     → risk_level (CRITICAL/HIGH/MEDIUM/LOW)                              │
│     → money_loss_estimate                                                │
│     → money_loss_confidence                                              │
│     → scoring_breakdown                                                  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Stage B5: Report Generation

```
┌─────────────────────────────────────────────────────────────────────────┐
│ STAGE B5: REPORT GENERATION                                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────────────────┐  │
│  │  Analysis   │      │   Report    │      │   Markdown Report       │  │
│  │  Results    │ ──▶  │   Generator │ ──▶  │   (Full/Summary)        │  │
│  └─────────────┘      └─────────────┘      └─────────────────────────┘  │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│ ARTIFACTS:                                                               │
│                                                                          │
│ Report Generator:                                                        │
│   • backend/app/services/content_analyzer/report_generator.py            │
│     → ReportGenerator class                                              │
│     → generate_full_report()                                             │
│     → generate_summary_report()                                          │
│                                                                          │
│ Report Templates:                                                        │
│   • docs/th-context/analysis-rules/templates/quantitative-alert.yaml     │
│     → Required Sections:                                                 │
│       1. Key Findings (metrics table, critical discovery, concentration) │
│       2. Business Context                                                │
│       3. Executive Summary                                               │
│       4. Key Metrics                                                     │
│       5. Concentration Analysis                                          │
│       6. Risk Assessment                                                 │
│       7. Recommended Actions                                             │
│       8. Technical Details                                               │
│                                                                          │
│ Output Location:                                                         │
│   • docs/analysis/{ALERT_ID}_Analysis.md                                 │
│                                                                          │
│ Example Reports:                                                         │
│   • docs/analysis/SD_Billing_Document_Status_Analysis.md                 │
│   • docs/analysis/SD_Negative_Profit_Deal_Analysis.md                    │
│   • docs/analysis/FI_Comparison_Monthly_Sales_Volume_Customer_Analysis.md│
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## FLOW C: Alert Dashboard

### Stage C1: Dashboard KPIs

```
┌─────────────────────────────────────────────────────────────────────────┐
│ STAGE C1: DASHBOARD KPIs                                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────────────────┐  │
│  │  Dashboard  │      │   Backend   │      │   KPI Data              │  │
│  │  Load       │ ──▶  │   API       │ ──▶  │   Response              │  │
│  └─────────────┘      └─────────────┘      └─────────────────────────┘  │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│ ARTIFACTS:                                                               │
│                                                                          │
│ Frontend:                                                                │
│   • frontend/src/pages/Dashboard.tsx           [Main Dashboard]          │
│   • frontend/src/styles/dashboard.css          [Dashboard Styles]        │
│   • frontend/src/pages/AlertDashboard.css      [Alert Dashboard Styles]  │
│   • frontend/src/components/KpiCard.tsx        [KPI Component]           │
│   • frontend/src/components/KpiCard.css        [KPI Styles]              │
│   • frontend/src/components/DashboardTabs.tsx  [Tab Navigation]          │
│                                                                          │
│ API Client:                                                              │
│   • frontend/src/services/api.ts                                         │
│     → getDashboardKPIs()                                                 │
│     → getCriticalDiscoveries()                                           │
│     → getActionQueue()                                                   │
│     → getAlertAnalyses()                                                 │
│                                                                          │
│ Backend API:                                                             │
│   • backend/app/api/alert_dashboard.py         [Route Handler]           │
│     → GET /kpis                                                          │
│     → GET /critical-discoveries                                          │
│     → GET /action-queue                                                  │
│     → GET /analyses                                                      │
│                                                                          │
│ Schemas:                                                                 │
│   • backend/app/schemas/alert_dashboard.py                               │
│     → DashboardKPIsResponse                                              │
│     → CriticalDiscoveryDrilldown                                         │
│     → TrendAnalysisResponse                                              │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Stage C2: Critical Discoveries

```
┌─────────────────────────────────────────────────────────────────────────┐
│ STAGE C2: CRITICAL DISCOVERIES                                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Dashboard displays Critical Discoveries from analyzed alerts:           │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ ALERT          │ MODULE │ SEV    │ DISC │ FINANCIAL IMPACT     │    │
│  ├─────────────────────────────────────────────────────────────────┤    │
│  │ Rarely Used... │ FI     │ HIGH   │ 1    │ $45,000,000          │    │
│  │ Modified Vend..│ FI     │ CRIT   │ 2    │ $12,500,000          │    │
│  │ Monthly Retur..│ SD     │ MEDIUM │ 1    │ $7,900,000           │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│ ARTIFACTS:                                                               │
│                                                                          │
│ Frontend Components:                                                     │
│   • frontend/src/components/DiscoveryDetailPanel.tsx [Detail View]       │
│   • frontend/src/components/ActionItemModal.tsx      [Action Items]      │
│                                                                          │
│ Backend Models (Alert Dashboard):                                        │
│   • backend/app/models/client.py               [Client Entity]           │
│   • backend/app/models/source_system.py        [SAP Systems]             │
│   • backend/app/models/exception_indicator.py  [EI Definitions]          │
│   • backend/app/models/alert_instance.py       [Alert Configs]           │
│   • backend/app/models/alert_analysis.py       [Analysis Results]        │
│   • backend/app/models/critical_discovery.py   [Critical Findings]       │
│   • backend/app/models/key_finding.py          [Key Findings]            │
│   • backend/app/models/concentration_metric.py [Concentration Data]      │
│   • backend/app/models/action_item.py          [Action Queue]            │
│                                                                          │
│ Database Migration:                                                      │
│   • backend/alembic/versions/001_add_alert_analysis_dashboard_tables.py  │
│     → Creates 10 tables for Alert Dashboard                              │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Stage C3: Action Queue

```
┌─────────────────────────────────────────────────────────────────────────┐
│ STAGE C3: ACTION QUEUE                                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Action Items with Status Tracking:                                      │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ STATUS  │ PRIORITY │ TITLE                    │ DUE DATE        │    │
│  ├─────────────────────────────────────────────────────────────────┤    │
│  │ PENDING │ 1        │ Investigate vendor...    │ 2025-12-15      │    │
│  │ IN_PROG │ 2        │ Review credit memos      │ 2025-12-12      │    │
│  │ DONE    │ 3        │ Audit concentration      │ 2025-12-10      │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│ ARTIFACTS:                                                               │
│                                                                          │
│ Backend API:                                                             │
│   • backend/app/api/alert_dashboard.py                                   │
│     → GET /action-queue                                                  │
│     → POST /action-items                                                 │
│     → PATCH /action-items/{item_id}                                      │
│                                                                          │
│ Schemas:                                                                 │
│   • backend/app/schemas/alert_dashboard.py                               │
│     → ActionItemCreate                                                   │
│     → ActionItemUpdate                                                   │
│     → ActionItemResponse                                                 │
│                                                                          │
│ Model:                                                                   │
│   • backend/app/models/action_item.py                                    │
│     → status: PENDING | IN_PROGRESS | RESOLVED | DISMISSED               │
│     → priority: 1-5                                                      │
│     → action_type: IMMEDIATE | SHORT_TERM | LONG_TERM                    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Data Model Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        DATABASE ENTITY RELATIONSHIPS                     │
└─────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────┐
    │                     ORIGINAL THA MODELS                           │
    │                                                                    │
    │  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐   │
    │  │DataSource│───▶│ Finding  │───▶│FocusArea │    │IssueType │   │
    │  └──────────┘    └────┬─────┘    └──────────┘    └──────────┘   │
    │                       │                                          │
    │                       ▼                                          │
    │  ┌──────────┐    ┌──────────┐    ┌──────────┐                   │
    │  │  Alert   │    │RiskAssess│    │MoneyLoss │                   │
    │  └──────────┘    └──────────┘    └──────────┘                   │
    │                                                                  │
    │  ┌──────────┐    ┌──────────┐    ┌──────────┐                   │
    │  │SoDAReport│    │AnalysRun │    │ AuditLog │                   │
    │  └──────────┘    └──────────┘    └──────────┘                   │
    └──────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────┐
    │                   ALERT DASHBOARD MODELS                          │
    │                                                                    │
    │  ┌──────────┐    ┌──────────┐    ┌──────────┐                   │
    │  │  Client  │───▶│SourceSys│    │ExceptInd │                   │
    │  └──────────┘    └────┬─────┘    └────┬─────┘                   │
    │                       │               │                          │
    │                       ▼               ▼                          │
    │                  ┌──────────────────────┐                        │
    │                  │    AlertInstance     │                        │
    │                  └──────────┬───────────┘                        │
    │                             │                                    │
    │                             ▼                                    │
    │                  ┌──────────────────────┐                        │
    │                  │    AlertAnalysis     │                        │
    │                  └──────────┬───────────┘                        │
    │                             │                                    │
    │        ┌────────────────────┼────────────────────┐               │
    │        ▼                    ▼                    ▼               │
    │  ┌──────────┐    ┌──────────────┐    ┌──────────────┐           │
    │  │CritDisc  │    │ KeyFinding   │    │ConcMetric    │           │
    │  └──────────┘    └──────────────┘    └──────────────┘           │
    │        │                                                         │
    │        ▼                                                         │
    │  ┌──────────┐                                                    │
    │  │ActionItem│                                                    │
    │  └──────────┘                                                    │
    └──────────────────────────────────────────────────────────────────┘
```

---

## Configuration Files

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          CONFIGURATION FILES                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ Docker:                                                                  │
│   • docker-compose.yml              [Development Setup]                  │
│   • docker-compose.prod.yml         [Production Setup]                   │
│   • backend/Dockerfile              [Backend Container]                  │
│   • frontend/Dockerfile             [Frontend Container]                 │
│                                                                          │
│ Backend:                                                                 │
│   • backend/app/core/config.py      [Pydantic Settings]                  │
│   • backend/app/core/database.py    [SQLAlchemy Connection]              │
│   • backend/.env                    [Environment Variables]              │
│   • backend/requirements.txt        [Python Dependencies]                │
│   • backend/alembic.ini             [Migrations Config]                  │
│                                                                          │
│ Frontend:                                                                │
│   • frontend/vite.config.ts         [Vite Build Config]                  │
│   • frontend/tsconfig.json          [TypeScript Config]                  │
│   • frontend/package.json           [NPM Dependencies]                   │
│   • frontend/.env                   [API URL Config]                     │
│                                                                          │
│ Claude:                                                                  │
│   • .claude/settings.local.json     [Tool Permissions]                   │
│   • CLAUDE.md                       [AI Instructions]                    │
│   • llm_handover.md                 [Session Handover]                   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Environment Variables

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        ENVIRONMENT VARIABLES                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ DATABASE:                                                                │
│   DATABASE_URL=postgresql://tha_user:password@postgres:5432/tha_db       │
│                                                                          │
│ LLM:                                                                     │
│   LLM_PROVIDER=openai              [openai or anthropic]                 │
│   OPENAI_API_KEY=sk-...                                                  │
│   ANTHROPIC_API_KEY=sk-ant-...                                           │
│                                                                          │
│ STORAGE:                                                                 │
│   STORAGE_TYPE=local               [local or s3]                         │
│   STORAGE_PATH=./storage                                                 │
│                                                                          │
│ APPLICATION:                                                             │
│   SECRET_KEY=your-secret-key                                             │
│   DEBUG=true                                                             │
│   ENVIRONMENT=development                                                │
│                                                                          │
│ PORTS:                                                                   │
│   Frontend: 3010                                                         │
│   Backend:  3011                                                         │
│   Postgres: 5432 (internal), 5433 (external)                             │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Command Reference

```bash
# Start Development Environment
docker-compose up -d

# Initialize Database
docker-compose exec backend python -m app.utils.init_db

# View Logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop Services
docker-compose down

# Rebuild After Code Changes
docker-compose down && docker-compose up -d --build

# Access Points
Frontend:     http://localhost:3010
Backend API:  http://localhost:3011
Swagger Docs: http://localhost:3011/docs
Health Check: http://localhost:3011/health
```

---

## File Index (Alphabetical)

| Category | File Path | Purpose |
|----------|-----------|---------|
| **API** | backend/app/api/alert_dashboard.py | Alert Dashboard endpoints |
| **API** | backend/app/api/analysis.py | Analysis endpoints |
| **API** | backend/app/api/content_analysis.py | Content Analysis endpoints |
| **API** | backend/app/api/dashboard.py | Dashboard KPIs |
| **API** | backend/app/api/ingestion.py | File upload endpoints |
| **API** | backend/app/api/maintenance.py | DB maintenance |
| **Config** | backend/app/core/config.py | Settings |
| **Config** | backend/app/core/database.py | DB connection |
| **Frontend** | frontend/src/pages/Dashboard.tsx | Main dashboard |
| **Frontend** | frontend/src/pages/Upload.tsx | File upload |
| **Frontend** | frontend/src/pages/AlertAnalysis.tsx | Analysis UI |
| **Frontend** | frontend/src/services/api.ts | API client |
| **Model** | backend/app/models/*.py | 20 ORM models |
| **Schema** | backend/app/schemas/alert_dashboard.py | Pydantic schemas |
| **Service** | backend/app/services/content_analyzer/analyzer.py | Main analyzer |
| **Service** | backend/app/services/content_analyzer/scoring_engine.py | Risk scoring |
| **Service** | backend/app/services/analysis/risk_scorer.py | Severity scores |
| **Service** | backend/app/services/hybrid_engine.py | Money loss (LLM+ML) |
| **Docs** | docs/th-context/*.md | Knowledge base |
| **Docs** | docs/scoring-rules/BUSINESS_PROTECTION.md | Scoring rules |
| **Rules** | .claude/rules/*.md | Claude enforcement |

---

*Document created: 2025-12-09 | Audit Cycle: 10/10 Complete*
