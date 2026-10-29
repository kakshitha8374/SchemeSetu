# SchemeSetu 🌉
*Bridging Indian Students to Government Scholarships & Schemes with Verified Deterministic AI*

Built for the **Nebius x NVIDIA Global AI Hackathon**.

---

## 📌 Problem

Over **₹10,000 Crore** in student welfare and scholarship funds in India go underutilized every year. Students—especially first-generation learners from rural and tier-2/3 regions—face severe hurdles:
1. **Fragmented Portals:** Schemes are scattered across the State Scholarship Portal (SSP), National Scholarship Portal (NSP), backward classes departments, and collegiate education sites.
2. **Opaque & Complex Rules:** Income caps vary widely (₹1 Lakh, ₹2.5 Lakh, ₹8 Lakh), with intricate combinations of caste categories, age brackets, and degree levels.
3. **Hallucination Risk:** Standard generative AI chatbots invent non-existent schemes or hallucinate eligibility criteria, leading to rejected applications and lost deadlines.

---

## 💡 Solution: SchemeSetu

SchemeSetu is an AI-guided eligibility copilot built with a strict **trust-first architecture**:
- **Deterministic Rules Engine (`rules.py`):** The LLM *never* decides eligibility. All eligibility calculations, income caps, and criteria are evaluated deterministically against hand-curated, official scheme data.
- **NVIDIA Nemotron via Nebius Token Factory (`llm.py`):** 
  - **Fast Model (`FAST_MODEL`):** High-speed extraction turning free-form natural language into structured student profiles.
  - **Strong Model (`STRONG_MODEL`):** Plain-language multilingual explanations (English, Hindi, Kannada) and customized application self-declarations using only verified profile facts.
- **Tavily Live API (`search.py`):** Real-time web verification queries confirming that government portals are open, detecting deadline extensions or closures, and attaching official `.gov.in` and `.nic.in` sources.
- **Exact Gap Analysis & What-If Simulator:** Ineligible schemes display the exact shortfall (e.g. *"Income is ₹50,000 above the cap"*) and allow students to test scenarios without LLM calls.
- **CSC Operator Batch Screening:** Common Service Centre (CSC) operators can screen batches of dozens of students instantly via CSV upload.

---

## 📸 Interface Preview

```
+-----------------------------------------------------------------------------------+
|  SchemeSetu 🌉           Language: [ English v ]                                  |
|  AI-guided scholarship and government scheme discovery for Indian students.       |
+-----------------------------------------------------------------------------------+
|  1. Tell us about yourself                                                        |
|  [ "I'm a 20 year old OBC girl from Karnataka studying engineering..."          ] |
|  [ Read my details ]   [ 📄 Optional: Upload Income/Caste Certificate (OCR) ]     |
+-----------------------------------------------------------------------------------+
|  2. Check your details                                                            |
|  Age: [ 20 ]   State: [ Karnataka ]   Income: [ 300,000 ]                         |
|  Category: [ OBC ]   Course: [ Engineering ]   Gender: [ Female ]                 |
+-----------------------------------------------------------------------------------+
|  3. Your results  ->  Schemes you qualify for: 3 of 9                             |
|  [ 🔮 What-If Simulator: See what changes if income/category changes ]            |
|  [ Explain my results in plain language ]                                         |
|                                                                                   |
|  🟢 Eligible — Post-Matric Scholarship for Backward Classes (SSP Karnataka)       |
|     • Benefit: Up to Rs 25,000/year | Official Source: bcwd.karnataka.gov.in      |
|     • 🟢 Verified live on 2026-10-28 via Tavily (Official .gov.in links attached)  |
|     • [ Draft my declaration ] -> [ 📥 Download as .txt ]                         |
|                                                                                   |
|  🔴 Not eligible — Post-Matric Scholarship for SC Students (SSP Karnataka)        |
|     • Gap: Category 'OBC' is not in the accepted list: SC                         |
|     • 💡 While unavailable, you currently qualify for: Vidyasiri, Pragati...      |
+-----------------------------------------------------------------------------------+
```

---

## 🏗️ System Architecture

```
                       User Input (Natural Text / In-Memory Certificate)
                                               │
                                               ▼
                         ┌───────────────────────────────────────────┐
                         │   Nebius Token Factory (OpenAI Client)    │
                         │   NVIDIA Nemotron Fast Model (llm.py)     │
                         └─────────────────────┬─────────────────────┘
                                               │ Structured Profile JSON
                                               ▼
                         ┌───────────────────────────────────────────┐
                         │   SchemeSetu Rules Engine (rules.py)      │
                         │   Deterministic matching vs schemes.json  │
                         └─────────────────────┬─────────────────────┘
                                               │
             ┌─────────────────────────────────┼─────────────────────────────────┐
             ▼                                 ▼                                 ▼
      Eligible Schemes                  Needs More Info                   Not Eligible
             │                                 │                                 │
             ▼                                 ▼                                 ▼
  ┌───────────────────────┐         ┌───────────────────────┐         ┌───────────────────────┐
  │ Tavily Live Search    │         │ Friendly Missing Info │         │ Exact Gap Analysis    │
  │ Portal verification & │         │ Prompts user only for │         │ & What-If Simulator   │
  │ .gov.in link matching │         │ unprovided fields     │         │ (Deterministic math)  │
  └──────────┬────────────┘         └──────────┬────────────┘         └───────────────────────┘
             │                                 │
             └────────────────┬────────────────┘
                              ▼
               ┌───────────────────────────────────────────┐
               │    Nebius Token Factory (OpenAI Client)   │
               │    NVIDIA Nemotron Strong Model (llm.py)  │
               │    Multilingual Plain Explanations &      │
               │    Customized Application Draft (.txt)    │
               └───────────────────────────────────────────┘
```

---

## 🤖 NVIDIA, Nebius Token Factory, and Tavily Integration

| Component | Provider & Model | Code File | Purpose |
| :--- | :--- | :--- | :--- |
| **Profile Extraction** | NVIDIA Nemotron Fast Model (e.g. `nvidia/nemotron-mini-4b-instruct`) via **Nebius Token Factory** | [`llm.py`](llm.py) | Parses conversational Indian English text into normalized structured JSON without hallucinating rules. |
| **Explanations & Drafts** | NVIDIA Nemotron Strong Model (e.g. `nvidia/llama-3.1-nemotron-70b-instruct`) via **Nebius Token Factory** | [`llm.py`](llm.py) | Synthesizes verified eligibility facts into accessible summaries and formal self-declaration letters in English, Hindi, or Kannada. |
| **Certificate OCR** *(Optional)* | NVIDIA Vision Model via **Nebius Token Factory** | [`llm.py`](llm.py) | Inspects uploaded income or caste certificates in memory with mandatory student verification before applying values. |
| **Live Portal Verification** | **Tavily Search API** | [`search.py`](search.py) | Real-time web verification prioritizing `.gov.in` and `.nic.in` domains, caching queries to protect quotas, and flagging deadline discrepancies. |
| **Eligibility Engine** | Python Rules Engine | [`rules.py`](rules.py) | 100% deterministic rule validation against income caps, social categories, domiciles, and course constraints. |

---

## 🚀 Setup & Local Execution

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/schemesetu.git
cd schemesetu
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux / macOS:
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Copy the example environment configuration:
```bash
cp .env.example .env
```
Fill in your credentials in `.env`:
```ini
TOKEN_FACTORY_API_KEY=your_nebius_token_factory_key
TOKEN_FACTORY_BASE_URL=https://api.tokenfactory.nebius.com/v1/
FAST_MODEL=nvidia/nemotron-mini-4b-instruct
STRONG_MODEL=nvidia/llama-3.1-nemotron-70b-instruct
TAVILY_API_KEY=your_tavily_api_key
MOCK_MODE=false
```

### 5. Launch the application
```bash
streamlit run app.py
```

---

## 🧪 Automated Testing

SchemeSetu includes 23 automated unit tests validating eligibility evaluation, exact gap calculation, missing-field precedence, Tavily offline fallbacks, multilingual output generation, and input error recovery.

Run the test suite:
```bash
python test_rules.py
```

---

## 📂 Data Sources & Verification Note

Every scheme represented in [`schemes.json`](schemes.json) is derived from official government departments and gazettes:
- **SSP Karnataka (Post-Matric):** `ssp.postmatric.karnataka.gov.in`
- **Backward Classes Welfare Department (BCWD):** `bcwd.karnataka.gov.in`
- **Social Welfare Department (SWD):** `sw.kar.nic.in`
- **National Scholarship Portal (NSP):** `scholarships.gov.in`
- **Department of Collegiate Education (DCE):** `dce.karnataka.gov.in`
- **AICTE (Pragati Scholarship):** `aicte-india.org`

For complete traceability, consult [`VERIFY.md`](VERIFY.md) for a line-by-line audit sheet mapping each rule parameter, income ceiling, and category condition directly to its government web source.

---

## 🛠️ Mock Mode vs Real Mode

- **Mock Mode:** Included as a robust offline fallback for local development or judges reviewing the codebase without API credentials. Activated when `MOCK_MODE=true` or when `TOKEN_FACTORY_API_KEY` is omitted. Uses deterministic regex parsing, sample certificate outputs, and template explanations clearly tagged with a yellow UI banner.
- **Real Production Mode:** Activated by setting `TOKEN_FACTORY_API_KEY` and `MOCK_MODE=false`. Makes live runtime requests to Nebius Token Factory for Nemotron inference and Tavily for web verification.

---

## ⚠️ Limitations & Disclaimer

- **Advisory Guidance:** SchemeSetu is designed as an informative guide. Final scholarship sanctions depend on physical document verification by competent government revenue authorities and institutional nodal officers.
- **State Coverage:** The initial pilot focuses on scholarships available to Karnataka domiciles and national central sector schemes; expansion to additional states is planned.
- **Privacy Assurance:** Uploaded certificates are analyzed entirely in memory and are never persisted to disk or sent to external storage.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
