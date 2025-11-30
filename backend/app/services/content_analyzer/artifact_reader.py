"""
Artifact Reader for 4C Alerts

Parses the 4 artifact files associated with each alert:
- Code_* - ABAP function code
- Explanation_* - Human-readable description
- Metadata_* - Alert configuration/parameters
- Summary_* - Actual output data to analyze

Enhanced with dynamic column detection for varying alert types.
"""

import os
import re
import logging
from typing import Dict, List, Optional, NamedTuple, Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum

logger = logging.getLogger(__name__)


class ColumnType(str, Enum):
    """Detected column data types."""
    NUMERIC = "numeric"       # Numbers, amounts, counts
    CURRENCY = "currency"     # Monetary values (has currency indicator)
    DATE = "date"            # Date/time values
    IDENTIFIER = "identifier" # IDs, codes, keys
    TEXT = "text"            # Free text, descriptions
    PERCENTAGE = "percentage" # Percentage values
    COUNT = "count"          # Count/counter values


@dataclass
class ColumnInfo:
    """Information about a detected column."""
    name: str
    original_name: str  # Name with SAP field code e.g., "Amount (DMBTR)"
    sap_field: Optional[str] = None  # Extracted SAP field e.g., "DMBTR"
    column_type: ColumnType = ColumnType.TEXT
    is_key_metric: bool = False  # True if this is an important metric column
    sample_values: List[Any] = field(default_factory=list)

    # Statistics for numeric columns
    total: Optional[float] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    avg_value: Optional[float] = None
    non_null_count: int = 0


@dataclass
class SummaryData:
    """Structured representation of Summary file data."""

    # Basic info
    row_count: int = 0
    column_count: int = 0

    # Column information
    columns: List[ColumnInfo] = field(default_factory=list)

    # Key metrics extracted
    key_metrics: Dict[str, Any] = field(default_factory=dict)

    # Aggregations
    total_amount: Optional[float] = None
    total_count: Optional[int] = None
    currency: Optional[str] = None

    # Sample data (first N rows as dicts)
    sample_rows: List[Dict[str, Any]] = field(default_factory=list)

    # Raw text representation (for backward compatibility)
    raw_text: str = ""

    def get_metric_summary(self) -> str:
        """Get a formatted summary of key metrics."""
        lines = []
        lines.append(f"Records: {self.row_count:,}")

        if self.total_amount is not None:
            currency_str = f" {self.currency}" if self.currency else ""
            lines.append(f"Total Amount: {self.total_amount:,.2f}{currency_str}")

        if self.total_count is not None:
            lines.append(f"Total Count: {self.total_count:,}")

        # Add key metric columns
        for col in self.columns:
            if col.is_key_metric and col.total is not None:
                lines.append(f"{col.name}: {col.total:,.2f} (sum)")

        return "\n".join(lines)


@dataclass
class AlertArtifacts:
    """Container for all artifacts of a single alert."""

    alert_id: str
    alert_name: str

    # The 4 artifact contents (raw text)
    code: Optional[str] = None
    explanation: Optional[str] = None
    metadata: Optional[str] = None
    summary: Optional[str] = None

    # Structured summary data (for quantitative alerts)
    summary_data: Optional[SummaryData] = None

    # Parsed/extracted information
    code_summary: Optional[str] = None  # Extracted purpose from code comments
    parameters: Dict[str, str] = field(default_factory=dict)

    # File paths (for reference)
    code_path: Optional[str] = None
    explanation_path: Optional[str] = None
    metadata_path: Optional[str] = None
    summary_path: Optional[str] = None

    @property
    def is_complete(self) -> bool:
        """Check if all 4 artifacts are present."""
        return all([self.code, self.explanation, self.metadata, self.summary])

    @property
    def has_minimum(self) -> bool:
        """Check if we have at least explanation and summary (minimum for analysis)."""
        return self.explanation is not None or self.summary is not None

    def get_analysis_context(self) -> str:
        """Get combined context for analysis."""
        parts = []

        if self.explanation:
            parts.append(f"## Explanation\n{self.explanation}")

        if self.code_summary:
            parts.append(f"## Code Purpose\n{self.code_summary}")
        elif self.code:
            # Extract summary from code if not already done
            summary = self._extract_code_summary()
            if summary:
                parts.append(f"## Code Purpose\n{summary}")

        if self.metadata:
            parts.append(f"## Metadata\n{self.metadata}")

        return "\n\n".join(parts)

    def _extract_code_summary(self) -> Optional[str]:
        """Extract the purpose/summary from ABAP code comments."""
        if not self.code:
            return None

        # Look for Alert Definition comment block
        patterns = [
            r'\*\s*Alert Definition\s*:\s*(.+?)(?:\n\*-|\n\*\s*CHANGE)',
            r'\*\s*Description\s*:\s*(.+?)(?:\n\*-|\n\*\s*CHANGE)',
            r"'Alert Definition:\s*(.+?)(?:\n|')",
        ]

        for pattern in patterns:
            match = re.search(pattern, self.code, re.DOTALL | re.IGNORECASE)
            if match:
                summary = match.group(1).strip()
                # Clean up the summary
                summary = re.sub(r'\n\*\s*', ' ', summary)
                summary = re.sub(r'\s+', ' ', summary)
                return summary[:500]  # Limit length

        return None

    def get_key_metrics(self) -> Dict[str, Any]:
        """Get key metrics from structured summary data."""
        if not self.summary_data:
            return {}

        metrics = {
            "record_count": self.summary_data.row_count,
            "column_count": self.summary_data.column_count,
        }

        if self.summary_data.total_amount is not None:
            metrics["total_amount"] = self.summary_data.total_amount
            if self.summary_data.currency:
                metrics["currency"] = self.summary_data.currency

        if self.summary_data.total_count is not None:
            metrics["total_count"] = self.summary_data.total_count

        # Add key metric columns
        for col in self.summary_data.columns:
            if col.is_key_metric and col.total is not None:
                key = f"{col.name.lower().replace(' ', '_')}_total"
                metrics[key] = col.total

        return metrics

    def get_column_summary(self) -> str:
        """Get a summary of detected columns and their types."""
        if not self.summary_data or not self.summary_data.columns:
            return "No structured column data available"

        lines = ["Detected Columns:"]
        for col in self.summary_data.columns:
            marker = "⭐" if col.is_key_metric else "  "
            sap = f" ({col.sap_field})" if col.sap_field else ""
            stats = ""
            if col.column_type in [ColumnType.NUMERIC, ColumnType.CURRENCY, ColumnType.COUNT]:
                if col.total is not None:
                    stats = f" | Total: {col.total:,.2f}"
            lines.append(f"  {marker} {col.name}{sap}: {col.column_type.value}{stats}")

        return "\n".join(lines)


class ArtifactReader:
    """
    Reads and parses the 4 artifact files for 4C alerts.

    Expected file naming convention:
    - Code_{alert_name}_{alert_id}.txt
    - Explanation_{alert_name}_{alert_id}.txt
    - Metadata_{alert_name}_{alert_id}.txt
    - Summary_{alert_name}_{alert_id}.txt (or .csv, .xlsx)
    """

    ARTIFACT_PREFIXES = ["Code_", "Explanation_", "Metadata_", "Summary_"]

    def __init__(self):
        self._artifacts_cache: Dict[str, AlertArtifacts] = {}

    def read_from_directory(self, directory_path: str) -> AlertArtifacts:
        """
        Read all artifacts from a directory containing alert files.

        Args:
            directory_path: Path to directory containing the 4 artifact files

        Returns:
            AlertArtifacts object with all loaded content
        """
        if not os.path.exists(directory_path):
            raise ValueError(f"Directory not found: {directory_path}")

        # Find and read each artifact type
        files = os.listdir(directory_path)

        # First pass: extract alert info from filenames
        alert_id = None
        alert_name = None
        for filename in files:
            parsed_id, parsed_name = self._parse_filename(filename)
            if parsed_id and not alert_id:
                alert_id = parsed_id
            if parsed_name and not alert_name:
                alert_name = parsed_name

        # Fallback to directory name if nothing found in filenames
        if not alert_id or not alert_name:
            dir_name = os.path.basename(directory_path)
            if not alert_id:
                alert_id = dir_name
            if not alert_name:
                alert_name = dir_name

        artifacts = AlertArtifacts(
            alert_id=alert_id,
            alert_name=alert_name
        )

        # Second pass: read file contents
        for filename in files:
            filepath = os.path.join(directory_path, filename)
            filename_lower = filename.lower()

            if filename_lower.startswith("code_"):
                artifacts.code = self._read_file(filepath)
                artifacts.code_path = filepath
                artifacts.code_summary = artifacts._extract_code_summary()

            elif filename_lower.startswith("explanation_"):
                artifacts.explanation = self._read_file(filepath)
                artifacts.explanation_path = filepath

            elif filename_lower.startswith("metadata"):  # Handle "Metadata " with space
                artifacts.metadata = self._read_file(filepath)
                artifacts.metadata_path = filepath
                artifacts.parameters = self._parse_metadata(artifacts.metadata)

            elif filename_lower.startswith("summary_"):
                artifacts.summary_path = filepath
                # For xlsx files, also get structured data
                if filename_lower.endswith('.xlsx'):
                    summary_data = self._read_xlsx_structured(filepath)
                    if summary_data:
                        artifacts.summary = summary_data.raw_text
                        artifacts.summary_data = summary_data
                else:
                    artifacts.summary = self._read_file(filepath)

        return artifacts

    def _parse_filename(self, filename: str) -> tuple:
        """
        Parse alert ID and name from artifact filename.

        Expected formats:
        - Code_Alert Name_200025_001372.txt
        - Summary_Alert Name_200025_001372.xlsx

        Returns:
            Tuple of (alert_id, alert_name) or (None, None) if not parseable
        """
        # Remove file extension
        name_without_ext = re.sub(r'\.(txt|csv|xlsx|docx|pdf)$', '', filename, flags=re.IGNORECASE)

        # Remove artifact prefix (Code_, Explanation_, Metadata_, Summary_)
        for prefix in self.ARTIFACT_PREFIXES:
            if name_without_ext.lower().startswith(prefix.lower()):
                name_without_ext = name_without_ext[len(prefix):]
                break

        # Also handle "Metadata " with space
        if name_without_ext.lower().startswith("metadata "):
            name_without_ext = name_without_ext[9:]

        # Try to extract alert ID (format: 200025_001372)
        match = re.search(r'_(\d{6}_\d{6})$', name_without_ext)
        if match:
            alert_id = match.group(1)
            alert_name = name_without_ext[:match.start()].strip('_').replace('_', ' ')
            return alert_id, alert_name

        return None, None

    def read_from_files(
        self,
        alert_id: str,
        alert_name: str,
        code_path: Optional[str] = None,
        explanation_path: Optional[str] = None,
        metadata_path: Optional[str] = None,
        summary_path: Optional[str] = None
    ) -> AlertArtifacts:
        """
        Read artifacts from individual file paths.

        Args:
            alert_id: The alert ID
            alert_name: The alert name
            code_path: Path to Code file
            explanation_path: Path to Explanation file
            metadata_path: Path to Metadata file
            summary_path: Path to Summary file

        Returns:
            AlertArtifacts object with all loaded content
        """
        artifacts = AlertArtifacts(
            alert_id=alert_id,
            alert_name=alert_name
        )

        if code_path and os.path.exists(code_path):
            artifacts.code = self._read_file(code_path)
            artifacts.code_path = code_path
            artifacts.code_summary = artifacts._extract_code_summary()

        if explanation_path and os.path.exists(explanation_path):
            artifacts.explanation = self._read_file(explanation_path)
            artifacts.explanation_path = explanation_path

        if metadata_path and os.path.exists(metadata_path):
            artifacts.metadata = self._read_file(metadata_path)
            artifacts.metadata_path = metadata_path
            artifacts.parameters = self._parse_metadata(artifacts.metadata)

        if summary_path and os.path.exists(summary_path):
            artifacts.summary = self._read_file(summary_path)
            artifacts.summary_path = summary_path

        return artifacts

    def read_from_content(
        self,
        alert_id: str,
        alert_name: str,
        code: Optional[str] = None,
        explanation: Optional[str] = None,
        metadata: Optional[str] = None,
        summary: Optional[str] = None
    ) -> AlertArtifacts:
        """
        Create AlertArtifacts from content strings directly.

        Args:
            alert_id: The alert ID
            alert_name: The alert name
            code: Code content
            explanation: Explanation content
            metadata: Metadata content
            summary: Summary content

        Returns:
            AlertArtifacts object
        """
        artifacts = AlertArtifacts(
            alert_id=alert_id,
            alert_name=alert_name,
            code=code,
            explanation=explanation,
            metadata=metadata,
            summary=summary
        )

        if code:
            artifacts.code_summary = artifacts._extract_code_summary()

        if metadata:
            artifacts.parameters = self._parse_metadata(metadata)

        return artifacts

    def _parse_directory_name(self, dir_name: str) -> tuple:
        """
        Parse alert ID and name from directory name.

        Expected format: "{alert_id} - {alert_name}" or "{alert_id}_{alert_name}"
        """
        # Try format: "200025_001373 - Comparison of monthly purchase volume by vendor"
        match = re.match(r'^(\d+_\d+)\s*-\s*(.+)$', dir_name)
        if match:
            return match.group(1), match.group(2)

        # Try format: "200025_001373_Alert_Name"
        match = re.match(r'^(\d+_\d+)_(.+)$', dir_name)
        if match:
            return match.group(1), match.group(2).replace('_', ' ')

        # Fallback
        return dir_name, dir_name

    def _read_file(self, filepath: str) -> Optional[str]:
        """Read file content with encoding handling and format detection."""
        filename_lower = filepath.lower()

        # Handle Word documents (.docx)
        if filename_lower.endswith('.docx'):
            return self._read_docx(filepath)

        # Handle Excel files (.xlsx)
        if filename_lower.endswith('.xlsx'):
            return self._read_xlsx(filepath)

        # Handle plain text files
        encodings = ['utf-8', 'latin-1', 'cp1252']

        for encoding in encodings:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.error(f"Error reading {filepath}: {e}")
                return None

        logger.error(f"Could not read {filepath} with any encoding")
        return None

    def _read_docx(self, filepath: str) -> Optional[str]:
        """Read text content from a Word document."""
        try:
            from docx import Document
            doc = Document(filepath)
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            return "\n\n".join(paragraphs)
        except ImportError:
            logger.warning("python-docx not installed, cannot read .docx files")
            return None
        except Exception as e:
            logger.error(f"Error reading docx {filepath}: {e}")
            return None

    def _read_xlsx(self, filepath: str) -> Optional[str]:
        """Read content from an Excel file as text summary (backward compatible)."""
        summary_data = self._read_xlsx_structured(filepath)
        if summary_data:
            return summary_data.raw_text
        return None

    def _read_xlsx_structured(self, filepath: str) -> Optional[SummaryData]:
        """
        Read Excel file with dynamic column detection and metric extraction.

        Returns:
            SummaryData object with structured column info and metrics
        """
        try:
            import pandas as pd
            import numpy as np

            # First, detect header row by reading raw data
            df_raw = pd.read_excel(filepath, header=None, nrows=5)

            # Find header row (skip "Data" marker row if present)
            header_row = 0
            for i, row in df_raw.iterrows():
                first_val = str(row.iloc[0]).strip().lower() if pd.notna(row.iloc[0]) else ""
                if first_val == "data":
                    header_row = i + 1
                    break
                # Check if this looks like a header row (multiple non-empty text values)
                non_empty = sum(1 for v in row if pd.notna(v) and str(v).strip())
                if non_empty > 3:
                    header_row = i
                    break

            # Read with detected header
            df = pd.read_excel(filepath, header=header_row)

            # Remove completely empty columns
            df = df.dropna(axis=1, how='all')

            # Build SummaryData
            summary_data = SummaryData(
                row_count=len(df),
                column_count=len(df.columns)
            )

            # Detect column info for each column
            currency_column = None
            for col_name in df.columns:
                col_info = self._analyze_column(df, col_name)
                summary_data.columns.append(col_info)

                # Track currency column for amount columns
                if col_info.column_type == ColumnType.TEXT:
                    col_lower = col_name.lower()
                    if 'currency' in col_lower or 'waers' in col_lower:
                        # Get most common currency
                        currency_values = df[col_name].dropna().astype(str)
                        if len(currency_values) > 0:
                            currency_column = currency_values.mode().iloc[0] if len(currency_values.mode()) > 0 else None

            # Set currency
            if currency_column:
                summary_data.currency = currency_column

            # Calculate total amount from key metric columns
            total_amount = 0.0
            for col_info in summary_data.columns:
                if col_info.is_key_metric and col_info.column_type in [ColumnType.CURRENCY, ColumnType.NUMERIC]:
                    if col_info.total is not None:
                        total_amount += col_info.total

            if total_amount > 0:
                summary_data.total_amount = total_amount

            # Extract sample rows
            sample_df = df.head(10)
            for _, row in sample_df.iterrows():
                row_dict = {}
                for col in df.columns:
                    val = row[col]
                    if pd.notna(val):
                        row_dict[str(col)] = val
                summary_data.sample_rows.append(row_dict)

            # Generate raw text representation
            summary_data.raw_text = self._generate_raw_text(df, summary_data)

            return summary_data

        except ImportError:
            logger.warning("pandas/openpyxl not installed, cannot read .xlsx files")
            return None
        except Exception as e:
            logger.error(f"Error reading xlsx {filepath}: {e}")
            return None

    def _analyze_column(self, df: "pd.DataFrame", col_name: str) -> ColumnInfo:
        """
        Analyze a column to detect its type and extract statistics.

        Args:
            df: DataFrame containing the column
            col_name: Name of the column to analyze

        Returns:
            ColumnInfo with detected type and statistics
        """
        import pandas as pd
        import numpy as np

        # Extract SAP field code if present (e.g., "Amount (DMBTR)" -> "DMBTR")
        sap_field = self._extract_sap_field(str(col_name))

        # Clean column name for display
        clean_name = str(col_name)
        if sap_field:
            # Remove SAP code from display name
            clean_name = re.sub(r'\s*\([A-Z0-9_]+\)\s*$', '', clean_name).strip()

        col_info = ColumnInfo(
            name=clean_name,
            original_name=str(col_name),
            sap_field=sap_field
        )

        series = df[col_name]
        non_null = series.dropna()
        col_info.non_null_count = len(non_null)

        if len(non_null) == 0:
            return col_info

        # Store sample values
        col_info.sample_values = list(non_null.head(5))

        # Detect column type
        col_info.column_type = self._detect_column_type(col_name, series, sap_field)

        # Check if this is a key metric column
        col_info.is_key_metric = self._is_key_metric_column(col_name, sap_field, col_info.column_type)

        # Calculate statistics for numeric columns
        if col_info.column_type in [ColumnType.NUMERIC, ColumnType.CURRENCY, ColumnType.COUNT, ColumnType.PERCENTAGE]:
            try:
                # Convert to numeric, handling string numbers with commas
                numeric_series = pd.to_numeric(
                    non_null.astype(str).str.replace(',', '').str.replace('-', ''),
                    errors='coerce'
                )
                numeric_series = numeric_series.dropna()

                if len(numeric_series) > 0:
                    col_info.total = float(numeric_series.sum())
                    col_info.min_value = float(numeric_series.min())
                    col_info.max_value = float(numeric_series.max())
                    col_info.avg_value = float(numeric_series.mean())
            except Exception as e:
                logger.debug(f"Could not calculate stats for {col_name}: {e}")

        return col_info

    def _detect_column_type(self, col_name: str, series: "pd.Series", sap_field: Optional[str]) -> ColumnType:
        """
        Detect the type of a column based on name, SAP field, and values.

        Args:
            col_name: Column name
            series: Pandas Series with column data
            sap_field: Extracted SAP field code (if any)

        Returns:
            ColumnType enum value
        """
        import pandas as pd

        col_lower = str(col_name).lower()
        sap_lower = (sap_field or "").lower()

        # Check for currency/amount indicators
        amount_indicators = ['amount', 'dmbtr', 'wrbtr', 'dmbe2', 'credit', 'debit', 'balance', 'total', 'sum']
        if any(ind in col_lower or ind in sap_lower for ind in amount_indicators):
            return ColumnType.CURRENCY

        # Check for count indicators
        count_indicators = ['count', 'counter', 'number of', 'qty', 'quantity', 'anzahl']
        if any(ind in col_lower or ind in sap_lower for ind in count_indicators):
            return ColumnType.COUNT

        # Check for percentage indicators
        if '%' in col_lower or 'percent' in col_lower or 'rate' in col_lower:
            return ColumnType.PERCENTAGE

        # Check for date indicators
        date_indicators = ['date', 'datum', 'erdat', 'budat', 'bldat', 'time', 'period']
        if any(ind in col_lower or ind in sap_lower for ind in date_indicators):
            return ColumnType.DATE

        # Check for identifier indicators
        id_indicators = ['id', 'code', 'key', 'bukrs', 'lifnr', 'kunnr', 'matnr', 'belnr', 'account', 'hkont']
        if any(ind in col_lower or ind in sap_lower for ind in id_indicators):
            return ColumnType.IDENTIFIER

        # Check for currency column (the currency code itself)
        if 'currency' in col_lower or 'waers' in sap_lower:
            return ColumnType.TEXT

        # Try to infer from data
        non_null = series.dropna()
        if len(non_null) > 0:
            # Check if numeric
            try:
                # Try converting first few values
                sample = non_null.head(20).astype(str).str.replace(',', '').str.replace('-', '')
                numeric_count = pd.to_numeric(sample, errors='coerce').notna().sum()
                if numeric_count / len(sample) > 0.8:
                    return ColumnType.NUMERIC
            except:
                pass

        return ColumnType.TEXT

    def _is_key_metric_column(self, col_name: str, sap_field: Optional[str], col_type: ColumnType) -> bool:
        """
        Determine if a column is a key metric that should be highlighted.

        Key metrics are typically:
        - Amount/currency columns
        - Balance columns
        - Credit/debit columns
        - Total columns
        """
        if col_type not in [ColumnType.CURRENCY, ColumnType.NUMERIC, ColumnType.COUNT]:
            return False

        col_lower = str(col_name).lower()
        sap_lower = (sap_field or "").lower()

        # Key metric SAP fields
        key_sap_fields = ['dmbtr', 'wrbtr', 'dmbe2', 'balance', 'amount', 'credit']
        if any(field in sap_lower for field in key_sap_fields):
            return True

        # Key metric name patterns
        key_patterns = ['amount', 'balance', 'credit', 'debit', 'total', 'sum']
        if any(pattern in col_lower for pattern in key_patterns):
            return True

        return False

    def _extract_sap_field(self, col_name: str) -> Optional[str]:
        """
        Extract SAP field code from column name.

        Examples:
            "Amount in LC (DMBTR)" -> "DMBTR"
            "Company Code (BUKRS)" -> "BUKRS"
            "Amount" -> None
        """
        match = re.search(r'\(([A-Z0-9_]+)\)\s*$', col_name)
        if match:
            return match.group(1)
        return None

    def _generate_raw_text(self, df: "pd.DataFrame", summary_data: SummaryData) -> str:
        """Generate raw text representation for backward compatibility."""
        lines = []
        lines.append(f"=== Summary Data ===")
        lines.append(f"Rows: {summary_data.row_count}, Columns: {summary_data.column_count}")

        # List columns with types
        lines.append("\nColumn Analysis:")
        for col in summary_data.columns:
            marker = "[KEY]" if col.is_key_metric else ""
            sap = f" ({col.sap_field})" if col.sap_field else ""
            stats = ""
            if col.total is not None:
                stats = f" | Total: {col.total:,.2f}"
            lines.append(f"  - {col.name}{sap}: {col.column_type.value}{marker}{stats}")

        # Key metrics summary
        if summary_data.total_amount is not None:
            currency = f" {summary_data.currency}" if summary_data.currency else ""
            lines.append(f"\nTotal Amount: {summary_data.total_amount:,.2f}{currency}")

        # Sample data
        lines.append("\nSample Data (first 10 rows):")
        lines.append(df.head(10).to_string())

        return "\n".join(lines)

    def _parse_metadata(self, metadata_content: Optional[str]) -> Dict[str, str]:
        """
        Parse metadata content to extract key parameters.

        Returns:
            Dictionary of parameter name -> value
        """
        if not metadata_content:
            return {}

        params = {}

        # Look for key-value patterns
        patterns = [
            r'(\w+)\s*[=:]\s*([^\n]+)',  # KEY = VALUE or KEY: VALUE
            r'"(\w+)"\s*:\s*"([^"]+)"',  # JSON-style "key": "value"
        ]

        for pattern in patterns:
            matches = re.findall(pattern, metadata_content)
            for key, value in matches:
                params[key.strip()] = value.strip()

        return params

    def find_artifacts_in_upload(
        self,
        uploaded_files: List[str],
        base_path: str
    ) -> List[AlertArtifacts]:
        """
        Find and group artifact files from an upload.

        Args:
            uploaded_files: List of uploaded filenames
            base_path: Base path where files are stored

        Returns:
            List of AlertArtifacts, one per alert
        """
        # Group files by alert
        alerts_map: Dict[str, Dict[str, str]] = {}

        for filename in uploaded_files:
            # Try to identify the artifact type and alert
            for prefix in self.ARTIFACT_PREFIXES:
                if filename.startswith(prefix):
                    # Extract alert identifier from filename
                    remainder = filename[len(prefix):]
                    # Remove file extension
                    alert_key = re.sub(r'\.(txt|csv|xlsx|pdf)$', '', remainder, flags=re.IGNORECASE)

                    if alert_key not in alerts_map:
                        alerts_map[alert_key] = {}

                    artifact_type = prefix.rstrip('_').lower()
                    alerts_map[alert_key][artifact_type] = os.path.join(base_path, filename)
                    break

        # Create AlertArtifacts for each alert
        artifacts_list = []
        for alert_key, files in alerts_map.items():
            # Parse alert_key to get ID and name
            parts = alert_key.split('_', 2)
            if len(parts) >= 2:
                alert_id = f"{parts[0]}_{parts[1]}" if parts[0].isdigit() else parts[0]
                alert_name = parts[2] if len(parts) > 2 else alert_key
            else:
                alert_id = alert_key
                alert_name = alert_key

            artifacts = self.read_from_files(
                alert_id=alert_id,
                alert_name=alert_name.replace('_', ' '),
                code_path=files.get('code'),
                explanation_path=files.get('explanation'),
                metadata_path=files.get('metadata'),
                summary_path=files.get('summary')
            )

            artifacts_list.append(artifacts)

        return artifacts_list
