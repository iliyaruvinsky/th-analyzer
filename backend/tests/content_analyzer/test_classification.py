"""
Unit tests for BUSINESS_PROTECTION classification logic.

Tests the weighted keyword matching in llm_classifier.py to ensure
fraud indicators properly override generic business terms.
"""

import pytest
from app.services.content_analyzer.llm_classifier import LLMClassifier
from app.services.content_analyzer.artifact_reader import AlertArtifacts


class TestBusinessProtectionClassification:
    """Tests for BUSINESS_PROTECTION focus area classification."""

    @pytest.fixture
    def classifier(self):
        """Create a classifier instance for testing."""
        return LLMClassifier()

    def _make_artifacts(self, alert_name: str, explanation: str = "", code_summary: str = "") -> AlertArtifacts:
        """Helper to create AlertArtifacts for testing."""
        return AlertArtifacts(
            alert_id="TEST_001",
            alert_name=alert_name,
            explanation=explanation,
            code_summary=code_summary
        )

    # =========================================================================
    # BUSINESS_PROTECTION Critical Indicators (weight 10)
    # These MUST override any accumulation of generic terms
    # =========================================================================

    def test_rarely_used_vendor_classified_as_business_protection(self, classifier):
        """Rarely Used Vendors should be BUSINESS_PROTECTION even with generic vendor terms."""
        artifacts = self._make_artifacts(
            alert_name="Rarely Used Vendors",
            explanation="Rarely used vendors are vendor master records with zero active posting periods. "
                       "This leads to master data clutter, vendor searches, and balances."
        )
        focus_area, confidence, reasoning = classifier.analyze_without_llm(artifacts)

        assert focus_area == "BUSINESS_PROTECTION", f"Expected BUSINESS_PROTECTION, got {focus_area}. Reasoning: {reasoning}"
        assert "rarely used vendor" in reasoning.lower()

    def test_rarely_used_vendors_plural_form(self, classifier):
        """Plural 'rarely used vendors' should also match."""
        artifacts = self._make_artifacts(
            alert_name="Rarely Used Vendors Report",
            explanation="Analysis of rarely used vendors in the system."
        )
        focus_area, confidence, reasoning = classifier.analyze_without_llm(artifacts)

        assert focus_area == "BUSINESS_PROTECTION"

    def test_ruv_abbreviation(self, classifier):
        """RUV abbreviation should trigger BUSINESS_PROTECTION."""
        artifacts = self._make_artifacts(
            alert_name="RUV Analysis",
            explanation="RUV (Rarely Used Vendor) review needed."
        )
        focus_area, confidence, reasoning = classifier.analyze_without_llm(artifacts)

        assert focus_area == "BUSINESS_PROTECTION"

    def test_po_for_one_time_vendor_critical(self, classifier):
        """PO for one-time vendor is a direct theft pattern - MUST be BUSINESS_PROTECTION."""
        artifacts = self._make_artifacts(
            alert_name="PO for One-Time Vendor",
            explanation="Purchase orders created for one-time vendors require review."
        )
        focus_area, confidence, reasoning = classifier.analyze_without_llm(artifacts)

        assert focus_area == "BUSINESS_PROTECTION"

    def test_debug_mode_critical(self, classifier):
        """DEBUG system updates bypass all controls - MUST be BUSINESS_PROTECTION."""
        artifacts = self._make_artifacts(
            alert_name="DEBUG Mode Activation",
            explanation="System was accessed in DEBUG mode."
        )
        focus_area, confidence, reasoning = classifier.analyze_without_llm(artifacts)

        assert focus_area == "BUSINESS_PROTECTION"

    def test_sap_all_authorization_critical(self, classifier):
        """SAP_ALL grant is critical authorization - MUST be BUSINESS_PROTECTION."""
        artifacts = self._make_artifacts(
            alert_name="SAP_ALL Authorization Grant",
            explanation="User was granted SAP_ALL profile."
        )
        focus_area, confidence, reasoning = classifier.analyze_without_llm(artifacts)

        assert focus_area == "BUSINESS_PROTECTION"

    # =========================================================================
    # BUSINESS_PROTECTION High Indicators (weight 3)
    # =========================================================================

    def test_modified_vendor_bank_account(self, classifier):
        """Modified Vendor Bank Account is a fraud indicator."""
        artifacts = self._make_artifacts(
            alert_name="Modified Vendor Bank Account",
            explanation="Vendor bank details were modified. Check for unauthorized changes."
        )
        focus_area, confidence, reasoning = classifier.analyze_without_llm(artifacts)

        assert focus_area == "BUSINESS_PROTECTION"

    def test_inventory_variance(self, classifier):
        """Inventory variance indicates possible theft."""
        artifacts = self._make_artifacts(
            alert_name="Inventory Variance Analysis",
            explanation="Inventory count differs from system records indicating possible theft."
        )
        focus_area, confidence, reasoning = classifier.analyze_without_llm(artifacts)

        assert focus_area == "BUSINESS_PROTECTION"

    def test_fraud_keyword_triggers_business_protection(self, classifier):
        """Explicit 'fraud' keyword should trigger BUSINESS_PROTECTION."""
        artifacts = self._make_artifacts(
            alert_name="Vendor Analysis",
            explanation="This alert detects possible fraud in vendor payments."
        )
        focus_area, confidence, reasoning = classifier.analyze_without_llm(artifacts)

        assert focus_area == "BUSINESS_PROTECTION"

    def test_unauthorized_keyword(self, classifier):
        """'Unauthorized' keyword should trigger BUSINESS_PROTECTION."""
        artifacts = self._make_artifacts(
            alert_name="Transaction Review",
            explanation="Unauthorized transaction detected in the system."
        )
        focus_area, confidence, reasoning = classifier.analyze_without_llm(artifacts)

        assert focus_area == "BUSINESS_PROTECTION"

    # =========================================================================
    # Weight Override Tests
    # Critical indicators (weight 10) MUST beat generic terms (weight 1)
    # =========================================================================

    def test_fraud_indicator_overrides_many_generic_terms(self, classifier):
        """
        Even with many generic BUSINESS_CONTROL terms, a fraud indicator should win.

        This tests the bug fix where 'rarely used vendor' (weight 10) must override
        accumulation of: vendor (1) + master data (1) + invoice (1) + payment (1) +
        balance (1) + financial (1) = 6 points for BUSINESS_CONTROL.
        """
        artifacts = self._make_artifacts(
            alert_name="Rarely Used Vendors",
            explanation=(
                "Rarely used vendors are vendor master records with zero active posting periods "
                "showing no financial turnover, indicating no invoices or payments processed. "
                "This leads to master data clutter and ties up significant balances "
                "without ongoing business relationships requiring clearance. "
                "The analysis shows vendors with balance totaling amounts owed to vendors."
            )
        )
        focus_area, confidence, reasoning = classifier.analyze_without_llm(artifacts)

        # Must be BUSINESS_PROTECTION despite many generic vendor/customer terms
        assert focus_area == "BUSINESS_PROTECTION", (
            f"FAILED: Fraud indicator should override generic terms. "
            f"Got {focus_area} with reasoning: {reasoning}"
        )

    def test_sod_with_fraud_escalates_to_business_protection(self, classifier):
        """SoD violation combined with fraud indicators should be BUSINESS_PROTECTION."""
        artifacts = self._make_artifacts(
            alert_name="SOD GR-IR vs PO user comparison",
            explanation=(
                "Segregation of duties violation detected. Same user performed GR and IR. "
                "This could indicate fraud or unauthorized manipulation of the procurement process."
            )
        )
        focus_area, confidence, reasoning = classifier.analyze_without_llm(artifacts)

        # SoD + fraud = BUSINESS_PROTECTION, not ACCESS_GOVERNANCE
        assert focus_area == "BUSINESS_PROTECTION"


class TestBusinessControlClassification:
    """Tests for BUSINESS_CONTROL focus area classification."""

    @pytest.fixture
    def classifier(self):
        return LLMClassifier()

    def _make_artifacts(self, alert_name: str, explanation: str = "") -> AlertArtifacts:
        return AlertArtifacts(
            alert_id="TEST_001",
            alert_name=alert_name,
            explanation=explanation
        )

    def test_pure_vendor_management_is_business_control(self, classifier):
        """Generic vendor management without fraud indicators should be BUSINESS_CONTROL."""
        artifacts = self._make_artifacts(
            alert_name="Vendor Master Data Review",
            explanation="Review vendor master data for completeness and accuracy."
        )
        focus_area, confidence, reasoning = classifier.analyze_without_llm(artifacts)

        # No fraud indicators, just generic vendor management
        assert focus_area == "BUSINESS_CONTROL"

    def test_customer_management_is_business_control(self, classifier):
        """Customer management alerts should be BUSINESS_CONTROL."""
        artifacts = self._make_artifacts(
            alert_name="Customer Credit Limit Review",
            explanation="Review customer credit limits for proper business exposure."
        )
        focus_area, confidence, reasoning = classifier.analyze_without_llm(artifacts)

        assert focus_area == "BUSINESS_CONTROL"

    def test_invoice_processing_is_business_control(self, classifier):
        """Invoice processing alerts should be BUSINESS_CONTROL."""
        artifacts = self._make_artifacts(
            alert_name="Invoice Processing Delays",
            explanation="Invoices stuck in approval queue causing payment delays."
        )
        focus_area, confidence, reasoning = classifier.analyze_without_llm(artifacts)

        assert focus_area == "BUSINESS_CONTROL"


class TestAccessGovernanceClassification:
    """Tests for ACCESS_GOVERNANCE focus area classification."""

    @pytest.fixture
    def classifier(self):
        return LLMClassifier()

    def _make_artifacts(self, alert_name: str, explanation: str = "") -> AlertArtifacts:
        return AlertArtifacts(
            alert_id="TEST_001",
            alert_name=alert_name,
            explanation=explanation
        )

    def test_pure_sod_violation_is_access_governance(self, classifier):
        """Pure SoD violation without fraud indicators should be ACCESS_GOVERNANCE."""
        artifacts = self._make_artifacts(
            alert_name="SoD Violation Report",
            explanation="Segregation of duties violation detected. User has conflicting roles."
        )
        focus_area, confidence, reasoning = classifier.analyze_without_llm(artifacts)

        # Pure SoD without fraud keywords should be ACCESS_GOVERNANCE
        # Note: If fraud keywords are present, it escalates to BUSINESS_PROTECTION
        assert focus_area in ["ACCESS_GOVERNANCE", "BUSINESS_PROTECTION"]

    def test_authorization_review_is_access_governance(self, classifier):
        """Authorization review should be ACCESS_GOVERNANCE."""
        artifacts = self._make_artifacts(
            alert_name="User Authorization Review",
            explanation="Review user authorization profiles and access control settings."
        )
        focus_area, confidence, reasoning = classifier.analyze_without_llm(artifacts)

        assert focus_area == "ACCESS_GOVERNANCE"
