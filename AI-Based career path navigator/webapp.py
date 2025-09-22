import os
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import random
import sqlite3
from serpapi import GoogleSearch
import openai

# ---------- Config ----------
st.set_page_config(page_title="AI Career Path Navigator", page_icon="🎓", layout="wide")

# Read API keys from environment (fallback to placeholders if you want to paste them directly)
SERPAPI_KEY = "api_key"
openai.api_key = "api_key"

# ---------- Database Helper Functions ----------
def get_career_paths():
    conn = sqlite3.connect("career_paths.db")
    c = conn.cursor()
    c.execute("SELECT career, skills FROM career_paths")
    data = {career: skills.split(",") for career, skills in c.fetchall()}
    conn.close()
    return data

def get_career_roadmap(career):
    conn = sqlite3.connect("career_paths.db")
    c = conn.cursor()
    c.execute("SELECT step FROM career_roadmaps WHERE career=? ORDER BY step_order", (career,))
    steps = [row[0] for row in c.fetchall()]
    conn.close()
    return steps

def get_skill_importance(career):
    conn = sqlite3.connect("career_paths.db")
    c = conn.cursor()
    c.execute("SELECT skill, importance FROM career_skill_importance WHERE career=?", (career,))
    skills = {skill: importance for skill, importance in c.fetchall()}
    conn.close()
    return skills

def get_career_income(career):
    conn = sqlite3.connect("career_paths.db")
    c = conn.cursor()
    c.execute("SELECT fresher_income, experienced_income FROM career_income WHERE career=?", (career,))
    row = c.fetchone()
    conn.close()
    if row:
        return row
    return (0, 0)

# ---------- Jobs + AI Helpers ----------
@st.cache_data(ttl=3600)  # cache for 1 hour to avoid hitting rate limits
def fetch_linkedin_jobs(career, location=None, limit=10):
    """
    Fetch job postings (prefers LinkedIn results) using SerpAPI Google Jobs engine.
    Returns a list of job dicts.
    """
    try:
        q = f"{career} site:linkedin.com/jobs"
        if location:
            q = f"{career} site:linkedin.com/jobs {location}"
        params = {
            "engine": "google_jobs",
            "q": q,
            "api_key": SERPAPI_KEY
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        jobs = results.get("jobs_results", []) or results.get("organic_results", []) or []
        return jobs[:limit]
    except Exception as e:
        # Return empty list on errors (show message upstream)
        st.session_state.setdefault("_serp_error", str(e))
        return []

def summarize_jobs_with_ai(jobs, career, max_jobs=5):
    """
    Use OpenAI to summarize the given job postings into a short, user-friendly summary.
    """
    if not jobs:
        return f"No recent LinkedIn job results found for **{career}**."

    snippets = []
    for job in jobs[:max_jobs]:
        title = job.get("title") or job.get("job_title") or "Unknown Role"
        company = job.get("company_name") or job.get("company") or "Unknown Company"
        location = job.get("location") or job.get("job_location") or "Unknown Location"
        desc = job.get("snippet") or job.get("description") or ""
        link = job.get("link") or job.get("source") or ""
        snippets.append(f"- **{title}** at {company} — {location}\n  {desc}\n  Link: {link}")

    prompt = f"""
You are a helpful career assistant. Summarize the following {len(snippets)} job postings for the role "{career}" into:
1) A 2-3 line overview for a fresher (is it relevant? why/why not).
2) Top 3 roles that look best (title @ company - reason).
3) Important skills to highlight from these listings.

Jobs:
{chr(10).join(snippets)}

Provide the summary in plain text with short bullet points.
"""

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a career advisor."},
                      {"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.2,
        )
        return resp["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"AI summarization failed: {e}"

# ---------- Small helpers ----------
def plot_roadmap(career, steps):
    fig, ax = plt.subplots(figsize=(6, max(3, len(steps) * 0.6)))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, len(steps))
    for i, step in enumerate(steps):
        y = len(steps) - i - 1
        ax.plot(0.1, y, "o", markersize=10)
        ax.text(0.15, y, step, fontsize=10, va="center")
    ax.axis("off")
    st.pyplot(fig)

def suggest_careers(user_skills, user_interests, career_paths):
    user_skills = [s.strip().lower() for s in user_skills.split(",") if s.strip() != ""]
    scores = {}
    for career, required_skills in career_paths.items():
        match_count = sum(skill.lower() in user_skills for skill in required_skills)
        interest_boost = any(word.lower() in career.lower() for word in user_interests.split())
        scores[career] = match_count + (1 if interest_boost else 0)
    sorted_careers = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [career for career, score in sorted_careers if score > 0]

def generate_default_roadmap(career):
    return [
        f"Learn basic skills for {career}",
        "Do a small project",
        "Build a portfolio",
        "Apply for internships / freelancing",
        "Keep learning advanced concepts"
    ]

def generate_default_skills(career):
    skills = ["Skill A", "Skill B", "Skill C", "Skill D"]
    values = [random.randint(15, 35) for _ in skills]
    total = sum(values)
    values = [int(v * 100 / total) for v in values]
    return dict(zip(skills, values))

# ---------- Sidebar Navigation ----------
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Career Navigator", "About"])

# ---------- HOME ----------
if page == "Home":
    st.title("🎓 AI Career Path Navigator")
    st.write("""
        Welcome to the **AI-based Career Path Navigator**!  
        Discover personalized career options based on your **skills, interests, and goals**.
        👉 Use the sidebar to start exploring!
    """)
    st.image("https://img.freepik.com/free-vector/flat-design-career-guidance-concept_23-2149153504.jpg", use_container_width=True)

# ---------- CAREER NAVIGATOR ----------
elif page == "Career Navigator":
    st.title("🚀 Find Your Career Path")

    name = st.text_input("Enter your name:")
    skills = st.text_area("List your skills (comma separated):")
    interests = st.text_area("What are your main interests?")
    goal = st.selectbox("Your career goal:", ["Job", "Higher Studies", "Entrepreneurship", "Not sure yet"])
    location_filter = st.text_input("Optional: Preferred location (city/country) for job search:")

    if st.button("Suggest Career Paths"):
        if skills.strip() == "" and interests.strip() == "":
            st.warning("⚠️ Please enter your skills and interests first.")
        else:
            career_paths = get_career_paths()
            suggestions = suggest_careers(skills, interests, career_paths)
            if suggestions:
                st.subheader(f"Hi {name}, here are some career suggestions for you:")
                for s in suggestions:
                    st.success(f"💡 {s}")
                    with st.expander(f"📘 Roadmap for {s}"):
                        roadmap = get_career_roadmap(s) or generate_default_roadmap(s)
                        for step in roadmap:
                            st.write(f"- {step}")

                        skills_dict = get_skill_importance(s) or generate_default_skills(s)
                        st.write("📊 Skill Importance Pie Chart:")
                        fig = px.pie(
                            names=list(skills_dict.keys()),
                            values=list(skills_dict.values()),
                            title=f"Skill Importance for {s}"
                        )
                        st.plotly_chart(fig)

                        # Display income
                        fresher_salary, experienced_salary = get_career_income(s)
                        st.write("💰 **Average Annual Salary**")
                        st.write(f"- Fresher: ₹{int(fresher_salary):,}" if fresher_salary else "- Fresher: N/A")
                        st.write(f"- Experienced: ₹{int(experienced_salary):,}" if experienced_salary else "- Experienced: N/A")

                        # ---------- LinkedIn Jobs (SerpAPI) + AI ----------
                        with st.expander(f"💼 Current LinkedIn Jobs & AI Summary for {s}"):
                            if "_serp_error" in st.session_state:
                                st.error(f"SerpAPI error: {st.session_state['_serp_error']}")
                            jobs = fetch_linkedin_jobs(s, location=location_filter, limit=10)
                            if not jobs:
                                st.info("No jobs found or SerpAPI returned no results. You can try changing the role text or location.")
                            else:
                                # Show summarized AI output
                                with st.spinner("Summarizing jobs with OpenAI..."):
                                    summary = summarize_jobs_with_ai(jobs, s, max_jobs=5)
                                st.markdown(summary)

                                st.markdown("**Top job listings (raw):**")
                                for job in jobs[:10]:
                                    title = job.get("title") or job.get("job_title") or "Unknown Role"
                                    company = job.get("company_name") or job.get("company") or "Unknown Company"
                                    location = job.get("location") or job.get("job_location") or ""
                                    link = job.get("link") or job.get("source") or ""
                                    snippet = job.get("snippet") or job.get("description") or ""
                                    st.markdown(f"**{title}**  \n{company} — {location}")
                                    if snippet:
                                        st.write(snippet)
                                    if link:
                                        st.write(link)
                                    st.write("---")

            else:
                st.error("😕 Sorry, we couldn’t find a good match. Try adding more skills or interests!")

# ---------- ABOUT ----------
elif page == "About":
    st.title("ℹ️ About this App")
    st.write("""
        This app was built during a **Hackathon** to guide students in choosing career paths.  
        Features:  
        - AI-based career recommendations  
        - Skill roadmap suggestions  
        - Interactive visualizations  
        - Average salary info for freshers and experienced professionals  
        - Live LinkedIn job/internship fetch + OpenAI-powered summarization
    """)
    st.write("Make sure you set SERPAPI_KEY and OPENAI_API_KEY environment variables before running this app.")
