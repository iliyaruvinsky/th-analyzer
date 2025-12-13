"""
Integration tests for the complete standalone analysis pipeline.

Tests the full flow: artifacts → analysis → ContentFinding
for both BUSINESS_PROTECTION and BUSINESS_CONTROL focus areas.
"""

import pytest
from app.services.content_analyzer.analyzer import ContentAnalyzer
from app.services.content_analyzer.artifact_reader import AlertArtifacts, SummaryData, ColumnInfo, ColumnType


class TestStandalonePipelineIntegration:
    """Integration tests for standalone analysis pipeline."""

    @pytest.fixture
    def analyzer(self):
        """Create a ContentAnalyzer instance with LLM disabled."""
        return ContentAnalyzer(use_llm=False)

    @pytest.fixture
    def business_protection_artifacts(self):
        """Create BUSINESS_PROTECTION alert artifacts."""
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
                total=100000.0
            )
        ]
        
        summary_data = SummaryData(
            row_count=50,
            column_count=2,
            columns=columns,
            total_amount=100000.0,
            total_count=50,
            currency="USD",
            sample_rows=[
                {"Vendor": "V001", "Amount": 50000.0},
                {"Vendor": "V002", "Amount": 30000.0}
            ]
        )
        
        return AlertArtifacts(
            alert_id="RUV_001",
            alert_name="Rarely Used Vendors",
            explanation="This alert identifies vendors that have been inactive for extended periods.",
            summary="Total vendors: 50\nTotal amount: $100,000",
            summary_data=summary_data,
            metadata="BACKDAYS=365",
            parameters={"BACKDAYS": "365"}
        )

    @pytest.fixture
    def business_control_artifacts(self):
        """Create BUSINESS_CONTROL alert artifacts."""
        columns = [
            ColumnInfo(
                name="Order",
                original_name="Order (VBELN)",
                column_type=ColumnType.IDENTIFIER
            ),
            ColumnInfo(
                name="Amount",
                original_name="Amount (NETWR)",
                column_type=ColumnType.CURRENCY,
                is_key_metric=True,
                total=50000.0
            )
        ]
        
        summary_data = SummaryData(
            row_count=25,
            column_count=2,
            columns=columns,
            total_amount=50000.0,
            total_count=25,
            currency="USD",
            sample_rows=[
                {"Order": "ORD001", "Amount": 20000.0},
                {"Order": "ORD002", "Amount": 15000.0}
            ]
        )
        
        return AlertArtifacts(
            alert_id="UBD_001",
            alert_name="Unbilled Delivery Alert",
            explanation="This alert monitors deliveries that have been shipped but not invoiced.",
            summary="Total orders: 25\nTotal amount: $50,000",
            summary_data=summary_data,
            metadata="BACKDAYS=30",
            parameters={"BACKDAYS": "30"}
        )

    def test_business_protection_end_to_end(self, analyzer, business_protection_artifacts):
        """Test complete analysis pipeline for BUSINESS_PROTECTION alert."""
        # Analyze alert
        content_finding = analyzer.analyze_alert(business_protection_artifacts, include_raw=False)
        
        # Validate ContentFinding structure
        assert content_finding.alert_id == "RUV_001"
        assert content_finding.focus_area == "BUSINESS_PROTECTION"
        assert content_finding.severity == "High"  # Rarely Used Vendors should be HIGH
        assert content_finding.risk_score is not None
        assert 0 <= content_finding.risk_score <= 100
        assert content_finding.total_count == 50
        assert content_finding.monetary_amount == 100000.0
        assert len(content_finding.notable_items) > 0
        
        # Validate qualitative analysis
        assert content_finding.what_happened is not None
        assert len(content_finding.what_happened) > 0
        assert content_finding.business_risk is not None
        assert len(content_finding.business_risk) > 0
        
        # Validate quantitative analysis (ContentFinding has flat structure, not nested)
        assert content_finding.total_count >= 0
        assert content_finding.monetary_amount >= 0
        assert len(content_finding.notable_items) >= 0
        
        # Validate severity reasoning includes quantitative factors or they're in risk_factors
        has_quantitative_in_reasoning = "50" in content_finding.severity_reasoning or "100,000" in content_finding.severity_reasoning or "100" in content_finding.severity_reasoning
        has_quantitative_in_risk_factors = any("50" in str(f) or "100,000" in str(f) or "100" in str(f) for f in content_finding.risk_factors)
        assert has_quantitative_in_reasoning or has_quantitative_in_risk_factors
        
        # Validate data completeness
        is_valid, warnings = analyzer._validate_content_finding(content_finding)
        assert is_valid is True, f"Validation failed: {warnings}"

    def test_business_control_end_to_end(self, analyzer, business_control_artifacts):
        """Test complete analysis pipeline for BUSINESS_CONTROL alert."""
        # Analyze alert
        content_finding = analyzer.analyze_alert(business_control_artifacts, include_raw=False)
        
        # Validate ContentFinding structure
        assert content_finding.alert_id == "UBD_001"
        assert content_finding.focus_area == "BUSINESS_CONTROL"
        assert content_finding.severity == "High"  # Unbilled Delivery should be HIGH
        assert content_finding.risk_score is not None
        assert 0 <= content_finding.risk_score <= 100
        assert content_finding.total_count == 25
        assert content_finding.monetary_amount == 50000.0
        
        # Validate qualitative analysis
        assert content_finding.what_happened is not None
        what_happened_lower = content_finding.what_happened.lower()
        assert "unbilled" in what_happened_lower or \
               "delivery" in what_happened_lower or \
               "deliveries" in what_happened_lower
        assert content_finding.business_risk is not None
        
        # Validate severity reasoning
        assert "unbilled" in content_finding.severity_reasoning.lower() or \
               "high" in content_finding.severity_reasoning.lower()
        
        # Validate data completeness
        is_valid, warnings = analyzer._validate_content_finding(content_finding)
        assert is_valid is True, f"Validation failed: {warnings}"

    def test_pipeline_handles_missing_artifacts(self, analyzer):
        """Test that pipeline handles incomplete artifacts gracefully."""
        # Create artifacts with only alert name (minimal data)
        artifacts = AlertArtifacts(
            alert_id="MINIMAL_001",
            alert_name="Minimal Alert",
            explanation=None,
            summary=None,
            summary_data=None
        )
        
        # Should still produce a valid ContentFinding
        content_finding = analyzer.analyze_alert(artifacts, include_raw=False)
        
        assert content_finding.alert_id == "MINIMAL_001"
        assert content_finding.focus_area is not None
        assert content_finding.severity is not None
        assert content_finding.risk_score is not None
        
        # Should have default values for missing data
        assert content_finding.total_count >= 0
        assert content_finding.monetary_amount >= 0

    def test_pipeline_creates_notable_items_when_available(self, analyzer, business_protection_artifacts):
        """Test that pipeline creates notable items from structured data."""
        content_finding = analyzer.analyze_alert(business_protection_artifacts, include_raw=False)
        
        # Should have notable items from summary_data
        assert len(content_finding.notable_items) > 0
        
        # Notable items should be sorted by amount
        amounts = [item.get("amount", 0) for item in content_finding.notable_items]
        assert amounts == sorted(amounts, reverse=True)

    def test_pipeline_validates_data_completeness(self, analyzer, business_protection_artifacts):
        """Test that pipeline validates data completeness."""
        content_finding = analyzer.analyze_alert(business_protection_artifacts, include_raw=False)
        
        # Validation should pass for complete finding
        is_valid, warnings = analyzer._validate_content_finding(content_finding)
        assert is_valid is True, f"Validation failed: {warnings}"
        
        # All required fields should be populated
        assert content_finding.alert_id is not None
        assert content_finding.alert_name is not None
        assert content_finding.focus_area is not None
        assert content_finding.severity is not None
        assert content_finding.risk_score is not None
        assert content_finding.total_count is not None

    def test_pipeline_uses_severity_mapping_for_business_protection(self, analyzer, business_protection_artifacts):
        """Test that BUSINESS_PROTECTION severity mapping is applied."""
        content_finding = analyzer.analyze_alert(business_protection_artifacts, include_raw=False)
        
        # Rarely Used Vendors should map to HIGH severity
        assert content_finding.severity == "High"
        assert "rarely used vendor" in content_finding.severity_reasoning.lower() or \
               "high" in content_finding.severity_reasoning.lower()

    def test_pipeline_uses_severity_mapping_for_business_control(self, analyzer, business_control_artifacts):
        """Test that BUSINESS_CONTROL severity mapping is applied."""
        content_finding = analyzer.analyze_alert(business_control_artifacts, include_raw=False)
        
        # Unbilled Delivery should map to HIGH severity
        assert content_finding.severity == "High"
        assert "unbilled" in content_finding.severity_reasoning.lower() or \
               "high" in content_finding.severity_reasoning.lower()
