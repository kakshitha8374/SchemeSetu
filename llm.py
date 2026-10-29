"""Token Factory calls (OpenAI-compatible API) using NVIDIA Nemotron models.

FAST_MODEL   -> small model for quick, cheap calls (profile extraction).
STRONG_MODEL -> larger model for reasoning and writing (explanations, drafts).
VISION_MODEL -> optional vision model for certificate OCR.
Set in .env or Streamlit secrets using the exact model IDs shown in the Token Factory model list.
"""
import json
import logging
import os
import re

from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("schemesetu")


def get_setting(key, default=""):
    """Read configuration from Streamlit secrets with fallback to environment variables."""
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return os.getenv(key, default)


def is_mock_mode():
    val = get_setting("MOCK_MODE", "").strip().lower()
    if val in ("true", "1", "yes"):
        return True
    key = get_setting("TOKEN_FACTORY_API_KEY", "").strip()
    return not key


TOKEN_FACTORY_BASE_URL = get_setting("TOKEN_FACTORY_BASE_URL", "https://api.tokenfactory.nebius.com/v1/")
FAST_MODEL = get_setting("FAST_MODEL", "nvidia/nemotron-mini-4b-instruct")
STRONG_MODEL = get_setting("STRONG_MODEL") or FAST_MODEL
VISION_MODEL = get_setting("VISION_MODEL", "")


def _client():
    from openai import OpenAI
    base_url = get_setting("TOKEN_FACTORY_BASE_URL", "https://api.tokenfactory.nebius.com/v1/")
    api_key = get_setting("TOKEN_FACTORY_API_KEY", "")
    return OpenAI(base_url=base_url, api_key=api_key, timeout=30.0)


def _chat(model, system, user, temperature=0.2):
    import time
    last_err = None
    for attempt in range(2):
        try:
            logger.info("Token Factory call to model=%s (attempt %d)", model, attempt + 1)
            resp = _client().chat.completions.create(
                model=model,
                temperature=temperature,
                timeout=30.0,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )
            return resp.choices[0].message.content.strip()
        except Exception as exc:
            last_err = exc
            logger.warning("Token Factory call failed (%s), retry %d/2", type(exc).__name__, attempt + 1)
            time.sleep(1.0)
    raise RuntimeError(f"Nebius Token Factory ({model}) request failed after 2 attempts: {type(last_err).__name__}")


def _parse_json(text):
    try:
        cleaned = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        raw_json = match.group(0) if match else cleaned
        return json.loads(raw_json)
    except Exception as exc:
        logger.warning("Model JSON decoding failed: %s", type(exc).__name__)
        return {}



EXTRACT_SYSTEM = """You extract a student profile from the user's text.
Return ONLY a JSON object with exactly these keys:
age (integer or null), state (string or null), annual_income (number in Indian rupees per year or null),
category (one of "General","OBC","SC","ST","EWS","Other" or null), course (short string such as "Engineering" or null),
gender ("Female","Male","Other" or null).
Convert amounts like "3 lakh" to 300000. Use null for anything not stated. Do not guess."""


def _mock_extract_profile(text):
    """Deterministic parser using regex/keywords for mock mode when no API key is present."""
    res = {
        "age": None,
        "state": None,
        "annual_income": None,
        "category": None,
        "course": None,
        "gender": None,
    }
    if not text or not text.strip():
        return res

    t = text.lower()

    # Age extraction: "20 year old", "20 years old", "20 yo", "20 yr old", "age 20", "age is 20"
    age_match = re.search(r"\b(\d{1,2})\s*(?:years?\s*old|yrs?\s*old|yo\b|yr\b)", t)
    if not age_match:
        age_match = re.search(r"\bage\s*(?:is|:)?\s*(\d{1,2})\b", t)
    if not age_match:
        # Also check "i'm 20" or "i am 20,"
        age_match = re.search(r"\b(?:i'?m|i am)\s+(\d{1,2})\b", t)
    if age_match:
        val = int(age_match.group(1))
        if 5 <= val <= 100:
            res["age"] = val

    # State extraction
    known_states = [
        "Karnataka", "Tamil Nadu", "Kerala", "Maharashtra", "Andhra Pradesh",
        "Telangana", "Delhi", "Uttar Pradesh", "Bihar", "Rajasthan",
        "West Bengal", "Gujarat", "Madhya Pradesh", "Punjab", "Haryana", "Odisha"
    ]
    for st_name in known_states:
        if re.search(r"\b" + re.escape(st_name.lower()) + r"\b", t):
            res["state"] = st_name
            break

    # Income extraction: e.g. "3 lakh", "2.5 lakhs", "1.5 lpa", "Rs 300000", "income is 3,00,000", "80000 yearly"
    lakh_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:lakhs?|lpa|lac)\b", t)
    if lakh_match:
        res["annual_income"] = int(float(lakh_match.group(1)) * 100000)
    else:
        # look for explicit numbers like 300000, 3,00,000, 80000
        rupee_match = re.search(r"(?:rs\.?|inr|₹)?\s*([0-9]{1,2}(?:,[0-9]{2,3})*(?:,[0-9]{3})|[0-9]{4,8})\s*(?:per\s*(?:year|annum)|yearly|annually|annual|income)?", t)
        if rupee_match:
            raw_num = rupee_match.group(1).replace(",", "")
            if raw_num.isdigit():
                val = int(raw_num)
                # check if this is not the age
                if val != res.get("age") and val >= 1000:
                    res["annual_income"] = val

    # Category extraction: General, OBC, SC, ST, EWS
    cat_patterns = [
        (r"\b(?:sc|scheduled\s+caste)\b", "SC"),
        (r"\b(?:st|scheduled\s+tribe)\b", "ST"),
        (r"\b(?:obc|other\s+backward\s+class(?:es)?)\b", "OBC"),
        (r"\b(?:ews|economically\s+weaker\s+section)\b", "EWS"),
        (r"\b(?:general|gen|unreserved|ur)\b", "General"),
    ]
    for pattern, cat in cat_patterns:
        if re.search(pattern, t):
            res["category"] = cat
            break

    # Gender extraction
    if re.search(r"\b(?:female|girl|woman|women|daughter)\b", t):
        res["gender"] = "Female"
    elif re.search(r"\b(?:male|boy|man|men|son)\b", t):
        res["gender"] = "Male"
    elif re.search(r"\b(?:transgender|other)\b", t):
        res["gender"] = "Other"

    # Course extraction
    course_patterns = [
        (r"\b(?:engineering|b\.?tech|b\.?e\.?)\b", "Engineering"),
        (r"\b(?:medicine|medical|mbbs|bams|bhms)\b", "Medicine"),
        (r"\b(?:commerce|b\.?com|m\.?com|bba|mba)\b", "Commerce"),
        (r"\b(?:science|b\.?sc|m\.?sc)\b", "Science"),
        (r"\b(?:arts|b\.?a|m\.?a|humanities)\b", "Arts"),
        (r"\b(?:diploma|polytechnic)\b", "Diploma"),
        (r"\b(?:law|llb)\b", "Law"),
        (r"\b(?:pharmacy|b\.?pharm)\b", "Pharmacy"),
        (r"\b(?:nursing)\b", "Nursing"),
    ]
    for pattern, c_name in course_patterns:
        if re.search(pattern, t):
            res["course"] = c_name
            break

    return res


def extract_profile(text):
    """Turns free text into a structured profile. The LLM never decides eligibility."""
    keys = ["age", "state", "annual_income", "category", "course", "gender"]
    if is_mock_mode():
        return _mock_extract_profile(text)
    try:
        raw = _chat(FAST_MODEL, EXTRACT_SYSTEM, text, temperature=0)
        data = _parse_json(raw)
        if not isinstance(data, dict):
            data = {}
        return {k: data.get(k) for k in keys}
    except Exception as exc:
        logger.warning("extract_profile fallback to manual entry on error: %s", type(exc).__name__)
        return {k: None for k in keys}



EXPLAIN_SYSTEM = """You explain scholarship eligibility results to a student in simple, friendly English.
Use ONLY the facts in the JSON you are given. Never invent amounts, deadlines or rules.
For each scheme: say if they qualify, why, and for schemes they miss, state the exact gap given.
Keep it under 200 words and end with one suggested next step."""


def _mock_explain_results(profile, results, language="English"):
    eligible = [r for r in results if r["status"] == "eligible"]
    needs_info = [r for r in results if r["status"] == "needs_info"]
    not_eligible = [r for r in results if r["status"] == "not_eligible"]

    lines = []
    lines.append(f"**Eligibility Summary ({language})**\n")
    if eligible:
        lines.append(f"Great news! You currently qualify for **{len(eligible)} scheme(s)**:")
        for r in eligible:
            s = r["scheme"]
            lines.append(f"- **{s['name']}**: Benefit of {s.get('benefit', 'N/A')} (Deadline: {s.get('deadline', 'N/A')}).")
    else:
        lines.append("You currently do not have fully confirmed eligible schemes based on the provided details.")

    if needs_info:
        lines.append(f"\n**{len(needs_info)} scheme(s) need more information**:")
        for r in needs_info:
            s = r["scheme"]
            missing_str = ", ".join(r["missing"]) if r["missing"] else "additional verification"
            lines.append(f"- **{s['name']}**: Missing {missing_str}.")

    if not_eligible:
        lines.append(f"\n**Schemes not eligible ({len(not_eligible)})**:")
        for r in not_eligible:
            s = r["scheme"]
            gap_str = "; ".join(r["gaps"]) if r["gaps"] else "Criteria not met"
            lines.append(f"- **{s['name']}**: {gap_str}.")

    lines.append("\n**Next step:** Gather your income and caste certificates, check official portal deadlines, and proceed to draft your applications.")
    return "\n".join(lines)


def explain_results(profile, results, language="English"):
    if is_mock_mode():
        return _mock_explain_results(profile, results, language)
    compact = [
        {
            "scheme": r["scheme"]["name"],
            "status": r["status"],
            "gaps": r["gaps"],
            "missing_info": r["missing"],
            "benefit": r["scheme"].get("benefit"),
            "deadline": r["scheme"].get("deadline"),
        }
        for r in results
    ]
    sys_prompt = EXPLAIN_SYSTEM
    if language and language.lower() != "english":
        sys_prompt += f"\nRespond in {language}."
    payload = json.dumps({"profile": profile, "results": compact, "language": language}, ensure_ascii=False)
    return _chat(STRONG_MODEL, sys_prompt, payload)


DRAFT_SYSTEM = """You draft a short self-declaration / statement of purpose for a scholarship application.
Use only the profile details provided. Put unknown details in [square brackets] for the student to fill in.
Keep it formal, honest and under 180 words. Do not claim anything not in the profile."""


def _mock_draft_declaration(profile, scheme, language="English"):
    name_ph = "[Your Full Name]"
    parent_ph = "[Parent/Guardian Name]"
    inst_ph = "[Institution/College Name]"
    course = profile.get("course") or "[Course Name]"
    state = profile.get("state") or "[State]"
    income = f"Rs {profile['annual_income']:,}" if profile.get("annual_income") is not None else "[Annual Income]"
    category = profile.get("category") or "[Category]"

    scheme_name = scheme.get("name", "Scholarship")
    provider = scheme.get("provider", "the Competent Authority")

    return f"""TO WHOM IT MAY CONCERN

APPLICATION FOR: {scheme_name}
SUBMITTED TO: {provider}

Respected Authority,

I, {name_ph}, son/daughter of {parent_ph}, am a resident of {state}. I am currently enrolled in and pursuing {course} at {inst_ph}.

I belong to the {category} category. My family's total annual income from all sources is {income}, as certified by the competent revenue authority. 

I solemnly declare that the information stated above and documents submitted in support of my application for {scheme_name} are true, complete, and authentic to the best of my knowledge. If any detail is found incorrect, my candidature may be cancelled.

Sincerely,

{name_ph}
Date: [DD/MM/YYYY]
Place: [City/Town, {state}]"""


def draft_declaration(profile, scheme, language="English"):
    if is_mock_mode():
        return _mock_draft_declaration(profile, scheme, language)
    user_payload = {
        "profile": profile,
        "scheme": scheme.get("name"),
        "provider": scheme.get("provider"),
        "language": language
    }
    sys_prompt = DRAFT_SYSTEM
    if language and language.lower() != "english":
        sys_prompt += f"\nDraft in {language}."
    return _chat(STRONG_MODEL, sys_prompt, json.dumps(user_payload), temperature=0.4)


def extract_certificate(file_bytes_or_buffer, mime_type="image/jpeg"):
    """Extract annual income and category from a certificate image or PDF page.
    Returns (data, is_mock). Always requires user confirmation in the UI.
    """
    if is_mock_mode() or not get_setting("VISION_MODEL", "").strip():
        # Deterministic sample output clearly marked as mock
        return {
            "annual_income": 180000,
            "category": "OBC",
            "confidence_note": "Sample extracted values (Mock Mode / Vision model unconfigured). Please verify and edit before saving."
        }, True

    # Real vision model call with retry and fallback
    import base64
    import time
    from openai import OpenAI
    client = OpenAI(
        base_url=get_setting("TOKEN_FACTORY_BASE_URL", "https://api.tokenfactory.nebius.com/v1/"),
        api_key=get_setting("TOKEN_FACTORY_API_KEY", ""),
        timeout=30.0,
    )
    b64 = base64.b64encode(file_bytes_or_buffer).decode("utf-8")
    vision_model = get_setting("VISION_MODEL")
    prompt = (
        "Examine this Indian government income/caste certificate or document. "
        "Extract the annual income (number in rupees) and caste category (General, OBC, SC, ST, EWS). "
        "Return ONLY a JSON object with keys: annual_income (number or null), category (string or null). "
        "Do not invent facts."
    )
    for attempt in range(2):
        try:
            logger.info("Calling vision model=%s (attempt %d)", vision_model, attempt + 1)
            resp = client.chat.completions.create(
                model=vision_model,
                timeout=30.0,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{b64}"}}
                        ]
                    }
                ],
                temperature=0.1
            )
            content = resp.choices[0].message.content.strip()
            data = _parse_json(content)
            if not isinstance(data, dict):
                data = {}
            return data, False
        except Exception as exc:
            logger.warning("Vision model call failed (%s), attempt %d/2", type(exc).__name__, attempt + 1)
            time.sleep(1.0)
    return {"annual_income": None, "category": None}, False


