#!/usr/bin/env python3
"""
Professional Resume PDF Converter using reportlab
Creates high-quality PDFs with professional typography and formatting
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import black, HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
import re
import sys
import os

def convert_markdown_to_pdf_professional(md_file_path, output_pdf_path=None):
    """
    Convert markdown resume to professional PDF with enhanced typography and formatting
    """
    
    # Generate output path if not provided
    if output_pdf_path is None:
        base_name = os.path.splitext(md_file_path)[0]
        output_pdf_path = f"{base_name}.pdf"
    
    # Read the markdown file
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Markdown file not found: {md_file_path}")
    
    # Create PDF document with professional margins and metadata
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.6*inch,
        bottomMargin=0.6*inch,
        title="Mark Cetola - Resume",
        author="Mark Cetola",
        subject="Professional Resume - CX AI Workflow Specialist",
        creator="Resume PDF Converter",
        keywords="resume, AI, customer experience, workflow specialist"
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Professional color scheme
    dark_blue = HexColor('#2C3E50')
    medium_gray = HexColor('#5D6D7E')
    light_gray = HexColor('#85929E')
    
    # Enhanced custom styles for professional appearance
    name_style = ParagraphStyle(
        'NameStyle',
        parent=styles['Heading1'],
        fontSize=22,
        spaceAfter=8,
        spaceBefore=0,
        textColor=dark_blue,
        fontName='Helvetica-Bold',
        alignment=TA_LEFT
    )
    
    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=16,
        spaceBefore=2,
        textColor=medium_gray,
        fontName='Helvetica',
        alignment=TA_LEFT
    )
    
    summary_style = ParagraphStyle(
        'SummaryStyle',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=16,
        spaceBefore=0,
        textColor=black,
        fontName='Helvetica',
        alignment=TA_JUSTIFY,
        leading=14
    )
    
    section_heading_style = ParagraphStyle(
        'SectionHeadingStyle',
        parent=styles['Heading2'],
        fontSize=15,
        spaceAfter=8,
        spaceBefore=18,
        textColor=dark_blue,
        fontName='Helvetica-Bold',
        alignment=TA_LEFT
    )
    
    subsection_heading_style = ParagraphStyle(
        'SubsectionHeadingStyle',
        parent=styles['Heading3'],
        fontSize=13,
        spaceAfter=4,
        spaceBefore=2,
        textColor=dark_blue,
        fontName='Helvetica-Bold',
        alignment=TA_LEFT
    )
    
    job_title_style = ParagraphStyle(
        'JobTitleStyle',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=6,
        spaceBefore=12,
        textColor=dark_blue,
        fontName='Helvetica-Bold',
        alignment=TA_LEFT
    )
    
    company_date_style = ParagraphStyle(
        'CompanyDateStyle',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        spaceBefore=2,
        textColor=medium_gray,
        fontName='Helvetica',
        alignment=TA_LEFT
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        spaceBefore=0,
        textColor=black,
        fontName='Helvetica',
        alignment=TA_LEFT,
        leading=13
    )
    
    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontSize=10.5,
        spaceAfter=4,
        spaceBefore=1,
        leftIndent=18,
        bulletIndent=0,
        textColor=black,
        fontName='Helvetica',
        alignment=TA_LEFT,
        leading=13
    )
    
    t_shaped_core_style = ParagraphStyle(
        'TShapedCoreStyle',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=4,
        spaceBefore=2,
        textColor=black,
        fontName='Helvetica',
        alignment=TA_LEFT,
        leading=14
    )
    
    # Parse content with enhanced formatting
    story = []
    lines = content.split('\n')
    current_section = None
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:
            i += 1
            continue
            
        # Name (first bold line with MARK CETOLA)
        if line.startswith('**') and line.endswith('**') and ('MARK CETOLA' in line.upper() or 'Mark Cetola' in line):
            name = line.replace('**', '')
            story.append(Paragraph(name, name_style))
            current_section = 'header'
            
        # Contact info (line with email/phone)
        elif '@' in line and ('|' in line or 'linkedin' in line.lower()):
            story.append(Paragraph(line, contact_style))
            
        # Summary paragraph (first non-header content)
        elif current_section == 'header' and not line.startswith('**') and not line.startswith('-') and '|' not in line:
            story.append(Paragraph(line, summary_style))
            current_section = 'summary'
            
        # Section headers (lines that start with **)
        elif line.startswith('**') and line.endswith('**'):
            header = line.replace('**', '')
            story.append(Paragraph(header, section_heading_style))
            current_section = header.lower()
            
        # T-shaped skills section special handling (works for any section containing "professional")
        elif 'professional' in current_section and ('full-stack' in current_section or 'client' in current_section or 'customer' in current_section):
            if line.startswith('Core:'):
                story.append(Paragraph(f"<b>Core:</b> {line[5:].strip()}", t_shaped_core_style))
            elif line.startswith('Adjacent:'):
                story.append(Paragraph(f"<b>Adjacent:</b> {line[9:].strip()}", t_shaped_core_style))
            elif line.startswith('Cross-functional:'):
                story.append(Paragraph(f"<b>Cross-functional:</b> {line[17:].strip()}", t_shaped_core_style))
            else:
                story.append(Paragraph(line, body_style))
                
        # General T-shaped skills handling for any line containing these patterns
        elif line.startswith('Core:') or line.startswith('Adjacent:') or line.startswith('Cross-functional:'):
            if line.startswith('Core:'):
                story.append(Paragraph(f"<b>Core:</b> {line[5:].strip()}", t_shaped_core_style))
            elif line.startswith('Adjacent:'):
                story.append(Paragraph(f"<b>Adjacent:</b> {line[9:].strip()}", t_shaped_core_style))
            elif line.startswith('Cross-functional:'):
                story.append(Paragraph(f"<b>Cross-functional:</b> {line[17:].strip()}", t_shaped_core_style))
                
        # Job titles and company info (enhanced parsing)
        elif '|' in line and ('202' in line or 'Present' in line):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3:
                # Format: **Job Title** | Company | Location | Date
                if parts[0].startswith('**') and parts[0].endswith('**'):
                    job_title = parts[0].replace('**', '')
                    company = parts[1]
                    location_date = ' | '.join(parts[2:])
                    
                    story.append(Paragraph(job_title, job_title_style))
                    story.append(Paragraph(location_date, company_date_style))
                    story.append(Paragraph(company, company_date_style))
                else:
                    # Format: Company | Job Title | Date | Location
                    company = parts[0]
                    job_title = parts[1] if len(parts) > 1 else parts[0]
                    location_date = ' | '.join(parts[2:])
                    
                    story.append(Paragraph(job_title, job_title_style))
                    story.append(Paragraph(location_date, company_date_style))
                    story.append(Paragraph(company, company_date_style))
            else:
                story.append(Paragraph(line, job_title_style))
                
        # Bullet points with enhanced formatting
        elif line.startswith('- '):
            bullet_text = line[2:].strip()
            story.append(Paragraph(f"• {bullet_text}", bullet_style))
            
        # Regular paragraphs - clean markdown formatting
        else:
            # Clean up markdown formatting in regular content
            clean_line = line
            
            # Handle bold text formatting **text** -> <b>text</b>
            clean_line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', clean_line)
            
            # Handle any remaining ** markers that aren't paired
            clean_line = clean_line.replace('**', '')
            
            story.append(Paragraph(clean_line, body_style))
            
        i += 1
    
    # Build PDF
    try:
        doc.build(story)
        return output_pdf_path
    except Exception as e:
        raise Exception(f"Error creating PDF: {str(e)}")

def main():
    """Main function for command line usage"""
    if len(sys.argv) < 2:
        print("Usage: python simple_pdf_converter.py <markdown_file> [output_pdf]")
        print("Example: python simple_pdf_converter.py resume.md")
        sys.exit(1)
    
    md_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        pdf_path = convert_markdown_to_pdf_professional(md_file, output_file)
        print(f"PDF created successfully: {pdf_path}")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()