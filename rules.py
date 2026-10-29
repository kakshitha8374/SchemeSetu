"""Deterministic eligibility engine.

The LLM never decides eligibility. It only turns free text into a profile dict.
This module checks that profile against the rules stored in schemes.json.
"""
import json
from pathlib import Path

PROFILE_FIELDS = ["age", "state", "annual_income", "category", "course", "gender"]


def load_schemes(path="schemes.json"):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _check(criterion, passed, detail, gap=None):
    # passed: True / False / None (None = profile value missing)
    return {"criterion": criterion, "passed": passed, "detail": detail, "gap": gap}


def _in_list(value, allowed):
    return str(value).strip().lower() in [str(a).strip().lower() for a in allowed]


def evaluate(profile, scheme):
    rules = scheme.get("rules", {})
    checks = []

    if "max_income" in rules:
        income = profile.get("annual_income")
        cap = rules["max_income"]
        if income is None:
            checks.append(_check("Family income", None, "Income not provided"))
        else:
            ok = income <= cap
            checks.append(
                _check(
                    "Family income",
                    ok,
                    f"Rs {income:,.0f} vs cap Rs {cap:,.0f}",
                    None if ok else f"Income is Rs {income - cap:,.0f} above the cap",
                )
            )

    for key, label, field in [
        ("categories", "Category", "category"),
        ("states", "State", "state"),
        ("courses", "Course", "course"),
        ("genders", "Gender", "gender"),
    ]:
        if key in rules:
            value = profile.get(field)
            allowed = rules[key]
            if value in (None, ""):
                checks.append(_check(label, None, f"{label} not provided"))
            else:
                ok = _in_list(value, allowed)
                checks.append(
                    _check(
                        label,
                        ok,
                        f"{value} (accepted: {', '.join(allowed)})",
                        None if ok else f"{label} '{value}' is not in the accepted list: {', '.join(allowed)}",
                    )
                )

    age = profile.get("age")
    if "min_age" in rules or "max_age" in rules:
        if age is None:
            checks.append(_check("Age", None, "Age not provided"))
        else:
            lo, hi = rules.get("min_age", 0), rules.get("max_age", 200)
            ok = lo <= age <= hi
            checks.append(
                _check(
                    "Age",
                    ok,
                    f"{age} (allowed {lo}-{hi})",
                    None if ok else f"Age {age} is outside the allowed range {lo}-{hi}",
                )
            )

    failed = [c for c in checks if c["passed"] is False]
    unknown = [c for c in checks if c["passed"] is None]
    if failed:
        status = "not_eligible"
    elif unknown:
        status = "needs_info"
    else:
        status = "eligible"

    return {
        "scheme": scheme,
        "status": status,
        "checks": checks,
        "gaps": [c["gap"] for c in failed if c["gap"]],
        "missing": [c["criterion"] for c in unknown],
    }


def evaluate_all(profile, schemes):
    return [evaluate(profile, s) for s in schemes]


def rank(results, by="benefit"):
    """Eligible first, then needs_info, then not eligible. Within a group sort by benefit or speed."""
    order = {"eligible": 0, "needs_info": 1, "not_eligible": 2}

    def key(r):
        s = r["scheme"]
        if by == "speed":
            secondary = s.get("typical_days", 9999)
        else:
            secondary = -s.get("benefit_amount", 0)
        return (order[r["status"]], secondary)

    return sorted(results, key=key)
