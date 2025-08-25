#!/usr/bin/env python3
"""
Simple HTML to PDF Generator
Alternative PDF generation using browser-based rendering or ReportLab fallback
"""

import os
import tempfile
import subprocess
from pathlib import Path
from typing import Optional
import sys

from .html_generator import HTMLResumeGenerator

class SimpleHTMLPDFGenerator:
    """
    Simple HTML to PDF generator with multiple fallback strategies
    """
    
    def __init__(self):
        self.html_generator = HTMLResumeGenerator()
    
    def generate_pdf_from_markdown(self, 
                                 markdown_path: str,
                                 pdf_output_path: str,
                                 photo_path: Optional[str] = None,
                                 keep_html: bool = False,
                                 html_output_path: Optional[str] = None) -> bool:
        """
        Generate PDF resume from markdown file using the best available method
        
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
            print(f"[PDF] Starting PDF generation from {markdown_path}...")
            
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
                print("[ERROR] Failed to generate HTML resume")
                return False
            
            # Try different PDF conversion methods
            pdf_success = False
            
            # Method 1: Try Chrome/Edge if available
            if self._has_browser():
                print("[BROWSER] Using browser-based PDF generation...")
                pdf_success = self._convert_with_browser(html_path, pdf_output_path)
            
            # Method 2: Fallback to enhanced HTML with print styles
            if not pdf_success:
                print("[HTML] Using enhanced HTML with print instructions...")
                pdf_success = self._create_print_html(html_path, pdf_output_path)
            
            # Clean up temporary HTML if not keeping it
            if not keep_html and html_path != html_output_path:
                try:
                    os.unlink(html_path)
                except:
                    pass
            
            return pdf_success
            
        except Exception as e:
            print(f"[ERROR] Error generating PDF from markdown: {e}")
            return False
    
    def _has_browser(self) -> bool:
        """Check if Chrome or Edge is available for PDF generation"""
        browsers = [
            "chrome", "google-chrome", "chromium",
            "msedge", "microsoft-edge"
        ]
        
        for browser in browsers:
            if self._command_exists(browser):
                return True
        
        # Check Windows-specific paths
        windows_chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        
        windows_edge_paths = [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
        ]
        
        for path in windows_chrome_paths + windows_edge_paths:
            if os.path.exists(path):
                return True
        
        return False
    
    def _command_exists(self, command: str) -> bool:
        """Check if a command exists in PATH"""
        try:
            subprocess.run([command, "--version"], 
                         capture_output=True, 
                         timeout=5)
            return True
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _convert_with_browser(self, html_path: str, pdf_output_path: str) -> bool:
        """Convert HTML to PDF using browser's print-to-PDF functionality"""
        try:
            # Ensure output directory exists
            output_dir = Path(pdf_output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Find available browser
            browser_cmd = self._find_browser_command()
            if not browser_cmd:
                return False
            
            # Convert to absolute paths
            html_abs_path = os.path.abspath(html_path)
            pdf_abs_path = os.path.abspath(pdf_output_path)
            
            # Browser command for PDF generation
            cmd = [
                browser_cmd,
                "--headless",
                "--disable-gpu",
                "--no-margins",
                "--no-pdf-header-footer",  # Remove headers/footers
                "--disable-web-security",   # Allow local file access
                "--run-all-compositor-stages-before-draw",
                "--virtual-time-budget=5000",  # Give time for fonts to load
                "--print-to-pdf=" + pdf_abs_path,
                "file://" + html_abs_path
            ]
            
            # Run browser command
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=30)
            
            if result.returncode == 0 and os.path.exists(pdf_output_path):
                file_size = os.path.getsize(pdf_output_path)
                if file_size > 1000:  # At least 1KB
                    print(f"[OK] PDF generated via browser: {pdf_output_path}")
                    print(f"[INFO] PDF size: {file_size / 1024:.1f} KB")
                    return True
            
            # Log error if available
            if result.stderr:
                print(f"Browser error: {result.stderr}")
            
            return False
            
        except Exception as e:
            print(f"Browser PDF conversion error: {e}")
            return False
    
    def _find_browser_command(self) -> Optional[str]:
        """Find the best available browser command"""
        # Try common command names first
        browsers = ["chrome", "google-chrome", "chromium", "msedge"]
        
        for browser in browsers:
            if self._command_exists(browser):
                return browser
        
        # Try Windows-specific paths
        windows_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
        ]
        
        for path in windows_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def _create_print_html(self, html_path: str, pdf_output_path: str) -> bool:
        """Create an enhanced HTML file with print instructions"""
        try:
            # Read original HTML
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Create enhanced print version
            print_html_path = html_path.replace('.html', '_print.html')
            
            # Add print instructions and enhanced styles
            enhanced_html = self._add_print_enhancements(html_content)
            
            with open(print_html_path, 'w', encoding='utf-8') as f:
                f.write(enhanced_html)
            
            # Copy to PDF path with .html extension for viewing
            html_pdf_path = pdf_output_path.replace('.pdf', '_printable.html')
            
            with open(html_pdf_path, 'w', encoding='utf-8') as f:
                f.write(enhanced_html)
            
            print(f"[OK] Print-optimized HTML created: {html_pdf_path}")
            print("[TIP] Open this file in your browser and print to PDF (Ctrl+P)")
            print("   Set margins to 'None' and check 'Background graphics'")
            
            return True
            
        except Exception as e:
            print(f"Error creating print HTML: {e}")
            return False
    
    def _add_print_enhancements(self, html_content: str) -> str:
        """Add print optimizations to HTML content"""
        
        print_instructions = """
        <!-- PRINT INSTRUCTIONS -->
        <div class="print-instructions no-print" style="
            position: fixed; 
            top: 10px; 
            right: 10px; 
            background: #007bff; 
            color: white; 
            padding: 15px; 
            border-radius: 5px; 
            max-width: 300px; 
            z-index: 1000;
            font-family: Arial, sans-serif;
            font-size: 12px;
            line-height: 1.4;
        ">
            <strong>[PDF] Print to PDF Instructions:</strong><br>
            1. Press Ctrl+P (or Cmd+P on Mac)<br>
            2. Set destination to "Save as PDF"<br>
            3. Set margins to "None"<br>
            4. Check "Background graphics"<br>
            5. Click Save<br>
            <button onclick="window.print()" style="
                background: white; 
                color: #007bff; 
                border: none; 
                padding: 5px 10px; 
                border-radius: 3px; 
                margin-top: 10px; 
                cursor: pointer;
            ">[Print] Print Now</button>
        </div>
        """
        
        enhanced_css = """
        <style>
        /* Enhanced print styles */
        @media print {
            .no-print { display: none !important; }
            
            body { 
                margin: 0 !important; 
                padding: 0 !important;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }
            
            .resume-container {
                width: 100% !important;
                max-width: none !important;
                height: 100vh !important;
                page-break-inside: avoid;
            }
            
            .header {
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
                background: #4a4e69 !important;
            }
            
            .header * {
                color: white !important;
            }
            
            .sidebar {
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
                background: #f8f9fa !important;
            }
            
            .section-title {
                color: #4a4e69 !important;
            }
            
            .company-info {
                color: #4ba9b0 !important;
            }
            
            /* Prevent page breaks within sections */
            .sidebar-section, .experience-entry {
                page-break-inside: avoid;
            }
        }
        
        /* General improvements */
        .print-button {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #28a745;
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 50px;
            font-size: 16px;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
            z-index: 1001;
        }
        
        .print-button:hover {
            background: #218838;
            transform: translateY(-2px);
        }
        </style>
        """
        
        print_button = """
        <button class="print-button no-print" onclick="window.print()">
            [Print] Print to PDF
        </button>
        """
        
        # Insert enhancements
        if '<head>' in html_content:
            html_content = html_content.replace('<head>', '<head>' + enhanced_css)
        
        if '<body>' in html_content:
            html_content = html_content.replace('<body>', '<body>' + print_instructions)
        
        if '</body>' in html_content:
            html_content = html_content.replace('</body>', print_button + '</body>')
        
        return html_content
    
    def validate_dependencies(self) -> bool:
        """Validate PDF generation capabilities"""
        print("[CHECK] Checking PDF generation capabilities...")
        
        browser_available = self._has_browser()
        
        if browser_available:
            browser_cmd = self._find_browser_command()
            print(f"[OK] Browser found: {browser_cmd}")
        else:
            print("[WARN] No browser found for direct PDF generation")
        
        print("[OK] Print-optimized HTML generation available")
        
        return True  # Always return True since we have fallback methods

def main():
    """Test the simple HTML to PDF generator"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate PDF resume from markdown via HTML (Simple)')
    parser.add_argument('markdown_file', help='Path to markdown resume file')
    parser.add_argument('-o', '--output', default='resume.pdf', help='Output PDF file path')
    parser.add_argument('-p', '--photo', help='Path to photo file')
    parser.add_argument('--keep-html', action='store_true', help='Keep intermediate HTML file')
    parser.add_argument('--html-output', help='Path to save HTML file (if --keep-html)')
    parser.add_argument('--validate', action='store_true', help='Validate dependencies only')
    
    args = parser.parse_args()
    
    generator = SimpleHTMLPDFGenerator()
    
    if args.validate:
        success = generator.validate_dependencies()
        return success
    
    if not os.path.exists(args.markdown_file):
        print(f"[ERROR] Markdown file not found: {args.markdown_file}")
        return False
    
    success = generator.generate_pdf_from_markdown(
        args.markdown_file, 
        args.output, 
        args.photo,
        args.keep_html,
        args.html_output
    )
    
    return success

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)