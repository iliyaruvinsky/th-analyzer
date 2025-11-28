"""
LLM-based Classifier for Content Analysis

Uses LLM (OpenAI/Anthropic) to intelligently classify alerts into focus areas
and analyze content based on contextual understanding.
"""

import json
import logging
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass

from .artifact_reader import AlertArtifacts
from .context_loader import ContextLoader, get_context_loader
from . import prompts

logger = logging.getLogger(__name__)


@dataclass
class ClassificationResult:
    """Result of LLM classification."""
    focus_area: str
    confidence: float
    reasoning: str
    raw_response: Optional[str] = None


@dataclass
class AnalysisResult:
    """Result of LLM analysis."""
    findings_summary: str
    qualitative_analysis: Dict[str, Any]
    quantitative_analysis: Dict[str, Any]
    severity: str
    severity_reasoning: str
    recommended_actions: List[str]
    raw_response: Optional[str] = None


@dataclass
class RiskScore:
    """Risk scoring result."""
    risk_score: int
    risk_level: str
    risk_factors: List[str]
    potential_financial_impact: Dict[str, Any]
    raw_response: Optional[str] = None


class LLMClassifier:
    """
    LLM-based classifier for analyzing alerts and extracting findings.

    Supports both OpenAI and Anthropic as LLM providers.
    """

    VALID_FOCUS_AREAS = [
        "BUSINESS_PROTECTION",
        "BUSINESS_CONTROL",
        "ACCESS_GOVERNANCE",
        "TECHNICAL_CONTROL",
        "JOBS_CONTROL",
    ]

    def __init__(
        self,
        llm_provider: str = "openai",
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        context_loader: Optional[ContextLoader] = None
    ):
        """
        Initialize the LLM classifier.

        Args:
            llm_provider: "openai" or "anthropic"
            api_key: API key for the provider
            model: Model to use (defaults based on provider)
            context_loader: Optional context loader instance
        """
        self.llm_provider = llm_provider.lower()
        self.api_key = api_key
        self.model = model or self._default_model()
        self.context_loader = context_loader or get_context_loader()
        self._client = None

    def _default_model(self) -> str:
        """Get default model based on provider."""
        if self.llm_provider == "anthropic":
            return "claude-3-sonnet-20240229"
        return "gpt-4o-mini"

    def _get_client(self):
        """Get or create the LLM client."""
        if self._client is not None:
            return self._client

        if self.llm_provider == "openai":
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=self.api_key)
            except ImportError:
                raise ImportError("OpenAI library not installed. Run: pip install openai")

        elif self.llm_provider == "anthropic":
            try:
                from anthropic import Anthropic
                self._client = Anthropic(api_key=self.api_key)
            except ImportError:
                raise ImportError("Anthropic library not installed. Run: pip install anthropic")

        else:
            raise ValueError(f"Unknown LLM provider: {self.llm_provider}")

        return self._client

    def _call_llm(self, system_prompt: str, user_prompt: str) -> str:
        """
        Make a call to the LLM.

        Args:
            system_prompt: System prompt setting context
            user_prompt: User prompt with the actual request

        Returns:
            LLM response text
        """
        client = self._get_client()

        try:
            if self.llm_provider == "openai":
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.3,  # Lower temperature for more consistent results
                    max_tokens=2000
                )
                return response.choices[0].message.content

            elif self.llm_provider == "anthropic":
                response = client.messages.create(
                    model=self.model,
                    max_tokens=2000,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": user_prompt}
                    ]
                )
                return response.content[0].text

        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise

    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """
        Parse JSON from LLM response, handling markdown code blocks.

        Args:
            response: Raw LLM response

        Returns:
            Parsed JSON dictionary
        """
        # Try to extract JSON from markdown code blocks
        json_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', response, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find JSON object directly
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = response

        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.debug(f"Response was: {response}")
            # Return a default structure
            return {"error": str(e), "raw": response}

    def classify_focus_area(self, artifacts: AlertArtifacts) -> ClassificationResult:
        """
        Classify an alert into a focus area using LLM.

        Args:
            artifacts: The alert artifacts to classify

        Returns:
            ClassificationResult with focus area and confidence
        """
        # Build the classification prompt
        prompt = prompts.CLASSIFICATION_PROMPT.format(
            alert_name=artifacts.alert_name,
            code_summary=artifacts.code_summary or "Not available",
            explanation=artifacts.explanation or "Not available",
            metadata=artifacts.metadata[:1000] if artifacts.metadata else "Not available"
        )

        try:
            response = self._call_llm(prompts.SYSTEM_PROMPT, prompt)
            result = self._parse_json_response(response)

            focus_area = result.get("focus_area", "BUSINESS_CONTROL")
            # Validate focus area
            if focus_area not in self.VALID_FOCUS_AREAS:
                logger.warning(f"Invalid focus area from LLM: {focus_area}, defaulting to BUSINESS_CONTROL")
                focus_area = "BUSINESS_CONTROL"

            return ClassificationResult(
                focus_area=focus_area,
                confidence=float(result.get("confidence", 0.5)),
                reasoning=result.get("reasoning", "Classification based on alert content"),
                raw_response=response
            )

        except Exception as e:
            logger.error(f"Classification failed: {e}")
            # Return default classification
            return ClassificationResult(
                focus_area="BUSINESS_CONTROL",
                confidence=0.3,
                reasoning=f"Default classification due to error: {str(e)}"
            )

    def analyze_summary(
        self,
        artifacts: AlertArtifacts,
        focus_area: str
    ) -> AnalysisResult:
        """
        Analyze the Summary data and extract findings.

        Args:
            artifacts: The alert artifacts
            focus_area: The classified focus area

        Returns:
            AnalysisResult with detailed analysis
        """
        # Truncate summary if too long
        summary_data = artifacts.summary
        if summary_data and len(summary_data) > 10000:
            summary_data = summary_data[:10000] + "\n... [truncated]"

        prompt = prompts.ANALYSIS_PROMPT.format(
            alert_name=artifacts.alert_name,
            focus_area=focus_area,
            explanation=artifacts.explanation or "Not available",
            summary_data=summary_data or "No summary data available"
        )

        try:
            response = self._call_llm(prompts.SYSTEM_PROMPT, prompt)
            result = self._parse_json_response(response)

            return AnalysisResult(
                findings_summary=result.get("findings_summary", "Analysis results"),
                qualitative_analysis=result.get("qualitative_analysis", {}),
                quantitative_analysis=result.get("quantitative_analysis", {}),
                severity=result.get("severity", "Medium"),
                severity_reasoning=result.get("severity_reasoning", ""),
                recommended_actions=result.get("recommended_actions", []),
                raw_response=response
            )

        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return AnalysisResult(
                findings_summary=f"Analysis failed: {str(e)}",
                qualitative_analysis={},
                quantitative_analysis={},
                severity="Medium",
                severity_reasoning="Default severity due to analysis error",
                recommended_actions=["Review alert manually"]
            )

    def calculate_risk_score(
        self,
        artifacts: AlertArtifacts,
        focus_area: str,
        analysis_result: AnalysisResult
    ) -> RiskScore:
        """
        Calculate risk score based on analysis results.

        Args:
            artifacts: The alert artifacts
            focus_area: The classified focus area
            analysis_result: The analysis result

        Returns:
            RiskScore with score and factors
        """
        # Format analysis results for the prompt
        analysis_json = json.dumps({
            "findings_summary": analysis_result.findings_summary,
            "qualitative_analysis": analysis_result.qualitative_analysis,
            "quantitative_analysis": analysis_result.quantitative_analysis,
            "severity": analysis_result.severity
        }, indent=2)

        prompt = prompts.RISK_SCORING_PROMPT.format(
            alert_name=artifacts.alert_name,
            focus_area=focus_area,
            analysis_results=analysis_json
        )

        try:
            response = self._call_llm(prompts.SYSTEM_PROMPT, prompt)
            result = self._parse_json_response(response)

            return RiskScore(
                risk_score=int(result.get("risk_score", 50)),
                risk_level=result.get("risk_level", "Medium"),
                risk_factors=result.get("risk_factors", []),
                potential_financial_impact=result.get("potential_financial_impact", {}),
                raw_response=response
            )

        except Exception as e:
            logger.error(f"Risk scoring failed: {e}")
            return RiskScore(
                risk_score=50,
                risk_level="Medium",
                risk_factors=["Unable to calculate specific risk factors"],
                potential_financial_impact={}
            )

    def generate_finding_description(
        self,
        artifacts: AlertArtifacts,
        focus_area: str,
        analysis_result: AnalysisResult
    ) -> Dict[str, str]:
        """
        Generate human-readable finding description.

        Args:
            artifacts: The alert artifacts
            focus_area: The classified focus area
            analysis_result: The analysis result

        Returns:
            Dictionary with title, description, business_impact
        """
        analysis_json = json.dumps({
            "findings_summary": analysis_result.findings_summary,
            "qualitative_analysis": analysis_result.qualitative_analysis,
            "quantitative_analysis": analysis_result.quantitative_analysis,
            "severity": analysis_result.severity
        }, indent=2)

        prompt = prompts.FINDING_DESCRIPTION_PROMPT.format(
            alert_name=artifacts.alert_name,
            focus_area=focus_area,
            analysis_results=analysis_json
        )

        try:
            response = self._call_llm(prompts.SYSTEM_PROMPT, prompt)
            result = self._parse_json_response(response)

            return {
                "title": result.get("title", artifacts.alert_name),
                "description": result.get("description", analysis_result.findings_summary),
                "business_impact": result.get("business_impact", ""),
                "technical_details": result.get("technical_details", "")
            }

        except Exception as e:
            logger.error(f"Description generation failed: {e}")
            return {
                "title": artifacts.alert_name,
                "description": analysis_result.findings_summary,
                "business_impact": "Review required",
                "technical_details": ""
            }

    def analyze_without_llm(self, artifacts: AlertArtifacts) -> Tuple[str, float, str]:
        """
        Fallback analysis without LLM (pattern-based).

        Uses keyword matching when LLM is unavailable.
        Updated to align with refined BUSINESS_PROTECTION severity classification.

        Args:
            artifacts: The alert artifacts

        Returns:
            Tuple of (focus_area, confidence, reasoning)
        """
        text = f"{artifacts.alert_name} {artifacts.explanation or ''} {artifacts.code_summary or ''}"
        text_lower = text.lower()

        # Pattern matching for focus areas
        # Patterns are weighted - more specific patterns get higher scores
        # IMPORTANT: Specific fraud patterns must have HIGH weights to override generic terms
        patterns = {
            "BUSINESS_PROTECTION": [
                # Critical indicators (weight 10) - MUST override ALL generic vendor/customer terms
                # Weight must be > sum of all BUSINESS_CONTROL keywords that might match
                ("rarely used vendor", 10),       # RUV = fraud indicator - HIGHEST priority
                ("rarely used vendors", 10),      # Plural form
                ("ruv ", 10),                     # RUV abbreviation
                ("po for one-time vendor", 10),   # Direct theft pattern
                ("purchase order for one-time", 10),
                ("debug", 10),                    # DEBUG system updates - security bypass
                ("sap_all", 10),                  # Critical authorization
                ("sap_new", 10),                  # Critical authorization
                # High indicators (weight 3)
                ("fraud", 3),
                ("theft", 3),
                ("cyber", 3),
                ("unauthorized", 3),
                ("manipulation", 3),
                ("suspicious", 3),
                ("bank.*changed.*reversed", 3),   # Vendor bank fraud pattern
                ("bank.*revert", 3),
                ("modified vendor bank", 3),      # Bank modification alert
                ("alternative payee", 3),
                ("sensitive transaction", 3),     # WHO/WHY/HOW needed
                ("inventory variance", 3),
                ("inventory count.*differ", 3),
                # Standard indicators (weight 1)
                ("irregular", 1),
                ("falsif", 1),
                ("diversion", 1),
            ],
            "BUSINESS_CONTROL": [
                # Vendor/customer management (weight 1) - LOWER than fraud patterns
                ("vendor", 1),
                ("customer", 1),
                ("master data", 1),
                ("invoice", 1),
                ("payment", 1),
                # Process indicators (weight 1)
                ("purchase order", 1),
                ("sales order", 1),
                ("balance", 1),
                ("financial", 1),
                ("pricing", 1),
                ("discount", 1),
                ("credit", 1),
                ("bottleneck", 1),
                ("delay", 1),
                ("approval", 1),
                ("stuck", 1),
                ("unbilled", 1),
                ("incomplete", 1),
                ("anomal", 1),
                ("inactive vendor", 1),
                ("inactive customer", 1),
            ],
            "ACCESS_GOVERNANCE": [
                # SoD indicators (weight 2)
                ("sod", 2),
                ("segregation of duties", 2),
                ("approved by creator", 2),
                ("parked.*posted.*same user", 2),
                # Authorization indicators (weight 1)
                ("privilege", 1),
                ("authorization", 1),
                ("access control", 1),
                ("permission", 1),
                ("role conflict", 1),
                ("user profile", 1),
            ],
            "TECHNICAL_CONTROL": [
                # Critical technical issues (weight 2)
                ("memory dump", 2),
                ("abap dump", 2),
                ("short dump", 2),
                ("system crash", 2),
                # Standard technical issues (weight 1)
                ("cpu usage", 1),
                ("runtime error", 1),
                ("performance", 1),
                ("database", 1),
            ],
            "JOBS_CONTROL": [
                # Job issues (weight 2)
                ("job failed", 2),
                ("job failure", 2),
                ("job runtime", 2),
                # Standard job indicators (weight 1)
                ("batch job", 1),
                ("background job", 1),
                ("scheduled task", 1),
                ("resource contention", 1),
            ]
        }

        scores = {}
        matched_keywords = {}

        for focus_area, keyword_weights in patterns.items():
            total_score = 0
            matched = []
            for keyword, weight in keyword_weights:
                # Use regex for patterns with special chars, otherwise simple match
                if any(c in keyword for c in ['*', '.', '+']):
                    import re
                    if re.search(keyword, text_lower):
                        total_score += weight
                        matched.append(keyword)
                elif keyword in text_lower:
                    total_score += weight
                    matched.append(keyword)
            scores[focus_area] = total_score
            matched_keywords[focus_area] = matched

        if max(scores.values()) > 0:
            best_area = max(scores, key=scores.get)
            confidence = min(0.85, scores[best_area] * 0.12)
            matched_str = ", ".join(matched_keywords[best_area][:5])
            return best_area, confidence, f"Matched keywords: {matched_str}"

        return "BUSINESS_CONTROL", 0.3, "Default classification"
