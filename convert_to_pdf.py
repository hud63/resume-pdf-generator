#!/usr/bin/env python3
"""
Resume PDF Converter
Converts markdown resume files to professionally formatted PDFs
"""

import markdown
from weasyprint import HTML, CSS
import os
import sys

def convert_markdown_to_pdf(md_file_path, output_pdf_path=None):
    """
    Convert a markdown file to a professionally formatted PDF.
    
    Args:
        md_file_path (str): Path to the markdown file
        output_pdf_path (str, optional): Output PDF path. If None, uses same name as md file
    
    Returns:
        str: Path to the created PDF file
    """
    
    # Generate output path if not provided
    if output_pdf_path is None:
        base_name = os.path.splitext(md_file_path)[0]
        output_pdf_path = f"{base_name}.pdf"
    
    # Read the markdown file
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Markdown file not found: {md_file_path}")
    
    # Convert markdown to HTML
    html_content = markdown.markdown(md_content)
    
    # Professional CSS styling for resume
    css_style = CSS(string='''
        @page {
            size: Letter;
            margin: 0.75in;
        }
        
        body { 
            font-family: "Segoe UI", Arial, sans-serif; 
            line-height: 1.4; 
            font-size: 11pt;
            color: #333;
            max-width: none;
        }
        
        h1 { 
            font-size: 18pt; 
            font-weight: bold;
            margin: 0 0 0.2em 0;
            color: #000;
        }
        
        h2 { 
            font-size: 14pt; 
            font-weight: bold;
            margin: 1em 0 0.3em 0;
            color: #000;
            border-bottom: 1px solid #ddd;
            padding-bottom: 2pt;
        }
        
        h3 { 
            font-size: 12pt; 
            font-weight: bold;
            margin: 0.8em 0 0.3em 0;
            color: #000;
        }
        
        p { 
            margin: 0.5em 0;
            text-align: justify;
        }
        
        strong { 
            font-weight: bold; 
            color: #000;
        }
        
        ul { 
            margin: 0.3em 0 0.8em 0; 
            padding-left: 1.2em; 
        }
        
        li { 
            margin-bottom: 0.25em; 
            text-align: justify;
            line-height: 1.3;
        }
        
        /* First paragraph (summary) styling */
        body > p:first-of-type {
            margin-bottom: 1em;
            font-size: 10.5pt;
        }
        
        /* Contact information styling */
        body > p:nth-of-type(2) {
            font-size: 10pt;
            color: #666;
            margin-bottom: 1em;
        }
    ''')
    
    # Create full HTML document
    full_html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Resume - PDF</title>
    </head>
    <body>
    {html_content}
    </body>
    </html>
    '''
    
    # Convert to PDF
    try:
        HTML(string=full_html).write_pdf(output_pdf_path, stylesheets=[css_style])
        return output_pdf_path
    except Exception as e:
        raise Exception(f"Error creating PDF: {str(e)}")

def main():
    """Main function for command line usage"""
    if len(sys.argv) < 2:
        print("Usage: python convert_to_pdf.py <markdown_file> [output_pdf]")
        print("Example: python convert_to_pdf.py resume.md")
        sys.exit(1)
    
    md_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        pdf_path = convert_markdown_to_pdf(md_file, output_file)
        print(f"✅ PDF created successfully: {pdf_path}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()