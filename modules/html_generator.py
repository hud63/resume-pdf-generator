#!/usr/bin/env python3
"""
HTML Resume Generator
Generates professional HTML resume from structured content using Jinja2 templating
"""

import os
from pathlib import Path
from typing import Optional
try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
except ImportError:
    print("Jinja2 not installed. Run: pip install jinja2")
    raise

from .html_content_processor import HTMLContentProcessor, StructuredContent

class HTMLResumeGenerator:
    """
    Generates HTML resume from structured content using professional template
    """
    
    def __init__(self, template_dir: Optional[str] = None):
        """
        Initialize HTML generator
        
        Args:
            template_dir: Directory containing HTML templates (default: ../templates)
        """
        if template_dir is None:
            # Default to templates directory relative to this module
            current_dir = Path(__file__).parent
            template_dir = current_dir.parent / "templates"
        
        self.template_dir = Path(template_dir)
        
        # Initialize Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )
        
        # Content processor
        self.content_processor = HTMLContentProcessor()
    
    def generate_html_from_markdown(self, 
                                  markdown_path: str, 
                                  output_path: str,
                                  photo_path: Optional[str] = None,
                                  template_name: str = "resume_template.html") -> bool:
        """
        Generate HTML resume from markdown file
        
        Args:
            markdown_path: Path to markdown resume file
            output_path: Where to save the HTML file
            photo_path: Optional path to photo file
            template_name: Name of template file to use
            
        Returns:
            bool: Success status
        """
        try:
            print(f"Processing resume content from {markdown_path}...")
            
            # Process content into structured format
            structured_content = self.content_processor.process_for_html_template(
                markdown_path, photo_path
            )
            
            # Optimize for single-page layout
            structured_content = self.content_processor.optimize_for_single_page(structured_content)
            
            return self.generate_html_from_content(
                structured_content, output_path, template_name
            )
            
        except Exception as e:
            print(f"Error generating HTML from markdown: {e}")
            return False
    
    def generate_html_from_content(self, 
                                 content: StructuredContent,
                                 output_path: str,
                                 template_name: str = "resume_template.html") -> bool:
        """
        Generate HTML resume from structured content
        
        Args:
            content: StructuredContent object with resume data
            output_path: Where to save the HTML file
            template_name: Name of template file to use
            
        Returns:
            bool: Success status
        """
        try:
            # Load template
            template = self.env.get_template(template_name)
            
            # Convert structured content to template variables
            template_vars = self._content_to_template_vars(content)
            
            # Render template
            html_output = template.render(**template_vars)
            
            # Ensure output directory exists
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Write HTML file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_output)
            
            print(f"[OK] HTML resume generated: {output_path}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error generating HTML: {e}")
            return False
    
    def _content_to_template_vars(self, content: StructuredContent) -> dict:
        """
        Convert StructuredContent to template variables
        
        Args:
            content: StructuredContent object
            
        Returns:
            dict: Template variables
        """
        return {
            'name': content.name,
            'tagline': content.tagline,
            'contact_parts': content.contact_parts,
            'photo_path': content.photo_path,
            'bio': content.bio,
            'strengths': content.strengths,
            'education': content.education,
            'languages': content.languages,
            'technical': content.technical,
            'experiences': content.experiences,
            'professional_development': content.professional_development
        }
    
    def preview_content_structure(self, markdown_path: str, photo_path: Optional[str] = None):
        """
        Preview the structured content without generating HTML
        
        Args:
            markdown_path: Path to markdown resume file
            photo_path: Optional path to photo file
        """
        try:
            structured_content = self.content_processor.process_for_html_template(
                markdown_path, photo_path
            )
            
            print("[PREVIEW] STRUCTURED CONTENT PREVIEW")
            print("=" * 50)
            
            print(f"[NAME] Name: {structured_content.name}")
            print(f"[TAGLINE] Tagline: {structured_content.tagline}")
            
            print(f"[CONTACT] Contact ({len(structured_content.contact_parts)} items):")
            for contact in structured_content.contact_parts:
                print(f"   • {contact}")
            
            print(f"[PHOTO] Photo: {structured_content.photo_path or 'Not found'}")
            
            print(f"[BIO] Bio: {structured_content.bio[:100]}...")
            
            print(f"[STRENGTHS] Strengths ({len(structured_content.strengths)} items):")
            for strength in structured_content.strengths:
                print(f"   • {strength['title']}: {strength['description'][:50]}...")
            
            print(f"[EDUCATION] Education ({len(structured_content.education)} items):")
            for edu in structured_content.education:
                print(f"   • {edu['degree']} - {edu['institution']}")
            
            print(f"[LANGUAGES] Languages ({len(structured_content.languages)} items):")
            for lang in structured_content.languages:
                print(f"   • {lang['name']}: {lang['level']}")
            
            print(f"[TECHNICAL] Technical ({len(structured_content.technical)} categories):")
            for tech in structured_content.technical:
                print(f"   • {tech['title']}: {tech['items'][:50]}...")
            
            print(f"[EXPERIENCE] Experiences ({len(structured_content.experiences)} jobs):")
            for exp in structured_content.experiences:
                achievements_count = len(exp.get('achievements', []))
                print(f"   • {exp['title']} at {exp['company']} ({achievements_count} achievements)")
            
            print(f"[DEVELOPMENT] Professional Development ({len(structured_content.professional_development)} items):")
            for dev in structured_content.professional_development:
                print(f"   • {dev}")
            
            print("=" * 50)
            
        except Exception as e:
            print(f"Error previewing content: {e}")

def main():
    """Test the HTML generator"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate HTML resume from markdown')
    parser.add_argument('markdown_file', help='Path to markdown resume file')
    parser.add_argument('-o', '--output', default='resume.html', help='Output HTML file path')
    parser.add_argument('-p', '--photo', help='Path to photo file')
    parser.add_argument('--preview', action='store_true', help='Preview content structure only')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.markdown_file):
        print(f"[ERROR] Markdown file not found: {args.markdown_file}")
        return False
    
    generator = HTMLResumeGenerator()
    
    if args.preview:
        generator.preview_content_structure(args.markdown_file, args.photo)
        return True
    else:
        success = generator.generate_html_from_markdown(
            args.markdown_file, args.output, args.photo
        )
        return success

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)