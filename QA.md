# SchemeSetu: Quality Assurance & Handover Report (QA.md)

**Project:** SchemeSetu 🌉  
**Date of Testing:** 2026-10-28  
**Operating System:** Windows  
**Python Version:** Python 3.12.x  
**Test Suite Runner:** `python test_rules.py`  

---

## 1. What Was Tested & Verified

### A. Automated Unit Test Suite (`test_rules.py`)
23 distinct test functions were executed covering all core algorithms and edge cases:
1. `test_eligible`: Verifies deterministic qualifying logic.
2. `test_income_gap_is_exact`: Validates exact mathematical shortfall calculation on excess income.
3. `test_missing_info`: Validates that unmentioned profile fields remain `None` and flag "Needs more info".
4. `test_missing_multiple_fields_and_precedence`: Validates that disqualifying criteria strictly override unknown fields.
5. `test_ranking_puts_eligible_first`: Confirms sorting priority (Eligible -> Needs info -> Ineligible) by benefit amount or speed.
6. `test_mock_mode_parser_sentences`: Tests deterministic regex extraction across 5 diverse realistic sentences covering age, income ("lakh", "lpa", numeric), caste categories, courses, and genders.
7. `test_mock_mode_flag_behavior`: Verifies toggling between mock mode and real mode based on environment variables and API key presence.
8. `test_scheme_ssp_sc_postmatric`: Tests qualifying criteria and individual rule failures (income, category, state, course, age).
9. `test_scheme_ssp_st_postmatric`: Tests qualifying criteria and rule failures for ST students.
10. `test_scheme_ssp_bcwd_postmatric`: Tests qualifying criteria and rule failures for OBC students.
11. `test_scheme_karnataka_vidyasiri`: Tests multi-category eligibility (OBC, SC, ST) and rule failures for Vidyasiri VFAS.
12. `test_scheme_aicte_pragati_girls`: Tests gender restriction (Female only), income ceiling (₹8 Lakh), and engineering courses.
13. `test_scheme_central_sector_scholarship`: Tests collegiate courses, age brackets (17-25), and income ceiling (₹4.5 Lakh).
14. `test_scheme_minority_mcm_technical`: Tests Karnataka domicile, technical courses, and income limits.
15. `test_scheme_ksbdb_saandeepani`: Tests EWS/General category eligibility and income ceilings.
16. `test_scheme_karnataka_free_laptop`: Tests first-year degree criteria, age brackets, and Karnataka domicile.
17. `test_tavily_search_fallback_and_discrepancy`: Validates Tavily offline fallback when keys are absent and tests automated regex detection for portal closure notices.
18. `test_gap_analysis_details`: Confirms multi-gap text synthesis for multiple failing criteria simultaneously.
19. `test_what_if_simulation_deterministic`: Verifies that simulating income reductions or category changes deterministically unlocks schemes without calling LLMs.
20. `test_draft_generator_brackets_for_unknowns`: Confirms application draft generation preserves verified profile facts while inserting square brackets `[...]` for unknown fields.
21. `test_ocr_extract_certificate_in_memory`: Confirms certificate extraction operates purely in memory with safe mock fallbacks.
22. `test_multilingual_explanation_and_draft`: Tests prompt formatting and language parameter passthrough for English, Hindi, and Kannada.
23. `test_json_parse_fallback_robustness`: Confirms robust JSON markdown stripping and graceful fallback on malformed model payloads.

**Result:** **23 of 23 Passed (100% Pass Rate).**

---

### B. Python Syntax and Module Import Verification
- Executed `python -m py_compile app.py rules.py llm.py search.py test_rules.py`.  
  **Result: 0 syntax errors.**
- Executed headless execution of `app.py` in mock mode.  
  **Result: Clean startup, zero unhandled exceptions, graceful UI degradation.**

---

## 2. Known Issues & Operational Considerations
- **Streamlit ScriptRunContext Warnings:** When running scripts outside of `streamlit run` (e.g. executing unit tests or module imports directly via bare `python`), Streamlit issues an informational log that `ScriptRunContext` is absent and session state does not persist. This is standard Streamlit behavior and does not impact normal execution or unit tests.
- **Vision Model Provisioning:** Vision capabilities for document OCR require an active `VISION_MODEL` deployment on Nebius Token Factory. If omitted or unsupported by your quota, SchemeSetu automatically hides the feature in production mode without breaking any core scholarship matching capabilities.

---

## 3. Mandatory Manual Steps Required by User

Before submitting to the Nebius x NVIDIA Global AI Hackathon, you must complete the following manual actions:

1. **Add Real API Keys to `.env` (Local) and Streamlit Cloud (Production):**
   - In `.env` or Streamlit Cloud Secrets:
     ```ini
     TOKEN_FACTORY_API_KEY=<your-real-nebius-token-factory-key>
     TOKEN_FACTORY_BASE_URL=https://api.tokenfactory.nebius.com/v1/
     FAST_MODEL=nvidia/nemotron-mini-4b-instruct
     STRONG_MODEL=nvidia/llama-3.1-nemotron-70b-instruct
     TAVILY_API_KEY=<your-real-tavily-api-key>
     MOCK_MODE=false
     ```
2. **Review & Confirm `VERIFY.md` Against Official Portals:**
   - Open each government portal listed in `VERIFY.md` (e.g., SSP Karnataka, BCWD, scholarships.gov.in).
   - Once verified, toggle `"verified": true` in `schemes.json` for verified schemes to clear the yellow review badge.
3. **Test in Real Mode Locally:**
   - Run `streamlit run app.py` with real keys.
   - Confirm that the yellow demo banner disappears.
   - Verify that extraction and explanations make live runtime calls to Nebius Token Factory and Tavily.
4. **Deploy on Streamlit Community Cloud:**
   - Push your code to your public GitHub repository (`git push origin main`).
   - Create the app on [share.streamlit.io](https://share.streamlit.io).
   - Paste your production credentials into **Settings -> Secrets**.
   - Open the live URL in an **Incognito / Private tab** while logged out to confirm public accessibility.
5. **Record the Demo Video (< 3 Minutes):**
   - Follow the timestamped script provided in `SUBMISSION.md`.
   - Record screen and voiceover showcasing:
     - Profile extraction from free-text.
     - Deterministic qualification and gap analysis.
     - Live Tavily search verification with `.gov.in` citations.
     - Multilingual drafting and download.
   - Upload to YouTube as Public or Unlisted.
6. **Submit on Devpost:**
   - Copy the pitch (< 200 chars) and project description (322 words) from `SUBMISSION.md`.
   - Add your personalized feedback in Section 4 of `SUBMISSION.md`.
   - Complete the Devpost submission checklist before the deadline.
