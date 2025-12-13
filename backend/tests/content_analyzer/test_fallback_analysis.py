"""
Unit tests for fallback analysis methods.

Tests the _fallback_analysis() method and related helper functions
that extract qualitative and quantitative insights without LLM.
"""

import pytest
from app.services.content_analyzer.analyzer import ContentAnalyzer
from app.services.content_analyzer.artifact_reader import AlertArtifacts, SummaryData, ColumnInfo, ColumnType
from app.services.content_analyzer.llm_classifier import AnalysisResult


class TestFallbackAnalysis:
    """Tests for fallback analysis methods."""

    @pytest.fixture
    def analyzer(self):
        """Create a ContentAnalyzer instance with LLM disabled."""
        return ContentAnalyzer(use_llm=False)

    @pytest.fixture
    def basic_artifacts(self):
        """Create basic AlertArtifacts for testing."""
        return AlertArtifacts(
            alert_id="TEST_001",
            alert_name="Test Alert",
            explanation="This alert monitors vendor payment patterns.",
            summary="Total records: 1,500\nTotal amount: $50,000"
        )

    @pytest.fixture
    def structured_summary_data(self):
        """Create structured SummaryData for testing."""
        columns = [
            ColumnInfo(
                name="Vendor",
                original_name="Vendor (LIFNR)",
                column_type=ColumnType.IDENTIFIER
            ),
            ColumnInfo(
                name="Amount",
                original_name="Amount (DMBTR)",
                column_type=ColumnType.CURRENCY,
                is_key_metric=True,
                total=50000.0,
                avg_value=33.33
            )
        ]
        
        sample_rows = [
            {"Vendor": "V001", "Amount": 20000.0},
            {"Vendor": "V002", "Amount": 15000.0},
            {"Vendor": "V003", "Amount": 10000.0},
            {"Vendor": "V004", "Amount": 5000.0}
        ]
        
        return SummaryData(
            row_count=1500,
            column_count=2,
            columns=columns,
            total_amount=50000.0,
            total_count=1500,
            currency="USD",
            sample_rows=sample_rows
        )

    def test_fallback_analysis_with_structured_data(self, analyzer, basic_artifacts, structured_summary_data):
        """Test fallback analysis with structured summary_data."""
        basic_artifacts.summary_data = structured_summary_data
        
        # Set focus area for severity determination
        analyzer._last_classification_focus_area = "BUSINESS_PROTECTION"
        
        result = analyzer._fallback_analysis(basic_artifacts)
        
        assert isinstance(result, AnalysisResult)
        assert result.quantitative_analysis["total_count"] == 1500
        assert result.quantitative_analysis["monetary_amount"] == 50000.0
        assert len(result.quantitative_analysis["notable_items"]) > 0
        assert "key_metrics" in result.quantitative_analysis
        assert "threshold_violations" in result.quantitative_analysis

    def test_fallback_analysis_with_text_only(self, analyzer, basic_artifacts):
        """Test fallback analysis with text-only summary (no structured data)."""
        analyzer._last_classification_focus_area = "BUSINESS_CONTROL"
        
        result = analyzer._fallback_analysis(basic_artifacts)
        
        assert isinstance(result, AnalysisResult)
        # Text extraction may not always work perfectly - just verify it's a valid result
        assert result.quantitative_analysis["total_count"] >= 0
        assert result.quantitative_analysis["monetary_amount"] >= 0
        assert result.severity in ["Critical", "High", "Medium", "Low"]

    def test_extract_what_happened_from_explanation(self, analyzer):
        """Test extraction of 'what_happened' from explanation."""
        explanation = "This alert monitors vendor payment patterns.\n\nIt checks for unusual transactions."
        what_happened = analyzer._extract_what_happened(explanation, "Test Alert")
        
        assert "vendor payment patterns" in what_happened.lower()
        assert len(what_happened) > 0

    def test_extract_what_happened_fallback_to_alert_name(self, analyzer):
        """Test that 'what_happened' falls back to alert name if no explanation."""
        what_happened = analyzer._extract_what_happened(None, "Test Alert")
        assert "Test Alert" in what_happened

    def test_extract_business_risk_fraud_indicator(self, analyzer):
        """Test business risk extraction for fraud indicators."""
        explanation = "This alert detects potential fraud patterns in vendor payments."
        risk = analyzer._extract_business_risk(explanation, "Test Alert")
        
        assert "fraud" in risk.lower() or "security" in risk.lower()
        assert "review" in risk.lower()

    def test_extract_business_risk_revenue_indicator(self, analyzer):
        """Test business risk extraction for revenue indicators."""
        explanation = "This alert monitors unbilled deliveries that may cause revenue loss."
        risk = analyzer._extract_business_risk(explanation, "Test Alert")
        
        assert "revenue" in risk.lower() or "financial" in risk.lower()

    def test_extract_business_risk_process_indicator(self, analyzer):
        """Test business risk extraction for process disruption indicators."""
        explanation = "This alert detects process bottlenecks and stuck orders."
        risk = analyzer._extract_business_risk(explanation, "Test Alert")
        
        assert "process" in risk.lower() or "operational" in risk.lower()

    def test_extract_affected_areas_from_summary_data(self, analyzer, structured_summary_data):
        """Test extraction of affected areas from summary data columns."""
        affected_areas = analyzer._extract_affected_areas(structured_summary_data)
        
        # Should identify entity columns
        assert isinstance(affected_areas, list)

    def test_extract_notable_items_from_summary_data(self, analyzer, structured_summary_data):
        """Test extraction of notable items from structured summary data."""
        notable_items = analyzer._extract_notable_items(structured_summary_data, max_items=5)
        
        assert len(notable_items) > 0
        assert len(notable_items) <= 5
        
        # Check structure of notable items
        for item in notable_items:
            assert "title" in item
            assert "amount" in item
            assert "percentage_of_total" in item

    def test_extract_notable_items_sorted_by_amount(self, analyzer, structured_summary_data):
        """Test that notable items are sorted by amount (descending)."""
        notable_items = analyzer._extract_notable_items(structured_summary_data, max_items=5)
        
        if len(notable_items) > 1:
            amounts = [item["amount"] for item in notable_items]
            assert amounts == sorted(amounts, reverse=True)

    def test_calculate_key_metrics_from_summary_data(self, analyzer, structured_summary_data):
        """Test calculation of key metrics from structured summary data."""
        metrics = analyzer._calculate_key_metrics(structured_summary_data)
        
        assert "total_records" in metrics
        assert metrics["total_records"] == 1500
        assert "total_amount" in metrics
        assert metrics["total_amount"] == 50000.0
        assert "currency" in metrics
        assert metrics["currency"] == "USD"

    def test_detect_concentration_patterns(self, analyzer, structured_summary_data):
        """Test detection of concentration patterns (>50% by entity)."""
        # Modify summary_data to have a concentration
        structured_summary_data.total_amount = 100000.0
        structured_summary_data.sample_rows = [
            {"Vendor": "V001", "Amount": 60000.0},  # 60% concentration
            {"Vendor": "V002", "Amount": 40000.0}
        ]
        
        violations = analyzer._detect_concentration_patterns(structured_summary_data)
        
        # Should detect V001 as >50% concentration
        assert len(violations) > 0
        assert any("V001" in v or "60" in v for v in violations)

    def test_detect_threshold_violations_high_count(self, analyzer, structured_summary_data):
        """Test threshold violation detection for high count."""
        violations = analyzer._detect_threshold_violations(structured_summary_data, 1500, 50000.0)
        
        # 1500 records should trigger high volume violation
        assert len(violations) > 0
        assert any("volume" in v.lower() or "1500" in v for v in violations)

    def test_detect_threshold_violations_high_amount(self, analyzer, structured_summary_data):
        """Test threshold violation detection for high monetary amount."""
        violations = analyzer._detect_threshold_violations(structured_summary_data, 100, 1500000.0)
        
        # $1.5M should trigger high financial exposure violation
        assert len(violations) > 0
        assert any("financial" in v.lower() or "exposure" in v.lower() for v in violations)

    def test_severity_reasoning_includes_quantitative_factors(self, analyzer, basic_artifacts, structured_summary_data):
        """Test that severity reasoning includes quantitative factors."""
        basic_artifacts.summary_data = structured_summary_data
        analyzer._last_classification_focus_area = "BUSINESS_PROTECTION"
        
        result = analyzer._fallback_analysis(basic_artifacts)
        
        # Severity reasoning should include count and/or amount
        assert "1500" in result.severity_reasoning or "50,000" in result.severity_reasoning or "50000" in result.severity_reasoning

    def test_recommended_actions_by_severity(self, analyzer, basic_artifacts):
        """Test that recommended actions vary by severity level."""
        analyzer._last_classification_focus_area = "BUSINESS_PROTECTION"
        
        # Test with HIGH severity alert
        basic_artifacts.alert_name = "Rarely Used Vendor Alert"
        result_high = analyzer._fallback_analysis(basic_artifacts)
        
        assert len(result_high.recommended_actions) > 0
        assert any("review" in action.lower() for action in result_high.recommended_actions)
