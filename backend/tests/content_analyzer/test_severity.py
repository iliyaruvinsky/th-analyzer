"""
Unit tests for BUSINESS_PROTECTION severity determination.

Tests the alert-type to severity mapping in scoring_engine.py.
"""

import pytest
from app.services.content_analyzer.scoring_engine import ScoringEngine, SeverityLevel


class TestBusinessProtectionSeverity:
    """Tests for BUSINESS_PROTECTION severity determination."""

    @pytest.fixture
    def scoring_engine(self):
        """Create a scoring engine instance for testing."""
        return ScoringEngine()

    # =========================================================================
    # CRITICAL Severity (Base Score: 90)
    # Cybersecurity breach, direct theft mechanism, full access grant
    # =========================================================================

    def test_debug_mode_is_critical(self, scoring_engine):
        """DEBUG system updates bypass all controls - CRITICAL."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="DEBUG Mode Activation",
            focus_area="BUSINESS_PROTECTION",
            explanation="System was accessed in DEBUG mode."
        )
        assert severity == SeverityLevel.CRITICAL
        assert "debug" in reasoning.lower()

    def test_sap_all_grant_is_critical(self, scoring_engine):
        """SAP_ALL authorization grant - CRITICAL."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="SAP_ALL Profile Granted",
            focus_area="BUSINESS_PROTECTION"
        )
        assert severity == SeverityLevel.CRITICAL

    def test_sap_new_grant_is_critical(self, scoring_engine):
        """SAP_NEW authorization grant - CRITICAL."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="SAP_NEW Profile Granted",
            focus_area="BUSINESS_PROTECTION"
        )
        assert severity == SeverityLevel.CRITICAL

    def test_po_for_one_time_vendor_is_critical(self, scoring_engine):
        """PO for one-time vendor is direct theft pattern - CRITICAL."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="PO for One-Time Vendor",
            focus_area="BUSINESS_PROTECTION"
        )
        assert severity == SeverityLevel.CRITICAL

    def test_unauthorized_transaction_is_critical(self, scoring_engine):
        """Unauthorized transaction execution - CRITICAL."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Unauthorized Transaction Detected",
            focus_area="BUSINESS_PROTECTION"
        )
        assert severity == SeverityLevel.CRITICAL

    # =========================================================================
    # HIGH Severity (Base Score: 75)
    # Possible fraud/theft, SoD+fraud combo, sensitive transactions
    # =========================================================================

    def test_rarely_used_vendor_is_high(self, scoring_engine):
        """Rarely Used Vendor is a fraud indicator - HIGH."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Rarely Used Vendors",
            focus_area="BUSINESS_PROTECTION"
        )
        assert severity == SeverityLevel.HIGH
        assert "rarely used vendor" in reasoning.lower()

    def test_rarely_used_vendor_singular_is_high(self, scoring_engine):
        """Singular form 'Rarely Used Vendor' should also be HIGH."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Rarely Used Vendor Analysis",
            focus_area="BUSINESS_PROTECTION"
        )
        assert severity == SeverityLevel.HIGH

    def test_modified_vendor_bank_is_high(self, scoring_engine):
        """Modified Vendor Bank Account is fraud pattern - HIGH."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Modified Vendor Bank Account",
            focus_area="BUSINESS_PROTECTION"
        )
        assert severity == SeverityLevel.HIGH

    def test_inventory_variance_is_high(self, scoring_engine):
        """Inventory variance indicates possible theft - HIGH."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Inventory Variance Report",
            focus_area="BUSINESS_PROTECTION",
            explanation="Inventory count differs from system records."
        )
        assert severity == SeverityLevel.HIGH

    def test_sensitive_transaction_is_high(self, scoring_engine):
        """Sensitive transaction usage - HIGH (WHO/WHY/HOW needed)."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Sensitive Transaction Usage",
            focus_area="BUSINESS_PROTECTION"
        )
        assert severity == SeverityLevel.HIGH

    def test_vendor_bank_changed_reversed_is_high(self, scoring_engine):
        """Vendor bank changed then reversed - classic fraud pattern - HIGH."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Vendor Bank Changed and Reversed",
            focus_area="BUSINESS_PROTECTION"
        )
        assert severity == SeverityLevel.HIGH

    def test_alternative_payee_is_high(self, scoring_engine):
        """Alternative payee assigned - payment redirection - HIGH."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Alternative Payee Assignment",
            focus_area="BUSINESS_PROTECTION",
            explanation="Alternative payee was assigned to vendor payment."
        )
        assert severity == SeverityLevel.HIGH

    # =========================================================================
    # MEDIUM Severity (Base Score: 60)
    # Pure SoD violations, process deviations
    # =========================================================================

    def test_exceptional_posting_is_medium(self, scoring_engine):
        """Exceptional posting by GL account - anomaly review - MEDIUM."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Exceptional Posting by GL Account",
            focus_area="BUSINESS_PROTECTION"
        )
        assert severity == SeverityLevel.MEDIUM

    def test_approved_by_creator_is_medium(self, scoring_engine):
        """PO approved by creator - pure SoD - MEDIUM."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="PO Approved by Creator",
            focus_area="BUSINESS_PROTECTION"
        )
        assert severity == SeverityLevel.MEDIUM

    def test_retroactive_po_is_medium(self, scoring_engine):
        """Retroactively created PO - process deviation - MEDIUM."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Retroactively Created PO",
            focus_area="BUSINESS_PROTECTION",
            explanation="Purchase order created retroactive to invoice date."
        )
        assert severity == SeverityLevel.MEDIUM

    def test_payment_terms_mismatch_is_medium(self, scoring_engine):
        """Payment terms mismatch - process error - MEDIUM."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Vendor Payment Terms Mismatch",
            focus_area="BUSINESS_PROTECTION",
            explanation="Payment terms mismatch between PO and vendor master."
        )
        assert severity == SeverityLevel.MEDIUM

    # =========================================================================
    # LOW Severity (Base Score: 50)
    # Tracking/housekeeping items
    # =========================================================================

    def test_one_time_vendor_created_is_low(self, scoring_engine):
        """One-time vendor created - tracking - LOW."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="One-Time Vendor Created",
            focus_area="BUSINESS_PROTECTION"
        )
        assert severity == SeverityLevel.LOW

    def test_credit_limit_changed_is_low(self, scoring_engine):
        """Credit limit changed - business decision tracking - LOW."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Customer Credit Limit Changed",
            focus_area="BUSINESS_PROTECTION"
        )
        assert severity == SeverityLevel.LOW

    # =========================================================================
    # Default Behavior
    # =========================================================================

    def test_unknown_alert_defaults_to_high_for_business_protection(self, scoring_engine):
        """Unknown alert in BUSINESS_PROTECTION defaults to HIGH."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Unknown Alert Type XYZ",
            focus_area="BUSINESS_PROTECTION"
        )
        # Default for BUSINESS_PROTECTION is HIGH (conservative)
        assert severity == SeverityLevel.HIGH
        assert "default" in reasoning.lower()

    def test_other_focus_areas_have_different_defaults(self, scoring_engine):
        """Other focus areas should have different default severities."""
        # BUSINESS_CONTROL defaults to MEDIUM
        severity, _ = scoring_engine.determine_severity_from_alert_type(
            alert_name="Unknown Alert",
            focus_area="BUSINESS_CONTROL"
        )
        assert severity == SeverityLevel.MEDIUM

        # JOBS_CONTROL defaults to LOW
        severity, _ = scoring_engine.determine_severity_from_alert_type(
            alert_name="Unknown Alert",
            focus_area="JOBS_CONTROL"
        )
        assert severity == SeverityLevel.LOW


class TestBusinessControlSeverity:
    """Tests for BUSINESS_CONTROL severity determination."""

    @pytest.fixture
    def scoring_engine(self):
        """Create a scoring engine instance for testing."""
        return ScoringEngine()

    # =========================================================================
    # HIGH Severity (Base Score: 75)
    # Significant business process issues requiring prompt review
    # =========================================================================

    def test_unbilled_delivery_is_high(self, scoring_engine):
        """Unbilled delivery is revenue risk - HIGH."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Unbilled Delivery Alert",
            focus_area="BUSINESS_CONTROL",
            explanation="Goods shipped but not invoiced."
        )
        assert severity == SeverityLevel.HIGH
        assert "unbilled" in reasoning.lower()

    def test_unbilled_delivery_pattern_matches(self, scoring_engine):
        """Test unbilled delivery pattern matching."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Unbilled Deliveries Report",
            focus_area="BUSINESS_CONTROL"
        )
        assert severity == SeverityLevel.HIGH

    def test_process_bottleneck_is_high(self, scoring_engine):
        """Process bottleneck is critical process stuck - HIGH."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Process Bottleneck Detected",
            focus_area="BUSINESS_CONTROL",
            explanation="Critical process is stuck."
        )
        assert severity == SeverityLevel.HIGH

    def test_stuck_order_is_high(self, scoring_engine):
        """Stuck order is customer impact - HIGH."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Stuck Purchase Orders",
            focus_area="BUSINESS_CONTROL"
        )
        assert severity == SeverityLevel.HIGH

    def test_blocked_order_is_high(self, scoring_engine):
        """Blocked order is customer impact - HIGH."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Blocked Sales Orders",
            focus_area="BUSINESS_CONTROL"
        )
        assert severity == SeverityLevel.HIGH

    def test_negative_profit_is_high(self, scoring_engine):
        """Negative profit deal is financial loss - HIGH."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Negative Profit Deals",
            focus_area="BUSINESS_CONTROL",
            explanation="Deals with negative profit detected."
        )
        assert severity == SeverityLevel.HIGH

    def test_exceptional_posting_is_high(self, scoring_engine):
        """Exceptional posting may indicate errors - HIGH."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Exceptional Posting Alert",
            focus_area="BUSINESS_CONTROL"
        )
        assert severity == SeverityLevel.HIGH

    def test_overdue_order_is_high(self, scoring_engine):
        """Overdue order is customer impact - HIGH."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Overdue Purchase Orders",
            focus_area="BUSINESS_CONTROL"
        )
        assert severity == SeverityLevel.HIGH

    # =========================================================================
    # MEDIUM Severity (Base Score: 60)
    # Process deviations, approval delays, pricing issues
    # =========================================================================

    def test_payment_terms_mismatch_is_medium(self, scoring_engine):
        """Payment terms mismatch is process error - MEDIUM."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Payment Terms Mismatch",
            focus_area="BUSINESS_CONTROL"
        )
        assert severity == SeverityLevel.MEDIUM

    def test_approval_delay_is_medium(self, scoring_engine):
        """Approval delay may be normal - MEDIUM."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Approval Delay Warning",
            focus_area="BUSINESS_CONTROL"
        )
        assert severity == SeverityLevel.MEDIUM

    def test_waiting_approval_is_medium(self, scoring_engine):
        """Waiting approval may be normal - MEDIUM."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="PO Waiting for Approval",
            focus_area="BUSINESS_CONTROL"
        )
        assert severity == SeverityLevel.MEDIUM

    def test_pricing_issue_is_medium(self, scoring_engine):
        """Pricing issue needs review - MEDIUM."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Pricing Issue Detected",
            focus_area="BUSINESS_CONTROL"
        )
        assert severity == SeverityLevel.MEDIUM

    def test_delay_pattern_is_medium(self, scoring_engine):
        """General delay pattern - MEDIUM."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Delivery Delay Alert",
            focus_area="BUSINESS_CONTROL"
        )
        assert severity == SeverityLevel.MEDIUM

    # =========================================================================
    # LOW Severity (Base Score: 50)
    # Tracking/housekeeping items
    # =========================================================================

    def test_credit_limit_changed_is_low(self, scoring_engine):
        """Credit limit changed is business decision - LOW."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Credit Limit Changed",
            focus_area="BUSINESS_CONTROL"
        )
        assert severity == SeverityLevel.LOW

    def test_inactive_vendor_no_balance_is_low(self, scoring_engine):
        """Inactive vendor with no balance is housekeeping - LOW."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Inactive Vendor No Balance",
            focus_area="BUSINESS_CONTROL"
        )
        assert severity == SeverityLevel.LOW

    def test_master_data_change_is_low(self, scoring_engine):
        """Master data change is informational - LOW."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Master Data Change",
            focus_area="BUSINESS_CONTROL"
        )
        assert severity == SeverityLevel.LOW

    # =========================================================================
    # Default Behavior
    # =========================================================================

    def test_unknown_alert_defaults_to_medium_for_business_control(self, scoring_engine):
        """Unknown alert in BUSINESS_CONTROL defaults to MEDIUM."""
        severity, reasoning = scoring_engine.determine_severity_from_alert_type(
            alert_name="Unknown Alert Type XYZ",
            focus_area="BUSINESS_CONTROL"
        )
        assert severity == SeverityLevel.MEDIUM
        assert "default" in reasoning.lower() or "business control" in reasoning.lower()

    def test_pattern_priority_critical_over_high(self, scoring_engine):
        """CRITICAL patterns should match before HIGH patterns."""
        # This test ensures pattern matching order is correct
        # If an alert matches both CRITICAL and HIGH, CRITICAL should win
        severity, _ = scoring_engine.determine_severity_from_alert_type(
            alert_name="DEBUG Mode Unbilled Delivery",  # Matches both DEBUG (CRITICAL) and unbilled (HIGH)
            focus_area="BUSINESS_PROTECTION"  # DEBUG is BUSINESS_PROTECTION CRITICAL
        )
        # Should be CRITICAL because CRITICAL is checked first
        assert severity == SeverityLevel.CRITICAL


class TestSeverityBaseScores:
    """Tests for severity base score values."""

    @pytest.fixture
    def scoring_engine(self):
        return ScoringEngine()

    def test_critical_base_score_is_90(self, scoring_engine):
        """CRITICAL severity should have base score 90."""
        assert scoring_engine.SEVERITY_BASE_SCORES[SeverityLevel.CRITICAL] == 90

    def test_high_base_score_is_75(self, scoring_engine):
        """HIGH severity should have base score 75."""
        assert scoring_engine.SEVERITY_BASE_SCORES[SeverityLevel.HIGH] == 75

    def test_medium_base_score_is_60(self, scoring_engine):
        """MEDIUM severity should have base score 60."""
        assert scoring_engine.SEVERITY_BASE_SCORES[SeverityLevel.MEDIUM] == 60

    def test_low_base_score_is_50(self, scoring_engine):
        """LOW severity should have base score 50."""
        assert scoring_engine.SEVERITY_BASE_SCORES[SeverityLevel.LOW] == 50
