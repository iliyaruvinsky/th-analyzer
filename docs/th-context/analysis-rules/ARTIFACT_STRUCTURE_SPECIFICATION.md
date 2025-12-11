# Artifact Structure Specification for AI Analysis

**Version:** 1.0  
**Date:** 2025-12-11  
**Purpose:** Define optimal input structure for 100% consistent, stable AI-generated alert analysis  
**Audience:** Developers preparing alert artifacts, AI agents analyzing alerts

---

## Executive Summary

This specification defines what AI analysis requires from alert artifacts to produce **100% consistent, stable output** aligned with alert metadata and summary data.

**Current Status:** 4 artifacts contain all necessary information, but structure/parsing gaps prevent optimal consistency.

**Goal:** Enable AI to generate analysis reports with zero ambiguity, full parameter extraction, and reliable structure.

---

## Current Artifact Structure (As-Is)

### The 4 Standard Artifacts

| Artifact | Current Format | Current Parsing | Status |
|----------|---------------|-----------------|--------|
| **Code_*.txt** | Plain text ABAP | Text + regex for comments | ✅ GOOD |
| **Explanation_*.docx** | Word document | Paragraph concatenation | ⚠️ STRUCTURE LOST |
| **Metadata_*.xlsx** | Excel (4 sheets) | **Read as text blob** | ❌ SHEET STRUCTURE LOST |
| **Summary_*.xlsx** | Excel (data table) | Full column detection | ✅ EXCELLENT |

### Current Parsing Implementation

**File:** `backend/app/services/content_analyzer/artifact_reader.py`

**Code Parsing:**
```python
# Line 282-284: ✅ WORKS WELL
if filename_lower.startswith("code_"):
    artifacts.code = self._read_file(filepath)
    artifacts.code_summary = artifacts._extract_code_summary()
```

**Explanation Parsing:**
```python
# Lines 476-488: ⚠️ LOSES STRUCTURE
def _read_docx(self, filepath: str) -> Optional[str]:
    doc = Document(filepath)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n\n".join(paragraphs)  # All headings/formatting lost
```

**Metadata Parsing:**
```python
# Line 291-293: ❌ READS AS TEXT
elif filename_lower.startswith("metadata"):
    artifacts.metadata = self._read_file(filepath)  # Tries text extraction on XLSX
    artifacts.parameters = self._parse_metadata(artifacts.metadata)  # Regex on text
```

**Summary Parsing:**
```python
# Lines 298-302: ✅ EXCELLENT
if filename_lower.endswith('.xlsx'):
    summary_data = self._read_xlsx_structured(filepath)
    if summary_data:
        artifacts.summary = summary_data.raw_text
        artifacts.summary_data = summary_data  # Full column detection, types, totals
```

---

## Gap Analysis: What Prevents 100% Consistency?

### Gap 1: Metadata XLSX Sheet Structure Lost (CRITICAL)

**The Problem:**

Metadata XLSX contains **4 structured sheets**:
1. **Metadata basic** - Alert Identity (ID, Name, Module, Category, Subcategory)
2. **Metadata general** - Execution Context (Source System, Created Date, Last Executed, EI ID)
3. **Alert Parameters** - All alert parameters with values
4. **Excep. Ind. Parameters** - EI built-in restrictions

**Current Parsing:**
- Attempts to read XLSX as text (fails or produces garbage)
- Falls back to generic text extraction
- Regex patterns try to find parameters in text blob
- Sheet boundaries completely lost

**Evidence from Code:**
```python
# artifact_reader.py line 291
artifacts.metadata = self._read_file(filepath)
# This calls _read_file() which tries text encoding on binary XLSX

# Then analyzer.py line 315-357 tries regex on this "text"
backdays_match = re.search(r'BACKDAYS\s*[=:]\s*(\d+)', metadata_text, re.IGNORECASE)
```

**Impact:**
- ❌ Cannot reliably extract all parameters
- ❌ Cannot distinguish parameter types (single value vs range vs list)
- ❌ Cannot access Source System reliably
- ❌ Cannot get Created Date, Last Executed dates
- ❌ Missing Category, Subcategory fields
- ❌ Inconsistent extraction across different alert types

**What AI Needs:**
```python
# Structured access to each sheet
metadata.alert_identity.alert_id        # From "Metadata basic" sheet
metadata.alert_identity.module          # From "Metadata basic" sheet
metadata.execution.source_system        # From "Metadata general" sheet
metadata.execution.last_executed        # From "Metadata general" sheet
metadata.parameters.BACKMONTHS          # From "Alert Parameters" sheet
metadata.parameters.PERC_VARI           # From "Alert Parameters" sheet
```

---

### Gap 2: Explanation Structure Not Preserved (HIGH)

**The Problem:**

Explanation DOCX contains structured information but parsed as flat text:
- Business Purpose paragraph
- Risk types and impacts
- Pattern interpretation guidance
- May include examples, warnings, notes

**Current Parsing:**
```python
# All paragraphs concatenated - no way to identify which is "Business Purpose"
paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
return "\n\n".join(paragraphs)
```

**Impact:**
- ❌ Cannot reliably extract "Business Purpose" for report
- ❌ May include example text that shouldn't be analyzed as real data
- ❌ Cannot identify risk types vs interpretation guidance
- ❌ Manual analyses show blockquote format, but source is unclear

**What AI Needs:**

**Option A - Structured DOCX:**
```
Explanation document with heading styles:
Heading 1: "Business Purpose"
  Paragraph: The one-sentence purpose
Heading 1: "Risk Types"
  Table: Risk Type | Business Impact
Heading 1: "Interpretation Guide"
  Table: Pattern | Legitimate | Red Flag
```

**Option B - Structured JSON:**
```json
{
  "business_purpose": "This alert tracks YoY changes...",
  "risk_types": [
    {"type": "Revenue Loss", "impact": "Major customer declines..."},
    {"type": "Concentration Risk", "impact": "92% in one region..."}
  ],
  "interpretation_guide": [
    {"pattern": "High growth (>200%)", "legitimate": "New contracts", "red_flag": "Duplicate accounts"}
  ]
}
```

---

### Gap 3: Parameter Type Ambiguity (MEDIUM)

**The Problem:**

Parameters extracted as strings, but they have different types:
- `BACKMONTHS: 1` (integer)
- `DC_IND: "D"` (string/enum)
- `PERC_VARI: "Exclude -50 to 200"` (range/filter expression)
- `ACCT_NUM: "multiple values"` (list/range)

**Current Extraction:**
```python
# artifact_reader.py lines 793-803
# All parameters become strings in a dict
params[key.strip()] = value.strip()
```

**Impact:**
- ❌ Cannot validate parameter values
- ❌ Cannot parse range expressions programmatically
- ❌ Cannot distinguish single value vs multi-value
- ❌ Hard to use parameters in calculations

**What AI Needs:**
```python
# Typed parameters
parameters = {
    "BACKMONTHS": {"value": 1, "type": "integer"},
    "DC_IND": {"value": "D", "type": "enum", "options": ["D", "C"]},
    "PERC_VARI": {
        "type": "range_exclusion",
        "min": -50,
        "max": 200,
        "operator": "exclude"
    }
}
```

---

### Gap 4: No Artifact Validation (MEDIUM)

**The Problem:**

No way to verify artifacts are complete/valid before analysis:
- May have missing sheets in Metadata
- May have corrupted Summary file
- May have incomplete Explanation

**Current Behavior:**
```python
# artifact_reader.py line 125-132
@property
def is_complete(self) -> bool:
    """Check if all 4 artifacts are present."""
    return all([self.code, self.explanation, self.metadata, self.summary])
```

**Issues:**
- Only checks files exist
- Doesn't validate content
- Doesn't check sheet structure
- Doesn't verify required fields present

**What AI Needs:**
```python
def validate_artifacts(self) -> ValidationResult:
    """Validate artifact quality and completeness."""
    issues = []
    
    # Check Metadata has all 4 sheets
    if not has_sheet(metadata, "Metadata basic"):
        issues.append("Missing Metadata basic sheet")
    
    # Check required fields in Metadata basic
    if not has_field(metadata_basic, "Alert Instance ID"):
        issues.append("Missing Alert Instance ID")
    
    # Check Summary has data rows
    if summary_data.row_count == 0:
        issues.append("Summary file has no data rows")
    
    return ValidationResult(is_valid=len(issues)==0, issues=issues)
```

---

## Proposed Optimal Structure

### Option A: Enhanced Parsing (Minimal Changes)

**Keep 4 artifacts unchanged**, fix parsing to read structure:

**Implementation Changes Needed:**

1. **Metadata Parsing** (CRITICAL FIX):
```python
# NEW: artifact_reader.py
def _read_metadata_structured(self, filepath: str) -> MetadataStructured:
    """Read Metadata XLSX with sheet-level structure."""
    import pandas as pd
    
    # Read each sheet separately
    metadata_basic = pd.read_excel(filepath, sheet_name="Metadata basic")
    metadata_general = pd.read_excel(filepath, sheet_name="Metadata general")
    alert_params = pd.read_excel(filepath, sheet_name="Alert Parameters")
    ei_params = pd.read_excel(filepath, sheet_name="Excep. Ind. Parameters")
    
    return MetadataStructured(
        alert_identity={
            "alert_id": get_cell(metadata_basic, "Alert Instance ID"),
            "alert_name": get_cell(metadata_basic, "Alert Instance Name"),
            "module": extract_module(metadata_basic),  # From Category/Subcategory
            "category": get_cell(metadata_basic, "Category"),
            "subcategory": get_cell(metadata_basic, "Subcategory")
        },
        execution_context={
            "source_system": get_cell(metadata_general, "Source System"),
            "created_on": get_cell(metadata_general, "Created On"),
            "created_by": get_cell(metadata_general, "Created By"),
            "last_executed": get_cell(metadata_general, "Last Executed"),
            "exception_indicator_id": get_cell(metadata_general, "Exception Indicator ID")
        },
        parameters=parse_parameters_sheet(alert_params),  # All parameters with types
        ei_parameters=parse_parameters_sheet(ei_params)
    )
```

2. **Explanation Parsing** (MEDIUM FIX):
```python
# NEW: artifact_reader.py
def _read_explanation_structured(self, filepath: str) -> ExplanationStructured:
    """Read Explanation DOCX with structure detection."""
    from docx import Document
    
    doc = Document(filepath)
    
    # Try to identify sections by heading styles or bold text
    sections = {
        "business_purpose": None,
        "risk_types": [],
        "interpretation_guide": [],
        "notes": []
    }
    
    current_section = None
    
    for para in doc.paragraphs:
        # Detect section by style or bold
        if para.style.name.startswith('Heading'):
            current_section = identify_section(para.text)
        elif para.runs and para.runs[0].bold:
            # Bold paragraph might be section header
            current_section = identify_section(para.text)
        else:
            # Add content to current section
            add_to_section(sections, current_section, para.text)
    
    # If no headings found, use first substantial paragraph as Business Purpose
    if not sections["business_purpose"]:
        sections["business_purpose"] = get_first_substantial_paragraph(doc)
    
    return ExplanationStructured(**sections)
```

3. **Parameter Type Detection** (MEDIUM FIX):
```python
# NEW: artifact_reader.py
def parse_parameter_value(self, param_name: str, param_value: str) -> dict:
    """Parse parameter value and detect type."""
    
    # Integer
    if param_value.isdigit():
        return {"value": int(param_value), "type": "integer"}
    
    # Range/filter expression
    if "exclude" in param_value.lower():
        # "Exclude -50 to 200"
        numbers = re.findall(r'-?\d+', param_value)
        return {
            "type": "range_exclusion",
            "min": int(numbers[0]),
            "max": int(numbers[1]),
            "operator": "exclude"
        }
    
    # Range comparison
    if any(op in param_value for op in ['>', '<', '>=', '<=']):
        # "> 500000" or "> 500,000 to 3,000,000"
        return parse_comparison(param_value)
    
    # Default: string
    return {"value": param_value, "type": "string"}
```

4. **Validation** (NEW):
```python
# NEW: artifact_reader.py
def validate_artifacts(self, artifacts: AlertArtifacts) -> dict:
    """Validate artifact completeness and quality."""
    issues = []
    warnings = []
    
    # Check all 4 present
    if not artifacts.is_complete:
        missing = []
        if not artifacts.code: missing.append("Code")
        if not artifacts.explanation: missing.append("Explanation")
        if not artifacts.metadata: missing.append("Metadata")
        if not artifacts.summary: missing.append("Summary")
        issues.append(f"Missing artifacts: {', '.join(missing)}")
    
    # Validate Metadata structure
    if artifacts.metadata_structured:
        if not artifacts.metadata_structured.alert_identity.get("alert_id"):
            issues.append("Metadata missing Alert Instance ID")
        if not artifacts.metadata_structured.execution_context.get("source_system"):
            warnings.append("Metadata missing Source System")
        if not artifacts.metadata_structured.parameters:
            warnings.append("No alert parameters found in Metadata")
    
    # Validate Summary has data
    if artifacts.summary_data and artifacts.summary_data.row_count == 0:
        issues.append("Summary file has no data rows")
    
    return {
        "is_valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings
    }
```

**Pros:**
- ✅ No changes to source artifacts
- ✅ Backward compatible
- ✅ Can implement incrementally

**Cons:**
- ⚠️ Still relies on parsing DOCX/XLSX correctly
- ⚠️ Fragile if document structure varies

---

### Option B: Structured JSON Format (Optimal for AI)

**Add structured JSON files** alongside existing artifacts:

**New Structure:**
```
alert_folder/
├── Code_*.txt                          # Original (keep for reference)
├── Explanation_*.docx                  # Original (keep for reference)
├── Metadata_*.xlsx                     # Original (keep for compliance)
├── Summary_*.xlsx                      # Original (keep - used for analysis)
└── structured/                         # NEW - Generated from originals
    ├── alert_identity.json             # From Metadata Basic sheet
    ├── execution_context.json          # From Metadata General sheet
    ├── parameters.json                 # From Alert Parameters sheet
    ├── business_context.json           # From Explanation docx
    └── manifest.json                   # Complete metadata
```

**File Formats:**

**alert_identity.json:**
```json
{
  "alert_id": "200025_001374",
  "alert_name": "Comparison of monthly sales volume by customer",
  "module": "FI",
  "category": "Applications",
  "subcategory": "FI Alerts",
  "version": "1.0"
}
```

**execution_context.json:**
```json
{
  "source_system": "PS4",
  "source_system_description": "Production S/4HANA",
  "created_on": "2025-10-20T10:57:00Z",
  "created_by": "SKYWATCH",
  "last_executed": [
    "2025-11-18",
    "2025-11-19",
    "2025-11-20",
    "2025-11-21",
    "2025-11-22",
    "2025-11-23"
  ],
  "execution_count": 8,
  "exception_indicator_id": "SW_10_07_CM_MN_VL_CV",
  "status": "Active"
}
```

**parameters.json:**
```json
{
  "BACKMONTHS": {
    "value": 1,
    "type": "integer",
    "description": "Months backwards from current period",
    "default": 1
  },
  "COMPMONTHS": {
    "value": 12,
    "type": "integer",
    "description": "Months to compare (for YoY comparison)",
    "default": 12
  },
  "DC_IND": {
    "value": "D",
    "type": "enum",
    "description": "Debtor/Creditor Indicator",
    "options": ["D", "C"],
    "display": "D = Debtor (Customer)"
  },
  "PERC_VARI": {
    "type": "range_exclusion",
    "min": -50,
    "max": 200,
    "operator": "exclude",
    "description": "Flag variances outside normal range",
    "display": "Exclude -50 to 200"
  },
  "ACCT_NUM": {
    "value": null,
    "type": "range",
    "description": "Account Number filter",
    "is_empty": true
  }
}
```

**business_context.json:**
```json
{
  "business_purpose": "This alert tracks year-over-year changes in customer sales revenue by comparing current fiscal period to prior year same period. It detects unusual sales patterns, pricing anomalies, major customer growth/loss, revenue leakage, duplicate customer accounts, or fraudulent sales schemes requiring sales management review and revenue analysis.",
  "what_it_monitors": "Compares customer transaction figures (KNC1 table) between fiscal periods, calculating percentage variance between current period sales (UMXXU_TGT) and prior year same period sales (UMXXU_CMP).",
  "risk_types": [
    {
      "risk_type": "Revenue Loss",
      "business_impact": "Major customer declines indicate lost market share"
    },
    {
      "risk_type": "Concentration Risk",
      "business_impact": "Heavy dependence on single region creates business vulnerability"
    },
    {
      "risk_type": "Pricing Anomaly",
      "business_impact": "Extreme variances may indicate pricing errors or revenue manipulation"
    }
  ],
  "interpretation_guide": [
    {
      "pattern": "High growth (>200%)",
      "legitimate_cause": "New contracts, market expansion, pricing corrections",
      "red_flag": "Duplicate customer accounts, revenue manipulation, fake sales"
    },
    {
      "pattern": "Severe decline (<-50%)",
      "legitimate_cause": "Customer churn, market conditions, seasonal effects",
      "red_flag": "Lost contracts without sales follow-up, undocumented customer losses"
    },
    {
      "pattern": "Extreme variance (>1000%)",
      "legitimate_cause": "New customer with minimal prior year, data correction",
      "red_flag": "Data quality problem, duplicate accounts, fraudulent activity"
    }
  ],
  "additional_notes": []
}
```

**manifest.json** (Complete metadata):
```json
{
  "version": "1.0",
  "generated": "2025-12-11T10:00:00Z",
  "alert": {
    "id": "200025_001374",
    "name": "Comparison of monthly sales volume by customer",
    "module": "FI",
    "category": "Applications",
    "subcategory": "FI Alerts",
    "exception_indicator": "SW_10_07_CM_MN_VL_CV"
  },
  "execution": {
    "source_system": "PS4",
    "created": "2025-10-20T10:57:00Z",
    "last_run": "2025-11-23",
    "run_count": 8
  },
  "parameters": {
    // Same as parameters.json
  },
  "business_context": {
    // Same as business_context.json
  },
  "artifacts": {
    "code": "Code_Comparison of monthly sales volume by customer_200025_001374.txt",
    "explanation": "Explanation_Comparison of monthly sales volume by customer_200025_001374.docx",
    "metadata": "Metadata _Comparison of monthly sales volume by customer_200025_001374.xlsx",
    "summary": "Summary_Comparison of monthly sales volume by customer_200025_001374.xlsx"
  }
}
```

**Pros:**
- ✅ 100% consistent structure
- ✅ Easy validation
- ✅ Typed parameters
- ✅ No parsing ambiguity
- ✅ Machine-readable
- ✅ Versioned schema

**Cons:**
- ⚠️ Requires JSON generation step
- ⚠️ Duplicates information
- ⚠️ Needs to stay in sync with originals

---

### Option C: Hybrid Approach (RECOMMENDED)

**Keep all 4 original artifacts** + Generate structured cache:

**Structure:**
```
alert_folder/
├── Code_*.txt                          # Original ABAP (keep)
├── Explanation_*.docx                  # Original Word (keep)
├── Metadata_*.xlsx                     # Original Excel (keep)
├── Summary_*.xlsx                      # Original data (keep)
└── .tha-cache/                         # Auto-generated, can be regenerated
    ├── metadata_structured.json        # Extracted from Metadata XLSX
    ├── explanation_structured.json     # Extracted from Explanation DOCX
    ├── validation_result.json          # Artifact quality check
    └── cache_timestamp.txt             # Last generation time
```

**How It Works:**

1. **On first analysis:**
   - Parse Metadata XLSX → generate `metadata_structured.json`
   - Parse Explanation DOCX → generate `explanation_structured.json`
   - Validate artifacts → generate `validation_result.json`
   - Cache results in `.tha-cache/`

2. **On subsequent analyses:**
   - Check if cache exists and is newer than source files
   - If yes: Use cached structured data (fast)
   - If no: Regenerate cache (slow but accurate)

3. **On artifact updates:**
   - Delete `.tha-cache/` folder
   - Next analysis regenerates cache
   - Always uses latest source data

**Benefits:**
- ✅ No changes to source artifacts (compliance/audit friendly)
- ✅ Structured access when needed
- ✅ Performance (cache avoids re-parsing)
- ✅ Can regenerate if parsing improves
- ✅ Backward compatible (works with/without cache)
- ✅ Gradual migration (add cache for new alerts, regenerate for old)

**Implementation:**
```python
# artifact_reader.py - NEW method
def read_from_directory(self, directory_path: str) -> AlertArtifacts:
    # Existing logic to find files...
    
    # NEW: Check for structured cache
    cache_dir = os.path.join(directory_path, ".tha-cache")
    
    if self._cache_is_valid(cache_dir, metadata_path, explanation_path):
        # Use cached structured data
        metadata_structured = load_json(os.path.join(cache_dir, "metadata_structured.json"))
        explanation_structured = load_json(os.path.join(cache_dir, "explanation_structured.json"))
    else:
        # Parse and cache
        metadata_structured = self._read_metadata_structured(metadata_path)
        explanation_structured = self._read_explanation_structured(explanation_path)
        
        # Save to cache
        os.makedirs(cache_dir, exist_ok=True)
        save_json(metadata_structured, os.path.join(cache_dir, "metadata_structured.json"))
        save_json(explanation_structured, os.path.join(cache_dir, "explanation_structured.json"))
    
    artifacts.metadata_structured = metadata_structured
    artifacts.explanation_structured = explanation_structured
    
    return artifacts
```

---

## What AI Needs for 100% Consistent Output

### Required Data Fields

**From Metadata (Must Be Structured):**
```
Alert Identity:
  - alert_id (required, string, format: XXXXXX_XXXXXX)
  - alert_name (required, string)
  - module (required, enum: FI|MM|SD|MD|PUR|HR|PP|QM|BASIS)
  - category (required, string)
  - subcategory (required, string)

Execution Context:
  - source_system (required, string, e.g., "PS4", "ECC")
  - created_on (required, datetime)
  - created_by (required, string)
  - last_executed (required, datetime or list)
  - exception_indicator_id (required, string)

Parameters:
  - ALL parameters from Alert Parameters sheet
  - Each parameter needs:
    - value (any type)
    - type (integer|string|enum|range|boolean)
    - description (string)
    - is_empty (boolean)
```

**From Explanation (Must Be Structured):**
```
Business Context:
  - business_purpose (required, string, 1-3 sentences)
  - what_it_monitors (optional, string)
  - risk_types (optional, array of {risk_type, business_impact})
  - interpretation_guide (optional, array of {pattern, legitimate, red_flag})
```

**From Summary (Already Structured ✅):**
```
Summary Data:
  - row_count (integer)
  - column_count (integer)
  - columns (array of ColumnInfo with types, totals, SAP fields)
  - total_amount (decimal)
  - currency (string)
  - sample_rows (array of dicts)
```

---

## Implementation Guidance for Developers

### Phase 1: Fix Metadata Parsing (CRITICAL)

**File to Modify:** `backend/app/services/content_analyzer/artifact_reader.py`

**Add new method:**
```python
def _read_metadata_structured(self, filepath: str) -> dict:
    """Read Metadata XLSX as structured data."""
    import pandas as pd
    
    try:
        # Read all sheets
        sheets = pd.read_excel(filepath, sheet_name=None)
        
        # Extract from each sheet
        basic = sheets.get("Metadata basic", pd.DataFrame())
        general = sheets.get("Metadata general", pd.DataFrame())
        params = sheets.get("Alert Parameters", pd.DataFrame())
        
        # Build structured output
        return {
            "alert_identity": self._parse_metadata_basic(basic),
            "execution_context": self._parse_metadata_general(general),
            "parameters": self._parse_parameters(params)
        }
    except Exception as e:
        logger.error(f"Failed to parse metadata: {e}")
        return None
```

**Helper methods needed:**
- `_parse_metadata_basic()` - Extract alert ID, name, module, category
- `_parse_metadata_general()` - Extract source system, dates, EI ID
- `_parse_parameters()` - Extract ALL parameters with type detection

**Update AlertArtifacts class:**
```python
@dataclass
class AlertArtifacts:
    # ... existing fields ...
    
    # NEW: Structured metadata
    metadata_structured: Optional[dict] = None
    explanation_structured: Optional[dict] = None
```

### Phase 2: Fix Explanation Parsing (HIGH)

**Add new method:**
```python
def _read_explanation_structured(self, filepath: str) -> dict:
    """Read Explanation DOCX with structure detection."""
    from docx import Document
    
    doc = Document(filepath)
    
    # Strategy 1: Look for headings
    # Strategy 2: Identify by bold text
    # Strategy 3: Fallback to first paragraph for business_purpose
    
    return {
        "business_purpose": extracted_purpose,
        "risk_types": extracted_risks,
        "interpretation_guide": extracted_guide
    }
```

### Phase 3: Add Validation (MEDIUM)

**Add validation before analysis:**
```python
# In analyzer.py analyze_alert() method
def analyze_alert(self, artifacts: AlertArtifacts, include_raw: bool = False):
    # NEW: Validate first
    validation = self.artifact_reader.validate_artifacts(artifacts)
    if not validation["is_valid"]:
        logger.error(f"Invalid artifacts: {validation['issues']}")
        # Return error finding or raise exception
    
    # Proceed with analysis...
```

### Phase 4: Implement Caching (OPTIONAL)

**Add cache logic:**
```python
def read_from_directory(self, directory_path: str) -> AlertArtifacts:
    # ... existing file discovery ...
    
    # NEW: Try cache first
    cache_dir = os.path.join(directory_path, ".tha-cache")
    if self._cache_valid(cache_dir, [metadata_path, explanation_path]):
        metadata_structured = load_json(cache_dir + "/metadata_structured.json")
        explanation_structured = load_json(cache_dir + "/explanation_structured.json")
    else:
        # Parse and cache
        metadata_structured = self._read_metadata_structured(metadata_path)
        explanation_structured = self._read_explanation_structured(explanation_path)
        self._save_cache(cache_dir, metadata_structured, explanation_structured)
    
    # ... rest of method ...
```

---

## Migration Path

### Step 1: Test Current Structure
1. Select 10 diverse alerts (different modules, parameters)
2. Run current analysis pipeline
3. Document extraction failures/inconsistencies

### Step 2: Implement Structured Metadata Parsing
1. Add `_read_metadata_structured()` method
2. Test with same 10 alerts
3. Compare: structured vs regex extraction
4. Fix any sheet format variations

### Step 3: Implement Structured Explanation Parsing
1. Add `_read_explanation_structured()` method
2. Test business_purpose extraction
3. Validate against manual analyses in `docs/analysis/`

### Step 4: Add Validation
1. Implement `validate_artifacts()` method
2. Add validation to analysis workflow
3. Generate validation reports for all alerts

### Step 5: Implement Caching (Optional)
1. Add cache directory logic
2. Generate cache for all alerts
3. Measure performance improvement

### Step 6: Gradual Rollout
1. Test with 10 alerts
2. Expand to 50 alerts
3. Analyze all 30+ alerts in repository
4. Compare consistency metrics

---

## Expected Improvements

### Before (Current State)

**Parameter Extraction:**
- ❌ BACKMONTHS: May or may not be extracted (depends on regex match)
- ❌ PERC_VARI: Extracted as string "Exclude -50 to 200" (cannot parse range)
- ❌ Source System: Not reliably extracted
- ❌ Module: Inferred from path (not from metadata)

**Consistency:**
- ⚠️ 70-80% consistency across alerts
- ⚠️ Missing fields in some analyses
- ⚠️ Parameter extraction varies by format

### After (With Structured Parsing)

**Parameter Extraction:**
- ✅ BACKMONTHS: Always extracted as integer from Alert Parameters sheet
- ✅ PERC_VARI: Parsed as range object {min: -50, max: 200, operator: "exclude"}
- ✅ Source System: Always extracted from Metadata general sheet
- ✅ Module: Extracted from Metadata basic sheet

**Consistency:**
- ✅ 100% consistency (all alerts use same structured schema)
- ✅ All required fields present (validated)
- ✅ Parameter extraction uniform

---

## Schema Definitions

### MetadataStructured Schema

```typescript
interface MetadataStructured {
  alert_identity: {
    alert_id: string;           // Format: XXXXXX_XXXXXX
    alert_name: string;
    module: "FI" | "MM" | "SD" | "MD" | "PUR" | "HR" | "PP" | "QM" | "BASIS";
    category: string;
    subcategory: string;
  };
  
  execution_context: {
    source_system: string;      // e.g., "PS4", "ECC", "BIP"
    created_on: string;         // ISO datetime
    created_by: string;
    last_executed: string | string[];  // Single or multiple dates
    execution_count?: number;
    exception_indicator_id: string;
    status?: string;
  };
  
  parameters: {
    [key: string]: {
      value: any;
      type: "integer" | "string" | "enum" | "range" | "range_exclusion" | "boolean";
      description: string;
      is_empty: boolean;
      default?: any;
      options?: string[];  // For enum types
      min?: number;        // For range types
      max?: number;        // For range types
      operator?: string;   // For range types (">", "exclude", etc.)
    }
  };
  
  ei_parameters?: {
    // Exception Indicator built-in parameters (if present)
  };
}
```

### ExplanationStructured Schema

```typescript
interface ExplanationStructured {
  business_purpose: string;  // Required: 1-3 sentence description
  
  what_it_monitors?: string; // Optional: Technical monitoring description
  
  risk_types?: Array<{
    risk_type: string;
    business_impact: string;
  }>;
  
  interpretation_guide?: Array<{
    pattern: string;
    legitimate_cause: string;
    red_flag: string;
  }>;
  
  additional_notes?: string[];
}
```

---

## Validation Rules

### Required Fields Validation

**Metadata:**
- MUST have: alert_id, alert_name, source_system, exception_indicator_id
- MUST have at least 1 parameter in Alert Parameters sheet
- Dates MUST be valid format

**Explanation:**
- MUST have: business_purpose (non-empty string)
- business_purpose MUST be 10-500 characters

**Summary:**
- MUST have: At least 1 data row
- MUST have: At least 2 columns
- MUST have identifiable currency or amount column

**Code:**
- MUST have: Alert Definition comment OR function definition
- SHOULD have: Parameter definitions section

### Completeness Validation

```python
def validate_completeness(artifacts: AlertArtifacts) -> dict:
    """Check if artifacts are complete for analysis."""
    
    score = 0
    max_score = 10
    issues = []
    
    # 4 artifacts present (4 points)
    if artifacts.code: score += 1
    else: issues.append("Missing Code artifact")
    
    if artifacts.explanation: score += 1
    else: issues.append("Missing Explanation artifact")
    
    if artifacts.metadata: score += 1
    else: issues.append("Missing Metadata artifact")
    
    if artifacts.summary: score += 1
    else: issues.append("Missing Summary artifact")
    
    # Metadata structure (2 points)
    if artifacts.metadata_structured:
        score += 1
        if artifacts.metadata_structured.get("parameters"):
            score += 1
        else:
            issues.append("No parameters in Metadata")
    else:
        issues.append("Metadata not parsed as structured")
    
    # Explanation structure (2 points)
    if artifacts.explanation_structured:
        score += 1
        if artifacts.explanation_structured.get("business_purpose"):
            score += 1
        else:
            issues.append("No business_purpose in Explanation")
    else:
        issues.append("Explanation not parsed as structured")
    
    # Summary has data (2 points)
    if artifacts.summary_data:
        score += 1
        if artifacts.summary_data.row_count > 0:
            score += 1
        else:
            issues.append("Summary has no data rows")
    else:
        issues.append("Summary not parsed as structured")
    
    return {
        "completeness_score": score,
        "max_score": max_score,
        "percentage": (score / max_score) * 100,
        "is_complete": score == max_score,
        "issues": issues
    }
```

---

## Developer Checklist

When preparing artifacts for AI analysis:

### Metadata XLSX Requirements

- [ ] File has 4 sheets exactly:
  - [ ] "Metadata basic"
  - [ ] "Metadata general"
  - [ ] "Alert Parameters"
  - [ ] "Excep. Ind. Parameters"
- [ ] Metadata basic contains:
  - [ ] Alert Instance ID
  - [ ] Alert Instance Name
  - [ ] Category
  - [ ] Subcategory
- [ ] Metadata general contains:
  - [ ] Source System
  - [ ] Created On (date)
  - [ ] Last Executed (date)
  - [ ] Exception Indicator ID
- [ ] Alert Parameters:
  - [ ] At least 1 parameter row
  - [ ] Parameter Name column
  - [ ] Parameter Value column
  - [ ] Include empty parameters (value shown as blank or "none")

### Explanation DOCX Requirements

- [ ] Contains Business Purpose section (clearly identifiable)
- [ ] Business Purpose is 1-3 sentences
- [ ] Describes what alert detects and why it matters
- [ ] (Optional) Risk Types section with table
- [ ] (Optional) Interpretation guidance
- [ ] No template placeholders (e.g., "[Insert description]")

### Summary XLSX/CSV Requirements

- [ ] Has header row
- [ ] At least 1 data row
- [ ] Columns have clear names (ideally with SAP field codes)
- [ ] Currency amounts have associated currency column
- [ ] No completely empty columns
- [ ] Data is actual findings (not examples)

### Code TXT Requirements

- [ ] Valid ABAP or SQL code
- [ ] Contains Alert Definition comment
- [ ] Parameter definitions section present
- [ ] Detection logic is readable

---

## Testing Plan

### Test Dataset
Select 10 alerts covering:
- 3 modules (FI, MM, SD)
- 3 complexity levels (simple, medium, complex parameters)
- 2 variance types (YoY comparison, threshold-based)

### Test Cases

**TC1: Parameter Extraction**
- Extract all parameters from Metadata
- Verify ALL parameters captured (compare to manual count)
- Verify parameter types detected correctly
- Verify empty parameters shown as "(none)"

**TC2: Structured Access**
- Access alert_id from metadata_structured.alert_identity.alert_id
- Access source_system from metadata_structured.execution_context.source_system
- Access BACKMONTHS from metadata_structured.parameters.BACKMONTHS.value
- Verify no parsing errors

**TC3: Business Purpose Extraction**
- Extract business_purpose from explanation_structured
- Verify it matches manual analyses in docs/analysis/
- Verify no template text included
- Verify 1-3 sentence format

**TC4: Validation**
- Run validation on complete alerts (expect 100% score)
- Run validation on incomplete alerts (expect issues flagged)
- Verify validation catches missing sheets
- Verify validation catches empty parameters

**TC5: End-to-End Analysis**
- Analyze 10 alerts with structured parsing
- Compare output consistency
- Measure: How many have all Executive Summary sections?
- Measure: How many have all parameters documented?
- Target: 100% (vs current ~70-80%)

---

## Success Criteria

### For 100% Consistent Output

**Metadata:**
- ✅ 100% of alerts extract alert_id correctly
- ✅ 100% of alerts extract source_system correctly
- ✅ 100% of alerts extract ALL parameters
- ✅ 100% of alerts identify module correctly

**Explanation:**
- ✅ 100% of alerts extract business_purpose
- ✅ Business purpose matches manual analysis format
- ✅ No template text included in analysis

**Analysis Output:**
- ✅ 100% of reports have Executive Summary with all 7 sections
- ✅ 100% of reports show ALL parameters (including empty ones)
- ✅ 100% of reports identify source system
- ✅ 100% of reports follow template structure exactly

**Validation:**
- ✅ All incomplete artifacts flagged before analysis
- ✅ All missing required fields reported
- ✅ Completeness score 100% for valid artifacts

---

## Appendix: Real-World Examples

### Example 1: Well-Structured Alert

**Alert:** FI - Comparison of monthly sales volume by customer (200025_001374)

**Artifacts Present:**
- ✅ Code_*.txt - 399 lines of ABAP
- ✅ Explanation_*.docx - Business description
- ✅ Metadata_*.xlsx - 4 sheets with complete info
- ✅ Summary_*.xlsx - 211 customer records

**Manual Analysis:** `docs/analysis/FI_Comparison_Monthly_Sales_Volume_Customer_Analysis.md`

**Parameters Extracted Manually:**
- BACKMONTHS: 1
- COMPMONTHS: 12
- DC_IND: D
- PERC_VARI: Exclude -50 to 200

**Source System:** PS4 (extracted manually from Metadata general sheet)

**With Structured Parsing:**
```json
// Auto-extracted
{
  "alert_identity": {"alert_id": "200025_001374", "module": "FI"},
  "execution_context": {"source_system": "PS4"},
  "parameters": {
    "BACKMONTHS": {"value": 1, "type": "integer"},
    "COMPMONTHS": {"value": 12, "type": "integer"},
    "DC_IND": {"value": "D", "type": "string"},
    "PERC_VARI": {"type": "range_exclusion", "min": -50, "max": 200}
  }
}
```

---

### Example 2: Multi-Currency Alert

**Alert:** SD - Monthly returns value by Payer (200025_001455)

**Challenge:** Summary has multiple currencies (KES, ZAR)

**Current Handling:**
- Summary_*.xlsx parsed ✅ (currencies detected)
- Metadata parameters ⚠️ (may not extract currency filter)

**With Structured Parsing:**
```json
{
  "parameters": {
    "WAERS_FR": {
      "value": ["KES", "ZAR"],
      "type": "list",
      "description": "Currency filter"
    }
  }
}
```

**AI Can Then:**
- Group Summary data by detected currencies
- Match against WAERS_FR parameter
- Validate: Are summary currencies allowed by parameter?
- Report discrepancies if found

---

## Conclusion

### Answer to Original Question

**Q: Are these artifacts 100% sufficient for consistent analysis output?**

**A: NO** - Following Anti-Hallucination Rule 8 (No "yesman" behavior) and Rule 9 (Truth as highest value):

The 4 artifacts **contain all necessary information**, but their **current structure prevents 100% consistency** due to:

1. ❌ **Metadata XLSX parsed as text** → fragile parameter extraction
2. ❌ **Explanation DOCX unstructured** → cannot reliably identify Business Purpose
3. ❌ **No validation** → may analyze incomplete artifacts
4. ❌ **No parameter typing** → ranges are text strings, not structured

### What Would Achieve 100% Consistency

**Recommended Approach: Option C (Hybrid)**

1. Keep 4 original artifacts unchanged (compliance, audit)
2. Enhance parsing to read XLSX/DOCX as structured data
3. Add `.tha-cache/` folder with extracted JSON
4. Validate artifacts before analysis
5. Use structured data for consistent access

**Implementation Priority:**
1. **Fix Metadata parsing** (CRITICAL) - Read sheets separately, extract all parameters
2. **Fix Explanation parsing** (HIGH) - Structure detection or explicit sections
3. **Add validation** (MEDIUM) - Verify completeness before analysis
4. **Add caching** (LOW) - Performance optimization

**Expected Result:**
- ✅ 100% of alerts extract all parameters correctly
- ✅ 100% of analyses include all required sections
- ✅ 100% alignment with alert metadata
- ✅ Stable, repeatable, consistent output

---

*This specification provides developers with clear requirements for preparing artifacts that enable optimal AI analysis.*

**Document Location:** `docs/th-context/analysis-rules/ARTIFACT_STRUCTURE_SPECIFICATION.md`  
**Related Files:**
- `docs/th-context/analysis-rules/templates/quantitative-alert.yaml` - Output template
- `.claude/rules/quantitative-alert-analysis.md` - Analysis rules
- `backend/app/services/content_analyzer/artifact_reader.py` - Implementation file

