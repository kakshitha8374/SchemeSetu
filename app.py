import datetime
import html
import json
import os
import pandas as pd
import streamlit as st

import llm
import search
from rules import PROFILE_FIELDS, evaluate_all, load_schemes, rank

# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SchemeSetu | National Student Scholarship Portal",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------------------------
# Clean Government Portal Responsive CSS
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Global Viewport & Scrollbar Constraints */
    html, body, [class*="css"], [data-testid="stAppViewContainer"] {
        overflow-x: hidden !important;
        word-break: break-word;
        overflow-wrap: anywhere;
        background-color: #F8FAFC !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
    }

    /* Centered responsive container (Max 1120px) */
    .block-container {
        width: 100% !important;
        max-width: 1120px !important;
        margin: 0 auto !important;
        padding-left: 24px !important;
        padding-right: 24px !important;
        padding-top: 0.5rem !important;
        padding-bottom: 2.5rem !important;
        box-sizing: border-box !important;
    }

    /* Top Navy Government Bar */
    .gov-topbar {
        background-color: #0A1C36;
        color: #CBD5E1;
        font-size: 11.5px;
        padding: 6px 16px;
        margin: -0.5rem -24px 0.75rem -24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 8px;
    }
    .gov-topbar a {
        color: #E2E8F0;
        text-decoration: none;
    }
    .gov-topbar a:hover {
        text-decoration: underline;
    }

    /* Main Institutional Header */
    .gov-header {
        background-color: #FFFFFF;
        border-bottom: 1px solid #E2E8F0;
        padding: 12px 18px;
        margin: 0 -24px 1rem -24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
    }
    .gov-brand {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .gov-brand-icon {
        width: 44px;
        height: 44px;
        background-color: #FFFBEB;
        border: 2px solid #D97706;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        color: #92400E;
    }
    .gov-brand-titles {
        display: flex;
        flex-direction: column;
    }
    .gov-dept {
        font-size: 10.5px;
        font-weight: 700;
        letter-spacing: 0.08em;
        color: #1E3A8A;
        text-transform: uppercase;
    }
    .gov-appname {
        font-size: 22px;
        font-weight: 800;
        color: #0A1C36;
        line-height: 1.15;
    }
    .gov-tagline {
        font-size: 12px;
        color: #64748B;
    }

    /* Yellow Demo Mode / Advisory Bar */
    .gov-demo-banner {
        background-color: #FFFBEB;
        border: 1px solid #FDE68A;
        color: #92400E;
        font-size: 13px;
        padding: 9px 16px;
        border-radius: 6px;
        margin-bottom: 1.25rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Hero Section */
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: #EFF6FF;
        color: #1D4ED8;
        border: 1px solid #DBEAFE;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 12.5px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .hero-heading {
        font-size: 28px;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 6px;
        line-height: 1.25;
    }
    .hero-subheading {
        font-size: 14.5px;
        color: #64748B;
        margin-bottom: 1.5rem;
        line-height: 1.5;
    }

    /* Horizontal 3-Step Progress Cards */
    .progress-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 14px;
        margin-bottom: 1.5rem;
    }
    .progress-step-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 12px 16px;
        display: flex;
        align-items: center;
        gap: 12px;
        transition: all 0.2s ease;
    }
    .progress-step-card.active {
        background-color: #FFFFFF;
        border: 2px solid #0A1C36;
        box-shadow: 0 2px 4px rgba(10, 28, 54, 0.08);
    }
    .progress-step-num {
        width: 28px;
        height: 28px;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13.5px;
        font-weight: 700;
        background-color: #E2E8F0;
        color: #475569;
        flex-shrink: 0;
    }
    .progress-step-card.active .progress-step-num {
        background-color: #0A1C36;
        color: #FFFFFF;
    }
    .progress-step-title {
        font-size: 14px;
        font-weight: 700;
        color: #1E293B;
        line-height: 1.2;
    }
    .progress-step-desc {
        font-size: 11.5px;
        color: #64748B;
        line-height: 1.2;
        margin-top: 2px;
    }

    /* Main Form Card */
    .white-form-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 22px 24px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
        margin-bottom: 1.5rem;
    }
    .form-card-header {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #F1F5F9;
    }
    .form-step-badge {
        width: 32px;
        height: 32px;
        background-color: #0A1C36;
        color: #FFFFFF;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        font-weight: 700;
        flex-shrink: 0;
    }
    .form-card-title {
        font-size: 18px;
        font-weight: 700;
        color: #0F172A;
        margin: 0;
    }
    .form-card-subtitle {
        font-size: 13.5px;
        color: #64748B;
        margin: 2px 0 0 0;
    }

    /* Sidebar Help Cards */
    .sidebar-help-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px 18px;
        margin-bottom: 14px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
    }
    .sidebar-help-title {
        font-size: 14.5px;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .sidebar-help-text {
        font-size: 13px;
        color: #475569;
        line-height: 1.45;
    }
    .sidebar-help-link {
        display: inline-block;
        margin-top: 8px;
        font-size: 12.5px;
        font-weight: 600;
        color: #1D4ED8;
        text-decoration: underline;
    }

    /* Scheme Result Cards */
    .scheme-result-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 18px 20px;
        margin-bottom: 14px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
    }
    .scheme-result-card.eligible {
        border-left: 5px solid #16A34A;
    }
    .scheme-result-card.needs_info {
        border-left: 5px solid #D97706;
    }
    .scheme-result-card.not_eligible {
        border-left: 5px solid #DC2626;
    }

    /* Badges */
    .badge-eligible {
        background-color: #DCFCE7;
        color: #15803D;
        font-weight: 700;
        font-size: 12px;
        padding: 3px 8px;
        border-radius: 4px;
        display: inline-block;
    }
    .badge-needs-info {
        background-color: #FEF3C7;
        color: #92400E;
        font-weight: 700;
        font-size: 12px;
        padding: 3px 8px;
        border-radius: 4px;
        display: inline-block;
    }
    .badge-not-eligible {
        background-color: #FEE2E2;
        color: #991B1B;
        font-weight: 700;
        font-size: 12px;
        padding: 3px 8px;
        border-radius: 4px;
        display: inline-block;
    }

    /* Form Controls & Inputs */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        min-height: 40px !important;
        border-radius: 6px !important;
        border-color: #CBD5E1 !important;
        font-size: 14px !important;
    }

    /* Saffron Primary Buttons */
    button[kind="primary"], [data-testid="baseButton-primary"] {
        background-color: #9A3412 !important; /* Authentic Saffron / Rust */
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 14.5px !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 10px 24px !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
    }
    button[kind="primary"]:hover, [data-testid="baseButton-primary"]:hover {
        background-color: #7C2D12 !important;
        color: #FFFFFF !important;
    }

    /* Secondary Buttons */
    button[kind="secondary"], [data-testid="baseButton-secondary"] {
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        border: 1px solid #CBD5E1 !important;
        font-weight: 600 !important;
        font-size: 13.5px !important;
        border-radius: 6px !important;
    }
    button[kind="secondary"]:hover, [data-testid="baseButton-secondary"]:hover {
        background-color: #F8FAFC !important;
        border-color: #94A3B8 !important;
    }

    /* Official Government Footer */
    .gov-footer {
        background-color: #0A1C36;
        color: #94A3B8;
        padding: 24px 20px;
        margin: 2.5rem -24px -2.5rem -24px;
        font-size: 12.5px;
    }
    .gov-footer-inner {
        max-width: 1120px;
        margin: 0 auto;
        padding: 0 4px;
    }
    .gov-footer-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        margin-bottom: 16px;
    }
    .gov-footer-brand {
        font-size: 16px;
        font-weight: 700;
        color: #FFFFFF;
    }
    .gov-footer-sub {
        font-size: 12px;
        color: #94A3B8;
    }
    .gov-footer-links a {
        color: #CBD5E1;
        text-decoration: none;
        margin-left: 14px;
    }
    .gov-footer-links a:hover {
        color: #FFFFFF;
        text-decoration: underline;
    }
    .gov-footer-divider {
        height: 1px;
        background-color: rgba(255, 255, 255, 0.1);
        margin: 12px 0;
    }

    /* Responsive Breakdown: Stack Sidebar Below Form at < 1050px */
    @media (max-width: 1050px) {
        [data-testid="stHorizontalBlock"]:has(.help-sidebar-container) {
            flex-direction: column !important;
            display: flex !important;
        }
        [data-testid="stHorizontalBlock"]:has(.help-sidebar-container) > [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }
    }

    /* Responsive Breakdown: Mobile Viewport (< 640px) */
    @media (max-width: 640px) {
        .progress-grid {
            grid-template-columns: 1fr !important;
        }
        [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            display: flex !important;
        }
        [data-testid="stHorizontalBlock"] > [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }
        .hero-heading {
            font-size: 22px !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Data & Constants
# -----------------------------------------------------------------------------
schemes = load_schemes()
CATEGORIES = ["General", "OBC", "SC", "ST", "EWS", "Other"]
GENDERS = ["Female", "Male", "Other"]
INDIAN_STATES = [
    "Karnataka", "Andhra Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Delhi", "Goa", "Gujarat", "Haryana", "Himachal Pradesh",
    "Jharkhand", "Kerala", "Madhya Pradesh", "Maharashtra", "Odisha",
    "Punjab", "Rajasthan", "Tamil Nadu", "Telangana", "Uttar Pradesh",
    "Uttarakhand", "West Bengal", "Other States / UTs"
]

# Session state defaults
st.session_state.setdefault("wizard_step", 1)
st.session_state.setdefault("input_age", 20)
st.session_state.setdefault("input_state", "Karnataka")
st.session_state.setdefault("input_income", 300000)
st.session_state.setdefault("input_category", "OBC")
st.session_state.setdefault("input_course", "Engineering")
st.session_state.setdefault("input_gender", "Female")
st.session_state.setdefault("text_desc", "I am a 20 year old OBC girl from Karnataka studying engineering. My family income is about 3 lakh.")
st.session_state.setdefault("extracted_missing", None)
st.session_state.setdefault("app_language", "English")
st.session_state.setdefault("portal_view", "student")

# -----------------------------------------------------------------------------
# 1. Top Government Bar
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="gov-topbar">
        <div>Government of India &middot; Student Services Portal</div>
        <div>
            <a href="#main">Skip to main content</a> &nbsp;|&nbsp;
            <a href="#accessibility">Screen reader access</a> &nbsp;|&nbsp;
            <span>Helpline: <strong>1800 11 8000</strong></span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 2. Main Institutional Header with SchemeSetu Branding & Utility Links
# -----------------------------------------------------------------------------
head_col1, head_col2 = st.columns([3.2, 1.2])

with head_col1:
    st.markdown(
        """
        <div class="gov-brand">
            <div class="gov-brand-icon">🏛️</div>
            <div class="gov-brand-titles">
                <span class="gov-dept">NATIONAL STUDENT SERVICES</span>
                <span class="gov-appname">SchemeSetu</span>
                <span class="gov-tagline">Discover scholarships and welfare schemes</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with head_col2:
    selected_language = st.selectbox(
        "🌐 Language / भाषा",
        ["English", "हिंदी (Hindi)", "ಕನ್ನಡ (Kannada)"],
        index=0,
        label_visibility="collapsed",
        key="global_lang_select",
    )
    st.session_state["app_language"] = selected_language

# -----------------------------------------------------------------------------
# 3. Yellow Demo Mode / Advisory Banner
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="gov-demo-banner">
        <span>⚠️</span>
        <span><strong>Demo mode:</strong> Results are illustrative. Please verify eligibility and apply only through the official government portal.</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# Compact Collapsible Architecture Transparency
with st.expander("ℹ️ How this was answered & Official Advisory Information", expanded=False):
    fast_m = llm.get_setting("FAST_MODEL", "nvidia/nemotron-mini-4b-instruct")
    strong_m = llm.get_setting("STRONG_MODEL") or fast_m
    has_tavily = bool(search.get_tavily_key())
    st.markdown(f"""
    - **Models:** Profile parsing with **NVIDIA Nemotron Fast** (`{fast_m}`). Explanations and drafts with **Nemotron Strong** (`{strong_m}`).
    - **Deterministic Rules:** Eligibility is verified strictly by deterministic code in `rules.py` against official criteria in `schemes.json`. *The LLM never decides eligibility.*
    - **Live Verification:** {'*Offline Notice (TAVILY_API_KEY not set)*' if not has_tavily else '**Tavily Search API** with `.gov.in` and `.nic.in` link matching'}.
    """)

# Navigation Switcher between Student Portal and CSC Operator Screening
portal_mode = st.radio(
    "Select Mode",
    ["🎓 Student Discovery (3-Step Guided Check)", "🏢 CSC Operator Batch Screening"],
    index=0 if st.session_state["portal_view"] == "student" else 1,
    horizontal=True,
    label_visibility="collapsed",
    key="nav_mode_radio"
)
st.session_state["portal_view"] = "student" if "Student Discovery" in portal_mode else "operator"

# =============================================================================
# VIEW A: CSC OPERATOR BATCH SCREENING
# =============================================================================
if st.session_state["portal_view"] == "operator":
    st.subheader("🏢 CSC Operator Batch Screening")
    st.caption("Upload a roster of students to screen all active government scholarships simultaneously.")

    sample_csv_data = (
        "name,age,state,annual_income,category,course,gender\n"
        "Priya Sharma,20,Karnataka,200000,OBC,Engineering,Female\n"
        "Ramesh Kumar,19,Karnataka,120000,SC,Science,Male\n"
        "Ananya Rao,21,Karnataka,400000,General,Commerce,Female\n"
        "Suresh Nayak,18,Karnataka,80000,ST,Diploma,Male\n"
        "Amina Bi,20,Karnataka,180000,Other,Medicine,Female\n"
    )
    st.download_button(
        "📥 Download Sample CSV Template",
        data=sample_csv_data,
        file_name="schemesetu_sample_students.csv",
        mime="text/csv",
        use_container_width=True,
    )

    uploaded_csv = st.file_uploader("Upload Student Batch CSV", type="csv", key="csc_csv_uploader")
    if uploaded_csv:
        df = pd.read_csv(uploaded_csv)
        rows = []
        for _, row in df.iterrows():
            prof = {
                "age": None if pd.isna(row.get("age")) else int(row["age"]),
                "state": row.get("state"),
                "annual_income": None if pd.isna(row.get("annual_income")) else float(row["annual_income"]),
                "category": row.get("category"),
                "course": row.get("course"),
                "gender": row.get("gender"),
            }
            eval_res = evaluate_all(prof, schemes)
            ok = [r["scheme"]["name"] for r in eval_res if r["status"] == "eligible"]
            needs = [r["scheme"]["name"] for r in eval_res if r["status"] == "needs_info"]
            rows.append({
                "Student Name": row.get("name", "Unknown"),
                "Eligible Count": len(ok),
                "Eligible Schemes": "; ".join(ok) if ok else "None",
                "Needs More Info": "; ".join(needs) if needs else "None",
            })
        results_df = pd.DataFrame(rows)
        st.dataframe(results_df, use_container_width=True)

        st.download_button(
            "📥 Download Screened Results CSV",
            data=results_df.to_csv(index=False),
            file_name="screened_student_results.csv",
            mime="text/csv",
            use_container_width=True,
        )

# =============================================================================
# VIEW B: STUDENT 3-STEP GUIDED WIZARD
# =============================================================================
else:
    # Hero Title & Subtitle
    st.markdown(
        """
        <div class="hero-badge">✨ Find support made for you</div>
        <h1 class="hero-heading">Find scholarships and schemes you may be eligible for</h1>
        <p class="hero-subheading">Complete a short step-by-step check. You stay in control of your information before viewing any recommendations.</p>
        """,
        unsafe_allow_html=True,
    )

    current_step = st.session_state["wizard_step"]

    # -------------------------------------------------------------------------
    # Horizontal 3-Step Progress Cards
    # -------------------------------------------------------------------------
    step1_active = "active" if current_step == 1 else ""
    step2_active = "active" if current_step == 2 else ""
    step3_active = "active" if current_step == 3 else ""

    st.markdown(
        f"""
        <div class="progress-grid">
            <div class="progress-step-card {step1_active}">
                <div class="progress-step-num">1</div>
                <div>
                    <div class="progress-step-title">Share your details</div>
                    <div class="progress-step-desc">Takes about 2 minutes</div>
                </div>
            </div>
            <div class="progress-step-card {step2_active}">
                <div class="progress-step-num">2</div>
                <div>
                    <div class="progress-step-title">Review your information</div>
                    <div class="progress-step-desc">Check before matching</div>
                </div>
            </div>
            <div class="progress-step-card {step3_active}">
                <div class="progress-step-num">3</div>
                <div>
                    <div class="progress-step-title">See your matches</div>
                    <div class="progress-step-desc">Clear reasons, no jargon</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -------------------------------------------------------------------------
    # STEP 1: SHARE YOUR DETAILS
    # -------------------------------------------------------------------------
    if current_step == 1:
        col_main, col_sidebar = st.columns([2.3, 1.0])

        with col_main:
            # White Card Header
            st.markdown(
                """
                <div class="white-form-card">
                    <div class="form-card-header">
                        <div class="form-step-badge">1</div>
                        <div>
                            <h2 class="form-card-title">Share your details</h2>
                            <p class="form-card-subtitle">Tell us a little about yourself. You can use plain language; this takes about 2 minutes.</p>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Natural Language Description
            text_input = st.text_area(
                "Describe yourself in your own words",
                value=st.session_state["text_desc"],
                placeholder="e.g. I am a 20 year old OBC girl from Karnataka studying engineering. My family income is about 3 lakh.",
                height=90,
                help="Natural language input is parsed by NVIDIA Nemotron Fast Model.",
                key="text_desc_input",
            )
            st.session_state["text_desc"] = text_input
            st.caption("For example: your age, state, category, course and family income.")

            if st.button("🔍 Extract Details from Description", use_container_width=False, key="btn_extract"):
                if text_input.strip():
                    try:
                        with st.spinner("Extracting profile attributes with Nemotron Fast Model..."):
                            p = llm.extract_profile(text_input)

                        if p.get("age") is not None:
                            st.session_state["input_age"] = int(p["age"])
                        if p.get("state") and p["state"] in INDIAN_STATES:
                            st.session_state["input_state"] = p["state"]
                        if p.get("annual_income") is not None:
                            st.session_state["input_income"] = int(p["annual_income"])
                        if p.get("category") and p["category"] in CATEGORIES:
                            st.session_state["input_category"] = p["category"]
                        if p.get("course"):
                            st.session_state["input_course"] = p["course"]
                        if p.get("gender") and p["gender"] in GENDERS:
                            st.session_state["input_gender"] = p["gender"]

                        missing = []
                        if p.get("age") is None: missing.append("Age")
                        if not p.get("state"): missing.append("State")
                        if p.get("annual_income") is None: missing.append("Family income")
                        if not p.get("category"): missing.append("Category")
                        if not p.get("course"): missing.append("Course")
                        if not p.get("gender"): missing.append("Gender")
                        st.session_state["extracted_missing"] = missing
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Extraction failed: {exc}")

            if st.session_state.get("extracted_missing") is not None:
                missing = st.session_state["extracted_missing"]
                if missing:
                    st.info(f"💡 Extracted details applied! Please confirm or fill remaining fields: **{', '.join(missing)}**.")
                else:
                    st.success("✅ All details successfully extracted! Please check them below.")

            st.write("")

            # 2-Column Form Fields (Stacked on mobile < 640px)
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                cur_age = st.session_state.get("input_age") or 20
                age_val = st.number_input("Age *", min_value=10, max_value=100, value=int(cur_age), key="w_age")
                st.session_state["input_age"] = age_val

                cur_course = st.session_state.get("input_course") or "Engineering"
                course_val = st.text_input("Course / Stream *", value=cur_course, placeholder="e.g. Engineering", key="w_course")
                st.session_state["input_course"] = course_val

                cur_inc = st.session_state.get("input_income") or 300000
                inc_val = st.number_input("Annual Family Income (₹) *", min_value=0, max_value=100000000, step=10000, value=int(cur_inc), key="w_income")
                st.session_state["input_income"] = inc_val

            with col_f2:
                cur_gen = st.session_state.get("input_gender") or "Female"
                gen_idx = GENDERS.index(cur_gen) if cur_gen in GENDERS else 0
                gender_val = st.selectbox("Gender *", GENDERS, index=gen_idx, key="w_gender")
                st.session_state["input_gender"] = gender_val

                cur_state = st.session_state.get("input_state") or "Karnataka"
                state_idx = INDIAN_STATES.index(cur_state) if cur_state in INDIAN_STATES else 0
                state_val = st.selectbox("State of Domicile *", INDIAN_STATES, index=state_idx, key="w_state")
                st.session_state["input_state"] = state_val

                cur_cat = st.session_state.get("input_category") or "OBC"
                cat_idx = CATEGORIES.index(cur_cat) if cur_cat in CATEGORIES else 1
                cat_val = st.selectbox("Caste / Social Category *", CATEGORIES, index=cat_idx, key="w_category")
                st.session_state["input_category"] = cat_val

            # Optional OCR Certificate Upload Expander
            has_vision = bool(llm.get_setting("VISION_MODEL", "").strip()) or llm.is_mock_mode()
            if has_vision:
                with st.expander("📄 Optional: Upload Income or caste certificate (OCR autofill)", expanded=False):
                    st.caption("Document is processed in-memory only — never saved to disk or logged.")
                    cert_file = st.file_uploader("Upload Scanned Certificate", type=["png", "jpg", "jpeg", "pdf"], key="cert_ocr_file")
                    if cert_file is not None:
                        if st.button("Extract from Certificate", key="btn_run_ocr"):
                            try:
                                with st.spinner("Extracting certificate data in memory..."):
                                    ocr_data, _ = llm.extract_certificate(cert_file.read(), cert_file.type or "image/jpeg")
                                    st.session_state["ocr_res"] = ocr_data
                            except Exception as err:
                                st.error(f"OCR failed: {err}")

                    if "ocr_res" in st.session_state:
                        ocr_d = st.session_state["ocr_res"]
                        st.info(f"Detected Income: ₹{ocr_d.get('annual_income', 'N/A')}, Category: {ocr_d.get('category', 'N/A')}")
                        if st.button("Apply Certificate Data to Form", key="btn_apply_ocr"):
                            if ocr_d.get("annual_income") is not None:
                                st.session_state["input_income"] = int(ocr_d["annual_income"])
                            if ocr_d.get("category") in CATEGORIES:
                                st.session_state["input_category"] = ocr_d["category"]
                            del st.session_state["ocr_res"]
                            st.success("Applied certificate details!")
                            st.rerun()

            st.write("")
            # Saffron Continue Button
            if st.button("Continue to review →", type="primary", use_container_width=True, key="btn_goto_review"):
                st.session_state["wizard_step"] = 2
                st.rerun()

        # Right Column: Trust & Assistance Cards
        with col_sidebar:
            st.markdown(
                """
                <div class="help-sidebar-container">
                    <div class="sidebar-help-card">
                        <div class="sidebar-help-title">🛡️ Your privacy matters</div>
                        <div class="sidebar-help-text">
                            We only use your information to show relevant schemes. Never share OTPs, passwords, or bank details here.
                        </div>
                        <a href="#privacy" class="sidebar-help-link">Read privacy policy &nearr;</a>
                    </div>
                    <div class="sidebar-help-card">
                        <div class="sidebar-help-title">📋 How it works</div>
                        <div class="sidebar-help-text">
                            <div style="margin-bottom: 6px;"><strong>01</strong> Share only basic information.</div>
                            <div style="margin-bottom: 6px;"><strong>02</strong> Review everything before matching.</div>
                            <div><strong>03</strong> Open official links to apply.</div>
                        </div>
                    </div>
                    <div class="sidebar-help-card">
                        <div class="sidebar-help-title">❓ Need help?</div>
                        <div class="sidebar-help-text">
                            Contact the National Student Helpline for application support.
                            <div style="font-size: 17px; font-weight: 800; color: #0A1C36; margin-top: 6px;">1800-11-8000</div>
                            <div style="font-size: 11.5px; color: #64748B;">Mon&ndash;Fri, 9:00 AM&ndash;6:00 PM</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # -------------------------------------------------------------------------
    # STEP 2: REVIEW YOUR INFORMATION
    # -------------------------------------------------------------------------
    elif current_step == 2:
        st.markdown(
            """
            <div class="white-form-card">
                <div class="form-card-header">
                    <div class="form-step-badge">2</div>
                    <div>
                        <h2 class="form-card-title">Review your information</h2>
                        <p class="form-card-subtitle">Please verify your entered details before finding scholarship matches.</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Summary Grid
        st.markdown(
            f"""
            <div class="white-form-card" style="margin-top: -0.5rem;">
                <h3 style="font-size: 16px; font-weight: 700; color: #0F172A; margin-bottom: 12px;">Candidate Profile Summary</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; font-size: 14px;">
                    <div style="background-color: #F8FAFC; padding: 12px 14px; border-radius: 6px; border: 1px solid #E2E8F0;">
                        <span style="color: #64748B; font-size: 12px; display: block;">AGE</span>
                        <strong>{st.session_state['input_age']} years</strong>
                    </div>
                    <div style="background-color: #F8FAFC; padding: 12px 14px; border-radius: 6px; border: 1px solid #E2E8F0;">
                        <span style="color: #64748B; font-size: 12px; display: block;">GENDER</span>
                        <strong>{st.session_state['input_gender']}</strong>
                    </div>
                    <div style="background-color: #F8FAFC; padding: 12px 14px; border-radius: 6px; border: 1px solid #E2E8F0;">
                        <span style="color: #64748B; font-size: 12px; display: block;">STATE OF DOMICILE</span>
                        <strong>{st.session_state['input_state']}</strong>
                    </div>
                    <div style="background-color: #F8FAFC; padding: 12px 14px; border-radius: 6px; border: 1px solid #E2E8F0;">
                        <span style="color: #64748B; font-size: 12px; display: block;">SOCIAL CATEGORY</span>
                        <strong>{st.session_state['input_category']}</strong>
                    </div>
                    <div style="background-color: #F8FAFC; padding: 12px 14px; border-radius: 6px; border: 1px solid #E2E8F0;">
                        <span style="color: #64748B; font-size: 12px; display: block;">COURSE / STREAM</span>
                        <strong>{st.session_state['input_course']}</strong>
                    </div>
                    <div style="background-color: #F8FAFC; padding: 12px 14px; border-radius: 6px; border: 1px solid #E2E8F0;">
                        <span style="color: #64748B; font-size: 12px; display: block;">ANNUAL FAMILY INCOME</span>
                        <strong>₹{st.session_state['input_income']:,}</strong>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        confirm_box = st.checkbox(
            "I confirm that the details entered above are accurate and match my official certificates.",
            value=True,
            key="check_confirm_accurate",
        )

        st.write("")
        col_nav1, col_nav2 = st.columns([1, 2])
        with col_nav1:
            if st.button("← Edit details (Back)", key="btn_back_to_step1", use_container_width=True):
                st.session_state["wizard_step"] = 1
                st.rerun()
        with col_nav2:
            if st.button("Find my matches →", type="primary", disabled=not confirm_box, use_container_width=True, key="btn_find_matches"):
                st.session_state["wizard_step"] = 3
                st.rerun()

    # -------------------------------------------------------------------------
    # STEP 3: SEE YOUR MATCHES
    # -------------------------------------------------------------------------
    elif current_step == 3:
        profile = {
            "age": st.session_state.get("input_age"),
            "state": st.session_state.get("input_state"),
            "annual_income": st.session_state.get("input_income"),
            "category": st.session_state.get("input_category"),
            "course": st.session_state.get("input_course"),
            "gender": st.session_state.get("input_gender"),
        }

        # Sorting Controls
        ctrl1, ctrl2, ctrl3 = st.columns([2.5, 1.2, 1.2])
        with ctrl1:
            st.markdown(
                """
                <div class="form-card-header" style="border: none; margin: 0; padding: 0;">
                    <div class="form-step-badge">3</div>
                    <div>
                        <h2 class="form-card-title">Your scholarship matches</h2>
                        <p class="form-card-subtitle">Transparent eligibility reasons with official verification links.</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with ctrl2:
            sort_by = st.radio("Sort by", ["Biggest benefit", "Fastest payout"], horizontal=True, label_visibility="collapsed")
            sort_mode = "speed" if sort_by == "Fastest payout" else "benefit"
        with ctrl3:
            if st.button("← Edit details", key="btn_step3_back", use_container_width=True):
                st.session_state["wizard_step"] = 1
                st.rerun()

        # Deterministic Evaluation & Ranking
        raw_results = evaluate_all(profile, schemes)
        results = rank(raw_results, by=sort_mode)

        n_ok = sum(1 for r in results if r["status"] == "eligible")
        n_info = sum(1 for r in results if r["status"] == "needs_info")
        n_total = len(results)

        st.info(f"🎯 **We found {n_ok} scheme(s) you may qualify for out of {n_total} available programs.**" + (f" ({n_info} need more information)" if n_info else ""))

        # What-If Simulator Expander
        with st.expander("🔮 What-If Simulator: See how income or category changes your eligibility", expanded=False):
            st.caption("Deterministic real-time simulation without modifying your main profile. No LLM calls are made.")
            sim_col1, sim_col2 = st.columns(2)
            base_income_val = profile.get("annual_income") if profile.get("annual_income") is not None else 300000
            sim_income = sim_col1.number_input("Simulate Family Income (₹)", min_value=0, max_value=2000000, value=int(base_income_val), step=25000, key="sim_inc_slider")
            base_cat_val = profile.get("category") if profile.get("category") in CATEGORIES else "General"
            sim_cat_idx = CATEGORIES.index(base_cat_val) if base_cat_val in CATEGORIES else 0
            sim_cat = sim_col2.selectbox("Simulate Category", CATEGORIES, index=sim_cat_idx, key="sim_cat_select")

            sim_profile = {**profile, "annual_income": sim_income, "category": sim_cat}
            sim_eval = evaluate_all(sim_profile, schemes)
            sim_eligible = [r for r in sim_eval if r["status"] == "eligible"]
            current_eligible_ids = {r["scheme"]["id"] for r in results if r["status"] == "eligible"}
            newly_unlocked = [r["scheme"]["name"] for r in sim_eligible if r["scheme"]["id"] not in current_eligible_ids]

            st.markdown(f"**Under this simulation, you qualify for {len(sim_eligible)} scheme(s).**")
            if newly_unlocked:
                st.success(f"✨ **Newly unlocked schemes:** {', '.join(newly_unlocked)}")
            elif len(sim_eligible) < n_ok:
                st.warning(f"Fewer schemes eligible ({len(sim_eligible)} vs {n_ok}) under this simulated bracket.")

        # Plain Language Explanation Button
        if st.button("Explain my results in plain language", use_container_width=True, key="btn_explain_results"):
            try:
                with st.spinner("Writing personalized explanation with Nemotron Strong Model..."):
                    explanation_text = llm.explain_results(profile, results, language=st.session_state["app_language"])
                    st.info(explanation_text)
            except Exception as exc:
                st.error(f"Explanation failed: {exc}")

        st.markdown("### Matching Schemes")

        # Scheme Result Cards
        for r in results:
            s = r["scheme"]
            status = r["status"]
            k = s["id"]

            status_badge_html = {
                "eligible": '<span class="badge-eligible">🟢 Eligible</span>',
                "needs_info": '<span class="badge-needs-info">🟡 Needs more info</span>',
                "not_eligible": '<span class="badge-not-eligible">🔴 Not eligible</span>'
            }[status]

            st.markdown(
                f"""
                <div class="scheme-result-card {status}">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px; margin-bottom: 6px;">
                        <h4 style="margin: 0; font-size: 17px; font-weight: 700; color: #0F172A;">{s['name']}</h4>
                        <div>{status_badge_html}</div>
                    </div>
                    <div style="font-size: 13.5px; color: #334155; line-height: 1.5;">
                        <strong>Benefit:</strong> {s.get('benefit')} &nbsp;|&nbsp; <strong>Deadline:</strong> {s.get('deadline')} &nbsp;|&nbsp; <strong>Ease:</strong> {s.get('ease')} Ease<br>
                        <strong>Provider:</strong> {s.get('provider')} &nbsp;|&nbsp; <strong>State:</strong> {s.get('state')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Ineligible Gap Shortfalls
            if status == "not_eligible":
                for g in r["gaps"]:
                    st.error(f"Shortfall: {g}")
                other_eligible = [x["scheme"]["name"] for x in results if x["status"] == "eligible"]
                if other_eligible:
                    st.info(f"💡 Alternative option: You qualify for **{'; '.join(other_eligible)}**")

            # Missing Information Notice
            if status == "needs_info":
                st.warning(f"**Needs more info to confirm eligibility:** Missing **{', '.join(r['missing'])}**.")

            # Tavily Live Verification
            if status in ("eligible", "needs_info"):
                v_data = search.verify_scheme(s)
                if v_data.get("verified_date"):
                    st.success(f"🟢 **Verified live on {v_data['verified_date']}** via Tavily Search")
                if v_data.get("warning"):
                    st.warning(f"⚠️ {v_data['warning']}")

            # Expandable Criteria Details & Actions
            with st.expander(f"View criteria & actions for {s['name']}", expanded=False):
                st.write(f"**Official Portal:** [{s.get('url')}]({s.get('url')})")

                checks_df = pd.DataFrame(
                    [{"Criterion": c["criterion"],
                      "Result": {True: "Pass", False: "Fail", None: "Unknown"}[c["passed"]],
                      "Detail": c["detail"]} for c in r["checks"]]
                )
                st.dataframe(checks_df, use_container_width=True, hide_index=True)

                if status in ("eligible", "needs_info"):
                    v_data = search.verify_scheme(s)
                    sources = v_data.get("results", [])
                    if sources:
                        st.caption("**Live Verified Official Sources:**")
                        for src in sources:
                            icon = "🏛️ [Official]" if src.get("is_official") else "🌐 [Portal]"
                            st.markdown(f"- {icon} [{src['title']}]({src['url']})  \n  <small>{src['snippet']}</small>", unsafe_allow_html=True)

                act_c1, act_c2 = st.columns(2)
                with act_c1:
                    if st.button("🔄 Refresh live status", key=f"reverify_{k}", use_container_width=True):
                        search.verify_scheme(s, force_refresh=True)
                        st.rerun()

                with act_c2:
                    if status != "not_eligible":
                        if st.button("Draft application", key=f"draft_btn_{k}", use_container_width=True):
                            try:
                                with st.spinner("Drafting declaration..."):
                                    st.session_state[f"draft_{k}"] = llm.draft_declaration(profile, s, language=st.session_state["app_language"])
                            except Exception as exc:
                                st.error(f"Draft failed: {exc}")

                if f"draft_{k}" in st.session_state:
                    draft_content = st.session_state[f"draft_{k}"]
                    edited_draft = st.text_area(
                        "Customized Declaration Draft:",
                        value=draft_content,
                        height=180,
                        key=f"draft_text_{k}",
                    )
                    st.download_button(
                        label="📥 Download Draft (.txt)",
                        data=edited_draft,
                        file_name=f"declaration_{s['id']}.txt",
                        mime="text/plain",
                        key=f"dl_draft_{k}",
                        use_container_width=True,
                    )

# -----------------------------------------------------------------------------
# 4. Official Government Footer
# -----------------------------------------------------------------------------
st.markdown(
    """
    <footer class="gov-footer">
        <div class="gov-footer-inner">
            <div class="gov-footer-row">
                <div>
                    <div class="gov-footer-brand">SchemeSetu</div>
                    <div class="gov-footer-sub">A student-first guide to public welfare schemes.</div>
                </div>
                <div class="gov-footer-links">
                    <a href="#accessibility">Accessibility</a>
                    <a href="#terms">Terms of use</a>
                    <a href="#privacy">Privacy</a>
                    <a href="#feedback">Feedback</a>
                </div>
            </div>
            <div class="gov-footer-divider"></div>
            <div style="font-size: 11.5px; color: #94A3B8;">
                This service is for guidance only. Eligibility, deadlines and benefits are subject to official government notifications.
            </div>
        </div>
    </footer>
    """,
    unsafe_allow_html=True,
)
