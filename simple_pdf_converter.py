#!/usr/bin/env python3
"""
Simple Resume PDF Converter using reportlab
Creates PDFs without external dependencies
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import black, gray
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import re
import sys
import os

def convert_markdown_to_pdf_simple(md_file_path, output_pdf_path=None):
    """
    Convert markdown resume to PDF using reportlab (no external dependencies)
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
    
    # Create PDF document
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    name_style = ParagraphStyle(
        'NameStyle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=6,
        textColor=black,
        fontName='Helvetica-Bold'
    )
    
    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=12,
        textColor=gray
    )
    
    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=6,
        spaceBefore=12,
        textColor=black,
        fontName='Helvetica-Bold'
    )
    
    job_title_style = ParagraphStyle(
        'JobTitleStyle',
        parent=styles['Heading3'],
        fontSize=11,
        spaceAfter=4,
        spaceBefore=8,
        textColor=black,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        alignment=0,  # Left align
        fontName='Helvetica'
    )
    
    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=3,
        leftIndent=20,
        bulletIndent=10,
        fontName='Helvetica'
    )
    
    # Parse content
    story = []
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Name (first bold line)
        if line.startswith('**') and line.endswith('**') and 'MARK CETOLA' in line:
            name = line.replace('**', '')
            story.append(Paragraph(name, name_style))
            
        # Contact info (line with email/phone)
        elif '@' in line and '|' in line:
            story.append(Paragraph(line, contact_style))
            
        # Section headers (lines that start with **)
        elif line.startswith('**') and line.endswith('**'):
            header = line.replace('**', '')
            story.append(Paragraph(header, heading_style))
            
        # Job titles (lines with company | title | dates)
        elif '|' in line and ('202' in line or 'Present' in line):
            # Make company name bold and remove ** markdown
            parts = line.split('|')
            if len(parts) >= 3:
                company = parts[0].strip().replace('**', '')  # Remove ** markdown
                rest = '|'.join(parts[1:])
                formatted_line = f"<b>{company}</b> |{rest}"
                story.append(Paragraph(formatted_line, job_title_style))
            else:
                story.append(Paragraph(line, job_title_style))
            
        # Bullet points
        elif line.startswith('- '):
            bullet_text = line[2:]  # Remove "- "
            story.append(Paragraph(f"• {bullet_text}", bullet_style))
            
        # Regular paragraphs
        else:
            story.append(Paragraph(line, body_style))
    
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
        pdf_path = convert_markdown_to_pdf_simple(md_file, output_file)
        print(f"PDF created successfully: {pdf_path}")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()