"""
Vercel Python serverless function — generates the resume PDF on demand.
Route: /api/resume

To update the resume content, edit RESUME (below) and push. No need to
regenerate or re-upload a PDF file by hand — every request builds it fresh
from this data.
"""
from http.server import BaseHTTPRequestHandler
from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, HRFlowable
from reportlab.lib.styles import ParagraphStyle

# ---------------------------------------------------------------------------
# SINGLE SOURCE OF TRUTH for the resume PDF's content.
# ---------------------------------------------------------------------------
RESUME = {
    "name": "Syed Ahmed Ali Shah",
    "role": "Software Developer — full-stack, blockchain & AI",
    "contact": (
        "ahmedalishah96@gmail.com &nbsp;&middot;&nbsp; +92 301 2278148 &nbsp;&middot;&nbsp; "
        "Sukkur, Pakistan &nbsp;&middot;&nbsp; github.com/Ahmeds168 &nbsp;&middot;&nbsp; "
        "linkedin.com/in/syed-ahmed-ali-shah-477936b4"
    ),
    "summary": (
        "Software developer with 5+ years spanning web, mobile, and database-driven applications. "
        "Most recently a Software Development Intern at Sukkur IBA University's Department of Electrical "
        "Engineering, managing OJS journal administration, departmental web systems, and office "
        "automation. Previously built Django/Flask and PostgreSQL solutions remotely for Clear Edge "
        "Technology (Canada). Holds a BS in Computer Science from Sukkur IBA University, with a "
        "blockchain-based voting system as a final-year project. Skilled in Python, JavaScript, Java, "
        "PHP, and Oracle/PostgreSQL administration, with growing expertise in prompt engineering, "
        "machine learning, and smart contract development."
    ),
    "skills": (
        "Python, JavaScript, Java, PHP, Django, Flask, Solidity &nbsp;|&nbsp; PostgreSQL Admin, "
        "Oracle DB Admin, Web Development, Android Development, Desktop Apps &nbsp;|&nbsp; "
        "Blockchain, Prompt Engineering, Machine Learning &nbsp;|&nbsp; Communication, Management"
    ),
    "experience": [
        {
            "title": "Software Development Intern — Dept. of Electrical Engineering, Sukkur IBA University",
            "meta": "Jun 2024 – Jul 2026 · Sukkur, Sindh, Pakistan",
            "bullets": [
                "Administered and upgraded the department's Open Journal Systems (OJS) installation",
                "Owned department website administration end-to-end",
                "Automated recurring office workflows and documentation",
            ],
        },
        {
            "title": "Software Developer — Clear Edge Technology",
            "meta": "May 2021 – May 2024 · Canada (Remote)",
            "bullets": [
                "Built and maintained Django/Flask applications backed by PostgreSQL",
                "Developed interactive canvas features with Konva.js",
            ],
        },
        {
            "title": "Web Application Developer Intern — Vasona Systems International",
            "meta": "Aug 2019 – Dec 2019 · Sukkur, Sindh, Pakistan",
            "bullets": ["Built features in .NET; handled website and email troubleshooting"],
        },
    ],
    "projects": [
        ("Decentralized Document Notary", "Blockchain-based document notarization app (Solidity, React, Node.js, Supabase, Cloudflare R2) — deployed on Sepolia, Render &amp; Vercel."),
        ("On-Chain Voting dApp", "Solidity (Hardhat) voting contract with a React + ethers.js frontend styled like an official paper ballot."),
        ("Groq Chat App", "Full-stack chat app — Node.js/Express backend calling the Groq API, React (Vite) frontend."),
        ("Election System Using Blockchain (SISC)", "Final-year project — permissioned blockchain voting system on Hyperledger Fabric via IBM Blockchain VS Code extension."),
        ("Analyzing Students' Mental Health", "PostgreSQL-driven analysis of whether studying abroad affects student mental health."),
        ("Pet Recognition (CNN)", "Convolutional neural network classifying cats vs. dogs at ~90% accuracy."),
        ("Campus Management Solution", "Java + Oracle SQL system for storing student, teacher and course records."),
    ],
    "education": [
        ("BS, Computer Science", "Sukkur IBA University, Sukkur (Aug 2016 – Aug 2021)"),
        ("Intermediate", "Islamia Science College, Sukkur (2012 – 2014)"),
    ],
    "certificates": [
        ("AI Agents and Agentic AI with Python &amp; Generative AI — Vanderbilt University, Coursera (Aug 2026)", "https://coursera.org/verify/QYURRCUBHM69"),
        ("Blockchain Basics — Cyfrin (Mar 2026)", "https://profiles.cyfrin.io/u/ahmedalishah96/certificates/blockchain-basics"),
        ("Solidity Smart Contract Development — Cyfrin (Aug 2026)", "https://profiles.cyfrin.io/u/ahmedalishah96/achievements/solidity"),
        ("Prompt Engineering with the OpenAI API — DataCamp (Jul 2026)", "https://www.datacamp.com/completed/statement-of-accomplishment/course/d976e79b35b1d1deeb33d3dba0738324770f45b1"),
        ("Introduction to SQL — DataCamp (Jul 2026)", None),
        ("Intermediate SQL — DataCamp (Aug 2026)", "https://www.datacamp.com/completed/statement-of-accomplishment/course/23b50d8a1f729b35261f7ad42dec9e8b456d2951"),
        ("Joining Data in SQL — DataCamp (Aug 2026)", "https://www.datacamp.com/completed/statement-of-accomplishment/course/3f4641402a4960d125c594b8acfcec8b4d7ab82f"),
        ("Working with Hugging Face — DataCamp (Aug 2026)", "https://www.datacamp.com/completed/statement-of-accomplishment/course/de7ca41c80b3ff209d431a2cfecbb90f51097597"),
        ("Vasona Systems International — Internship Certificate (2019)", None),
    ],
    "achievements": "Won Aptech Web Development Challenge (Nov 2017 – Feb 2018)",
    "languages": "English (Full Professional), Urdu (Native), Sindhi (Native)",
}

NAVY = colors.HexColor("#12161C")
ACCENT = colors.HexColor("#000000")  # black — classic, recruiter-safe for print
GREY = colors.HexColor("#555555")


def build_pdf() -> bytes:
    buf = BytesIO()

    styles = {
        "name": ParagraphStyle("name", fontName="Helvetica-Bold", fontSize=20, textColor=NAVY, leading=24, spaceAfter=4),
        "role": ParagraphStyle("role", fontName="Helvetica", fontSize=11, textColor=ACCENT, spaceBefore=2, spaceAfter=8),
        "contact": ParagraphStyle("contact", fontName="Helvetica", fontSize=9, textColor=GREY, spaceAfter=10),
        "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=11.5, textColor=NAVY, spaceBefore=12, spaceAfter=4),
        "body": ParagraphStyle("body", fontName="Helvetica", fontSize=9.3, textColor=colors.HexColor("#222222"), leading=13, spaceAfter=4),
        "jobtitle": ParagraphStyle("jobtitle", fontName="Helvetica-Bold", fontSize=9.8, textColor=NAVY, spaceBefore=6),
        "jobmeta": ParagraphStyle("jobmeta", fontName="Helvetica-Oblique", fontSize=8.7, textColor=GREY, spaceAfter=3),
        "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.2, textColor=colors.HexColor("#222222"), leading=12.5, leftIndent=12, spaceAfter=2),
    }

    def hr():
        return HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#CCCCCC"), spaceBefore=2, spaceAfter=6)

    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        topMargin=0.55 * inch, bottomMargin=0.55 * inch,
        leftMargin=0.65 * inch, rightMargin=0.65 * inch,
    )

    flow = []
    flow.append(Paragraph(RESUME["name"], styles["name"]))
    flow.append(Paragraph(RESUME["role"], styles["role"]))
    flow.append(Paragraph(RESUME["contact"], styles["contact"]))
    flow.append(hr())

    flow.append(Paragraph("SUMMARY", styles["h2"]))
    flow.append(Paragraph(RESUME["summary"], styles["body"]))

    flow.append(Paragraph("SKILLS", styles["h2"]))
    flow.append(Paragraph(RESUME["skills"], styles["body"]))

    flow.append(Paragraph("EXPERIENCE", styles["h2"]))
    for job in RESUME["experience"]:
        flow.append(Paragraph(job["title"], styles["jobtitle"]))
        flow.append(Paragraph(job["meta"], styles["jobmeta"]))
        for b in job["bullets"]:
            flow.append(Paragraph("• " + b, styles["bullet"]))

    flow.append(Paragraph("PROJECTS", styles["h2"]))
    for title, desc in RESUME["projects"]:
        flow.append(Paragraph(f"<b>{title}</b> — {desc}", styles["bullet"]))

    flow.append(Paragraph("EDUCATION", styles["h2"]))
    for degree, meta in RESUME["education"]:
        flow.append(Paragraph(f"<b>{degree}</b> — {meta}", styles["bullet"]))

    flow.append(Paragraph("CERTIFICATES", styles["h2"]))
    for text, url in RESUME["certificates"]:
        if url:
            flow.append(Paragraph(f'• <link href="{url}" color="#000000">{text}</link>', styles["bullet"]))
        else:
            flow.append(Paragraph("• " + text, styles["bullet"]))

    flow.append(Paragraph("ACHIEVEMENTS &amp; LANGUAGES", styles["h2"]))
    flow.append(Paragraph(RESUME["achievements"], styles["bullet"]))
    flow.append(Paragraph("Languages: " + RESUME["languages"], styles["bullet"]))

    doc.build(flow)
    return buf.getvalue()


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        pdf_bytes = build_pdf()
        self.send_response(200)
        self.send_header("Content-Type", "application/pdf")
        self.send_header("Content-Disposition", 'attachment; filename="Ahmed_Ali_Shah_Resume.pdf"')
        self.send_header("Content-Length", str(len(pdf_bytes)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(pdf_bytes)
        return
