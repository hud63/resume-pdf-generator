#!/usr/bin/env python3
"""
HTML to PDF Generator
Converts HTML resume to high-quality PDF using WeasyPrint
"""

import os
import tempfile
from pathlib import Path
from typing import Optional

try:
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
    WEASYPRINT_AVAILABLE = True
except ImportError as e:
    # WeasyPrint not available or has dependency issues
    HTML = None
    CSS = None
    FontConfiguration = None
    WEASYPRINT_AVAILABLE = False

from .html_generator import HTMLResumeGenerator

class HTMLPDFGenerator:
    """
    Generates high-quality PDF from HTML resume using WeasyPrint
    """
    
    def __init__(self):
        """Initialize PDF generator with font configuration"""
        if not WEASYPRINT_AVAILABLE:
            raise ImportError("WeasyPrint is not available or has dependency issues")
        self.font_config = FontConfiguration()
        self.html_generator = HTMLResumeGenerator()
    
    def generate_pdf_from_markdown(self, 
                                 markdown_path: str,
                                 pdf_output_path: str,
                                 photo_path: Optional[str] = None,
                                 keep_html: bool = False,
                                 html_output_path: Optional[str] = None) -> bool:
        """
        Generate PDF resume directly from markdown file
        
        Args:
            markdown_path: Path to markdown resume file
            pdf_output_path: Where to save the PDF file
            photo_path: Optional path to photo file
            keep_html: Whether to keep the intermediate HTML file
            html_output_path: Where to save HTML if keep_html=True
            
        Returns:
            bool: Success status
        """
        try:
            print(f"🔄 Starting PDF generation from {markdown_path}...")
            
            # Generate HTML first
            if keep_html and html_output_path:
                html_path = html_output_path
            else:
                # Create temporary HTML file
                temp_html = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8')
                html_path = temp_html.name
                temp_html.close()
            
            # Generate HTML resume
            success = self.html_generator.generate_html_from_markdown(
                markdown_path, html_path, photo_path
            )
            
            if not success:
                print("❌ Failed to generate HTML resume")
                return False
            
            # Convert HTML to PDF
            success = self.convert_html_to_pdf(html_path, pdf_output_path)
            
            # Clean up temporary HTML if not keeping it
            if not keep_html and html_path != html_output_path:
                try:
                    os.unlink(html_path)
                except:
                    pass
            
            return success
            
        except Exception as e:
            print(f"❌ Error generating PDF from markdown: {e}")
            return False
    
    def convert_html_to_pdf(self, html_path: str, pdf_output_path: str) -> bool:
        """
        Convert HTML file to PDF using WeasyPrint
        
        Args:
            html_path: Path to HTML file
            pdf_output_path: Where to save the PDF file
            
        Returns:
            bool: Success status
        """
        try:
            print(f"📄 Converting HTML to PDF...")
            
            if not os.path.exists(html_path):
                print(f"❌ HTML file not found: {html_path}")
                return False
            
            # Ensure output directory exists
            output_dir = Path(pdf_output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Additional CSS for PDF optimization
            pdf_css = CSS(string="""
                @page {
                    size: Letter;
                    margin: 0;
                    -webkit-print-color-adjust: exact;
                    print-color-adjust: exact;
                }
                
                body {
                    -webkit-print-color-adjust: exact;
                    print-color-adjust: exact;
                }
                
                .resume-container {
                    width: 100%;
                    height: 100vh;
                    max-width: none;
                }
                
                /* Ensure colors print correctly */
                .header {
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                }
                
                /* Better font rendering for PDF */
                body {
                    font-size: 11px;
                    line-height: 1.3;
                }
                
                .header-name {
                    font-size: 42px;
                }
                
                .header-tagline {
                    font-size: 16px;
                }
            """, font_config=self.font_config)
            
            # Convert HTML to PDF
            html_doc = HTML(filename=html_path)
            
            # Generate PDF with custom CSS
            html_doc.write_pdf(
                pdf_output_path, 
                stylesheets=[pdf_css],
                font_config=self.font_config,
                optimize_images=True
            )
            
            print(f"✅ PDF generated successfully: {pdf_output_path}")
            
            # Verify PDF was created and has reasonable size
            if os.path.exists(pdf_output_path):
                file_size = os.path.getsize(pdf_output_path)
                if file_size > 1000:  # At least 1KB
                    print(f"📊 PDF file size: {file_size / 1024:.1f} KB")
                    return True
                else:
                    print("⚠️ PDF file seems too small, may be corrupted")
                    return False
            else:
                print("❌ PDF file was not created")
                return False
                
        except Exception as e:
            print(f"❌ Error converting HTML to PDF: {e}")
            return False
    
    def generate_pdf_with_custom_css(self, 
                                   html_path: str, 
                                   pdf_output_path: str,
                                   additional_css: Optional[str] = None) -> bool:
        """
        Generate PDF with additional custom CSS
        
        Args:
            html_path: Path to HTML file
            pdf_output_path: Where to save the PDF file
            additional_css: Optional additional CSS string
            
        Returns:
            bool: Success status
        """
        try:
            base_css = """
                @page {
                    size: Letter;
                    margin: 0;
                    -webkit-print-color-adjust: exact;
                    print-color-adjust: exact;
                }
                
                body {
                    -webkit-print-color-adjust: exact;
                    print-color-adjust: exact;
                }
            """
            
            if additional_css:
                base_css += "\n" + additional_css
            
            css = CSS(string=base_css, font_config=self.font_config)
            
            # Convert with custom CSS
            html_doc = HTML(filename=html_path)
            html_doc.write_pdf(
                pdf_output_path,
                stylesheets=[css], 
                font_config=self.font_config
            )
            
            print(f"✅ PDF with custom CSS generated: {pdf_output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error generating PDF with custom CSS: {e}")
            return False
    
    def validate_dependencies(self) -> bool:
        """
        Validate that all required dependencies are available
        
        Returns:
            bool: True if all dependencies are available
        """
        try:
            # Test WeasyPrint import
            from weasyprint import HTML, CSS
            
            # Test font configuration
            font_config = FontConfiguration()
            
            # Test basic HTML rendering
            test_html = "<html><body><h1>Test</h1></body></html>"
            HTML(string=test_html)
            
            print("✅ All PDF generation dependencies are available")
            return True
            
        except Exception as e:
            print(f"❌ Missing dependencies for PDF generation: {e}")
            print("💡 Install with: pip install weasyprint")
            return False

class PDFOptimizer:
    """
    Additional PDF optimization utilities
    """
    
    @staticmethod
    def estimate_pdf_size(content_length: int) -> str:
        """Estimate PDF file size based on content length"""
        # Rough estimation: 1 page ≈ 50KB, content ratio affects size
        base_size = 50  # KB
        content_factor = content_length / 10000  # Rough factor
        estimated_size = base_size + (content_factor * 20)
        return f"{estimated_size:.1f} KB"
    
    @staticmethod
    def get_pdf_info(pdf_path: str) -> dict:
        """Get information about generated PDF"""
        if not os.path.exists(pdf_path):
            return {"exists": False}
        
        file_size = os.path.getsize(pdf_path)
        return {
            "exists": True,
            "size_bytes": file_size,
            "size_kb": file_size / 1024,
            "size_mb": file_size / (1024 * 1024)
        }

def main():
    """Test the HTML to PDF generator"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate PDF resume from markdown via HTML')
    parser.add_argument('markdown_file', help='Path to markdown resume file')
    parser.add_argument('-o', '--output', default='resume.pdf', help='Output PDF file path')
    parser.add_argument('-p', '--photo', help='Path to photo file')
    parser.add_argument('--keep-html', action='store_true', help='Keep intermediate HTML file')
    parser.add_argument('--html-output', help='Path to save HTML file (if --keep-html)')
    parser.add_argument('--validate', action='store_true', help='Validate dependencies only')
    
    args = parser.parse_args()
    
    generator = HTMLPDFGenerator()
    
    if args.validate:
        success = generator.validate_dependencies()
        return success
    
    if not os.path.exists(args.markdown_file):
        print(f"❌ Markdown file not found: {args.markdown_file}")
        return False
    
    # Validate dependencies first
    if not generator.validate_dependencies():
        return False
    
    success = generator.generate_pdf_from_markdown(
        args.markdown_file, 
        args.output, 
        args.photo,
        args.keep_html,
        args.html_output
    )
    
    if success:
        info = PDFOptimizer.get_pdf_info(args.output)
        print(f"📊 Final PDF: {info['size_kb']:.1f} KB")
    
    return success

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)