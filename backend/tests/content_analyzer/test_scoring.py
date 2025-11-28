"""
Unit tests for risk score calculation and BACKDAYS normalization.

Tests the 5-factor scoring calculation in scoring_engine.py.
"""

import pytest
from app.services.content_analyzer.scoring_engine import (
    ScoringEngine, SeverityLevel, RiskLevel, QuantitativeScore
)


class TestBackdaysNormalization:
    """Tests for BACKDAYS parameter extraction and normalization."""

    @pytest.fixture
    def scoring_engine(self):
        return ScoringEngine()

    def test_extract_backdays_from_metadata(self, scoring_engine):
        """BACKDAYS should be extracted from metadata dict."""
        metadata = {"BACKDAYS": 7}
        backdays = scoring_engine._extract_backdays(metadata)
        assert backdays == 7

    def test_extract_backdays_lowercase(self, scoring_engine):
        """BACKDAYS extraction should be case-insensitive."""
        metadata = {"backdays": 30}
        backdays = scoring_engine._extract_backdays(metadata)
        assert backdays == 30

    def test_extract_backdays_from_raw_metadata(self, scoring_engine):
        """BACKDAYS should be extracted from raw_metadata string."""
        metadata = {"raw_metadata": "BACKDAYS = 14\nOTHER_PARAM = 5"}
        backdays = scoring_engine._extract_backdays(metadata)
        assert backdays == 14

    def test_extract_backdays_colon_format(self, scoring_engine):
        """BACKDAYS should be extracted with colon format."""
        metadata = {"raw_metadata": "BACKDAYS: 21"}
        backdays = scoring_engine._extract_backdays(metadata)
        assert backdays == 21

    def test_no_backdays_returns_none(self, scoring_engine):
        """Missing BACKDAYS should return None."""
        metadata = {"some_other_param": 5}
        backdays = scoring_engine._extract_backdays(metadata)
        assert backdays is None

    def test_empty_metadata_returns_none(self, scoring_engine):
        """Empty metadata should return None."""
        backdays = scoring_engine._extract_backdays({})
        assert backdays is None

    def test_none_metadata_returns_none(self, scoring_engine):
        """None metadata should return None."""
        backdays = scoring_engine._extract_backdays(None)
        assert backdays is None


class TestCountAdjustment:
    """Tests for count-based score adjustment."""

    @pytest.fixture
    def scoring_engine(self):
        return ScoringEngine()

    # With BACKDAYS (daily rate thresholds)
    def test_count_adjustment_critical_daily_rate(self, scoring_engine):
        """100+ items per day = +15 points."""
        adj = scoring_engine._calculate_count_adjustment(150, backdays=1)
        assert adj == 15

    def test_count_adjustment_high_daily_rate(self, scoring_engine):
        """50-99 items per day = +10 points."""
        adj = scoring_engine._calculate_count_adjustment(75, backdays=1)
        assert adj == 10

    def test_count_adjustment_medium_daily_rate(self, scoring_engine):
        """10-49 items per day = +5 points."""
        adj = scoring_engine._calculate_count_adjustment(25, backdays=1)
        assert adj == 5

    def test_count_adjustment_low_daily_rate(self, scoring_engine):
        """1-9 items per day = +2 points."""
        adj = scoring_engine._calculate_count_adjustment(5, backdays=1)
        assert adj == 2

    def test_count_normalization_example(self, scoring_engine):
        """1943 items in 7 days = 277/day = critical."""
        normalized = 1943 / 7  # 277.57
        adj = scoring_engine._calculate_count_adjustment(normalized, backdays=7)
        assert adj == 15  # >= 100/day

    def test_count_normalization_reduces_severity(self, scoring_engine):
        """1943 items in 30 days = 65/day = high (not critical)."""
        normalized = 1943 / 30  # 64.77
        adj = scoring_engine._calculate_count_adjustment(normalized, backdays=30)
        assert adj == 10  # >= 50/day but < 100/day

    # Without BACKDAYS (raw count thresholds)
    def test_raw_count_critical_threshold(self, scoring_engine):
        """1000+ raw count = +15 points."""
        adj = scoring_engine._calculate_count_adjustment(1500, backdays=None)
        assert adj == 15

    def test_raw_count_high_threshold(self, scoring_engine):
        """500-999 raw count = +10 points."""
        adj = scoring_engine._calculate_count_adjustment(750, backdays=None)
        assert adj == 10

    def test_raw_count_medium_threshold(self, scoring_engine):
        """100-499 raw count = +5 points."""
        adj = scoring_engine._calculate_count_adjustment(250, backdays=None)
        assert adj == 5

    def test_raw_count_low_threshold(self, scoring_engine):
        """Below 100 raw count = +0 points."""
        adj = scoring_engine._calculate_count_adjustment(50, backdays=None)
        assert adj == 0


class TestMoneyAdjustment:
    """Tests for money-based score adjustment."""

    @pytest.fixture
    def scoring_engine(self):
        return ScoringEngine()

    def test_money_adjustment_over_1m(self, scoring_engine):
        """$1M+ = +20 points."""
        adj = scoring_engine._calculate_money_adjustment(2_500_000)
        assert adj == 20

    def test_money_adjustment_exactly_1m(self, scoring_engine):
        """Exactly $1M = +20 points."""
        adj = scoring_engine._calculate_money_adjustment(1_000_000)
        assert adj == 20

    def test_money_adjustment_100k_to_1m(self, scoring_engine):
        """$100K-$1M = +15 points."""
        adj = scoring_engine._calculate_money_adjustment(500_000)
        assert adj == 15

    def test_money_adjustment_10k_to_100k(self, scoring_engine):
        """$10K-$100K = +10 points."""
        adj = scoring_engine._calculate_money_adjustment(50_000)
        assert adj == 10

    def test_money_adjustment_1k_to_10k(self, scoring_engine):
        """$1K-$10K = +5 points."""
        adj = scoring_engine._calculate_money_adjustment(5_000)
        assert adj == 5

    def test_money_adjustment_under_1k(self, scoring_engine):
        """Under $1K = +0 points."""
        adj = scoring_engine._calculate_money_adjustment(500)
        assert adj == 0

    def test_money_adjustment_zero(self, scoring_engine):
        """$0 = +0 points."""
        adj = scoring_engine._calculate_money_adjustment(0)
        assert adj == 0


class TestFocusAreaMultiplier:
    """Tests for focus area risk multipliers."""

    @pytest.fixture
    def scoring_engine(self):
        return ScoringEngine()

    def test_business_protection_multiplier(self, scoring_engine):
        """BUSINESS_PROTECTION has 1.2x multiplier."""
        assert scoring_engine.FOCUS_AREA_MULTIPLIERS["BUSINESS_PROTECTION"] == 1.2

    def test_business_control_multiplier(self, scoring_engine):
        """BUSINESS_CONTROL has 1.0x multiplier."""
        assert scoring_engine.FOCUS_AREA_MULTIPLIERS["BUSINESS_CONTROL"] == 1.0

    def test_access_governance_multiplier(self, scoring_engine):
        """ACCESS_GOVERNANCE has 1.15x multiplier."""
        assert scoring_engine.FOCUS_AREA_MULTIPLIERS["ACCESS_GOVERNANCE"] == 1.15

    def test_technical_control_multiplier(self, scoring_engine):
        """TECHNICAL_CONTROL has 0.9x multiplier."""
        assert scoring_engine.FOCUS_AREA_MULTIPLIERS["TECHNICAL_CONTROL"] == 0.9

    def test_jobs_control_multiplier(self, scoring_engine):
        """JOBS_CONTROL has 0.85x multiplier."""
        assert scoring_engine.FOCUS_AREA_MULTIPLIERS["JOBS_CONTROL"] == 0.85


class TestCombinedScoreCalculation:
    """Tests for complete score calculation with all factors."""

    @pytest.fixture
    def scoring_engine(self):
        return ScoringEngine()

    def test_high_severity_high_volume_high_money_business_protection(self, scoring_engine):
        """
        HIGH severity + high volume + high money in BUSINESS_PROTECTION.
        Factor 1: 75 (HIGH)
        Factor 2: +15 (1000+ count)
        Factor 3: +20 ($1M+)
        Factor 4: x1.2
        = (75 + 15 + 20) * 1.2 = 132 -> capped at 100
        """
        result = scoring_engine.calculate_score(
            focus_area="BUSINESS_PROTECTION",
            qualitative_data={},
            quantitative_data={"total_count": 1500, "monetary_amount": 2_000_000},
            severity="High",
            alert_name="Test Alert"
        )
        assert result.risk_score == 100  # Capped at 100
        assert result.risk_level == RiskLevel.CRITICAL

    def test_medium_severity_low_volume_no_money_business_control(self, scoring_engine):
        """
        MEDIUM severity + low volume + no money in BUSINESS_CONTROL.
        Factor 1: 60 (MEDIUM)
        Factor 2: +0 (< 100 count)
        Factor 3: +0 ($0)
        Factor 4: x1.0
        = 60 * 1.0 = 60
        Note: Score 60 falls in HIGH risk level (51-75), not MEDIUM (26-50)
        """
        result = scoring_engine.calculate_score(
            focus_area="BUSINESS_CONTROL",
            qualitative_data={},
            quantitative_data={"total_count": 50, "monetary_amount": 0},
            severity="Medium",
            alert_name="Test Alert"
        )
        assert result.risk_score == 60
        assert result.risk_level == RiskLevel.HIGH  # Score 60 = HIGH risk level

    def test_score_capped_at_100(self, scoring_engine):
        """Score should never exceed 100."""
        result = scoring_engine.calculate_score(
            focus_area="BUSINESS_PROTECTION",
            qualitative_data={},
            quantitative_data={"total_count": 10000, "monetary_amount": 100_000_000},
            severity="Critical",
            alert_name="Extreme Alert"
        )
        assert result.risk_score == 100

    def test_score_minimum_is_0(self, scoring_engine):
        """Score should never go below 0."""
        result = scoring_engine.calculate_score(
            focus_area="JOBS_CONTROL",  # Lowest multiplier
            qualitative_data={},
            quantitative_data={"total_count": 0, "monetary_amount": 0},
            severity="Low",
            alert_name="Minimal Alert"
        )
        assert result.risk_score >= 0

    def test_scoring_breakdown_included(self, scoring_engine):
        """Scoring breakdown should be included in result."""
        result = scoring_engine.calculate_score(
            focus_area="BUSINESS_PROTECTION",
            qualitative_data={},
            quantitative_data={"total_count": 500, "monetary_amount": 50_000},
            severity="High",
            alert_name="Test Alert"
        )
        breakdown = result.scoring_breakdown
        assert "factor1_severity_base" in breakdown
        assert "factor2_count_adjustment" in breakdown
        assert "factor3_money_adjustment" in breakdown
        assert "factor4_focus_area_multiplier" in breakdown
        assert "final_score" in breakdown


class TestRiskLevelDetermination:
    """Tests for risk level determination from score."""

    @pytest.fixture
    def scoring_engine(self):
        return ScoringEngine()

    def test_score_76_100_is_critical(self, scoring_engine):
        """Score 76-100 = CRITICAL risk level."""
        assert scoring_engine._score_to_risk_level(100) == RiskLevel.CRITICAL
        assert scoring_engine._score_to_risk_level(76) == RiskLevel.CRITICAL

    def test_score_51_75_is_high(self, scoring_engine):
        """Score 51-75 = HIGH risk level."""
        assert scoring_engine._score_to_risk_level(75) == RiskLevel.HIGH
        assert scoring_engine._score_to_risk_level(51) == RiskLevel.HIGH

    def test_score_26_50_is_medium(self, scoring_engine):
        """Score 26-50 = MEDIUM risk level."""
        assert scoring_engine._score_to_risk_level(50) == RiskLevel.MEDIUM
        assert scoring_engine._score_to_risk_level(26) == RiskLevel.MEDIUM

    def test_score_0_25_is_low(self, scoring_engine):
        """Score 0-25 = LOW risk level."""
        assert scoring_engine._score_to_risk_level(25) == RiskLevel.LOW
        assert scoring_engine._score_to_risk_level(0) == RiskLevel.LOW
