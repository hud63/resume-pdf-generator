#!/usr/bin/env python3
"""
SVG-to-PDF Resume Generator
Main script that orchestrates the entire process from markdown resume to PDF via SVG template
"""

import sys
import os
import argparse
from pathlib import Path

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

from modules.svg_parser import SVGParser
from modules.content_processor import ContentProcessor
from modules.pdf_builder import PDFBuilder

class SVGPDFGenerator:
    """
    Main class that orchestrates the SVG-to-PDF resume generation process
    """
    
    def __init__(self, svg_template_path: str, resume_md_path: str):
        self.svg_template_path = svg_template_path
        self.resume_md_path = resume_md_path
        self.svg_parser = SVGParser(svg_template_path)
        self.content_processor = ContentProcessor()
        self.pdf_builder = PDFBuilder()
        
    def generate_resume_pdf(self, output_path: str = None, use_fallback: bool = False) -> bool:
        """
        Generate PDF resume from SVG template and markdown content
        
        Args:
            output_path: Where to save the PDF (default: resume_output.pdf)
            use_fallback: If True, use fallback PDF generation instead of SVG
            
        Returns:
            bool: Success status
        """
        if output_path is None:
            output_path = "resume_output.pdf"
            
        try:
            print("Starting SVG-to-PDF resume generation...")
            
            # Step 1: Parse resume markdown content
            print("Processing resume content...")
            raw_sections = self.content_processor.parse_markdown_resume(self.resume_md_path)
            
            if not raw_sections:
                print("Failed to extract content from resume markdown")
                return False
                
            processed_content = self.content_processor.process_content_for_regions(raw_sections)
            print(f"Processed {len(processed_content)} content regions")
            
            # Show content summary
            self._show_content_summary(processed_content)
            
            if use_fallback:
                # Use fallback PDF generation (no SVG template)
                print("Generating fallback PDF (without SVG template)...")
                success = self.pdf_builder.create_fallback_pdf(processed_content, output_path)
            else:
                # Step 2: Parse SVG template
                print("Loading SVG template...")
                if not self.svg_parser.load_svg():
                    print("Failed to load SVG template")
                    return False
                    
                # Step 3: Identify text regions in SVG
                print("Identifying text placement regions...")
                text_regions = self.svg_parser.identify_text_regions()
                print(f"Found {len(text_regions)} text regions in template")
                
                # Step 4: Map content to SVG regions
                print("Mapping content to SVG regions...")
                content_mapping = self._map_content_to_regions(processed_content, text_regions)
                
                # Step 5: Generate SVG with embedded text
                print("Adding text to SVG template...")
                svg_with_text = self.svg_parser.add_text_to_svg(content_mapping)
                
                if not svg_with_text:
                    print("Failed to generate SVG with text")
                    return False
                    
                # Step 6: Convert to PDF using template-based approach
                print("Converting to PDF using template layout...")
                success = self.pdf_builder.create_pdf_from_svg_template(svg_with_text, output_path, processed_content)
            
            if success:
                print(f"Resume PDF generated successfully: {output_path}")
                return True
            else:
                print("PDF generation failed")
                return False
                
        except Exception as e:
            print(f"Error generating resume PDF: {e}")
            return False
    
    def _show_content_summary(self, processed_content):
        """Show summary of processed content"""
        print("\nContent Summary:")
        for region_type, content in processed_content.items():
            status = "TRUNCATED" if content.truncated else "OK"
            char_count = f"{content.char_count} chars"
            print(f"  • {region_type.ljust(12)}: {char_count.ljust(10)} {status}")
        print()
    
    def _map_content_to_regions(self, processed_content, text_regions):
        """Map processed content to SVG text regions"""
        content_mapping = {}
        
        # Simple mapping based on region types
        # In a more sophisticated version, this would use AI/ML to find best matches
        
        for region_id, region in text_regions.items():
            content_key = self._find_matching_content(region.region_type, processed_content)
            if content_key and content_key in processed_content:
                content_mapping[region_id] = processed_content[content_key].content
                
        return content_mapping
    
    def _find_matching_content(self, region_type, processed_content):
        """Find matching processed content for a region type"""
        # Direct matches
        if region_type in processed_content:
            return region_type
            
        # Special mappings
        mappings = {
            'photo': None,  # Skip photo regions
            'contact': 'contact',
            'name': 'name',
            'tagline': 'tagline', 
            'bio': 'bio',
            'experience': 'experience_1',  # Map to first experience
            'strengths': 'strengths',
            'technical': 'technical',
            'education': 'education',
            'languages': 'languages'
        }
        
        return mappings.get(region_type)
    
    def analyze_template(self):
        """Analyze SVG template and show region information"""
        print("Analyzing SVG template structure...")
        
        if not self.svg_parser.load_svg():
            print("Failed to load SVG template")
            return False
            
        text_regions = self.svg_parser.identify_text_regions()
        
        if not text_regions:
            print("No text regions identified in template")
            return False
            
        print(f"\nFound {len(text_regions)} text regions:")
        print("-" * 60)
        
        for region_id, region in text_regions.items():
            print(f"Region: {region_id}")
            print(f"  Type: {region.region_type}")
            print(f"  Position: ({region.x:.1f}, {region.y:.1f})")
            print(f"  Size: {region.width:.1f} × {region.height:.1f}")
            print(f"  Max chars: {region.max_chars}")
            print(f"  Font size: {region.font_size}")
            print()
            
        return True
    
    def test_content_processing(self):
        """Test content processing without generating PDF"""
        print("Testing content processing...")
        
        raw_sections = self.content_processor.parse_markdown_resume(self.resume_md_path)
        
        if not raw_sections:
            print("Failed to extract content from resume")
            return False
            
        print(f"Extracted {len(raw_sections)} sections:")
        for section, content in raw_sections.items():
            preview = content[:100] + "..." if len(content) > 100 else content
            print(f"  • {section}: {preview}")
        print()
        
        processed_content = self.content_processor.process_content_for_regions(raw_sections)
        
        print(f"Processed {len(processed_content)} regions:")
        for region_type, content in processed_content.items():
            status = "TRUNCATED" if content.truncated else "OK"
            print(f"  • {region_type}: {content.char_count} chars {status}")
            print(f"    Preview: {content.content[:80]}...")
            print()
            
        return True

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description='Generate PDF resume from SVG template and markdown content')
    
    parser.add_argument('resume_md', help='Path to resume markdown file')
    parser.add_argument('--svg-template', default='12.svg', help='Path to SVG template file (default: 12.svg)')
    parser.add_argument('--output', '-o', default='resume_output.pdf', help='Output PDF path (default: resume_output.pdf)')
    parser.add_argument('--fallback', action='store_true', help='Use fallback PDF generation (no SVG template)')
    parser.add_argument('--analyze', action='store_true', help='Analyze SVG template structure only')
    parser.add_argument('--test-content', action='store_true', help='Test content processing only')
    
    args = parser.parse_args()
    
    # Validate input files
    if not os.path.exists(args.resume_md):
        print(f"Resume markdown file not found: {args.resume_md}")
        sys.exit(1)
        
    if not args.fallback and not os.path.exists(args.svg_template):
        print(f"SVG template file not found: {args.svg_template}")
        print("Use --fallback to generate PDF without SVG template")
        sys.exit(1)
    
    # Create generator instance
    generator = SVGPDFGenerator(args.svg_template, args.resume_md)
    
    # Handle different modes
    if args.analyze:
        success = generator.analyze_template()
    elif args.test_content:
        success = generator.test_content_processing()
    else:
        success = generator.generate_resume_pdf(args.output, args.fallback)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()