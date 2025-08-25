#!/usr/bin/env python3
"""
PDF Builder Module  
Converts SVG templates with text content to high-quality PDFs
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
import xml.etree.ElementTree as ET
import tempfile
import os
from typing import Dict, Optional
from .content_processor import ProcessedContent
from .template_pdf_builder import TemplatePDFBuilder

class PDFBuilder:
    """
    Builds PDF from SVG template with inserted text content
    """
    
    def __init__(self):
        self.page_width = 8.5 * inch  # Letter size
        self.page_height = 11 * inch
        self.margin = 0.5 * inch  # Standard margins
        
    def create_pdf_from_svg_template(self, svg_content: str, output_path: str, content_dict: Dict[str, ProcessedContent] = None) -> bool:
        """
        Create PDF using template-based approach (replaces SVG conversion)
        
        Args:
            svg_content: SVG content (ignored, kept for compatibility)
            output_path: Path where PDF should be saved
            content_dict: Processed content dictionary
            
        Returns:
            bool: Success status
        """
        try:
            # Use new template-based PDF builder for high-quality, searchable text
            if content_dict:
                template_builder = TemplatePDFBuilder()
                return template_builder.create_template_pdf(content_dict, output_path)
            else:
                print("No content dictionary provided for template PDF generation")
                return False
                
        except Exception as e:
            print(f"Error creating template PDF: {e}")
            
            # Fallback to SVG conversion if template method fails
            try:
                return self._fallback_svg_conversion(svg_content, output_path)
            except Exception as fallback_error:
                print(f"Fallback SVG conversion also failed: {fallback_error}")
                return False
    
    def _fallback_svg_conversion(self, svg_content: str, output_path: str) -> bool:
        """Fallback SVG conversion method (original approach)"""
        try:
            # Create temporary SVG file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.svg', delete=False, encoding='utf-8') as temp_svg:
                temp_svg.write(svg_content)
                temp_svg_path = temp_svg.name
            
            # Convert SVG to ReportLab drawing
            drawing = svg2rlg(temp_svg_path)
            
            if drawing:
                # Fix drawing dimensions and positioning
                self._fix_drawing_properties(drawing)
                
                # Create PDF with proper page setup
                from reportlab.pdfgen import canvas
                from reportlab.lib.pagesizes import letter
                
                # Create canvas with letter size
                c = canvas.Canvas(output_path, pagesize=letter)
                
                # Calculate positioning to remove excessive margins
                page_width, page_height = letter
                
                # Scale and position drawing to fill page properly
                if hasattr(drawing, 'width') and hasattr(drawing, 'height'):
                    # Calculate scale to fit page with minimal margins
                    scale_x = (page_width - self.margin) / drawing.width
                    scale_y = (page_height - self.margin) / drawing.height 
                    scale = min(scale_x, scale_y)
                    
                    # Position drawing with small top margin
                    x_offset = (page_width - drawing.width * scale) / 2
                    y_offset = page_height - drawing.height * scale - (self.margin / 2)
                    
                    # Apply transformations
                    c.saveState()
                    c.translate(x_offset, y_offset)
                    c.scale(scale, scale)
                    
                    # Draw the SVG content
                    renderPDF.draw(drawing, c, 0, 0)
                    c.restoreState()
                else:
                    # Fallback: draw without scaling
                    renderPDF.draw(drawing, c, 0, 0)
                
                c.showPage()
                c.save()
                
                # Clean up temp file
                os.unlink(temp_svg_path)
                
                return True
            else:
                print("Failed to render SVG")
                return False
                
        except Exception as e:
            print(f"Error in SVG fallback: {e}")
            return False
    
    def _fix_drawing_properties(self, drawing):
        """Fix drawing properties for proper PDF rendering"""
        if hasattr(drawing, 'width') and hasattr(drawing, 'height'):
            # Ensure proper dimensions (SVG uses points, ReportLab uses points too)
            # The SVG viewBox is "0 0 594.96 842.25" which is close to A4
            # Convert to letter size proportions
            if drawing.width > 600:  # Looks like A4 size
                # Scale from A4 to letter size
                drawing.width = 8.5 * 72  # 72 points per inch
                drawing.height = 11 * 72
    
    def _scale_drawing(self, drawing):
        """Scale drawing to fit page size if needed"""
        if hasattr(drawing, 'width') and hasattr(drawing, 'height'):
            # Calculate scale factor to fit page
            scale_x = self.page_width / drawing.width
            scale_y = self.page_height / drawing.height
            scale = min(scale_x, scale_y, 1.0)  # Don't scale up
            
            if scale < 1.0:
                drawing.scale(scale, scale)
    
    def create_fallback_pdf(self, content_dict: Dict[str, ProcessedContent], output_path: str) -> bool:
        """
        Create fallback PDF using ReportLab when SVG conversion fails
        This creates a basic resume layout without the template design
        """
        try:
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.colors import black, HexColor
            from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
            
            # Create document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=0.75*inch,
                leftMargin=0.75*inch,
                topMargin=0.6*inch,
                bottomMargin=0.6*inch
            )
            
            # Get styles
            styles = getSampleStyleSheet()
            
            # Professional colors
            dark_blue = HexColor('#2C3E50')
            medium_gray = HexColor('#5D6D7E')
            
            # Create custom styles
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
            
            tagline_style = ParagraphStyle(
                'TaglineStyle',
                parent=styles['Normal'],
                fontSize=12,
                spaceAfter=16,
                spaceBefore=2,
                textColor=medium_gray,
                fontName='Helvetica',
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
            
            section_style = ParagraphStyle(
                'SectionStyle',
                parent=styles['Heading2'],
                fontSize=15,
                spaceAfter=8,
                spaceBefore=18,
                textColor=dark_blue,
                fontName='Helvetica-Bold',
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
            
            # Build content
            story = []
            
            # Add name
            if 'name' in content_dict:
                story.append(Paragraph(content_dict['name'].content, name_style))
                
            # Add tagline
            if 'tagline' in content_dict:
                story.append(Paragraph(content_dict['tagline'].content, tagline_style))
                
            # Add contact
            if 'contact' in content_dict:
                story.append(Paragraph(content_dict['contact'].content, contact_style))
                
            # Add bio
            if 'bio' in content_dict:
                story.append(Paragraph("PROFESSIONAL SUMMARY", section_style))
                story.append(Paragraph(content_dict['bio'].content, body_style))
                
            # Add experience
            experience_sections = [k for k in content_dict.keys() if k.startswith('experience_')]
            if experience_sections:
                story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_style))
                for exp_key in sorted(experience_sections):
                    exp_content = content_dict[exp_key].content
                    # Format experience content
                    lines = exp_content.split('\n')
                    for line in lines:
                        if line.strip():
                            story.append(Paragraph(line, body_style))
                    story.append(Spacer(1, 6))
                    
            # Add technical skills
            if 'technical' in content_dict:
                story.append(Paragraph("TECHNICAL SKILLS", section_style))
                story.append(Paragraph(content_dict['technical'].content, body_style))
                
            # Add strengths
            if 'strengths' in content_dict:
                story.append(Paragraph("KEY STRENGTHS", section_style))
                story.append(Paragraph(content_dict['strengths'].content, body_style))
                
            # Add education
            if 'education' in content_dict:
                story.append(Paragraph("EDUCATION", section_style))
                story.append(Paragraph(content_dict['education'].content, body_style))
                
            # Add languages
            if 'languages' in content_dict:
                story.append(Paragraph("LANGUAGES", section_style))
                story.append(Paragraph(content_dict['languages'].content, body_style))
            
            # Build PDF
            doc.build(story)
            return True
            
        except Exception as e:
            print(f"Error creating fallback PDF: {e}")
            return False

def main():
    """Test the PDF builder"""
    # This would normally be called by the main generator
    print("PDF Builder module loaded successfully")
    print("Use via svg_pdf_generator.py for full functionality")

if __name__ == "__main__":
    main()