#!/usr/bin/env python3
"""
Generate dynamic resume with JD analysis
"""

import sys
import os
sys.path.insert(0, 'modules')
from html_content_processor import HTMLContentProcessor

# For PDF generation, try WeasyPrint approach
from jinja2 import Template
import tempfile
import os

# Try to import HTMLPDFGenerator, but don't fail if WeasyPrint is unavailable
try:
    from modules.html_pdf_generator import HTMLPDFGenerator
    WEASYPRINT_AVAILABLE = True
except ImportError as e:
    HTMLPDFGenerator = None
    WEASYPRINT_AVAILABLE = False
    print(f"[INFO] WeasyPrint not available: {e}")
except Exception as e:
    HTMLPDFGenerator = None
    WEASYPRINT_AVAILABLE = False
    print(f"[INFO] WeasyPrint dependencies missing: {e}")

def generate_dynamic_resume(jd_text, output_filename):
    """Generate resume tailored to job description"""
    
    # Create processor with JD analysis
    processor = HTMLContentProcessor(jd_text)
    
    # Process resume with dynamic content
    content = processor.process_for_html_template('cetola_resume.md', '039-Dm2VwCrean0.jpeg')
    
    # Optimize for single page
    content = processor.optimize_for_single_page(content)
    
    # Load template
    with open('templates/resume_template.html', 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    template = Template(template_content)
    
    # Render HTML
    html_content = template.render(
        name=content.name,
        tagline=content.tagline,
        contact_parts=content.contact_parts,
        photo_path=content.photo_path,
        bio=content.bio,
        strengths=content.strengths,
        technical=content.technical,
        languages=content.languages,
        experiences=content.experiences,
        professional_development=content.professional_development,
        font_scale_factor=content.font_scale_factor
    )
    
    # Generate PDF using WeasyPrint
    temp_html_path = output_filename.replace('.pdf', '_temp.html')
    
    try:
        # Write HTML to temporary file
        with open(temp_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Try WeasyPrint first if available
        if WEASYPRINT_AVAILABLE and HTMLPDFGenerator:
            try:
                pdf_generator = HTMLPDFGenerator()
                success = pdf_generator.convert_html_to_pdf(temp_html_path, output_filename)
                
                if success:
                    print(f"[OK] Dynamic resume generated: {output_filename}")
                    return output_filename
                else:
                    print("[INFO] WeasyPrint PDF generation failed, trying Chrome fallback...")
                    
            except Exception as e:
                print(f"[INFO] WeasyPrint failed ({e}), trying Chrome fallback...")
        else:
            print("[INFO] WeasyPrint not available, using Chrome fallback...")
        
        # Fallback: try Chrome headless approach with absolute paths
        import subprocess
        try:
            # Convert to absolute paths to avoid permission issues
            abs_temp_html = os.path.abspath(temp_html_path)
            abs_output = os.path.abspath(output_filename)
            
            for chrome_path in [
                r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
                'chrome', 'google-chrome', 'chromium', 'chromium-browser'
            ]:
                try:
                    cmd = [
                        chrome_path,
                        '--headless',
                        '--disable-gpu',
                        '--no-sandbox',
                        '--disable-dev-shm-usage',
                        f'--print-to-pdf={abs_output}',
                        '--print-to-pdf-no-header',
                        '--disable-extensions',
                        '--run-all-compositor-stages-before-draw',
                        '--virtual-time-budget=5000',
                        abs_temp_html
                    ]
                    
                    print(f"[DEBUG] Trying Chrome at: {chrome_path}")
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=os.getcwd())
                    
                    if result.returncode == 0 and os.path.exists(abs_output):
                        print(f"[OK] Dynamic resume generated via Chrome: {abs_output}")
                        return abs_output
                    else:
                        print(f"[DEBUG] Chrome failed with code {result.returncode}")
                        if result.stderr:
                            print(f"[DEBUG] Chrome stderr: {result.stderr}")
                            
                except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError) as e:
                    print(f"[DEBUG] Chrome attempt failed: {e}")
                    continue
            
            print("[INFO] Chrome PDF generation failed on all attempts")
        except Exception as e:
            print(f"[INFO] Chrome fallback failed: {e}")
        
        # Fallback: create print-optimized HTML
        html_output = output_filename.replace('.pdf', '.html')
        with open(html_output, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"[FALLBACK] Created print-optimized HTML: {html_output}")
        print("Please open in browser and use Ctrl+P to generate PDF")
        return html_output
        
    finally:
        if os.path.exists(temp_html_path):
            os.unlink(temp_html_path)

if __name__ == "__main__":
    # AI Optimization JD
    jd_text = """AI Optimization Specialist, Support
    At Vanta, our mission is to help businesses earn and prove trust. As a Support Conversation Designer, you will empower both our customers and Support team by building and maintaining the AI-powered knowledge that fuels our customer-facing chatbot and internal AI Copilot. You'll collaborate closely with Support, Customer Education, Product, and Engineering teams to ensure our AI tools deliver accurate, helpful responses while enhancing customer experience and support efficiency at scale.
    
    Key requirements:
    - AI Experience: Exposure to AI-powered support tools and expertise in chatbot design, automation, and conversation optimization
    - Content Creation & Curation: Strong writing and organizational skills for crafting and maintaining structured knowledge
    - Technical Skills: Familiarity with APIs, JSON, or scripting languages (e.g., Python, JavaScript)
    - Data-Driven Mindset: Ability to interpret AI performance data and make insights-driven decisions
    - Support Expertise: Proven experience in technical troubleshooting and customer inquiries"""
    
    generate_dynamic_resume(jd_text, "MarkCetola_AIO_Dynamic.pdf")