import streamlit as st
import pdfplumber
from groq import Groq
import json
import os
from dotenv import load_dotenv
 
load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
 
st.set_page_config(page_title="ATS Resume Analyzer", page_icon="💾", layout="centered")
 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=VT323&family=Press+Start+2P&display=swap');
 
* {
    font-family: 'VT323', monospace !important;
    font-size: 18px;
}
 
body, .stApp {
    background-color: #fff0f5 !important;
    background-image: 
        radial-gradient(circle at 20% 20%, #ffe4ef 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, #ffd6e8 0%, transparent 50%);
}
 
/* Hide streamlit branding */
#MainMenu, footer, header {visibility: hidden;}
 
.main .block-container {
    padding: 2rem 2rem;
    max-width: 800px;
}
 
/* Window chrome style */
.win-window {
    background: #ffcce5;
    border: 3px solid #000;
    box-shadow: 4px 4px 0px #000;
    margin-bottom: 20px;
    border-radius: 0px;
}
 
.win-titlebar {
    background: linear-gradient(90deg, #ff79b0, #ffadd4);
    color: #000;
    padding: 6px 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #000;
    font-family: 'Press Start 2P', monospace !important;
    font-size: 12px !important;
}
 
.win-buttons {
    display: flex;
    gap: 4px;
}
 
.win-btn {
    width: 18px;
    height: 18px;
    background: #ffcce5;
    border: 2px solid #000;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 11px !important;
    font-weight: bold;
    cursor: pointer;
    box-shadow: 2px 2px 0px #000;
    color: #000;
    font-family: 'VT323', monospace !important;
}
 
.win-content {
    padding: 16px;
}
 
/* Main title */
.main-title {
    font-family: 'Press Start 2P', monospace !important;
    font-size: 16px !important;
    color: #fff;
    text-shadow: 3px 3px 0px #c0006a;
    text-align: center;
    margin-bottom: 6px;
    letter-spacing: 1px;
}
 
.subtitle {
    text-align: center;
    color: #fff;
    font-size: 20px !important;
    margin-bottom: 20px;
    text-shadow: 1px 1px 0px #c0006a;
}
 
/* Score display */
.score-window {
    background: #fff0f7;
    border: 3px solid #000;
    box-shadow: 4px 4px 0px #000;
    padding: 20px;
    text-align: center;
    margin: 16px 0;
}
 
.score-big {
    font-family: 'Press Start 2P', monospace !important;
    font-size: 42px !important;
    color: #c0006a;
    text-shadow: 4px 4px 0px #ffadd4;
    line-height: 1.2;
}
 
.score-label {
    font-family: 'Press Start 2P', monospace !important;
    font-size: 12px !important;
    color: #000;
    margin-top: 8px;
}
 
.summary-text {
    font-size: 20px !important;
    color: #444;
    margin-top: 10px;
    padding: 8px;
    background: #ffcce5;
    border: 2px solid #000;
}
 
/* Progress bar retro */
.retro-bar-bg {
    background: #fff;
    border: 2px solid #000;
    height: 24px;
    margin: 12px 0;
    position: relative;
    box-shadow: 2px 2px 0px #000;
}
 
.retro-bar-fill {
    height: 100%;
    background: repeating-linear-gradient(
        90deg,
        #ff79b0 0px,
        #ff79b0 12px,
        #c0006a 12px,
        #c0006a 24px
    );
    transition: width 0.5s;
}
 
/* Cards */
.retro-card {
    background: #fff0f7;
    border: 3px solid #000;
    box-shadow: 4px 4px 0px #000;
    padding: 14px;
    margin-bottom: 16px;
}
 
.retro-card-title {
    font-family: 'Press Start 2P', monospace !important;
    font-size: 10px !important;
    color: #c0006a;
    border-bottom: 2px solid #000;
    padding-bottom: 8px;
    margin-bottom: 10px;
}
 
.retro-card p {
    margin: 4px 0;
    font-size: 17px !important;
    color: #222;
    padding: 4px 0;
    border-bottom: 1px dashed #ffadd4;
}
 
/* Streamlit widget overrides */
.stButton > button {
    font-family: 'Press Start 2P', monospace !important;
    font-size: 11px !important;
    background: #ff79b0 !important;
    color: #fff !important;
    border: 3px solid #000 !important;
    box-shadow: 4px 4px 0px #000 !important;
    border-radius: 0px !important;
    padding: 12px 24px !important;
    width: 100%;
    cursor: pointer;
    transition: all 0.1s;
}
 
.stButton > button:hover {
    background: #c0006a !important;
    transform: translate(2px, 2px);
    box-shadow: 2px 2px 0px #000 !important;
}
 
.stButton > button:active {
    transform: translate(4px, 4px);
    box-shadow: 0px 0px 0px #000 !important;
}
 
.stFileUploader, .stTextArea textarea {
    border: 3px solid #000 !important;
    border-radius: 0px !important;
    background: #ffcce5 !important;
    box-shadow: 3px 3px 0px #000 !important;
    font-family: 'VT323', monospace !important;
    font-size: 18px !important;
}
 
.stSpinner > div {
    border-color: #c0006a !important;
}
 
label, .stFileUploader label {
    font-family: 'Press Start 2P', monospace !important;
    font-size: 13px !important;
    color: #000 !important;
    text-shadow: none;
}

/* Fix doubled upload button text */
[data-testid="stFileUploaderDropzone"] button {
    font-size: 0px !important;
}

[data-testid="stFileUploaderDropzone"] button::after {
    content: "UPLOAD";
    font-size: 11px !important;
    font-family: 'Press Start 2P', monospace !important;
}

/* Fallback for older Streamlit versions */
.stFileUploader button {
    font-size: 0px !important;
}

.stFileUploader button::after {
    content: "UPLOAD";
    font-size: 11px !important;
    font-family: 'Press Start 2P', monospace !important;
}

[data-testid="stFileUploaderDropzone"] button::after {
    content: "UPLOAD";
    font-size: 11px !important;
    font-family: 'Press Start 2P', monospace !important;
}
 
.stInfo {
    background: #ffcce5 !important;
    border: 3px solid #000 !important;
    border-radius: 0px !important;
    box-shadow: 3px 3px 0px #000 !important;
    color: #000 !important;
    font-size: 18px !important;
}
</style>
""", unsafe_allow_html=True)
 
# --- Header Window ---
st.markdown("""
<div class="win-window">
    <div class="win-titlebar">
        <span>💾 ATS_RESUME_ANALYZER.exe</span>
        <div class="win-buttons">
            <span class="win-btn">_</span>
            <span class="win-btn">□</span>
            <span class="win-btn">×</span>
        </div>
    </div>
    <div class="win-content">
        <div class="main-title">ATS RESUME ANALYZER</div>
        <div class="subtitle">⬆ upload resume · 📋 paste JD · 🎯 get your score</div>
    </div>
</div>
""", unsafe_allow_html=True)
 
# --- Upload Window ---
uploaded_file = st.file_uploader("📄 SELECT YOUR RESUME (PDF)", type="pdf")
job_description = st.text_area("📋 PASTE JOB DESCRIPTION", height=180, placeholder="Paste the job description here...")
 
# --- Functions ---
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text
 
def analyze_resume(resume_text, job_desc):
    prompt = f"""
You are a precise ATS (Applicant Tracking System) expert.

Compare this resume against the job description CAREFULLY. 
Read the ENTIRE resume before making any judgments.

CRITICAL RULES:
- If a skill, tool, or keyword appears ANYWHERE in the resume, it is NOT missing
- Only add something to "missing_keywords" if it is genuinely absent from the resume
- Only add something to "improvements" if it is genuinely not addressed in the resume
- Do NOT suggest adding something that is already clearly present
- Be specific and accurate — false negatives hurt candidates

SCORING RULES:
- If a mandatory requirement (marked as "required" or "mandatory") is missing, 
  cap the score at 65 maximum
- Hard disqualifiers (wrong degree level, missing mandatory certifications) 
  should heavily penalize the score
- Distinguish between "preferred" and "required" qualifications in scoring

Respond ONLY with a JSON object — no explanation, no markdown, just raw JSON.
 
Resume:
{resume_text}
 
Job Description:
{job_desc}
 
Return this exact JSON structure:
{{
  "ats_score": <number from 0 to 100>,
  "matched_keywords": [<list of keywords from JD found in resume>],
  "missing_keywords": [<important keywords from JD missing in resume>],
  "strengths": [<2-3 things the resume does well>],
  "improvements": [<3-5 specific suggestions to improve the resume>],
  "summary": "<one sentence overall verdict>"
}}
"""
    response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}]
)
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())
 
# --- Analyze ---
if uploaded_file and job_description:
    if st.button("▶ RUN ANALYSIS"):
        with st.spinner("⏳ Scanning resume... please wait..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            result = analyze_resume(resume_text, job_description)
 
        score = result["ats_score"]
        verdict = "STRONG MATCH! ★" if score >= 70 else "NEEDS WORK ⚠" if score >= 50 else "LOW MATCH ✖"
        bar_width = score
 
        st.markdown(f"""
        <div class="win-window">
            <div class="win-titlebar">
                <span>📊 Analysis Results</span>
                <div class="win-buttons"><span class="win-btn">×</span></div>
            </div>
            <div class="win-content">
                <div class="score-window">
                    <div class="score-big">{score}</div>
                    <div class="score-label">/ 100 — {verdict}</div>
                    <div class="retro-bar-bg">
                        <div class="retro-bar-fill" style="width:{bar_width}%"></div>
                    </div>
                    <div class="summary-text">💬 {result['summary']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
 
        col1, col2 = st.columns(2)
 
        with col1:
            st.markdown(f"""
            <div class="retro-card">
                <div class="retro-card-title">✅ MATCHED KEYWORDS</div>
                {"".join([f"<p>✔ {kw}</p>" for kw in result["matched_keywords"]])}
            </div>
            <div class="retro-card">
                <div class="retro-card-title">💪 STRENGTHS</div>
                {"".join([f"<p>⭐ {s}</p>" for s in result["strengths"]])}
            </div>
            """, unsafe_allow_html=True)
 
        with col2:
            st.markdown(f"""
            <div class="retro-card">
                <div class="retro-card-title">❌ MISSING KEYWORDS</div>
                {"".join([f"<p>✖ {kw}</p>" for kw in result["missing_keywords"]])}
            </div>
            <div class="retro-card">
                <div class="retro-card-title">🛠 HOW TO IMPROVE</div>
                {"".join([f"<p>💡 {tip}</p>" for tip in result["improvements"]])}
            </div>
            """, unsafe_allow_html=True)
 
else:
    st.info("⚠ Please upload a resume PDF and paste a job description to begin analysis.")
# refresh
