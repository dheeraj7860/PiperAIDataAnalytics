"""
PDF Report Generation using ReportLab.
Generates Course Progress Report matching the reference Canva design.
"""

from io import BytesIO
from datetime import datetime
from typing import Dict, List
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.pdfgen import canvas


def calculate_statistics(chapter_data: List[dict]) -> Dict:
    """
    Calculate statistics from chapter data for remarks section.
    
    Args:
        chapter_data: List of chapter performance dictionaries
        
    Returns:
        Dictionary with completed_count, total_count, average_score
    """
    completed_count = 0
    total_scores = []
    
    for chapter in chapter_data:
        if chapter["status"] == "Completed":
            completed_count += 1
            
        # Calculate average score (exclude "NA")
        if chapter["score"] != "NA":
            total_scores.append(int(chapter["score"]))
    
    avg_score = sum(total_scores) / len(total_scores) if total_scores else 0
    
    return {
        "completed_count": completed_count,
        "total_count": len(chapter_data),
        "average_score": round(avg_score, 1),
        "completion_rate": round((completed_count / len(chapter_data)) * 100, 1)
    }


def generate_course_report(user_data: Dict, session_data: Dict) -> BytesIO:
    """
    Generate a Course Progress Report PDF matching the reference Canva design.
    
    Args:
        user_data: Dictionary with email, trainee_name, role
        session_data: Dictionary with session_id, session_timestamp, chapter_data
        
    Returns:
        BytesIO buffer containing the PDF
    """
    buffer = BytesIO()
    
    # Create PDF document with exact margins
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=50*mm,
        leftMargin=50*mm,
        topMargin=40*mm,
        bottomMargin=40*mm
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles matching reference PDF
    styles = getSampleStyleSheet()
    
    # Title: "COURSE PROGRESS REPORT" - Bold, Large, Dark
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.black,
        alignment=TA_CENTER,
        spaceAfter=8,
        spaceBefore=0,
        fontName='Helvetica-Bold',
        leading=24
    )
    
    # Subtitle: "PIPER ALPHA" - Bold, Medium
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.black,
        alignment=TA_CENTER,
        spaceAfter=30,
        spaceBefore=0,
        fontName='Helvetica-Bold',
        leading=20
    )
    
    # Section heading: "TRAINEE DETAILS", "REMARKS"
    section_heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.black,
        spaceAfter=12,
        spaceBefore=15,
        fontName='Helvetica-Bold',
        leading=14
    )
    
    # Normal text style
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        spaceAfter=6,
        fontName='Helvetica',
        leading=14
    )
    
    # Remarks text - Justified, all caps
    remarks_style = ParagraphStyle(
        'Remarks',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.black,
        alignment=TA_JUSTIFY,
        spaceAfter=10,
        fontName='Helvetica',
        leading=13
    )
    
    # ========== Header Section ==========
    # Title
    title = Paragraph("COURSE PROGRESS REPORT", title_style)
    elements.append(title)
    
    # Subtitle
    subtitle = Paragraph("PIPER ALPHA", subtitle_style)
    elements.append(subtitle)
    
    # ========== Trainee Details Section ==========
    section_title = Paragraph("TRAINEE DETAILS", section_heading_style)
    elements.append(section_title)
    
    # Format session date
    session_date = session_data["session_timestamp"].strftime("%B %d, %Y")
    
    # Trainee details - Simple format matching reference
    trainee_details = f"""
    <b>Name:</b> {user_data["trainee_name"]}<br/>
    <b>Email:</b> {user_data["email"]}<br/>
    <b>Date:</b> {session_date}<br/>
    <b>Session ID:</b> {session_data["session_id"]}
    """
    details_para = Paragraph(trainee_details, normal_style)
    elements.append(details_para)
    
    elements.append(Spacer(1, 20*mm))
    
    # ========== Performance Table ==========
    # Prepare table data - EXACTLY matching reference
    table_data = [
        ["Chapter", "Score ", "Status"]  # Header row (note the space after "Score")
    ]
    
    # Add chapter data rows
    for chapter in session_data["chapter_data"]:
        # Convert score to display format
        score_display = str(chapter["score"]) if chapter["score"] != "NA" else "N/A"
        
        table_data.append([
            chapter["chapter"],
            score_display,
            chapter["status"]
        ])
    
    # Create table with specific column widths
    table = Table(table_data, colWidths=[75*mm, 25*mm, 40*mm])
    
    # Style the table - Simple black and white design like reference
    table_style = [
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        
        # Data rows
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),  # Chapter names left-aligned
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),  # Score left-aligned
        ('ALIGN', (2, 1), (2, -1), 'LEFT'),  # Status left-aligned
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        
        # Grid lines - thin black lines
        ('LINEBELOW', (0, 0), (-1, 0), 1.5, colors.black),  # Bold line under header
        ('LINEBELOW', (0, 1), (-1, -2), 0.5, colors.lightgrey),  # Light lines between rows
        ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),  # Line at bottom
    ]
    
    table.setStyle(TableStyle(table_style))
    elements.append(table)
    
    elements.append(Spacer(1, 15*mm))
    
    # ========== Remarks Section ==========
    section_title = Paragraph("REMARKS", section_heading_style)
    elements.append(section_title)
    
    # Calculate statistics
    stats = calculate_statistics(session_data["chapter_data"])
    
    # Generate remarks text - ALL CAPS like reference
    trainee_name_upper = user_data["trainee_name"].upper()
    
    if stats["completed_count"] == stats["total_count"]:
        remarks_text = (
            f"{trainee_name_upper} HAS EXHIBITED GREAT FOCUS AND PERSEVERANCE TO COMPLETE "
            f"THE COURSE WITH AN OVERALL PASS RATE OF {stats['completion_rate']}%. "
            f"CONTINUED GROWTH AND APPLICATION OF THESE SKILLS WILL ENSURE FURTHER SUCCESS."
        )
    elif stats["completed_count"] > 0:
        remarks_text = (
            f"{trainee_name_upper} HAS COMPLETED {stats['completed_count']} OUT OF "
            f"{stats['total_count']} CHAPTERS WITH AN OVERALL COMPLETION RATE OF "
            f"{stats['completion_rate']}%. CONTINUED EFFORT AND FOCUS WILL SUPPORT "
            f"SUCCESSFUL COMPLETION OF THE REMAINING MODULES."
        )
    else:
        remarks_text = (
            f"{trainee_name_upper} HAS INITIATED THE TRAINING PROGRAM. "
            f"CONSISTENT ENGAGEMENT AND APPLICATION OF TRAINING MATERIAL WILL "
            f"SUPPORT SKILL DEVELOPMENT AND COURSE COMPLETION."
        )
    
    remarks_para = Paragraph(remarks_text, remarks_style)
    elements.append(remarks_para)
    
    # Build PDF
    doc.build(elements)
    
    # Reset buffer position to beginning
    buffer.seek(0)
    
    return buffer

