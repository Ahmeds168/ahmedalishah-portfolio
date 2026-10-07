"""
Vercel Python serverless function — generates the resume PDF on demand.
Route: /api/resume

Single source of truth: reads src/data/resume.json — the SAME file the
Astro site's pages render from. Update content there once; both the
website and this PDF stay in sync automatically.
"""
import hmac
import json
import os
from urllib.parse import urlparse, parse_qs
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
        "contact": ParagraphStyle("contact", fontName="Helvetica", fontSize=9, textColor=GREY, spaceAfter=2),
        "contact2": ParagraphStyle("contact2", fontName="Helvetica", fontSize=9, textColor=GREY, spaceAfter=10),
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
    contact_line1 = (
        f'<link href="mailto:{contact["email"]}" color="#000000">{contact["email"]}</link> &nbsp;&middot;&nbsp; '
        f'{contact["location"]}'
    )
    contact_line2 = (
        f'<link href="{contact["website"]}" color="#000000">{contact["websiteLabel"]}</link> &nbsp;&middot;&nbsp; '
        f'<link href="{contact["github"]}" color="#000000">{contact["githubLabel"]}</link> &nbsp;&middot;&nbsp; '
        f'<link href="{contact["linkedin"]}" color="#000000">{contact["linkedinLabel"]}</link>'
    )

    flow = []
    flow.append(Paragraph(resume["name"], styles["name"]))
    flow.append(Paragraph(resume["role"], styles["role"]))
    flow.append(Paragraph(contact_line1, styles["contact"]))
    flow.append(Paragraph(contact_line2, styles["contact2"]))
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


def key_is_valid(supplied: str) -> bool:
    """Check the access key against RESUME_ACCESS_KEY.

    Fails closed: if the variable is not set, nobody can download. The
    comparison is constant-time so response timing reveals nothing about the key.
    """
    expected = os.environ.get("RESUME_ACCESS_KEY", "")
    if not expected or not supplied:
        return False
    return hmac.compare_digest(supplied.strip().encode(), expected.encode())


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        supplied = (query.get("key") or [""])[0]

        if not key_is_valid(supplied):
            # No key or a wrong key: send them to the contact page to ask for access.
            self.send_response(302)
            self.send_header("Location", "/contact?resume=denied")
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Robots-Tag", "noindex, nofollow")
            self.end_headers()
            return

        pdf_bytes = build_pdf()
        self.send_response(200)
        self.send_header("Content-Type", "application/pdf")
        self.send_header("Content-Disposition", 'attachment; filename="Ahmed_Ali_Shah_Resume.pdf"')
        self.send_header("Content-Length", str(len(pdf_bytes)))
        self.send_header("X-Robots-Tag", "noindex, nofollow")
        # Gated now, so never cache it anywhere shared.
        self.send_header("Cache-Control", "private, no-store")
        self.end_headers()
        self.wfile.write(pdf_bytes)
