"""
Context Loader for Treasure Hunt Analyzer

Loads and caches TH principles and domain knowledge from documentation.
This provides the foundational context for the LLM classifier.
"""

import os
import logging
from typing import Dict, List, Optional
from pathlib import Path
from functools import lru_cache

logger = logging.getLogger(__name__)


class ContextLoader:
    """
    Loads TH principles and domain knowledge from documentation files.

    Context sources:
    - docs/th-context/readmore/ - Focus area detailed explanations
    - docs/product-docs/ - Product documentation
    - docs/case-studies/ - Real-world examples and case studies
    """

    # Base paths relative to project root
    TH_CONTEXT_PATH = "docs/th-context/readmore"
    PRODUCT_DOCS_PATH = "docs/product-docs"
    CASE_STUDIES_PATH = "docs/case-studies"

    # Focus area mapping to documentation files
    FOCUS_AREA_DOCS = {
        "BUSINESS_PROTECTION": "ReadMore_BusinessProtection.md",
        "BUSINESS_CONTROL": "ReadMore_BusinessControl.md",
        "ACCESS_GOVERNANCE": "ReadMore_AccessGovernance.md",
        "TECHNICAL_CONTROL": "ReadMore_TechnicalControl.md",
        "JOBS_CONTROL": "ReadMore_JobsControl.md",
        "S4HANA_EXCELLENCE": "ReadMore_S4HANAExcellence.md",
    }

    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize the context loader.

        Args:
            base_path: Base path to the project root. If None, attempts to auto-detect.
        """
        self.base_path = base_path or self._detect_base_path()
        self._context_cache: Dict[str, str] = {}
        self._loaded = False

    def _detect_base_path(self) -> str:
        """Auto-detect the project base path."""
        # Try common locations
        possible_paths = [
            "/app",  # Docker container
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))),
            os.getcwd(),
        ]

        for path in possible_paths:
            if os.path.exists(os.path.join(path, "docs", "th-context")):
                return path

        logger.warning("Could not auto-detect base path, using /app")
        return "/app"

    def load_all_context(self) -> Dict[str, str]:
        """
        Load all context documents into memory.

        Returns:
            Dictionary of context_name -> content
        """
        if self._loaded:
            return self._context_cache

        logger.info("Loading TH context documents...")

        # Load focus area documentation
        self._load_focus_area_docs()

        # Load product documentation
        self._load_product_docs()

        # Load case studies (selective - only text files)
        self._load_case_studies()

        self._loaded = True
        logger.info(f"Loaded {len(self._context_cache)} context documents")

        return self._context_cache

    def _load_focus_area_docs(self):
        """Load focus area documentation from th-context/readmore/"""
        th_context_dir = os.path.join(self.base_path, self.TH_CONTEXT_PATH)

        if not os.path.exists(th_context_dir):
            logger.warning(f"TH context directory not found: {th_context_dir}")
            return

        for focus_area, filename in self.FOCUS_AREA_DOCS.items():
            filepath = os.path.join(th_context_dir, filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self._context_cache[f"focus_area_{focus_area}"] = content
                    logger.debug(f"Loaded focus area doc: {focus_area}")
                except Exception as e:
                    logger.error(f"Error loading {filepath}: {e}")

    def _load_product_docs(self):
        """Load product documentation."""
        product_docs_dir = os.path.join(self.base_path, self.PRODUCT_DOCS_PATH)

        if not os.path.exists(product_docs_dir):
            logger.warning(f"Product docs directory not found: {product_docs_dir}")
            return

        for filename in os.listdir(product_docs_dir):
            if filename.endswith('.md'):
                filepath = os.path.join(product_docs_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    doc_name = filename.replace('.md', '').replace(' ', '_').lower()
                    self._context_cache[f"product_doc_{doc_name}"] = content
                    logger.debug(f"Loaded product doc: {filename}")
                except Exception as e:
                    logger.error(f"Error loading {filepath}: {e}")

    def _load_case_studies(self):
        """Load relevant case studies (text files only)."""
        case_studies_dir = os.path.join(self.base_path, self.CASE_STUDIES_PATH)

        if not os.path.exists(case_studies_dir):
            logger.warning(f"Case studies directory not found: {case_studies_dir}")
            return

        # Walk through case studies directory
        for root, dirs, files in os.walk(case_studies_dir):
            for filename in files:
                if filename.endswith(('.txt', '.md')):
                    filepath = os.path.join(root, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()

                        # Only load if content is reasonable size (< 50KB)
                        if len(content) < 50000:
                            relative_path = os.path.relpath(filepath, case_studies_dir)
                            doc_name = relative_path.replace(os.sep, '_').replace(' ', '_').lower()
                            doc_name = doc_name.replace('.txt', '').replace('.md', '')
                            self._context_cache[f"case_study_{doc_name}"] = content
                            logger.debug(f"Loaded case study: {filename}")
                    except Exception as e:
                        logger.error(f"Error loading {filepath}: {e}")

    def get_focus_area_context(self, focus_area: str) -> Optional[str]:
        """
        Get the context document for a specific focus area.

        Args:
            focus_area: The focus area code (e.g., "BUSINESS_PROTECTION")

        Returns:
            The content of the focus area documentation, or None if not found
        """
        if not self._loaded:
            self.load_all_context()

        return self._context_cache.get(f"focus_area_{focus_area}")

    def get_all_focus_area_contexts(self) -> Dict[str, str]:
        """
        Get all focus area context documents.

        Returns:
            Dictionary mapping focus_area_code -> content
        """
        if not self._loaded:
            self.load_all_context()

        return {
            key.replace("focus_area_", ""): value
            for key, value in self._context_cache.items()
            if key.startswith("focus_area_")
        }

    def get_combined_context_summary(self, max_length: int = 4000) -> str:
        """
        Get a combined summary of all context for use in LLM prompts.

        Args:
            max_length: Maximum length of the summary

        Returns:
            Combined context summary string
        """
        if not self._loaded:
            self.load_all_context()

        summaries = []

        # Add focus area summaries
        for focus_area in ["BUSINESS_PROTECTION", "BUSINESS_CONTROL", "ACCESS_GOVERNANCE",
                          "TECHNICAL_CONTROL", "JOBS_CONTROL"]:
            content = self.get_focus_area_context(focus_area)
            if content:
                # Extract just the first paragraph (summary)
                lines = content.split('\n')
                summary_lines = []
                for line in lines[1:]:  # Skip title
                    if line.strip() and not line.startswith('#'):
                        summary_lines.append(line.strip())
                        if len(summary_lines) >= 2:
                            break
                summaries.append(f"**{focus_area}**: {' '.join(summary_lines)}")

        result = "\n\n".join(summaries)

        if len(result) > max_length:
            result = result[:max_length] + "..."

        return result

    def clear_cache(self):
        """Clear the context cache to force reload."""
        self._context_cache.clear()
        self._loaded = False


# Global cached instance
_context_loader_instance: Optional[ContextLoader] = None


def get_context_loader(base_path: Optional[str] = None) -> ContextLoader:
    """
    Get the global context loader instance.

    Args:
        base_path: Optional base path override

    Returns:
        ContextLoader instance
    """
    global _context_loader_instance

    if _context_loader_instance is None:
        _context_loader_instance = ContextLoader(base_path)

    return _context_loader_instance
