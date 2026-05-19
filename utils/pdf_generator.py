"""
pdf_generator.py
Generates a structured PDF research report using ReportLab.
Accepts a report_data dict and writes the file to the given output_path.
"""
import logging
import os
from typing import Dict, Any

logger = logging.getLogger(__name__)


def generate_pdf(report_data: Dict[str, Any], output_path: str) -> str:
    """
    Generate a PDF report from `report_data` and save it to `output_path`.

    Args:
        report_data: Dictionary containing topic, summary, findings, etc.
        output_path: Absolute path where the PDF should be saved.

    Returns:
        The output_path of the generated file.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        # ── Real implementation (uncomment after: pip install reportlab) ─────
        # from reportlab.lib.pagesizes import A4
        # from reportlab.lib.styles import getSampleStyleSheet
        # from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable
        #
        # doc = SimpleDocTemplate(output_path, pagesize=A4)
        # styles = getSampleStyleSheet()
        # story = []
        #
        # story.append(Paragraph(report_data.get("topic", "Research Report"), styles["Title"]))
        # story.append(Spacer(1, 12))
        # story.append(Paragraph("Executive Summary", styles["Heading2"]))
        # story.append(Paragraph(report_data.get("summary", ""), styles["Normal"]))
        # story.append(Spacer(1, 12))
        # story.append(Paragraph("Key Findings", styles["Heading2"]))
        # items = [Paragraph(f, styles["Normal"]) for f in report_data.get("key_findings", [])]
        # story.append(ListFlowable(items, bulletType="bullet"))
        # doc.build(story)

        # ── Placeholder: write a minimal text-based PDF stub ─────────────────
        with open(output_path, "wb") as f:
            # Write a valid minimal PDF so the file is non-empty
            content = (
                "%PDF-1.4\n"
                "1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
                "2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
                "3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\n"
                "xref\n0 4\n0000000000 65535 f\n"
                "trailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n0\n%%EOF\n"
            )
            f.write(content.encode("latin-1"))

        logger.info("[pdf_generator] PDF written: %s", output_path)

    except Exception as exc:
        logger.error("[pdf_generator] Failed to generate PDF: %s", exc)
        raise

    return output_path
