# THA Development TODO List

*Last Updated: 2025-11-26 (Session 2 - Data Source Fix)*

---

## COMPLETED ✅

### BUSINESS_PROTECTION Testing (Session 2 - 2025-11-26)
- [x] Test with real alerts: Rarely Used Vendors, Modified Vendor Bank Account, Inventory Count
- [x] Fix classification bug: weighted patterns now override generic terms (weight 10 vs 1)
- [x] Fix severity bug: use scoring engine severity, not fallback "Medium"
- [x] Fix BACKDAYS extraction: check Code file as fallback
- [x] Verify severity mapping: HIGH for RUV, Modified Bank, Inventory; MEDIUM for Exceptional Posting
- [x] **BUG FIX**: Extract quantitative data ONLY from Summary_* (not Explanation_* which has template text)

### Scoring Engine Updates
- [x] Update severity base scores (90/75/60/50)
- [x] Implement alert-type to severity mapping for BUSINESS_PROTECTION
- [x] Add BACKDAYS parameter extraction from Metadata AND Code files
- [x] Normalize count by BACKDAYS for meaningful risk scoring
- [x] Add Factor 5 (quantities/patterns) to scoring calculation
- [x] Update llm_classifier.py with weighted keyword matching (critical=10, high=3, generic=1)

### Infrastructure
- [x] Multi-file artifact upload UI (add files one-by-one)
- [x] Content Analyzer with pattern-based classification
- [x] End-to-end flow: Upload → Analyze → Dashboard
- [x] API endpoints for content analysis
- [x] Quantitative extraction (comma-separated numbers, currency formats)

### Documentation
- [x] Skywind documentation imported (72 TXT files)
- [x] Product documentation (10 MD files)
- [x] Core Principles document
- [x] BUSINESS_PROTECTION scoring rules document

---

## COMPLETED ✅ (Session 2 Continued)

### Unit Tests for BUSINESS_PROTECTION
- [x] Write tests for classification edge cases (17 tests)
- [x] Write tests for severity determination (22 tests)
- [x] Write tests for BACKDAYS normalization (40 tests)
- [x] All 79 tests passing

---

## IN PROGRESS 🔄

### User Review
- [ ] Review BUSINESS_PROTECTION.md for any corrections

---

## SHORT-TERM TODO 📋

### Scoring Rules for Other Focus Areas
- [ ] Define ACCESS_GOVERNANCE alert-type to severity mapping
- [ ] Define TECHNICAL_CONTROL alert-type to severity mapping
- [ ] Define JOBS_CONTROL alert-type to severity mapping
- [ ] Define BUSINESS_CONTROL alert-type to severity mapping

### Scoring Logic Improvements
- [ ] Validate money adjustment thresholds with business input
- [ ] Add alert-specific thresholds (different alerts may have different $$ thresholds)
- [ ] Consider time-decay factor (older issues vs recent)

### Database & Persistence
- [ ] Create rules database structure for storing scoring logic
- [ ] Allow runtime rule updates without code changes
- [ ] Store scoring breakdown with each finding for audit trail

### Analysis Quality
- [ ] Improve qualitative analysis (better "what_happened" descriptions)
- [ ] Extract more context from Explanation files
- [ ] Better severity reasoning messages

---

## MEDIUM-TERM TODO 📅

### LLM Integration
- [ ] Enable LLM mode for better classification (requires API key config)
- [ ] Add API key configuration UI or environment setup guide
- [ ] Hybrid mode: pattern-based + LLM validation

### SoDA Report Support
- [ ] Understand SoDA artifact structure (different from 4C alerts)
- [ ] Implement SoDA-specific parsing
- [ ] Add SoDA classification rules

### User Experience
- [ ] Show scoring breakdown in UI (which factors contributed)
- [ ] Add severity override capability (user can adjust)
- [ ] Feedback loop: user marks findings as "correct" or "incorrect"
- [ ] Historical comparison (this week vs last week)

### Reporting
- [ ] Export findings to Excel/PDF
- [ ] Summary report generation
- [ ] Trend analysis over time

---

## LONG-TERM TODO 🎯

### Machine Learning
- [ ] Train ML model on user feedback (correct/incorrect classifications)
- [ ] Auto-tune thresholds based on historical data
- [ ] Anomaly detection for unusual patterns

### Integration
- [ ] SOC/SIEM integration (push alerts to external systems)
- [ ] Email notifications for critical findings
- [ ] Scheduled automatic analysis

### Multi-tenancy
- [ ] Support multiple clients/environments
- [ ] Client-specific scoring rules
- [ ] Role-based access control

### Performance
- [ ] Batch processing for large alert volumes
- [ ] Caching for repeated analysis
- [ ] Async processing with status tracking

---

## KNOWN ISSUES 🐛

1. **LLM mode disabled** - No API key configured in Docker environment
2. **Other focus areas need severity mapping** - Only BUSINESS_PROTECTION done
3. **Money thresholds may need tuning** - $1M/$100K/$10K/$1K arbitrary
4. **No user feedback loop** - Can't learn from corrections yet

---

## QUESTIONS TO RESOLVE ❓

1. Should different alert types have different money thresholds?
   - Example: $10K might be critical for "PO for one-time vendor" but low for "Inactive vendor with balance"

2. How should time factor into severity?
   - Recent events more urgent than old ones?

3. Should there be client-specific rule overrides?
   - Some orgs may accept certain SoD violations as normal

4. What's the expected alert volume?
   - Affects performance optimization priorities

---

## FILES TO REVIEW/EDIT

| File | Purpose |
|------|---------|
| `docs/scoring-rules/BUSINESS_PROTECTION.md` | Severity classification - MAKE CORRECTIONS HERE |
| `backend/app/services/content_analyzer/scoring_engine.py` | Scoring implementation |
| `backend/app/services/content_analyzer/llm_classifier.py` | Classification patterns |
| `backend/app/services/content_analyzer/analyzer.py` | Main orchestrator |
| `llm_handover.md` | Project state for AI agents |

---

*Update this file as tasks are completed or new requirements emerge*
