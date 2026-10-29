import os
from rules import evaluate, evaluate_all, load_schemes, rank
import llm
import search


SCHEME = {
    "id": "t",
    "name": "Test",
    "benefit_amount": 1,
    "rules": {"max_income": 250000, "categories": ["OBC", "SC"], "states": ["Karnataka"]},
}


def test_eligible():
    p = {"annual_income": 200000, "category": "obc", "state": "Karnataka"}
    assert evaluate(p, SCHEME)["status"] == "eligible"


def test_income_gap_is_exact():
    p = {"annual_income": 300000, "category": "OBC", "state": "Karnataka"}
    r = evaluate(p, SCHEME)
    assert r["status"] == "not_eligible"
    assert "50,000 above the cap" in r["gaps"][0]


def test_missing_info():
    p = {"annual_income": 200000, "state": "Karnataka"}
    r = evaluate(p, SCHEME)
    assert r["status"] == "needs_info"
    assert r["missing"] == ["Category"]


def test_missing_multiple_fields_and_precedence():
    # When both category and income are missing
    p_empty = {"state": "Karnataka"}
    r1 = evaluate(p_empty, SCHEME)
    assert r1["status"] == "needs_info"
    assert "Family income" in r1["missing"]
    assert "Category" in r1["missing"]

    # When a field fails (e.g. state is wrong), status must be not_eligible even if income is missing
    p_fail_and_missing = {"state": "Tamil Nadu"}
    r2 = evaluate(p_fail_and_missing, SCHEME)
    assert r2["status"] == "not_eligible"
    assert len(r2["gaps"]) > 0



def test_ranking_puts_eligible_first():
    schemes = load_schemes()
    p = {"age": 20, "state": "Karnataka", "annual_income": 200000, "category": "OBC", "course": "Engineering", "gender": "Female"}
    ranked = rank(evaluate_all(p, schemes))
    assert ranked[0]["status"] == "eligible"


def test_mock_mode_parser_sentences():
    # Sentence 1: Standard full sentence
    s1 = "I'm a 20 year old OBC girl from Karnataka studying engineering. Family income is about 3 lakh."
    p1 = llm._mock_extract_profile(s1)
    assert p1["age"] == 20
    assert p1["state"] == "Karnataka"
    assert p1["annual_income"] == 300000
    assert p1["category"] == "OBC"
    assert p1["course"] == "Engineering"
    assert p1["gender"] == "Female"

    # Sentence 2: Medicine, SC, 1.5 lakhs
    s2 = "19 yo male SC student in Karnataka pursuing Medicine with annual income of 1.5 lakhs."
    p2 = llm._mock_extract_profile(s2)
    assert p2["age"] == 19
    assert p2["state"] == "Karnataka"
    assert p2["annual_income"] == 150000
    assert p2["category"] == "SC"
    assert p2["course"] == "Medicine"
    assert p2["gender"] == "Male"

    # Sentence 3: Commerce, General, 450000
    s3 = "I'm 22, studying Commerce in Karnataka, female, General category, household income 450000 per annum."
    p3 = llm._mock_extract_profile(s3)
    assert p3["age"] == 22
    assert p3["state"] == "Karnataka"
    assert p3["annual_income"] == 450000
    assert p3["category"] == "General"
    assert p3["course"] == "Commerce"
    assert p3["gender"] == "Female"

    # Sentence 4: Science, ST, 80000
    s4 = "ST boy, 18 years old, doing Science in Karnataka, parents earn 80000 yearly."
    p4 = llm._mock_extract_profile(s4)
    assert p4["age"] == 18
    assert p4["state"] == "Karnataka"
    assert p4["annual_income"] == 80000
    assert p4["category"] == "ST"
    assert p4["course"] == "Science"
    assert p4["gender"] == "Male"

    # Sentence 5: EWS, 2.4 lakh
    s5 = "21 yr old EWS female engineering student from Karnataka, family income 2.4 lakh."
    p5 = llm._mock_extract_profile(s5)
    assert p5["age"] == 21
    assert p5["state"] == "Karnataka"
    assert p5["annual_income"] == 240000
    assert p5["category"] == "EWS"
    assert p5["course"] == "Engineering"
    assert p5["gender"] == "Female"


def test_mock_mode_flag_behavior():
    orig_key = os.environ.get("TOKEN_FACTORY_API_KEY")
    orig_mock = os.environ.get("MOCK_MODE")
    try:
        # Case 1: No key, mock mode should be True
        os.environ["TOKEN_FACTORY_API_KEY"] = ""
        os.environ["MOCK_MODE"] = ""
        assert llm.is_mock_mode() is True

        # Case 2: Key set and MOCK_MODE not true -> mock mode should be False
        os.environ["TOKEN_FACTORY_API_KEY"] = "fake-nebius-key-12345"
        os.environ["MOCK_MODE"] = "false"
        assert llm.is_mock_mode() is False

        # Case 3: Key set but MOCK_MODE explicitly true -> mock mode should be True
        os.environ["MOCK_MODE"] = "true"
        assert llm.is_mock_mode() is True
    finally:
        if orig_key is not None:
            os.environ["TOKEN_FACTORY_API_KEY"] = orig_key
        else:
            os.environ.pop("TOKEN_FACTORY_API_KEY", None)
        if orig_mock is not None:
            os.environ["MOCK_MODE"] = orig_mock
        else:
            os.environ.pop("MOCK_MODE", None)


def _get_scheme_by_id(schemes, sid):
    for s in schemes:
        if s["id"] == sid:
            return s
    raise ValueError(f"Scheme {sid} not found")


def test_scheme_ssp_sc_postmatric():
    schemes = load_schemes()
    s = _get_scheme_by_id(schemes, "ssp-sc-postmatric")
    p_ok = {"age": 19, "state": "Karnataka", "annual_income": 150000, "category": "SC", "course": "Engineering", "gender": "Male"}
    assert evaluate(p_ok, s)["status"] == "eligible"
    # Fail income
    assert evaluate({**p_ok, "annual_income": 300000}, s)["status"] == "not_eligible"
    # Fail category
    assert evaluate({**p_ok, "category": "General"}, s)["status"] == "not_eligible"
    # Fail state
    assert evaluate({**p_ok, "state": "Tamil Nadu"}, s)["status"] == "not_eligible"
    # Course and age rules were removed because no source confirmed them
    assert evaluate({**p_ok, "course": "Fashion Design"}, s)["status"] == "eligible"
    assert evaluate({**p_ok, "age": 14}, s)["status"] == "eligible"


def test_scheme_ssp_st_postmatric():
    schemes = load_schemes()
    s = _get_scheme_by_id(schemes, "ssp-st-postmatric")
    p_ok = {"age": 18, "state": "Karnataka", "annual_income": 120000, "category": "ST", "course": "Science", "gender": "Female"}
    assert evaluate(p_ok, s)["status"] == "eligible"
    assert evaluate({**p_ok, "annual_income": 350000}, s)["status"] == "not_eligible"
    assert evaluate({**p_ok, "category": "OBC"}, s)["status"] == "not_eligible"
    assert evaluate({**p_ok, "state": "Kerala"}, s)["status"] == "not_eligible"


def test_scheme_ssp_bcwd_postmatric():
    schemes = load_schemes()
    s = _get_scheme_by_id(schemes, "ssp-bcwd-postmatric")
    p_ok = {"age": 20, "state": "Karnataka", "annual_income": 200000, "category": "OBC", "course": "Commerce", "gender": "Male"}
    assert evaluate(p_ok, s)["status"] == "eligible"
    assert evaluate({**p_ok, "annual_income": 300000}, s)["status"] == "not_eligible"
    assert evaluate({**p_ok, "category": "SC"}, s)["status"] == "not_eligible"
    assert evaluate({**p_ok, "state": "Maharashtra"}, s)["status"] == "not_eligible"
    # The card text must warn about the lower Rs 1 lakh cap for Categories 2A, 3A and 3B
    assert "Categories 2A, 3A and 3B" in s["benefit"]


def test_scheme_karnataka_vidyasiri():
    schemes = load_schemes()
    s = _get_scheme_by_id(schemes, "karnataka-vidyasiri")
    p_ok = {"age": 19, "state": "Karnataka", "annual_income": 180000, "category": "OBC", "course": "Arts", "gender": "Female"}
    assert evaluate(p_ok, s)["status"] == "eligible"
    assert evaluate({**p_ok, "category": "SC"}, s)["status"] == "eligible"
    assert evaluate({**p_ok, "category": "ST"}, s)["status"] == "eligible"
    assert evaluate({**p_ok, "annual_income": 300000}, s)["status"] == "not_eligible"
    assert evaluate({**p_ok, "category": "General"}, s)["status"] == "not_eligible"
    assert evaluate({**p_ok, "state": "Goa"}, s)["status"] == "not_eligible"


def test_scheme_aicte_pragati_girls():
    schemes = load_schemes()
    s = _get_scheme_by_id(schemes, "aicte-pragati-girls")
    p_ok = {"gender": "Female", "annual_income": 400000, "course": "Engineering", "state": "Karnataka", "age": 19}
    assert evaluate(p_ok, s)["status"] == "eligible"
    assert evaluate({**p_ok, "annual_income": 900000}, s)["status"] == "not_eligible"
    assert evaluate({**p_ok, "gender": "Male"}, s)["status"] == "not_eligible"
    assert evaluate({**p_ok, "course": "Arts"}, s)["status"] == "not_eligible"


def test_scheme_central_sector_scholarship():
    schemes = load_schemes()
    s = _get_scheme_by_id(schemes, "central-sector-scholarship")
    p_ok = {"age": 19, "annual_income": 300000, "course": "Science", "state": "Karnataka", "gender": "Female"}
    assert evaluate(p_ok, s)["status"] == "eligible"
    # Income cap is Rs 4.5 lakh (inclusive)
    assert evaluate({**p_ok, "annual_income": 450000}, s)["status"] == "eligible"
    assert evaluate({**p_ok, "annual_income": 450001}, s)["status"] == "not_eligible"
    # Missing income needs more info
    assert evaluate({**p_ok, "annual_income": None}, s)["status"] == "needs_info"
    # Age and course rules were removed because no source confirmed them
    assert evaluate({**p_ok, "age": 16}, s)["status"] == "eligible"
    assert evaluate({**p_ok, "age": 26}, s)["status"] == "eligible"
    # The 80th percentile condition cannot be checked by the app, so the card must say so
    assert "80th percentile" in s["benefit"]


def test_removed_schemes_are_gone():
    ids = {s["id"] for s in load_schemes()}
    for removed in ["karnataka-free-laptop", "ksbdb-saandeepani", "minority-mcm-technical"]:
        assert removed not in ids


def test_scheme_data_integrity():
    schemes = load_schemes()
    ids = [s["id"] for s in schemes]
    assert len(ids) == len(set(ids))
    for s in schemes:
        for key in ["id", "name", "provider", "benefit", "url", "rules", "verified", "needs_check"]:
            assert key in s, f"{s.get('id')} missing {key}"
        assert s["url"].startswith("https://")
        # Nothing is marked verified until a human has checked the official page
        assert s["verified"] is False


def test_tavily_search_fallback_and_discrepancy():
    orig_key = os.environ.get("TAVILY_API_KEY")
    try:
        os.environ["TAVILY_API_KEY"] = ""
        sample_scheme = {"id": "test-sch", "name": "Karnataka Test Scheme", "state": "Karnataka", "url": "https://karnataka.gov.in"}
        res = search.verify_scheme(sample_scheme)
        assert res["error"] == "Live verification unavailable (no API key)"
        assert len(res["results"]) > 0
        assert "Live verification unavailable" in res["results"][0]["title"]

        # Test discrepancy detector
        closed_results = [{"title": "Portal closed", "snippet": "Applications closed for academic year"}]
        warn = search._check_discrepancies(sample_scheme, closed_results)
        assert warn is not None
        assert "closed" in warn.lower()

        open_results = [{"title": "SSP Portal", "snippet": "Fresh applications are open for students"}]
        assert search._check_discrepancies(sample_scheme, open_results) is None
    finally:
        if orig_key is not None:
            os.environ["TAVILY_API_KEY"] = orig_key
        else:
            os.environ.pop("TAVILY_API_KEY", None)


def test_gap_analysis_details():
    schemes = load_schemes()
    s = _get_scheme_by_id(schemes, "ssp-sc-postmatric")
    # Profile with multiple failures: higher income, wrong category, wrong state
    p = {
        "age": 19,
        "state": "Maharashtra",
        "annual_income": 350000,
        "category": "General",
        "course": "Dance",
        "gender": "Female"
    }
    r = evaluate(p, s)
    assert r["status"] == "not_eligible"
    assert len(r["gaps"]) == 3
    # Income gap must have exact calculation: 350000 - 250000 = 100000
    assert any("100,000 above the cap" in g for g in r["gaps"])
    assert any("Category 'General' is not in the accepted list" in g for g in r["gaps"])
    assert any("State 'Maharashtra' is not in the accepted list" in g for g in r["gaps"])


def test_what_if_simulation_deterministic():
    schemes = load_schemes()
    # Baseline: General student with 350,000 income in Karnataka
    base_profile = {
        "age": 19,
        "state": "Karnataka",
        "annual_income": 350000,
        "category": "General",
        "course": "Engineering",
        "gender": "Male"
    }
    base_res = evaluate_all(base_profile, schemes)
    base_eligible_ids = {r["scheme"]["id"] for r in base_res if r["status"] == "eligible"}
    assert "central-sector-scholarship" in base_eligible_ids
    assert "ssp-bcwd-postmatric" not in base_eligible_ids

    # What-if 1: Category changed to OBC with income 200,000 unlocks BCWD and Vidyasiri
    sim_profile_1 = {**base_profile, "annual_income": 200000, "category": "OBC"}
    sim_res_1 = evaluate_all(sim_profile_1, schemes)
    sim_1_eligible_ids = {r["scheme"]["id"] for r in sim_res_1 if r["status"] == "eligible"}
    assert "ssp-bcwd-postmatric" in sim_1_eligible_ids
    assert "karnataka-vidyasiri" in sim_1_eligible_ids
    assert "karnataka-vidyasiri" not in base_eligible_ids

    # What-if 2: Category changed to SC with 200,000 unlocks the SC scholarship and Vidyasiri
    sim_profile_2 = {**base_profile, "annual_income": 200000, "category": "SC"}
    sim_res_2 = evaluate_all(sim_profile_2, schemes)
    sim_2_eligible_ids = {r["scheme"]["id"] for r in sim_res_2 if r["status"] == "eligible"}
    assert "ssp-sc-postmatric" in sim_2_eligible_ids
    assert "karnataka-vidyasiri" in sim_2_eligible_ids


def test_draft_generator_brackets_for_unknowns():
    orig_mock = os.environ.get("MOCK_MODE")
    try:
        os.environ["MOCK_MODE"] = "true"
        schemes = load_schemes()
        s = _get_scheme_by_id(schemes, "ssp-sc-postmatric")
        # Partial profile with missing course and income
        p = {
            "state": "Karnataka",
            "category": "SC",
            "annual_income": None,
            "course": None,
            "age": 19,
            "gender": "Female"
        }
        draft = llm.draft_declaration(p, s)
        assert "[Course Name]" in draft or "[" in draft
        assert "[Annual Income]" in draft
        assert "[Your Full Name]" in draft
        assert "Karnataka" in draft
        assert "SC" in draft
    finally:
        if orig_mock is not None:
            os.environ["MOCK_MODE"] = orig_mock
        else:
            os.environ.pop("MOCK_MODE", None)


def test_ocr_extract_certificate_in_memory():
    orig_mock = os.environ.get("MOCK_MODE")
    try:
        os.environ["MOCK_MODE"] = "true"
        # Test mock certificate extraction
        dummy_bytes = b"fake-certificate-image-bytes"
        data, is_mock = llm.extract_certificate(dummy_bytes, "image/jpeg")
        assert is_mock is True
        assert "annual_income" in data
        assert "category" in data
        assert data["annual_income"] > 0
        assert data["category"] in ["General", "OBC", "SC", "ST", "EWS"]
    finally:
        if orig_mock is not None:
            os.environ["MOCK_MODE"] = orig_mock
        else:
            os.environ.pop("MOCK_MODE", None)


def test_multilingual_explanation_and_draft():
    orig_mock = os.environ.get("MOCK_MODE")
    try:
        os.environ["MOCK_MODE"] = "true"
        schemes = load_schemes()
        s = _get_scheme_by_id(schemes, "ssp-sc-postmatric")
        p = {
            "state": "Karnataka",
            "category": "SC",
            "annual_income": 150000,
            "course": "Engineering",
            "age": 19,
            "gender": "Female"
        }
        results = evaluate_all(p, schemes)
        # Test English
        exp_en = llm.explain_results(p, results, language="English")
        assert "English" in exp_en or "Eligibility" in exp_en
        # Test Kannada
        exp_kn = llm.explain_results(p, results, language="Kannada")
        assert "Kannada" in exp_kn
        # Test Hindi
        exp_hi = llm.explain_results(p, results, language="Hindi")
        assert "Hindi" in exp_hi

        # Draft generation with language
        draft_en = llm.draft_declaration(p, s, language="English")
        assert "APPLICATION FOR" in draft_en
    finally:
        if orig_mock is not None:
            os.environ["MOCK_MODE"] = orig_mock
        else:
            os.environ.pop("MOCK_MODE", None)



def test_json_parse_fallback_robustness():
    # Valid markdown block
    assert llm._parse_json('```json\n{"age": 20}\n```') == {"age": 20}
    # Surrounding noise
    assert llm._parse_json('Here is the json: {"age": 22, "category": "OBC"} thank you') == {"age": 22, "category": "OBC"}
    # Malformed JSON should not crash, returns empty dict
    assert llm._parse_json('This is not valid json at all { unclosed') == {}
    assert llm._parse_json('') == {}


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)