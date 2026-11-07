
import streamlit as st
import re
from pypdf import PdfReader
from collections import Counter
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

st.set_page_config(
    page_title="JobMate AI",
    page_icon="💼",
    layout="wide"
)


SKILLS = [
    # Programming Languages
    "python", "java", "javascript", "c++", "sql",

    # Web Development
    "html", "css", "react", "node.js", "streamlit",

    # Software Testing
    "manual testing", "automation testing",
    "software testing", "functional testing",
    "regression testing", "smoke testing",
    "sanity testing", "integration testing",
    "system testing", "unit testing",
    "acceptance testing", "performance testing",
    "api testing", "mobile testing",

    # Testing Concepts
    "stlc", "sdlc", "test cases",
    "test scenarios", "bug tracking",
    "bug reporting", "defect tracking",
    "test execution", "jira", "selenium",
    "postman", "agile", "scrum",

    # Databases and Tools
    "mysql", "database testing", "excel",
    "git", "docker", "aws", "azure",

    # Data and AI
    "machine learning", "deep learning",
    "data analysis", "pandas", "numpy",
    "tensorflow", "pytorch", "power bi",
    "tableau",

    # Soft Skills
    "communication", "leadership",
    "problem solving", "analytical skills",
    "teamwork", "time management",
    "critical thinking", "attention to detail",
    "project management"
]
def generate_pdf_report(results):
    buffer = BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 50

    pdf.setTitle("JobMate AI Resume Analysis Report")

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(50, y, "JobMate AI")
    y -= 30

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Resume Analysis Report")
    y -= 40

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "ATS Analysis")
    y -= 25

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Overall Match: {results['score']}%")
    y -= 20
    pdf.drawString(50, y, f"Technical Score: {results['technical_score']}%")
    y -= 20
    pdf.drawString(50, y, f"Soft Skills Score: {results['soft_score']}%")
    y -= 35

    sections = [
        ("Required Skills - Matched", results["required_matched"]),
        ("Required Skills - Missing", results["required_missing"]),
        ("Preferred Skills - Matched", results["preferred_matched"]),
        ("Preferred Skills - Missing", results["preferred_missing"]),
    ]

    for heading, skills in sections:
        if y < 100:
            pdf.showPage()
            y = height - 50

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y, heading)
        y -= 20

        pdf.setFont("Helvetica", 10)

        text = ", ".join(skills) if skills else "None"

        for line in text.split(", "):
            if y < 60:
                pdf.showPage()
                y = height - 50

            pdf.drawString(60, y, line)
            y -= 15

        y -= 15

    pdf.setFont("Helvetica-Oblique", 9)
    pdf.drawString(
        50, 35,
        "Keyword-based estimate. Not an official ATS score."
    )

    pdf.save()

    buffer.seek(0)
    return buffer
def generate_resume_pdf(
    name, email, phone, location,
    linkedin, github, education,
    experience, skills, projects, summary, template
):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    if template == "Modern":
        accent_color = (0.10, 0.25, 0.45)
        heading_color = (0.10, 0.25, 0.45)
    else:
        accent_color = (0.25, 0.25, 0.25)
        heading_color = (0.15, 0.15, 0.15)
    width, height = A4
    y = height - 55

    pdf.setTitle("Professional Resume")

    def check_space():
        nonlocal y
        if y < 65:
            pdf.showPage()
            y = height - 55

    def add_heading(heading):
        nonlocal y
        check_space()
        pdf.setFillColorRGB(*heading_color)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(50, y, heading)
        pdf.setFillColorRGB(0, 0, 0)
        y -= 22

    def add_text(text):
        nonlocal y

        if not text.strip():
            text = "Not provided"

        pdf.setFont("Helvetica", 10)

        for paragraph in text.splitlines():
            words = paragraph.split()
            line = ""

            for word in words:
                test_line = f"{line} {word}".strip()

                if pdf.stringWidth(test_line, "Helvetica", 10) > width - 100:
                    check_space()
                    pdf.drawString(55, y, line)
                    y -= 15
                    line = word
                else:
                    line = test_line

            if line:
                check_space()
                pdf.drawString(55, y, line)
                y -= 15

        y -= 8

    # Name and Contact
    pdf.setFillColorRGB(*accent_color)
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawCentredString(width / 2, y, name or "Your Name")
    pdf.setFillColorRGB(0, 0, 0)
    y -= 28
    pdf.setFont("Helvetica", 10)

    contact = " | ".join(
        item for item in [email, phone, location] if item
    )

    pdf.drawCentredString(width / 2, y, contact[:100])
    y -= 22

    links = " | ".join(
        item for item in [linkedin, github] if item
    )

    if links:
        pdf.drawCentredString(width / 2, y, links[:100])
        y -= 25

    pdf.setStrokeColorRGB(*accent_color)
    pdf.setLineWidth(1.5)
    pdf.line(50, y, width - 50, y)
    pdf.setStrokeColorRGB(0, 0, 0)
    pdf.setLineWidth(1)
    y -= 25

    # Resume Sections
    sections = [
        ("PROFESSIONAL SUMMARY", summary),
        ("TECHNICAL SKILLS", skills),
        ("EDUCATION", education),
        ("WORK EXPERIENCE", experience),
        ("PROJECTS", projects)
    ]

    for heading, content in sections:
        add_heading(heading)
        add_text(content)

    pdf.save()
    buffer.seek(0)

    return buffer
def extract_resume(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"
    return text

def extract_skills(text):
    text = text.lower()
    return [skill for skill in SKILLS if
            re.search(r"(?<!\w)" + re.escape(skill) + r"(?!\w)", text)]


SOFT_SKILLS = [
    "communication", "leadership", "teamwork",
    "problem solving", "analytical skills",
    "time management", "critical thinking",
    "attention to detail"
]

def analyze_resume(resume, job_description):
    resume_skills = set(extract_skills(resume))
    jd = job_description.lower()

    preferred_pattern = (
        r"(preferred skills|preferred qualifications|"
        r"nice to have|good to have|bonus skills)"
    )

    match = re.search(preferred_pattern, jd)

    if match:
        required_text = jd[:match.start()]
        preferred_text = jd[match.start():]
    else:
        required_text = jd
        preferred_text = ""

    required_skills = set(extract_skills(required_text))
    preferred_skills = (
        set(extract_skills(preferred_text)) - required_skills
    )

    soft_set = set(SOFT_SKILLS)

    required_technical = required_skills - soft_set
    preferred_technical = preferred_skills - soft_set

    required_soft = required_skills & soft_set
    preferred_soft = preferred_skills & soft_set

    matched_required = required_skills & resume_skills
    matched_preferred = preferred_skills & resume_skills

    missing_required = required_skills - resume_skills
    missing_preferred = preferred_skills - resume_skills

    def percentage(matched, total):
        return round(len(matched) / len(total) * 100) if total else 0

    total_weight = (
        3 * len(required_skills) + len(preferred_skills)
    )

    earned_weight = (
        3 * len(matched_required) + len(matched_preferred)
    )

    overall_score = (
        round(earned_weight / total_weight * 100)
        if total_weight else 0
    )

    technical_total = required_technical | preferred_technical
    technical_matched = resume_skills & technical_total

    soft_total = required_soft | preferred_soft
    soft_matched = resume_skills & soft_total

    return {
        "score": overall_score,
        "matched": sorted(matched_required | matched_preferred),
        "missing": sorted(missing_required | missing_preferred),
        "required_matched": sorted(matched_required),
        "required_missing": sorted(missing_required),
        "preferred_matched": sorted(matched_preferred),
        "preferred_missing": sorted(missing_preferred),
        "technical_score": percentage(
            technical_matched, technical_total
        ),
        "soft_score": percentage(soft_matched, soft_total)
    }
SKILL_GROUPS = {
    "Testing Fundamentals": [
        "manual testing", "software testing", "functional testing",
        "regression testing", "smoke testing", "sanity testing",
        "integration testing", "system testing", "unit testing",
        "acceptance testing", "performance testing", "api testing",
        "mobile testing", "stlc", "sdlc", "test cases",
        "test scenarios", "test execution"
    ],
    "Testing Tools": [
        "jira", "selenium", "postman", "automation testing",
        "bug tracking", "bug reporting", "defect tracking"
    ],
    "Programming & Web": [
        "python", "java", "javascript", "c++", "html",
        "css", "react", "node.js", "sql", "streamlit"
    ],
    "Databases": [
        "mysql", "database testing", "excel"
    ],
    "Cloud & DevOps": [
        "git", "docker", "aws", "azure"
    ],
    "Data & AI": [
        "machine learning", "deep learning", "data analysis",
        "pandas", "numpy", "tensorflow", "pytorch",
        "power bi", "tableau"
    ],
    "Soft Skills": [
        "communication", "leadership", "teamwork",
        "problem solving", "analytical skills",
        "time management", "critical thinking",
        "attention to detail", "project management"
    ]
}

CATEGORY_TIPS = {
    "Testing Fundamentals": "Learn SDLC and STLC, then practice writing test cases, bug reports and regression tests.",
    "Testing Tools": "Start with Jira, then practice API testing with Postman and automation with Selenium.",
    "Programming & Web": "Build small projects and practice programming fundamentals.",
    "Databases": "Practice SQL queries, joins and database validation.",
    "Cloud & DevOps": "Learn Git basics, then explore Docker and cloud fundamentals.",
    "Data & AI": "Start with Python, Pandas and NumPy before machine learning.",
    "Soft Skills": "Practice through team projects, presentations and problem-solving exercises."
}
LEARNING_ROADMAP = {
    "Testing Fundamentals": {
        "duration": "2 Days",
        "topics": [
            "SDLC and STLC",
            "Test Scenarios and Test Cases",
            "Functional Testing",
            "Smoke, Sanity and Regression Testing"
        ],
        "task": "Create 10 test cases for a login page."
    },

    "Testing Tools": {
        "duration": "2 Days",
        "topics": [
            "Jira for Bug Tracking",
            "Postman for API Testing",
            "Selenium Basics"
        ],
        "task": "Create a bug report and test a sample API."
    },

    "Databases": {
        "duration": "1 Day",
        "topics": [
            "SQL SELECT Queries",
            "WHERE, ORDER BY and GROUP BY",
            "SQL JOIN Operations",
            "Database Validation"
        ],
        "task": "Write 10 SQL queries using sample employee data."
    },

    "Programming & Web": {
        "duration": "2 Days",
        "topics": [
            "Programming Fundamentals",
            "HTML and CSS Basics",
            "Python Fundamentals"
        ],
        "task": "Build a simple webpage and test its functionality."
    },

    "Cloud & DevOps": {
        "duration": "1 Day",
        "topics": [
            "Git and GitHub Basics",
            "Docker Fundamentals",
            "Cloud Computing Basics"
        ],
        "task": "Upload a small project to GitHub."
    },

    "Data & AI": {
        "duration": "2 Days",
        "topics": [
            "Python for Data Analysis",
            "Pandas and NumPy",
            "Machine Learning Basics"
        ],
        "task": "Analyze a small dataset using Pandas."
    },

    "Soft Skills": {
        "duration": "Ongoing Practice",
        "topics": [
            "Communication",
            "Problem Solving",
            "Attention to Detail",
            "Teamwork"
        ],
        "task": "Explain your testing project in a 2-minute presentation."
    }
}
SKILL_IMPROVEMENT_TIPS = {
    "manual testing": "Mention hands-on experience testing applications manually.",
    "functional testing": "Practice testing application features against requirements.",
    "regression testing": "Learn how to verify existing features after code changes.",
    "smoke testing": "Practice basic build verification test cases.",
    "sanity testing": "Learn focused testing after minor application changes.",
    "stlc": "Understand all phases of the Software Testing Life Cycle.",
    "sdlc": "Learn the stages of the Software Development Life Cycle.",
    "test cases": "Practice writing test cases with steps and expected results.",
    "test scenarios": "Create test scenarios for login, signup and checkout pages.",
    "database testing": "Practice SQL queries and database validation.",
    "defect tracking": "Learn how to report, track and verify software defects.",
    "bug reporting": "Write bug reports with steps, expected and actual results.",
    "jira": "Practice creating and tracking bugs using Jira.",
    "selenium": "Start learning Selenium WebDriver with Java or Python.",
    "postman": "Practice sending API requests and validating responses.",
    "api testing": "Learn HTTP methods, status codes and API validation.",
    "automation testing": "Understand automation testing concepts and frameworks.",
    "agile": "Learn Agile principles and iterative software development.",
    "scrum": "Understand sprint planning, daily standups and retrospectives.",
    "communication": "Practice explaining your projects and sharing updates clearly.",
    "attention to detail": "Practice reviewing test results and identifying small inconsistencies."
}
JOB_ROLES = {
    "Python Developer": [
        "python", "sql", "git", "problem solving"
    ],
    "Data Analyst": [
        "python", "sql", "excel", "pandas",
        "numpy", "data analysis", "power bi"
    ],
    "QA Tester": [
    "manual testing",
    "software testing",
    "test cases",
    "test scenarios",
    "bug reporting",
    "defect tracking",
    "jira",
    "sql",
    "functional testing",
    "regression testing",
    "smoke testing",
    "sanity testing",
    "sdlc",
    "stlc"
    ],
    "Software Tester": [
        "manual testing", "software testing",
        "test cases", "bug reporting",
        "jira", "sql", "regression testing"
    ],
    "Web Developer": [
        "html", "css", "javascript",
        "react", "node.js", "git"
    ],
    "Machine Learning Engineer": [
        "python", "machine learning",
        "deep learning", "pandas", "numpy"
    ],
    "Database Developer": [
        "sql", "mysql", "database testing", "excel"
    ]
}
# Sidebar
with st.sidebar:
    st.title("💼 JobMate AI")
    st.caption("Your Personal AI Career Assistant")
    page = st.radio(
        "Navigation",
        [
    "Dashboard",
    "Resume Analyzer",
    "Resume Builder",
    "Job Recommendations",
    "About"
]
    )
    st.divider()
    st.caption("Hackathon Edition 🚀")


# Dashboard
if page == "Dashboard":
    st.title("💼 Welcome to JobMate AI")
    st.subheader("Your Personal AI-Powered Job Assistant")

    st.success("Your career journey starts here!")

    col1, col2, col3 = st.columns(3)
    col1.metric("Core Features", "5")
    col2.metric("Resume Analysis", "Ready")
    col3.metric("Job Matching", "Ready")

    st.markdown("### Explore your career tools")

    st.write("📄 **Resume Analyzer** – Analyze your PDF resume.")
    st.write("🎯 **ATS Matching** – Compare your resume with a job description.")
    st.write("🧠 **Skills Gap Analysis** – Identify missing skills.")
    st.write("💡 **Career Recommendations** – Get improvement suggestions.")

    st.info("Select Resume Analyzer from the sidebar to get started.")


# Resume Analyzer
elif page == "Resume Analyzer":
    st.title("📄 Smart Resume Analyzer")
    st.write("Upload your resume and compare it with your target job.")

    uploaded_file = st.file_uploader(
        "Upload your resume (PDF)",
        type=["pdf"]
    )

    job_description = st.text_area(
        "Paste the Job Description",
        height=200,
        placeholder="Paste the job requirements here..."
    )

    if st.button("Analyze My Resume", type="primary"):
        if uploaded_file is None:
            st.error("Please upload your PDF resume.")
        elif not job_description.strip():
            st.error("Please enter a job description.")
        else:
            
            try:
                with st.spinner("Analyzing your resume..."):
                    resume_text = extract_resume(uploaded_file)

                    if not resume_text.strip():
                        st.error(
                            "No readable text found. Please use a text-based PDF."
                        )
                    else:
                        results = analyze_resume(
                            resume_text, job_description
                        )

                        st.divider()
                        st.subheader("📊 Intelligent ATS Analysis")

                        col1, col2, col3 = st.columns(3)

                        col1.metric("Overall Match", f"{results['score']}%")
                        col2.metric("Technical Score", f"{results['technical_score']}%")
                        col3.metric("Soft Skills Score", f"{results['soft_score']}%")

                        st.progress(results["score"] / 100)

                        if results["score"] >= 75:
                            st.success("Strong keyword match!")
                        elif results["score"] >= 40:
                            st.warning("Moderate match. Some improvements needed.")
                        else:
                            st.error("Low match. Consider improving your skill alignment.")

                        st.subheader("🎯 Required Skills")
                        st.write("✅ Matched:")
                        st.write(", ".join(results["required_matched"]) or "None")

                        st.write("⚠️ Missing:")
                        st.write(", ".join(results["required_missing"]) or "None")

                        st.subheader("⭐ Preferred Skills")
                        st.write("✅ Matched:")
                        st.write(", ".join(results["preferred_matched"]) or "None")

                        st.write("⚠️ Missing:")
                        st.write(", ".join(results["preferred_missing"]) or "None")
                        st.subheader("🧠 Smart Skill Gap Analysis")

                        missing_skills = set(results["missing"])
                        gap_found = False

                        for category, skills in SKILL_GROUPS.items():
                            category_gaps = [
                                skill for skill in skills
                                if skill in missing_skills
                            ]

                            if category_gaps:
                                gap_found = True

                                with st.expander(
                                    f"📌 {category} — "
                                    f"{len(category_gaps)} missing skills"
                                ):
                                    st.write("**Skills to improve:**")
                                    st.write(", ".join(category_gaps))

                                    st.info(CATEGORY_TIPS[category])

                        if not gap_found:
                            st.success(
                                "🎉 No skill gaps detected! "
                                "Your resume matches all detected skills."
                            )
                        st.subheader("📈 ATS Score Improvement Suggestions")

                        all_missing_skills = (
                            results["required_missing"]
                            + results["preferred_missing"]
                        )

                        for skill in all_missing_skills:
                            tip = SKILL_IMPROVEMENT_TIPS.get(
                                skill,
                                f"Learn {skill} and add genuine evidence of it to your resume."
                            )

                            st.info(f"💡 **{skill.title()}:** {tip}")
                        st.subheader("🚀 Personalized Recommendations")

                        for skill in results["required_missing"]:
                            st.warning(
                                f"Required: Improve or add evidence for **{skill}**."
                            )

                        for skill in results["preferred_missing"]:
                            st.info(
                                f"Preferred: Consider learning **{skill}** "
                                "for an additional advantage."
                            )
                        st.divider()
                        st.subheader("🗺️ Your Personalized Learning Roadmap")

                        roadmap_found = False

                        for category, skills in SKILL_GROUPS.items():
                            category_gaps = [
                                skill for skill in skills
                                if skill in missing_skills
                            ]

                            if category_gaps and category in LEARNING_ROADMAP:
                                roadmap_found = True
                                roadmap = LEARNING_ROADMAP[category]

                                with st.expander(
                                    f"📚 {category} | {roadmap['duration']}"
                                ):
                                    st.write("**What you should learn:**")

                                    for topic in roadmap["topics"]:
                                        st.write(f"📌 {topic}")

                                    st.success(
                                        f"🎯 Practice Task: {roadmap['task']}"
                                    )

                        if not roadmap_found:
                            st.success(
                                "🎉 Great! No learning gaps found. "
                                "Keep improving your skills!"
                            )
                        st.caption(
                            "This is a weighted keyword-based estimate, "
                            "not an official ATS score or hiring prediction."
                        )
                        pdf_report = generate_pdf_report(results)

                        st.download_button(
                            label="📥 Download Analysis Report",
                            data=pdf_report,
                            file_name="JobMate_AI_Analysis_Report.pdf",
                            mime="application/pdf"
                        )
            except Exception as e:
                st.error(f"Something went wrong: {e}")
            
# Resume Builder
elif page == "Resume Builder":
    st.title("📝 Professional Resume Builder")
    st.write("Create your professional resume in minutes!")

    st.subheader("👤 Personal Information")

    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    location = st.text_input("City / Location")
    linkedin = st.text_input("LinkedIn Profile URL")
    github = st.text_input("GitHub Profile URL")
    st.divider()
    st.subheader("🎓 Education")

    education = st.text_area(
        "Education Details",
        placeholder="Degree, College Name, University, Graduation Year..."
    )

    st.divider()
    st.subheader("💼 Work Experience")

    experience = st.text_area(
        "Work Experience / Internship",
        placeholder="Company Name, Role, Duration and Responsibilities..."
    )

    st.divider()
    st.subheader("🛠️ Skills")

    skills = st.text_area(
        "Your Skills",
        placeholder="Python, SQL, HTML, CSS, Manual Testing..."
    )

    st.divider()
    st.subheader("🚀 Projects")

    projects = st.text_area(
        "Project Details",
        placeholder="Project Name, Technologies Used and Description..."
    )
    st.divider()
    st.subheader("🎨 Choose Your Resume Template")

    template = st.radio(
        "Select a design",
        ["Modern", "Minimal"],
        horizontal=True
    )
    st.divider()
    st.subheader("📝 Professional Summary")

    summary = st.text_area(
        "About Yourself",
        placeholder="Write 2-3 lines about your professional profile..."
    )
    st.divider()

    if st.button("📄 Generate My Resume", type="primary"):
        if not name.strip():
            st.error("Please enter your full name.")
        else:
            resume_pdf = generate_resume_pdf(
                name, email, phone, location,
                linkedin, github, education,
                experience, skills, projects, summary, template
            )

            st.success("Your professional resume is ready!")

            st.download_button(
                label="📥 Download My Resume",
                data=resume_pdf,
                file_name="My_Professional_Resume.pdf",
                mime="application/pdf"
            ) 
# Job Recommendations
elif page == "Job Recommendations":
    st.title("🎯 AI Job Recommendations")
    st.write(
        "Upload your resume to discover job roles "
        "that match your skills."
    )

    uploaded_file = st.file_uploader(
        "Upload your Resume (PDF)",
        type=["pdf"],
        key="job_recommendation_resume"
    )

    if uploaded_file is not None:
        try:
            resume_text = extract_resume(uploaded_file)

            if not resume_text.strip():
                st.error(
                    "No readable text found in this PDF."
                )
            else:
                resume_skills = set(
                    extract_skills(resume_text)
                )

                st.divider()
                st.subheader("🛠️ Skills Found in Your Resume")

                if resume_skills:
                    st.write(
                        ", ".join(sorted(resume_skills))
                    )
                else:
                    st.warning(
                        "No recognized skills found. "
                        "Try uploading a detailed resume."
                    )

                st.divider()
                st.subheader("💼 Recommended Job Roles")

                recommendations = []

                for role, required_skills in JOB_ROLES.items():
                    matched = (
                        resume_skills & set(required_skills)
                    )
                    missing = (
                        set(required_skills) - resume_skills
                    )

                    score = round(
                        len(matched) / len(required_skills) * 100
                    )

                    recommendations.append(
                        (role, score, matched, missing)
                    )

                recommendations.sort(
                    key=lambda item: item[1],
                    reverse=True
                )

                for role, score, matched, missing in recommendations:
                    with st.expander(
                        f"{role} — {score}% Match"
                    ):
                        st.progress(score / 100)

                        st.write("✅ **Matched Skills:**")
                        st.write(
                            ", ".join(sorted(matched)) or "None"
                        )

                        st.write("⚠️ **Skills to Improve:**")
                        st.write(
                            ", ".join(sorted(missing)) or "None"
                        )

                        if score >= 70:
                            st.success(
                                "Great match! This role aligns "
                                "well with your detected skills."
                            )
                        elif score >= 40:
                            st.warning(
                                "Good starting point. Improve "
                                "the missing skills."
                            )
                        else:
                            st.info(
                                "You may need additional learning "
                                "and practice for this role."
                            )

                st.caption(
                    "Recommendations are based on keyword matching "
                    "and do not guarantee job eligibility."
                )

        except Exception as e:
            st.error(f"Something went wrong: {e}")
elif page == "About":
    st.title("About JobMate AI")
    st.write("""
    JobMate AI is an intelligent career assistant designed
    to help job seekers improve their resumes and find better
    job opportunities.

    Our goal is to make career preparation smarter,
    simpler and more accessible.
    """)
    st.info("Built with Python and Streamlit.")
