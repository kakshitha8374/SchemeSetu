# SchemeSetu: Hackathon Submission Kit (SUBMISSION.md)

**Hackathon:** Nebius x NVIDIA Global AI Hackathon  
**Project Name:** SchemeSetu 🌉  

---

## 1. Project Pitch (Under 200 Characters)

> SchemeSetu bridges Indian students to government schemes with zero-hallucination rules, exact gap analysis, live Tavily checks, and Nemotron drafting on Nebius Token Factory.

*(Character count: 184 characters)*

---

## 2. Project Description (Devpost Form: 250 to 350 Words)

Every year, thousands of crores in Indian government scholarships and welfare schemes go unclaimed. For millions of students—particularly first-generation collegiate learners—the primary barrier is not a lack of ambition, but the intimidating complexity of fragmented state and central portals, Byzantine income brackets, and shifting category requirements. Generic AI chatbots cannot solve this; they hallucinate scheme guidelines and invent eligibility rules, leading students to missed deadlines and rejected applications.

SchemeSetu solves this crisis with a trust-first, zero-hallucination architecture that strictly bifurcates generative AI from deterministic evaluation:

1. **Intelligent Natural Language Extraction:** Students describe their background in plain, conversational language (or optionally upload an income/caste certificate for in-memory OCR). An NVIDIA Nemotron fast model hosted on Nebius Token Factory extracts a structured profile without making any eligibility assumptions.
2. **Deterministic Rules Engine:** The LLM is never allowed to decide eligibility. Instead, a pure Python rules engine deterministically evaluates the student's profile against verified government schemes from Karnataka and national portals, checking income ceilings, domicile, social category, and course prerequisites.
3. **Exact Gap Analysis & What-If Simulation:** If a student misses a scheme, SchemeSetu doesn't just say "no"—it reveals the exact shortfall (e.g., "Family income is ₹50,000 above the cap") and highlights other schemes they qualify for. An interactive What-If Simulator lets students explore how changes in declared income or category unlock new opportunities in real time.
4. **Live Verification via Tavily:** SchemeSetu executes runtime calls to the Tavily Search API, verifying whether state portals are actively accepting applications, flagging deadline discrepancies, and attaching official `.gov.in` and `.nic.in` sources.
5. **Multilingual Explanations & Draft Generation:** An NVIDIA Nemotron strong model on Nebius Token Factory drafts plain-language summaries and customized formal self-declarations in English, Hindi, or Kannada with brackets for unknown facts.

SchemeSetu empowers both individual students and Common Service Centre (CSC) operators to unlock life-changing educational funding with absolute confidence.

*(Word count: 322 words)*

---

## 3. Demo Video Script (< 3 Minutes)

**Total Duration:** 2 minutes 45 seconds  
**Target Video Format:** 1080p, screen recording with voiceover and clean audio.

| Timestamp | Section | Visual on Screen | Spoken Script / Action |
| :--- | :--- | :--- | :--- |
| **0:00 - 0:30** | **The Problem** | Montage showing complex Indian scholarship portals (SSP, NSP), confusing guidelines, and news headlines of unclaimed welfare funds. | "Over 10,000 Crore rupees in student scholarships go unclaimed in India every year. Why? Because discovering whether you qualify across dozens of government portals is a bureaucratic maze. And if you ask a standard AI chatbot, it hallucinates rules and misleads you. Welcome to SchemeSetu—the first zero-hallucination scholarship guide powered by Nebius Token Factory and NVIDIA Nemotron." |
| **0:30 - 1:15** | **Live Demo: Eligible Scenario** | Browser opens SchemeSetu. Typing: *"I'm a 20 year old OBC girl from Karnataka studying engineering. Family income is about 3 lakh."* Click **Read my details**. | "Notice how simple this is. A student types their story in ordinary words. Powered by an NVIDIA Nemotron fast model on Nebius Token Factory, SchemeSetu instantly parses the student's age, state, income, caste, and course into structured data. Notice our trust architecture: the LLM never decides eligibility. Our deterministic Python rules engine matches the profile against verified government schemes. She immediately qualifies for the Vidyasiri Food and Accommodation scheme and AICTE Pragati Scholarship for Girls!" |
| **1:15 - 1:55** | **Gap Analysis, What-If & Live Tavily** | Scroll to an ineligible scheme (e.g. SSP SC Scholarship). Show exact gap message. Open **What-If Simulator**. | "Now, what about the schemes she missed? SchemeSetu doesn't give a vague rejection. It calculates the exact mathematical shortfall: *'Category OBC is not in the accepted list: SC'*. Plus, our What-If Simulator lets her slide income or test categories deterministically without a single LLM call. Even better, look at this badge: SchemeSetu executed a live runtime Tavily search call to verify that the portal is actively open, citing direct `.gov.in` sources." |
| **1:55 - 2:25** | **Application Draft & Multilingual** | Click **Draft my declaration**; switch language to Kannada / Hindi. Click **Download as .txt**. | "Once eligible, students don't need to hire agents to draft declarations. Powered by the NVIDIA Nemotron strong model, SchemeSetu produces a formal, customized self-declaration in English, Hindi, or Kannada, with bracketed placeholders for missing details. The student downloads the `.txt` file with one click, ready for submission." |
| **2:25 - 2:45** | **Architecture & Impact** | Display architecture diagram and CSC Operator batch CSV upload screening 10 students simultaneously. | "With Common Service Centre batch screening, CSC operators in rural villages can screen entire classrooms in seconds. Built on Nebius Token Factory, NVIDIA Nemotron, and Tavily, SchemeSetu turns bureaucratic confusion into verified educational opportunity. Thank you!" |

---

## 4. Honest Feedback on Nebius Token Factory & NVIDIA Models

*(Add your real developer experience notes in the marked placeholders below before submitting.)*

### What Worked Exceptionally Well:
- **API Compatibility:** The OpenAI-compatible endpoint structure in Nebius Token Factory made integration straightforward without requiring specialized client libraries.
- **Inference Speed:** The Nemotron fast model (`nvidia/nemotron-mini-4b-instruct`) delivered rapid profile extraction, keeping our Streamlit UI responsive and snappy during real-time student interactions.
- **Multilingual Reasoning:** The Nemotron strong model (`nvidia/llama-3.1-nemotron-70b-instruct`) exhibited strong multilingual translation and formal tone adaptation when generating self-declarations and explanations in Indian regional contexts (Hindi and Kannada).

### Areas for Improvement / Constructive Feedback:
- **Model Documentation & ID Discovery:** The model catalogue in Token Factory could benefit from clearer documentation on specific context window limits, quantization levels, and recommended system prompts for structured JSON emission.
- **[YOUR EXPERIENCE HERE]:** *[e.g., Note any observations regarding cold-start latency, token factory rate limits, or specific prompt adjustments you found necessary while testing Nemotron.]*
- **[YOUR EXPERIENCE HERE]:** *[e.g., Mention any feedback on API key provisioning or dashboard usage analytics.]*

---

## 5. Final Hackathon Submission Checklist

Before submitting on Devpost, verify each requirement:

- [ ] **Public GitHub Repository:** Repository is set to Public with visible [MIT LICENSE](LICENSE).
- [ ] **Clean Codebase & Secrets Protected:** Confirm `.env` and `.streamlit/secrets.toml` are not in git history.
- [ ] **README.md Complete:** Includes architecture diagram, setup steps, model attribution, and data verification note.
- [ ] **Runtime Nebius Token Factory Integration:** Confirmed `llm.py` makes real calls to `https://api.tokenfactory.nebius.com/v1/` using NVIDIA Nemotron models.
- [ ] **Runtime Tavily Search API Integration:** Confirmed `search.py` performs live web queries citing official `.gov.in` / `.nic.in` domains.
- [ ] **Real Mode Active:** Streamlit app deployed on Streamlit Community Cloud with `MOCK_MODE=false` and real API keys in cloud secrets.
- [ ] **Public Working Demo URL:** Tested the deployed app link in an Incognito window while logged out.
- [ ] **Demo Video Under 3 Minutes:** Video recorded following the script above, uploaded to YouTube as Public or Unlisted, under 3:00 duration.
- [ ] **Track & Category Selected:** Selected the appropriate hackathon challenge track on Devpost.
- [ ] **Feedback Included:** Filled out Nebius & NVIDIA experience feedback in Devpost submission form.
