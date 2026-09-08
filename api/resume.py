"""
Vercel Python serverless function — generates the resume PDF on demand.
Route: /api/resume

Single source of truth: reads src/data/resume.json — the SAME file the
Astro site's pages render from. Update content there once; both the
website and this PDF stay in sync automatically.
"""
import json
import os
from http.server import BaseHTTPRequestHandler
from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, HRFlowable
from reportlab.lib.styles import ParagraphStyle

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "src", "data", "resume.json")

NAVY = colors.HexColor("#12161C")
ACCENT = colors.HexColor("#000000")  # black — classic, recruiter-safe for print
GREY = colors.HexColor("#555555")


def load_resume():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_pdf() -> bytes:
    resume = load_resume()
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

    contact = resume["contact"]
    contact_line = (
        f'{contact["email"]} &nbsp;&middot;&nbsp; {contact["phone"]} &nbsp;&middot;&nbsp; '
        f'{contact["location"]} &nbsp;&middot;&nbsp; {contact["githubLabel"]} &nbsp;&middot;&nbsp; '
        f'{contact["linkedinLabel"]}'
    )

    flow = []
    flow.append(Paragraph(resume["name"], styles["name"]))
    flow.append(Paragraph(resume["role"], styles["role"]))
    flow.append(Paragraph(contact_line, styles["contact"]))
    flow.append(hr())

    flow.append(Paragraph("SUMMARY", styles["h2"]))
    flow.append(Paragraph(resume["summary"], styles["body"]))

    flow.append(Paragraph("SKILLS", styles["h2"]))
    skill_line = " &nbsp;|&nbsp; ".join(", ".join(items) for items in resume["skills"].values())
    flow.append(Paragraph(skill_line, styles["body"]))

    flow.append(Paragraph("EXPERIENCE", styles["h2"]))
    for job in resume["experience"]:
        flow.append(Paragraph(f'{job["title"]} — {job["org"]}', styles["jobtitle"]))
        flow.append(Paragraph(job["meta"], styles["jobmeta"]))
        for b in job["bullets"]:
            flow.append(Paragraph("• " + b, styles["bullet"]))

    flow.append(Paragraph("PROJECTS", styles["h2"]))
    for p in resume["projects"]:
        flow.append(Paragraph(f'<b>{p["name"]}</b> — {p["shortDesc"]}', styles["bullet"]))

    flow.append(Paragraph("EDUCATION", styles["h2"]))
    for edu in resume["education"]:
        flow.append(Paragraph(f'<b>{edu["degree"]}</b> — {edu["school"]} ({edu["date"]})', styles["bullet"]))

    flow.append(Paragraph("CERTIFICATES", styles["h2"]))
    for cert in resume["certificates"]:
        label = f'{cert["title"]} — {cert["issuer"]} ({cert["date"]})'
        if cert.get("url"):
            flow.append(Paragraph(f'• <link href="{cert["url"]}" color="#000000">{label}</link>', styles["bullet"]))
        else:
            flow.append(Paragraph("• " + label, styles["bullet"]))

    flow.append(Paragraph("ACHIEVEMENTS &amp; LANGUAGES", styles["h2"]))
    flow.append(Paragraph(resume["achievements"], styles["bullet"]))
    flow.append(Paragraph("Languages: " + resume["languages"], styles["bullet"]))

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
