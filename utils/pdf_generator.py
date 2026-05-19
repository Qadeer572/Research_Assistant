import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

def generate_pdf(report_content: dict,
                 session_id: str,
                 output_dir: str = "outputs/reports") -> str:
    os.makedirs(output_dir, exist_ok=True)
    path = f"{output_dir}/{session_id}_report.pdf"
    doc = SimpleDocTemplate(path, pagesize=A4)
    styles = getSampleStyleSheet()
    GREEN = HexColor("#15803D")
    DARK = HexColor("#1F2937")
    
    title_style = ParagraphStyle("Title", fontSize=20,
        textColor=GREEN, spaceAfter=20, fontName="Helvetica-Bold")
    heading_style = ParagraphStyle("Heading", fontSize=14,
        textColor=GREEN, spaceAfter=10, fontName="Helvetica-Bold")
    body_style = ParagraphStyle("Body", fontSize=11,
        textColor=DARK, spaceAfter=12, leading=16)
    
    story = []
    sections_order = [
        ("title", None),
        ("abstract", "Abstract"),
        ("introduction", "Introduction"),
        ("key_findings", "Key Findings"),
        ("analysis", "Analysis"),
        ("research_gaps", "Research Gaps"),
        ("emerging_trends", "Emerging Trends"),
        ("conclusion", "Conclusion")
    ]
    
    for key, heading in sections_order:
        content = report_content.get(key, "Content not available")
        if heading is None:
            story.append(Paragraph(str(content), title_style))
        else:
            story.append(Paragraph(heading, heading_style))
            story.append(Paragraph(str(content), body_style))
        story.append(Spacer(1, 0.2*inch))
    
    doc.build(story)
    return os.path.abspath(path)
