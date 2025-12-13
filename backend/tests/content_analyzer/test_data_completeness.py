"""
Unit tests for data completeness validation.

Tests the _validate_content_finding() method and validation rules
for AlertInstance, AlertAnalysis, and CriticalDiscovery creation.
"""

import pytest
from app.services.content_analyzer.analyzer import ContentAnalyzer, ContentFinding


class TestDataCompletenessValidation:
    """Tests for data completeness validation."""

    @pytest.fixture
    def analyzer(self):
        """Create a ContentAnalyzer instance."""
        return ContentAnalyzer(use_llm=False)

    @pytest.fixture
    def valid_finding(self):
        """Create a valid ContentFinding for testing."""
        return ContentFinding(
            alert_id="TEST_001",
            alert_name="Test Alert",
            focus_area="BUSINESS_PROTECTION",
            focus_area_confidence=0.9,
            classification_reasoning="Pattern match",
            title="Test Finding",
            description="Test description",
            business_impact="Test business impact",
            what_happened="Test event",
            business_risk="Test risk",
            affected_areas=["Area1"],
            total_count=100,
            monetary_amount=1000.0,
            currency="USD",
            key_metrics={},
            notable_items=[{"title": "Item1", "amount": 1000.0}],
            severity="High",
            severity_reasoning="Test reasoning",
            risk_score=75,
            risk_level="High",
            risk_factors=["Factor1"],
            money_loss_estimate=500.0,
            money_loss_confidence=0.7,
            recommended_actions=["Action1"]
        )

    def test_validation_passes_for_valid_finding(self, analyzer, valid_finding):
        """Test that validation passes for a valid ContentFinding."""
        is_valid, warnings = analyzer._validate_content_finding(valid_finding)
        
        assert is_valid is True
        assert len(warnings) == 0

    def test_validation_fails_missing_alert_id(self, analyzer, valid_finding):
        """Test that validation fails when alert_id is missing."""
        valid_finding.alert_id = ""
        is_valid, warnings = analyzer._validate_content_finding(valid_finding)
        
        assert is_valid is False
        assert any("alert_id" in w.lower() for w in warnings)

    def test_validation_fails_missing_alert_name(self, analyzer, valid_finding):
        """Test that validation fails when alert_name is missing."""
        valid_finding.alert_name = ""
        is_valid, warnings = analyzer._validate_content_finding(valid_finding)
        
        assert is_valid is False
        assert any("alert_name" in w.lower() for w in warnings)

    def test_validation_fails_missing_focus_area(self, analyzer, valid_finding):
        """Test that validation fails when focus_area is missing."""
        valid_finding.focus_area = ""
        is_valid, warnings = analyzer._validate_content_finding(valid_finding)
        
        assert is_valid is False
        assert any("focus_area" in w.lower() for w in warnings)

    def test_validation_fails_missing_severity(self, analyzer, valid_finding):
        """Test that validation fails when severity is missing."""
        valid_finding.severity = ""
        is_valid, warnings = analyzer._validate_content_finding(valid_finding)
        
        assert is_valid is False
        assert any("severity" in w.lower() for w in warnings)

    def test_validation_fails_missing_risk_score(self, analyzer, valid_finding):
        """Test that validation fails when risk_score is missing."""
        valid_finding.risk_score = None
        is_valid, warnings = analyzer._validate_content_finding(valid_finding)
        
        assert is_valid is False
        assert any("risk_score" in w.lower() for w in warnings)

    def test_validation_fails_negative_total_count(self, analyzer, valid_finding):
        """Test that validation fails when total_count is negative."""
        valid_finding.total_count = -10
        is_valid, warnings = analyzer._validate_content_finding(valid_finding)
        
        assert is_valid is False
        assert any("negative" in w.lower() or "total_count" in w.lower() for w in warnings)

    def test_validation_fails_invalid_severity(self, analyzer, valid_finding):
        """Test that validation fails when severity is invalid."""
        valid_finding.severity = "INVALID"
        is_valid, warnings = analyzer._validate_content_finding(valid_finding)
        
        assert is_valid is False
        assert any("invalid" in w.lower() and "severity" in w.lower() for w in warnings)

    def test_validation_fails_risk_score_out_of_range(self, analyzer, valid_finding):
        """Test that validation fails when risk_score is out of range."""
        valid_finding.risk_score = 150  # > 100
        is_valid, warnings = analyzer._validate_content_finding(valid_finding)
        
        assert is_valid is False
        assert any("range" in w.lower() or "100" in w for w in warnings)

    def test_validation_warns_no_notable_items_or_description(self, analyzer, valid_finding):
        """Test that validation warns when no notable_items or description available."""
        valid_finding.notable_items = []
        valid_finding.description = ""
        valid_finding.business_impact = ""
        valid_finding.title = ""
        
        is_valid, warnings = analyzer._validate_content_finding(valid_finding)
        
        assert any("notable_items" in w.lower() or "description" in w.lower() for w in warnings)

    def test_validation_passes_with_description_only(self, analyzer, valid_finding):
        """Test that validation passes with description even without notable_items."""
        valid_finding.notable_items = []
        valid_finding.description = "Test description"
        
        is_valid, warnings = analyzer._validate_content_finding(valid_finding)
        
        # Should pass because description is available
        assert not any("notable_items" in w.lower() and "description" in w.lower() for w in warnings)

    def test_validation_passes_with_notable_items_only(self, analyzer, valid_finding):
        """Test that validation passes with notable_items even without description."""
        valid_finding.description = ""
        valid_finding.business_impact = ""
        valid_finding.title = ""
        valid_finding.notable_items = [{"title": "Item1"}]
        
        is_valid, warnings = analyzer._validate_content_finding(valid_finding)
        
        # Should pass because notable_items are available
        assert not any("notable_items" in w.lower() and "description" in w.lower() for w in warnings)

    def test_validation_handles_business_purpose_derivation(self, analyzer, valid_finding):
        """Test that validation checks business_purpose can be derived."""
        # Remove all sources of business_purpose
        valid_finding.business_impact = ""
        valid_finding.description = ""
        valid_finding.alert_name = ""
        
        is_valid, warnings = analyzer._validate_content_finding(valid_finding)
        
        # Should warn about business_purpose
        assert any("business_purpose" in w.lower() for w in warnings)
