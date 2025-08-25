#!/usr/bin/env python3
"""
Professional HTML Resume Generator
Main script for generating high-quality PDF resumes via HTML/CSS templating
"""

import sys
import os
import argparse
from pathlib import Path

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

try:
    from modules.html_generator import HTMLResumeGenerator
    from modules.html_content_processor import HTMLContentProcessor
    
    # Try WeasyPrint first, fall back to simple generator
    try:
        from modules.html_pdf_generator import HTMLPDFGenerator
        PDF_GENERATOR_TYPE = "weasyprint"
    except ImportError:
        print("⚠️ WeasyPrint not available, using browser-based PDF generation")
        from modules.simple_html_pdf import SimpleHTMLPDFGenerator as HTMLPDFGenerator
        PDF_GENERATOR_TYPE = "browser"
        
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("💡 Make sure all required dependencies are installed:")
    print("   pip install jinja2")
    sys.exit(1)

class ProfessionalResumeGenerator:
    """
    Main class for generating professional PDF resumes using HTML/CSS approach
    """
    
    def __init__(self):
        self.pdf_generator = HTMLPDFGenerator()
        self.html_generator = HTMLResumeGenerator()
        self.content_processor = HTMLContentProcessor()
        self.generator_type = PDF_GENERATOR_TYPE
    
    def generate_resume(self, 
                       markdown_path: str, 
                       output_path: str = None,
                       output_format: str = "pdf",
                       photo_path: str = None,
                       keep_html: bool = False) -> bool:
        """
        Generate professional resume in specified format
        
        Args:
            markdown_path: Path to markdown resume file
            output_path: Output file path (auto-determined if None)
            output_format: "pdf", "html", or "both"
            photo_path: Optional path to photo file
            keep_html: Keep HTML file when generating PDF
            
        Returns:
            bool: Success status
        """
        if not os.path.exists(markdown_path):
            print(f"❌ Resume markdown file not found: {markdown_path}")
            return False
        
        # Auto-determine output paths
        if output_path is None:
            base_name = Path(markdown_path).stem
            if output_format == "pdf":
                output_path = f"{base_name}_professional.pdf"
            elif output_format == "html":
                output_path = f"{base_name}_professional.html"
            else:  # both
                output_path = f"{base_name}_professional"
        
        try:
            if output_format == "html":
                return self._generate_html_only(markdown_path, output_path, photo_path)
            elif output_format == "pdf":
                return self._generate_pdf_only(markdown_path, output_path, photo_path, keep_html)
            elif output_format == "both":
                return self._generate_both_formats(markdown_path, output_path, photo_path)
            else:
                print(f"❌ Unsupported output format: {output_format}")
                return False
                
        except Exception as e:
            print(f"❌ Error during generation: {e}")
            return False
    
    def _generate_html_only(self, markdown_path: str, output_path: str, photo_path: str) -> bool:
        """Generate HTML resume only"""
        print("🌐 Generating HTML resume...")
        
        if not output_path.endswith('.html'):
            output_path += '.html'
        
        success = self.html_generator.generate_html_from_markdown(
            markdown_path, output_path, photo_path
        )
        
        if success:
            print(f"✅ HTML resume generated: {output_path}")
            self._show_html_preview_instructions(output_path)
        
        return success
    
    def _generate_pdf_only(self, markdown_path: str, output_path: str, photo_path: str, keep_html: bool) -> bool:
        """Generate PDF resume only"""
        print("📄 Generating professional PDF resume...")
        
        if not output_path.endswith('.pdf'):
            output_path += '.pdf'
        
        # Prepare HTML output path if keeping HTML
        html_path = None
        if keep_html:
            html_path = output_path.replace('.pdf', '.html')
        
        success = self.pdf_generator.generate_pdf_from_markdown(
            markdown_path, output_path, photo_path, keep_html, html_path
        )
        
        if success:
            print(f"✅ Professional PDF resume generated: {output_path}")
            if keep_html and html_path:
                print(f"📝 HTML file saved: {html_path}")
            self._show_pdf_info(output_path)
        
        return success
    
    def _generate_both_formats(self, markdown_path: str, base_path: str, photo_path: str) -> bool:
        """Generate both HTML and PDF formats"""
        print("📄🌐 Generating both HTML and PDF formats...")
        
        html_path = f"{base_path}.html"
        pdf_path = f"{base_path}.pdf"
        
        # Generate HTML first
        html_success = self.html_generator.generate_html_from_markdown(
            markdown_path, html_path, photo_path
        )
        
        if not html_success:
            print("❌ Failed to generate HTML, cannot proceed to PDF")
            return False
        
        # Generate PDF from HTML
        pdf_success = self.pdf_generator.convert_html_to_pdf(html_path, pdf_path)
        
        if html_success and pdf_success:
            print(f"✅ HTML resume: {html_path}")
            print(f"✅ PDF resume: {pdf_path}")
            self._show_html_preview_instructions(html_path)
            self._show_pdf_info(pdf_path)
            return True
        
        return html_success  # At least HTML succeeded
    
    def preview_content(self, markdown_path: str, photo_path: str = None):
        """Preview structured content without generating files"""
        print("🔍 Previewing resume content structure...")
        
        if not os.path.exists(markdown_path):
            print(f"❌ Resume file not found: {markdown_path}")
            return False
        
        try:
            self.html_generator.preview_content_structure(markdown_path, photo_path)
            return True
        except Exception as e:
            print(f"❌ Error previewing content: {e}")
            return False
    
    def validate_system(self) -> bool:
        """Validate that all system dependencies are available"""
        print("🔧 Validating system dependencies...")
        print(f"📄 Using PDF generator: {self.generator_type}")
        
        # Check PDF generation dependencies
        pdf_valid = self.pdf_generator.validate_dependencies()
        
        # Check template directory
        template_dir = Path(__file__).parent / "templates"
        template_exists = (template_dir / "resume_template.html").exists()
        
        if template_exists:
            print("✅ HTML template found")
        else:
            print("❌ HTML template not found")
        
        # Check photo file
        photo_paths = ['039-Dm2VwCrean0.jpeg', 'photo.jpg', 'headshot.jpg']
        photo_found = any(os.path.exists(p) for p in photo_paths)
        
        if photo_found:
            found_photo = next(p for p in photo_paths if os.path.exists(p))
            print(f"✅ Photo found: {found_photo}")
        else:
            print("⚠️ No photo found (will use placeholder)")
        
        overall_valid = pdf_valid and template_exists
        
        if overall_valid:
            print("✅ System validation successful - ready to generate resumes")
        else:
            print("❌ System validation failed - check dependencies")
        
        return overall_valid
    
    def _show_html_preview_instructions(self, html_path: str):
        """Show instructions for previewing HTML file"""
        abs_path = os.path.abspath(html_path)
        print(f"🌐 Preview HTML in browser: file://{abs_path}")
    
    def _show_pdf_info(self, pdf_path: str):
        """Show PDF file information"""
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"📊 PDF size: {file_size / 1024:.1f} KB")
        
    def compare_with_template(self, generated_pdf: str, template_pdf: str = "Template.pdf"):
        """Compare generated PDF with template for quality assessment"""
        if not os.path.exists(generated_pdf):
            print(f"❌ Generated PDF not found: {generated_pdf}")
            return
        
        if not os.path.exists(template_pdf):
            print(f"⚠️ Template PDF not found: {template_pdf}")
            return
        
        gen_size = os.path.getsize(generated_pdf) / 1024
        template_size = os.path.getsize(template_pdf) / 1024
        
        print("📊 Quality Comparison:")
        print(f"   Generated PDF: {gen_size:.1f} KB")
        print(f"   Template PDF:  {template_size:.1f} KB")
        print(f"   Size Ratio:    {gen_size/template_size:.2f}x")
        
        if gen_size > 50:  # Reasonable size for professional resume
            print("✅ Generated PDF has professional file size")
        else:
            print("⚠️ Generated PDF may be too small")

def main():
    """Command line interface"""
    parser = argparse.ArgumentParser(
        description='Generate professional PDF resume from markdown using HTML/CSS approach'
    )
    
    parser.add_argument('resume_md', nargs='?', default='cetola_resume.md', 
                       help='Path to resume markdown file (default: cetola_resume.md)')
    parser.add_argument('-o', '--output', help='Output file path (auto-generated if not specified)')
    parser.add_argument('-f', '--format', choices=['pdf', 'html', 'both'], default='pdf',
                       help='Output format (default: pdf)')
    parser.add_argument('-p', '--photo', help='Path to photo file')
    parser.add_argument('--keep-html', action='store_true',
                       help='Keep HTML file when generating PDF')
    parser.add_argument('--preview', action='store_true',
                       help='Preview content structure without generating files')
    parser.add_argument('--validate', action='store_true',
                       help='Validate system dependencies')
    parser.add_argument('--compare', action='store_true',
                       help='Compare generated PDF with Template.pdf')
    
    args = parser.parse_args()
    
    generator = ProfessionalResumeGenerator()
    
    # Handle different modes
    if args.validate:
        success = generator.validate_system()
        sys.exit(0 if success else 1)
    
    if args.preview:
        success = generator.preview_content(args.resume_md, args.photo)
        sys.exit(0 if success else 1)
    
    # Generate resume
    print("🚀 Professional Resume Generator")
    print("=" * 50)
    
    success = generator.generate_resume(
        args.resume_md,
        args.output, 
        args.format,
        args.photo,
        args.keep_html
    )
    
    # Compare with template if requested
    if args.compare and success and args.format in ['pdf', 'both']:
        output_path = args.output or 'cetola_resume_professional.pdf'
        if not output_path.endswith('.pdf'):
            output_path += '.pdf'
        generator.compare_with_template(output_path)
    
    if success:
        print("=" * 50)
        print("🎉 Resume generation completed successfully!")
        
        if args.format == 'pdf':
            print("💡 Your professional PDF resume is ready for job applications!")
        elif args.format == 'html':
            print("💡 Your HTML resume is ready - perfect for online portfolios!")
        else:
            print("💡 Both formats ready - use PDF for applications, HTML for web!")
    else:
        print("❌ Resume generation failed")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()