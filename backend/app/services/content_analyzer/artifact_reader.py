"""
Artifact Reader for 4C Alerts

Parses the 4 artifact files associated with each alert:
- Code_* - ABAP function code
- Explanation_* - Human-readable description
- Metadata_* - Alert configuration/parameters
- Summary_* - Actual output data to analyze
"""

import os
import re
import logging
from typing import Dict, List, Optional, NamedTuple
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class AlertArtifacts:
    """Container for all artifacts of a single alert."""

    alert_id: str
    alert_name: str

    # The 4 artifact contents
    code: Optional[str] = None
    explanation: Optional[str] = None
    metadata: Optional[str] = None
    summary: Optional[str] = None

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

        # Extract alert info from directory name
        dir_name = os.path.basename(directory_path)
        alert_id, alert_name = self._parse_directory_name(dir_name)

        artifacts = AlertArtifacts(
            alert_id=alert_id,
            alert_name=alert_name
        )

        # Find and read each artifact type
        files = os.listdir(directory_path)

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

            elif filename_lower.startswith("metadata_"):
                artifacts.metadata = self._read_file(filepath)
                artifacts.metadata_path = filepath
                artifacts.parameters = self._parse_metadata(artifacts.metadata)

            elif filename_lower.startswith("summary_"):
                artifacts.summary = self._read_file(filepath)
                artifacts.summary_path = filepath

        return artifacts

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
        """Read file content with encoding handling."""
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
