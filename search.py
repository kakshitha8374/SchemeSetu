"""Tavily live verification: confirm a scheme is still open and attach official sources."""
import datetime
import logging
import os
import re
import time

from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("schemesetu")


def get_tavily_key():
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "TAVILY_API_KEY" in st.secrets:
            return str(st.secrets["TAVILY_API_KEY"])
    except Exception:
        pass
    return os.getenv("TAVILY_API_KEY", "")


def _check_discrepancies(scheme, results):
    """Detect if live search results indicate a scheme is closed or deadline changed."""
    text_corpus = " ".join([f"{r.get('title', '')} {r.get('snippet', '')}" for r in results]).lower()
    
    # Check for closed indications
    closed_keywords = ["closed", "applications closed", "portal closed", "last date is over", "deadline expired"]
    for kw in closed_keywords:
        if kw in text_corpus:
            return f"Notice: Live search snippets suggest applications may be closed ({kw}). Please check the official link directly."
            
    # Check for deadline extension keywords
    if "extended" in text_corpus or "last date extended" in text_corpus:
        return "Notice: Live search mentions a possible deadline extension. Check the official portal for current active dates."
        
    return None


def verify_scheme(scheme, max_results=3, force_refresh=False):
    """Returns a dict with:
    - results: list of {title, url, snippet, is_official}
    - error: str or None
    - verified_date: YYYY-MM-DD or None
    - warning: str or None (e.g. deadline discrepancy)
    Results are cached in st.session_state to conserve API quota.
    """
    sid = scheme.get("id", "scheme")
    cache_key = f"tavily_cache_{sid}"
    
    # Try retrieving from Streamlit session_state cache
    try:
        import streamlit as st
        if not force_refresh and hasattr(st, "session_state") and cache_key in st.session_state:
            return st.session_state[cache_key]
    except Exception:
        pass

    api_key = get_tavily_key().strip()
    if not api_key:
        payload = {
            "results": [
                {
                    "title": "Live verification unavailable (no API key)",
                    "url": scheme.get("url", ""),
                    "snippet": "Live verification is unavailable because TAVILY_API_KEY is not configured in .env or secrets.",
                    "is_official": False,
                }
            ],
            "error": "Live verification unavailable (no API key)",
            "verified_date": None,
            "warning": None,
        }
        return payload

    # Call Tavily with up to 2 retries and timeout
    last_err = None
    for attempt in range(2):
        try:
            from tavily import TavilyClient
            client = TavilyClient(api_key=api_key)
            query = f"{scheme['name']} {scheme.get('state', '')} official application deadline eligibility"
            resp = client.search(query=query, max_results=max_results)
            raw_results = resp.get("results", [])

            processed = []
            for r in raw_results:
                url = r.get("url", "")
                is_official = any(dom in url.lower() for dom in [".gov.in", ".nic.in", "aicte-india.org"])
                processed.append({
                    "title": r.get("title", ""),
                    "url": url,
                    "snippet": (r.get("content") or "")[:350],
                    "is_official": is_official,
                })

            # Sort official .gov.in/.nic.in domains first
            processed.sort(key=lambda x: not x["is_official"])

            today_str = datetime.date.today().isoformat()
            warning = _check_discrepancies(scheme, processed)

            payload = {
                "results": processed,
                "error": None,
                "verified_date": today_str,
                "warning": warning,
            }

            try:
                import streamlit as st
                if hasattr(st, "session_state"):
                    st.session_state[cache_key] = payload
            except Exception:
                pass

            return payload
        except Exception as exc:
            last_err = str(exc)
            time.sleep(0.5)

    fail_payload = {
        "results": [],
        "error": f"Live verification failed: {last_err}",
        "verified_date": None,
        "warning": None,
    }
    return fail_payload


