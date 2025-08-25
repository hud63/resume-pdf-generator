#!/usr/bin/env python3
"""
Template-Based PDF Builder
Recreates the exact Template.pdf layout using ReportLab with searchable text
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import black, white, HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether, Table, TableStyle
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from typing import Dict
from .content_processor import ProcessedContent
import os
from PIL import Image, ImageDraw


class TemplatePDFBuilder:
    """
    Builds PDF that matches Template.pdf layout exactly using ReportLab
    """
    
    def __init__(self):
        self.page_width, self.page_height = letter
        
        # Layout dimensions (based on Template.pdf analysis)
        self.margin_left = 0.5 * inch
        self.margin_right = 0.5 * inch  
        self.margin_top = 0.5 * inch
        self.margin_bottom = 0.5 * inch
        
        # Two-column layout
        self.sidebar_width = 2.8 * inch  # Left sidebar
        self.main_width = 4.7 * inch     # Right main content
        self.column_gap = 0.3 * inch
        
        # Header dimensions
        self.header_height = 2.2 * inch
        
        # Colors from template
        self.header_color = HexColor('#4a4e69')  # Dark blue-gray
        self.accent_color = HexColor('#4ba9b0')  # Teal accent
        self.text_color = HexColor('#333333')    # Dark gray text
        
        # Create styles
        self._create_styles()
    
    def _create_styles(self):
        """Create paragraph styles matching template"""
        from reportlab.lib.styles import StyleSheet1
        self.styles = StyleSheet1()
        
        # Add base Normal style first
        self.styles.add(ParagraphStyle(
            name='Normal',
            fontName='Helvetica',
            fontSize=10,
            leading=12,
            textColor=black
        ))
        
        # Header styles
        self.styles.add(ParagraphStyle(
            name='HeaderName',
            parent=self.styles['Normal'],
            fontSize=32,
            leading=36,
            textColor=white,
            fontName='Helvetica-Bold',
            alignment=TA_LEFT
        ))
        
        self.styles.add(ParagraphStyle(
            name='HeaderTagline', 
            parent=self.styles['Normal'],
            fontSize=14,
            leading=16,
            textColor=white,
            fontName='Helvetica',
            alignment=TA_LEFT
        ))
        
        self.styles.add(ParagraphStyle(
            name='HeaderContact',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=13,
            textColor=white,
            fontName='Helvetica',
            alignment=TA_CENTER
        ))
        
        # Section headers
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Normal'],
            fontSize=12,
            leading=14,
            textColor=self.header_color,
            fontName='Helvetica-Bold',
            alignment=TA_LEFT,
            spaceBefore=16,
            spaceAfter=8
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='BodyText',
            parent=self.styles['Normal'],
            fontSize=9,
            leading=11,
            textColor=self.text_color,
            fontName='Helvetica',
            alignment=TA_LEFT
        ))
        
        # Job titles
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=13,
            textColor=self.text_color,
            fontName='Helvetica-Bold',
            alignment=TA_LEFT,
            spaceBefore=12,
            spaceAfter=4
        ))
        
        # Company info
        self.styles.add(ParagraphStyle(
            name='CompanyInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            leading=12,
            textColor=self.accent_color,
            fontName='Helvetica',
            alignment=TA_LEFT,
            spaceAfter=6
        ))
        
        # Bullet points
        self.styles.add(ParagraphStyle(
            name='BulletPoint',
            parent=self.styles['Normal'],
            fontSize=9,
            leading=11,
            textColor=self.text_color,
            fontName='Helvetica',
            alignment=TA_LEFT,
            leftIndent=12,
            bulletIndent=6
        ))
        
        # Skills/Technical
        self.styles.add(ParagraphStyle(
            name='SkillCategory',
            parent=self.styles['Normal'],
            fontSize=9,
            leading=11,
            textColor=self.text_color,
            fontName='Helvetica-Bold',
            alignment=TA_LEFT,
            spaceBefore=8,
            spaceAfter=4
        ))
        
        self.styles.add(ParagraphStyle(
            name='SkillList',
            parent=self.styles['Normal'],
            fontSize=9,
            leading=11,
            textColor=self.text_color,
            fontName='Helvetica',
            alignment=TA_LEFT
        ))
    
    def create_template_pdf(self, content_dict: Dict[str, ProcessedContent], output_path: str) -> bool:
        """
        Create PDF matching Template.pdf layout exactly
        """
        try:
            # Create canvas for custom layout
            c = canvas.Canvas(output_path, pagesize=letter)
            
            # Draw header section
            self._draw_header(c, content_dict)
            
            # Draw two-column content
            self._draw_sidebar(c, content_dict)
            self._draw_main_content(c, content_dict)
            
            c.showPage()
            c.save()
            
            return True
            
        except Exception as e:
            print(f"Error creating template PDF: {e}")
            return False
    
    def _draw_header(self, c: canvas.Canvas, content: Dict[str, ProcessedContent]):
        """Draw the dark header section with name, tagline, and contact"""
        
        # Draw header background
        c.setFillColor(self.header_color)
        c.rect(0, self.page_height - self.header_height, self.page_width, self.header_height, fill=1)
        
        # Position for header content
        header_y = self.page_height - self.margin_top - 30
        
        # Draw name
        name_text = content.get('name', ProcessedContent('name', 'MARK CETOLA', 11, False)).content
        c.setFont('Helvetica-Bold', 32)
        c.setFillColor(white)
        c.drawString(self.margin_left + 150, header_y, name_text)  # Offset for photo space
        
        # Draw tagline
        tagline_text = content.get('tagline', ProcessedContent('tagline', 'Professional tagline', 50, False)).content
        c.setFont('Helvetica', 14)
        c.drawString(self.margin_left + 150, header_y - 35, tagline_text)
        
        # Draw contact info (centered)
        contact_text = content.get('contact', ProcessedContent('contact', 'Contact info', 50, False)).content
        contact_parts = contact_text.split(' | ')
        
        contact_y = header_y - 80
        c.setFont('Helvetica', 11)
        
        # Center the contact info
        total_width = sum([c.stringWidth(part, 'Helvetica', 11) for part in contact_parts]) + (len(contact_parts) - 1) * 20
        start_x = (self.page_width - total_width) / 2
        
        for i, part in enumerate(contact_parts):
            if i > 0:
                c.drawString(start_x, contact_y, ' | ')
                start_x += 20
            c.drawString(start_x, contact_y, part)
            start_x += c.stringWidth(part, 'Helvetica', 11)
        
        # Professional headshot integration
        self._draw_professional_photo(c, self.margin_left + 20, header_y - 60, 80)
    
    def _draw_sidebar(self, c: canvas.Canvas, content: Dict[str, ProcessedContent]):
        """Draw left sidebar with BIO, STRENGTHS, EDUCATION, etc."""
        
        sidebar_x = self.margin_left
        current_y = self.page_height - self.header_height - 30
        
        # BIO Section
        current_y = self._draw_section(c, 'BIO', content.get('bio', None), sidebar_x, current_y, self.sidebar_width)
        
        # STRENGTHS Section
        current_y = self._draw_section(c, 'STRENGTHS', content.get('strengths', None), sidebar_x, current_y, self.sidebar_width)
        
        # EDUCATION Section  
        current_y = self._draw_section(c, 'EDUCATION', content.get('education', None), sidebar_x, current_y, self.sidebar_width)
        
        # LANGUAGES Section
        current_y = self._draw_section(c, 'LANGUAGES', content.get('languages', None), sidebar_x, current_y, self.sidebar_width)
        
        # TECHNICAL Section
        current_y = self._draw_section(c, 'TECHNICAL', content.get('technical', None), sidebar_x, current_y, self.sidebar_width)
    
    def _draw_main_content(self, c: canvas.Canvas, content: Dict[str, ProcessedContent]):
        """Draw right column with career highlights and experience"""
        
        main_x = self.margin_left + self.sidebar_width + self.column_gap
        current_y = self.page_height - self.header_height - 30
        
        # CAREER HIGHLIGHTS Section
        current_y = self._draw_section(c, 'CAREER HIGHLIGHTS', content.get('bio', None), main_x, current_y, self.main_width, is_main=True)
        
        # Experience sections (if available)
        for i in range(1, 4):  # Up to 3 experience entries
            exp_key = f'experience_{i}'
            if exp_key in content:
                current_y = self._draw_experience_entry(c, content[exp_key], main_x, current_y, self.main_width)
    
    def _draw_section(self, c: canvas.Canvas, title: str, content_item: ProcessedContent, x: float, y: float, width: float, is_main: bool = False):
        """Draw a content section with title and content"""
        
        # Draw section title
        c.setFont('Helvetica-Bold', 12)
        c.setFillColor(self.header_color)
        c.drawString(x, y, title)
        y -= 20
        
        # Draw content if available
        if content_item and content_item.content:
            content_text = content_item.content
            
            # Handle different content types
            if title == 'TECHNICAL':
                y = self._draw_technical_content(c, content_text, x, y, width)
            elif title == 'LANGUAGES':
                y = self._draw_languages_content(c, content_text, x, y, width)
            elif title == 'STRENGTHS':
                y = self._draw_strengths_content(c, content_text, x, y, width)
            else:
                y = self._draw_text_content(c, content_text, x, y, width)
        
        return y - 20  # Add spacing after section
    
    def _draw_text_content(self, c: canvas.Canvas, text: str, x: float, y: float, width: float):
        """Draw wrapped text content"""
        c.setFont('Helvetica', 9)
        c.setFillColor(self.text_color)
        
        # Simple text wrapping
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if c.stringWidth(test_line, 'Helvetica', 9) <= width - 10:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Draw lines
        line_height = 11
        for line in lines[:8]:  # Limit lines to fit space
            c.drawString(x, y, line)
            y -= line_height
            
        return y
    
    def _draw_technical_content(self, c: canvas.Canvas, text: str, x: float, y: float, width: float):
        """Draw technical skills with categories"""
        c.setFont('Helvetica', 9)
        c.setFillColor(self.text_color)
        
        # Parse and format technical skills
        skills = text.replace(',', '\n').replace('-', '').strip()
        lines = [line.strip() for line in skills.split('\n') if line.strip()]
        
        line_height = 11
        for line in lines[:10]:  # Limit to fit space
            c.drawString(x, y, f"• {line}")
            y -= line_height
            
        return y
    
    def _draw_languages_content(self, c: canvas.Canvas, text: str, x: float, y: float, width: float):
        """Draw languages with proficiency levels"""
        c.setFont('Helvetica', 9)
        c.setFillColor(self.text_color)
        
        lines = text.replace('-', '').strip().split('\n')
        line_height = 11
        
        for line in lines[:3]:
            if line.strip():
                c.drawString(x, y, line.strip())
                y -= line_height
                
        return y
    
    def _draw_strengths_content(self, c: canvas.Canvas, text: str, x: float, y: float, width: float):
        """Draw strengths with bullet points"""
        c.setFont('Helvetica', 9)
        c.setFillColor(self.text_color)
        
        # Parse strengths (look for patterns like "**Title:** description")
        lines = text.split('\n')
        line_height = 11
        
        for line in lines[:6]:
            if line.strip():
                # Handle bold titles
                if '**' in line and ':' in line:
                    parts = line.split(':', 1)
                    title = parts[0].replace('**', '').strip()
                    desc = parts[1].strip() if len(parts) > 1 else ''
                    
                    # Draw title in bold
                    c.setFont('Helvetica-Bold', 9)
                    c.drawString(x, y, title + ':')
                    y -= line_height
                    
                    # Draw description
                    if desc:
                        c.setFont('Helvetica', 9)
                        y = self._draw_text_content(c, desc, x + 10, y, width - 10)
                else:
                    y = self._draw_text_content(c, line.strip(), x, y, width)
                    
        return y
    
    def _draw_experience_entry(self, c: canvas.Canvas, exp_content: ProcessedContent, x: float, y: float, width: float):
        """Draw a job experience entry"""
        
        # This would be expanded to handle experience entries
        # For now, just draw as text content
        return self._draw_text_content(c, exp_content.content, x, y, width)
    
    def _create_circular_photo(self, image_path: str, size: int) -> str:
        """
        Create a circular cropped version of the photo and return temp path
        """
        try:
            # Open the image
            img = Image.open(image_path)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize to square
            img = img.resize((size * 3, size * 3), Image.Resampling.LANCZOS)  # High res for quality
            
            # Create circular mask
            mask = Image.new('L', (size * 3, size * 3), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, size * 3, size * 3), fill=255)
            
            # Apply mask
            img.putalpha(mask)
            
            # Save to temp file
            temp_path = os.path.join(os.path.dirname(image_path), 'temp_circular_photo.png')
            img.save(temp_path, 'PNG')
            
            return temp_path
            
        except Exception as e:
            print(f"Error processing photo: {e}")
            return None
    
    def _draw_professional_photo(self, c: canvas.Canvas, x: float, y: float, size: int):
        """
        Draw the professional headshot photo (circular crop)
        """
        # Try to find the photo file
        photo_paths = [
            os.path.join(os.path.dirname(os.path.dirname(__file__)), '039-Dm2VwCrean0.jpeg'),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'headshot.jpg'),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'photo.jpg'),
        ]
        
        photo_path = None
        for path in photo_paths:
            if os.path.exists(path):
                photo_path = path
                break
        
        if photo_path:
            try:
                # Create circular version
                circular_photo_path = self._create_circular_photo(photo_path, size)
                
                if circular_photo_path and os.path.exists(circular_photo_path):
                    # Draw the photo
                    c.drawImage(circular_photo_path, x, y, width=size, height=size, mask='auto')
                    
                    # Clean up temp file
                    try:
                        os.remove(circular_photo_path)
                    except:
                        pass
                    
                    return
                    
            except Exception as e:
                print(f"Error drawing photo: {e}")
        
        # Fallback: draw placeholder circle
        c.setStrokeColor(white)
        c.setFillColor(colors.lightgrey)
        c.circle(x + size/2, y + size/2, size/2, fill=1)
        
        # Add "Photo" text
        c.setFillColor(white)
        c.setFont('Helvetica', 10)
        text_width = c.stringWidth('Photo', 'Helvetica', 10)
        c.drawString(x + size/2 - text_width/2, y + size/2 - 5, 'Photo')