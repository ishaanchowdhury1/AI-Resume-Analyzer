"""
AI Resume Analyzer & ATS Optimizer — Streamlit App
Upgraded with Zero-API-Key requirement, unlimited file upload support, multi-format extraction,
and AI bullet rewriting.
"""

import os
import json
import streamlit as st
from resume_analyzer import analyze_resume, extract_text_from_file, fallback_heuristic_analyzer

# Streamlit Page Config
st.set_page_config(
    page_title="AI Resume Analyzer & ATS Optimizer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    
    .stApp {
        background-color: #0b0f19;
    }
    
    /* Header Gradient */
    .hero-container {
        padding: 24px 0 16px 0;
        margin-bottom: 24px;
    }
    
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -1.5px;
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 50%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
        margin-bottom: 8px;
    }
    
    .hero-sub {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #9ca3af;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    /* Card Styles */
    .metric-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    
    .score-number {
        font-size: 4.5rem;
        font-weight: 800;
        letter-spacing: -3px;
        line-height: 1;
        margin-bottom: 8px;
    }
    
    .score-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .verdict-box {
        background: #111827;
        border: 1px solid #1f2937;
        border-left: 4px solid #3b82f6;
        border-radius: 12px;
        padding: 20px 24px;
        font-size: 1.05rem;
        line-height: 1.6;
        color: #e5e7eb;
        margin-bottom: 20px;
    }
    
    .section-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 16px;
    }
    
    .section-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 2.5px;
        color: #9ca3af;
        margin-bottom: 14px;
        font-weight: 600;
    }
    
    /* Tag Pills */
    .tag {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.82rem;
        margin: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 500;
    }
    
    .tag-green {
        background: rgba(16, 185, 129, 0.12);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .tag-red {
        background: rgba(239, 68, 68, 0.12);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    /* Recommendation Badges */
    .hire-badge {
        display: inline-block;
        padding: 8px 24px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 1px;
        font-family: 'JetBrains Mono', monospace;
    }
    .hire-yes { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid #059669; }
    .hire-maybe { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid #d97706; }
    .hire-no { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid #dc2626; }

    /* Bullet Rewrite Box */
    .rewrite-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .rewrite-orig {
        color: #9ca3af;
        text-decoration: line-through;
        font-size: 0.9rem;
        margin-bottom: 6px;
    }
    .rewrite-new {
        color: #34d399;
        font-weight: 600;
        font-size: 0.95rem;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.5px !important;
        padding: 14px 32px !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)


# Sidebar Configuration
with st.sidebar:
    st.markdown("### 📁 File Upload Info")
    st.markdown("""
    - **No File Size Limit** (up to 2 GB)
    - **Formats Supported**: PDF, DOCX, DOC, TXT, MD
    - **Offline Engine**: Default ATS matching requires no key or account.
    """)
    
    st.divider()
    st.markdown("### 💡 Features")
    st.markdown("""
    - 📊 **Overall Match Score (0-100)**
    - 🎯 **Matched vs Missing Keywords**
    - 🛠️ **ATS Format & Content Audit**
    - 🚀 **AI Bullet Point Rewriter**
    - 📄 **Exportable Analysis Report**
    """)

    st.divider()
    # Collapsed Streamlit Expander titled "Advanced AI Settings (Optional)"
    with st.expander("Advanced AI Settings (Optional)", expanded=False):
        st.caption("Provide an API key to enable LLM-powered insights. Leave empty to use the built-in ATS engine.")
        api_key = st.text_input("API Key", type="password", placeholder="Paste API Key here...", help="Supported: Groq, Gemini, OpenAI")
        provider = st.selectbox("Provider", ["Auto-detect", "Groq", "Gemini", "OpenAI"])


# Header
st.markdown("""
<div class="hero-container">
    <div class="hero-title">AI Resume Analyzer & ATS Optimizer</div>
    <div class="hero-sub">Instant Feedback · ATS Keyword Match · Unlimited File Size · 100% Free & No API Key Needed</div>
</div>
""", unsafe_allow_html=True)


# Sample Data Handler
if "sample_loaded" not in st.session_state:
    st.session_state.sample_loaded = False
    st.session_state.sample_resume = ""
    st.session_state.sample_jd = ""

sample_col, _ = st.columns([1, 2])
with sample_col:
    if st.button("✨ Load Sample Resume & Job Description"):
        st.session_state.sample_loaded = True
        st.session_state.sample_resume = """JOHN DOE
Senior Full Stack Engineer | San Francisco, CA | john@example.com | (555) 019-2834 | linkedin.com/in/johndoe | github.com/johndoe

SUMMARY
Versatile Full Stack Engineer with 6+ years of experience designing scalable web applications, microservices, and REST APIs. Proficient in Python, React, Node.js, TypeScript, PostgreSQL, and AWS cloud deployment.

EXPERIENCE
Senior Software Engineer | Acme Tech Solutions | 2022 – Present
- Architected and built high-performance microservices using Python (FastAPI), React, and PostgreSQL, handling 2M+ daily active API calls.
- Spearheaded migration from legacy monolithic server to Docker & Kubernetes on AWS (EKS), reducing infrastructure costs by 35%.
- Led a team of 5 engineers in adopting Agile best practices, decreasing sprint cycle release times from 2 weeks to 3 days.

Software Engineer | Innovate Cloud Inc. | 2019 – 2022
- Developed responsive single-page frontend applications using React.js, Redux, and Tailwind CSS.
- Implemented CI/CD pipelines using GitHub Actions, automating test suites and reducing deployment bugs by 45%.
- Optimized complex SQL queries in PostgreSQL, improving dashboard data loading speeds by 60%.

SKILLS
Programming: Python, JavaScript, TypeScript, SQL, HTML/CSS, C++
Frameworks: React.js, Node.js, Express, FastAPI, Django, Tailwind CSS
Cloud & DevOps: AWS (S3, EC2, Lambda, EKS), Docker, Kubernetes, Git, CI/CD, Terraform
Databases: PostgreSQL, Redis, MongoDB

EDUCATION
B.S. in Computer Science | University of California, Berkeley | 2015 – 2019
"""
        st.session_state.sample_jd = """Senior Full Stack Software Engineer

We are seeking an experienced Senior Full Stack Engineer to join our core product team.

Responsibilities:
- Design, build, and maintain scalable web applications and distributed backend microservices.
- Collaborate with product designers and engineers to build intuitive frontend user interfaces in React and TypeScript.
- Optimize backend services in Python (FastAPI/Django) and Node.js for maximum performance and reliability.
- Manage AWS cloud infrastructure using Docker, Kubernetes, and Terraform.

Requirements:
- 5+ years of full stack software development experience.
- Strong proficiency in Python, JavaScript/TypeScript, React.js, and Node.js.
- Deep experience with relational databases (PostgreSQL/MySQL) and caching (Redis).
- Hands-on experience with AWS, Docker, Kubernetes, and CI/CD pipelines.
- Proven track record of quantifying business impact and mentoring junior developers.
- Bachelor's degree in Computer Science or equivalent practical experience.
"""
        st.rerun()


# File & Job Description Input
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("#### 📄 Candidate Resume")
    uploaded_file = st.file_uploader(
        "Upload Resume (PDF, DOCX, TXT, MD)",
        type=["pdf", "docx", "doc", "txt", "md"],
        label_visibility="collapsed"
    )
    
    resume_text = ""
    if uploaded_file:
        try:
            file_bytes = uploaded_file.read()
            resume_text = extract_text_from_file(file_bytes, uploaded_file.name)
            st.success(f"✅ Loaded '{uploaded_file.name}' ({len(file_bytes)/1024:.1f} KB, {len(resume_text.split())} words)")
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
    elif st.session_state.sample_loaded:
        resume_text = st.session_state.sample_resume
        st.info("ℹ️ Using loaded Sample Resume")
        with st.expander("View Loaded Sample Resume"):
            st.code(resume_text, language="text")

with col2:
    st.markdown("#### 🎯 Target Job Description")
    initial_jd = st.session_state.sample_jd if st.session_state.sample_loaded else ""
    job_description = st.text_area(
        "Paste Job Description",
        value=initial_jd,
        height=220,
        placeholder="Paste the target job description here...",
        label_visibility="collapsed"
    )

st.write("")
analyze_btn = st.button("🚀 ANALYZE RESUME NOW", use_container_width=True)

# Analysis Execution
if analyze_btn:
    if not resume_text.strip():
        st.error("Please upload a resume file or click 'Load Sample Resume'.")
        st.stop()
    if not job_description.strip():
        st.error("Please paste the job description.")
        st.stop()

    user_key = api_key if ('api_key' in locals() and api_key) else None
    user_provider = provider if ('provider' in locals() and provider) else "Auto-detect"

    with st.spinner("⚡ Analyzing resume against job description..."):
        try:
            result = analyze_resume(
                resume_text=resume_text,
                job_description=job_description,
                api_key=user_key,
                provider=user_provider
            )
        except Exception:
            result = fallback_heuristic_analyzer(resume_text, job_description)

    if "warning" in result:
        st.warning(result["warning"])

    st.divider()
    st.markdown("## 📊 Analysis Dashboard")
    st.write("")

    # Top Metric Summary Cards
    score = result.get("match_score", 0)
    score_color = "#34d399" if score >= 75 else ("#fbbf24" if score >= 50 else "#f87171")
    hire = result.get("hire_recommendation", "Maybe")
    hire_class = "hire-yes" if "Yes" in hire else ("hire-no" if hire == "No" else "hire-maybe")

    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="score-number" style="color:{score_color}">{score}</div>
            <div class="score-label">Match Score / 100</div>
        </div>
        ''', unsafe_allow_html=True)
    with m_col2:
        st.markdown(f'''
        <div class="metric-card">
            <div style="font-size:2.5rem;font-weight:800;color:#60a5fa;margin-bottom:8px">{len(result.get("matched_skills", []))}</div>
            <div class="score-label">Skills Matched</div>
        </div>
        ''', unsafe_allow_html=True)
    with m_col3:
        st.markdown(f'''
        <div class="metric-card">
            <div style="font-size:2.5rem;font-weight:800;color:#f87171;margin-bottom:8px">{len(result.get("missing_skills", []))}</div>
            <div class="score-label">Missing Skills</div>
        </div>
        ''', unsafe_allow_html=True)
    with m_col4:
        st.markdown(f'''
        <div class="metric-card">
            <div style="margin-bottom:12px"><span class="hire-badge {hire_class}">{hire}</span></div>
            <div class="score-label">Recruiter Verdict</div>
        </div>
        ''', unsafe_allow_html=True)

    st.write("")

    # Detailed Analysis Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Overview & Fit Assessment",
        "🎯 Skills & Keyword Gap Matrix",
        "🚀 AI Bullet Point Rewriter",
        "🛠️ ATS Formatting & Audit",
        "📄 Raw Resume Text"
    ])

    with tab1:
        st.markdown(f'<div class="verdict-box"><b>Executive Assessment:</b><br>{result.get("verdict", "")}</div>', unsafe_allow_html=True)
        
        c_a, c_b = st.columns(2, gap="large")
        with c_a:
            st.markdown('<div class="section-card"><div class="section-title">✨ Key Strengths</div>', unsafe_allow_html=True)
            for s in result.get("strengths", []):
                st.markdown(f"- {s}")
            st.markdown('</div>', unsafe_allow_html=True)

        with c_b:
            st.markdown('<div class="section-card"><div class="section-title">📈 Actionable Improvements</div>', unsafe_allow_html=True)
            for imp in result.get("improvements", []):
                st.markdown(f"- {imp}")
            st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        col_m1, col_m2 = st.columns(2, gap="large")
        with col_m1:
            matched = result.get("matched_skills", [])
            st.markdown('<div class="section-card"><div class="section-title">✅ Matched Qualifications & Skills</div>', unsafe_allow_html=True)
            if matched:
                st.markdown("".join([f'<span class="tag tag-green">{s}</span>' for s in matched]), unsafe_allow_html=True)
            else:
                st.info("No specific technical skills matched automatically.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_m2:
            missing = result.get("missing_skills", [])
            st.markdown('<div class="section-card"><div class="section-title">⚠️ Missing Target Keywords</div>', unsafe_allow_html=True)
            if missing:
                st.markdown("".join([f'<span class="tag tag-red">{s}</span>' for s in missing]), unsafe_allow_html=True)
            else:
                st.success("All primary job keywords were identified in the resume!")
            st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown("### 🚀 Tailored Bullet Point Rewrites")
        st.caption("Transform generic or weak bullet points into high-impact, ATS-optimized statements tailored to the job description.")
        
        rewrites = result.get("bullet_rewrites", [])
        if rewrites:
            for item in rewrites:
                st.markdown(f'''
                <div class="rewrite-card">
                    <div class="rewrite-orig">❌ Original: {item.get("original", "")}</div>
                    <div class="rewrite-new">✅ Optimized: {item.get("improved", "")}</div>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.info("Your bullet points are already well structured!")

    with tab4:
        st.markdown("### 🛠️ ATS Readiness Audit & Formatting Checklist")
        ats_tips = result.get("ats_tips", [])
        for tip in ats_tips:
            st.markdown(f"- 💡 {tip}")

    with tab5:
        st.markdown("### 📄 Extracted Resume Text")
        st.text_area("Extracted Text", value=resume_text, height=350, label_visibility="collapsed")

    # Export Report Section
    st.divider()
    st.markdown("### 📥 Download Analysis Report")
    
    report_md = f"""# AI Resume & ATS Analysis Report
**Match Score**: {score} / 100
**Hire Recommendation**: {hire}

## Verdict
{result.get('verdict', '')}

## Key Strengths
{"".join([f"- {s}\n" for s in result.get('strengths', [])])}

## Matched Skills
{", ".join(result.get('matched_skills', []))}

## Missing Keywords & Gaps
{", ".join(result.get('missing_skills', []))}

## Actionable Improvements
  {"".join("- " + str(x) + chr(10) for x in result.get("improvements", []))}

## ATS Formatting Tips
  {"".join("- " + str(x) + chr(10) for x in result.get("ats_tips", []))}
"""

    # Ensure result dictionary contains NO sensitive keys before exporting
    clean_result = {k: v for k, v in result.items() if "key" not in k.lower() and "token" not in k.lower()}

    down_col1, down_col2 = st.columns([1, 1])
    with down_col1:
        st.download_button(
            label="📄 Download Report (Markdown .md)",
            data=report_md,
            file_name="resume_ats_analysis_report.md",
            mime="text/markdown"
        )
    with down_col2:
        st.download_button(
            label="📊 Download Raw JSON Data",
            data=json.dumps(clean_result, indent=2),
            file_name="resume_ats_analysis.json",
            mime="application/json"
        )
