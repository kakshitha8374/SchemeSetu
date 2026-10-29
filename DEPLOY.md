# SchemeSetu: Deployment Guide (DEPLOY.md)

This guide walks you through deploying **SchemeSetu** on **Streamlit Community Cloud** with live Nebius Token Factory and Tavily credentials.

---

## Prerequisites
- A GitHub account with a public repository for the project.
- Nebius Token Factory API key (`TOKEN_FACTORY_API_KEY`).
- Tavily API key (`TAVILY_API_KEY`).

---

## Step 1: Push Code to a Public GitHub Repository

1. Ensure secrets are strictly ignored:
   ```bash
   git status
   ```
   Confirm that `.env` and `.streamlit/secrets.toml` are listed in `.gitignore` and are NOT staged.

2. Initialize (if not already done) and commit the codebase:
   ```bash
   git init
   git add .
   git commit -m "feat: complete SchemeSetu hackathon implementation"
   ```

3. Push to your public GitHub repository:
   ```bash
   git branch -M main
   git remote add origin https://github.com/<your-username>/schemesetu.git
   git push -u origin main
   ```

---

## Step 2: Deploy on Streamlit Community Cloud

1. Navigate to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
2. Click **Create app** (or **New app**).
3. Fill in the repository details:
   - **Repository:** `<your-username>/schemesetu`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL:** Customize if desired (e.g., `schemesetu.streamlit.app`).

---

## Step 3: Configure Cloud Secrets

1. Before or during deployment, click **Advanced settings** -> **Secrets**.
2. Paste the contents of `.streamlit/secrets.toml.example` with your real keys:
   ```toml
   TOKEN_FACTORY_API_KEY = "your_actual_nebius_token_factory_key"
   TOKEN_FACTORY_BASE_URL = "https://api.tokenfactory.nebius.com/v1/"
   FAST_MODEL = "nvidia/nemotron-mini-4b-instruct"
   STRONG_MODEL = "nvidia/llama-3.1-nemotron-70b-instruct"
   VISION_MODEL = "" # Leave empty or set if you have a Vision model provisioned
   TAVILY_API_KEY = "your_actual_tavily_key"
   MOCK_MODE = "false"
   ```
3. Click **Save** and **Deploy**.

---

## Step 4: Verify Deployment

1. Watch the build log. Dependencies from `requirements.txt` will install automatically.
2. Once the app launches:
   - Verify that the **Demo mode banner is NOT visible** (confirming real mode is active).
   - Test "Read my details" with a sample sentence.
   - Click "Explain my results" to confirm Nebius Token Factory and NVIDIA Nemotron output.
   - Inspect a scheme to confirm real-time **Tavily verification badges** and source links.
3. Open an **Incognito / Private browser window** while logged out of GitHub/Streamlit, paste the public URL, and verify that any external judge or student can use the app without authorization barriers.
