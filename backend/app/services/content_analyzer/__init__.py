"""
Content Analyzer Module for Treasure Hunt Analyzer (THA)

This module provides intelligent content analysis for 4C alerts and SoDA reports.
It reads contextual documents, classifies findings into focus areas, and scores
them using both qualitative and quantitative metrics.

Key Components:
- ContentAnalyzer: Main orchestrator for analysis
- ContextLoader: Loads TH principles from documentation
- ArtifactReader: Parses the 4 alert artifacts (Code, Explanation, Metadata, Summary)
- LLMClassifier: LLM-based focus area classification
- ScoringEngine: Qualitative and quantitative scoring
- ReportGenerator: Generates markdown reports (summary/full)
"""

from .analyzer import ContentAnalyzer, create_content_analyzer
from .context_loader import ContextLoader, get_context_loader
from .artifact_reader import (
    ArtifactReader,
    AlertArtifacts,
    ColumnType,
    ColumnInfo,
    SummaryData,
)
from .llm_classifier import LLMClassifier
from .scoring_engine import ScoringEngine
from .report_generator import ReportGenerator

__all__ = [
    "ContentAnalyzer",
    "create_content_analyzer",
    "ContextLoader",
    "get_context_loader",
    "ArtifactReader",
    "AlertArtifacts",
    "ColumnType",
    "ColumnInfo",
    "SummaryData",
    "LLMClassifier",
    "ScoringEngine",
    "ReportGenerator",
]
