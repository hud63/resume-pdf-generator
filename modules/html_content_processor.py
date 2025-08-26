#!/usr/bin/env python3
"""
HTML Content Processor
Enhanced content processor that formats resume data specifically for HTML template integration
"""

import re
from typing import Dict, List, Optional
from dataclasses import dataclass
from .content_processor import ContentProcessor, ProcessedContent

@dataclass
class StructuredContent:
    """Enhanced structured content for HTML templates"""
    name: str
    tagline: str
    contact_parts: List[str]
    photo_path: Optional[str]
    bio: str
    strengths: List[Dict[str, str]]
    education: List[Dict[str, str]]
    languages: List[Dict[str, str]]
    technical: List[Dict[str, str]]
    experiences: List[Dict[str, any]]
    professional_development: List[str]
    font_scale_factor: float = 1.0  # Dynamic font scaling factor

class HTMLContentProcessor(ContentProcessor):
    """
    Enhanced content processor that structures data for HTML template rendering
    """
    
    def __init__(self):
        super().__init__()
        
    def process_for_html_template(self, md_file_path: str, photo_path: Optional[str] = None) -> StructuredContent:
        """
        Process markdown resume into structured data for HTML template
        
        Args:
            md_file_path: Path to markdown resume file
            photo_path: Optional path to photo file
            
        Returns:
            StructuredContent object ready for template rendering
        """
        # Parse raw content from markdown
        raw_sections = self.parse_markdown_resume(md_file_path)
        
        if not raw_sections:
            raise ValueError("Failed to extract content from resume markdown")
        
        # Process each section with enhanced formatting
        return StructuredContent(
            name=self._process_name_for_html(raw_sections.get('raw_name', '')),
            tagline=self._process_tagline_for_html(raw_sections.get('raw_tagline', '')),
            contact_parts=self._process_contact_for_html(raw_sections.get('raw_contact', '')),
            photo_path=self._resolve_photo_path(photo_path),
            bio=self._process_bio_for_html(raw_sections.get('raw_bio', '')),
            strengths=self._process_strengths_for_html(raw_sections.get('raw_strengths', '')),
            education=self._process_education_for_html(raw_sections.get('raw_education', '')),
            languages=self._process_languages_for_html(raw_sections.get('raw_languages', '')),
            technical=self._process_technical_for_html(raw_sections.get('raw_technical', '')),
            experiences=self._process_experiences_for_html(raw_sections.get('raw_experience', '')),
            professional_development=self._process_professional_development(raw_sections)
        )
    
    def _process_name_for_html(self, raw_name: str) -> str:
        """Clean and format name for HTML display"""
        if not raw_name:
            return "MARK CETOLA"
        return re.sub(r'\*\*', '', raw_name).strip().upper()
    
    def _process_tagline_for_html(self, raw_tagline: str) -> str:
        """Format tagline for HTML display"""
        if not raw_tagline:
            return "On a mission to unleash business profitability through automation and AI innovation"
        
        clean_tagline = re.sub(r'\*\*', '', raw_tagline).strip()
        # Ensure it doesn't end with a period for tagline display
        if clean_tagline.endswith('.'):
            clean_tagline = clean_tagline[:-1]
        return clean_tagline
    
    def _process_contact_for_html(self, raw_contact: str) -> List[str]:
        """Process contact info into list for template"""
        if not raw_contact:
            return ["(561) 600-8773", "mark.newagemedia@gmail.com", "www.linkedin.com/in/MarkCetola"]
        
        # Clean URLs
        clean_contact = raw_contact.replace('https://', '').replace('http://', '')
        clean_contact = clean_contact.replace('www.', '')
        
        # Split on common separators
        parts = re.split(r'\s*[|•]\s*', clean_contact)
        return [part.strip() for part in parts if part.strip()]
    
    def _resolve_photo_path(self, photo_path: Optional[str]) -> Optional[str]:
        """Resolve photo path for template"""
        import os
        
        if photo_path and os.path.exists(photo_path):
            return os.path.abspath(photo_path)
        
        # Try to find photo in current directory
        possible_paths = [
            '039-Dm2VwCrean0.jpeg',
            'photo.jpg',
            'headshot.jpg',
            'profile.png'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return os.path.abspath(path)
                
        return None
    
    def _process_bio_for_html(self, raw_bio: str) -> str:
        """Format bio content for HTML with proper paragraphs"""
        if not raw_bio:
            return """Finance & Sales professional with 8 years' experience in small to enterprise companies 
            and a strong understanding of marketing funnels, what-if analyses and automation tools. 
            Outside of work, highlights include successfully growing an Instagram Channel to 529,000+ subscribers 
            and TikTok Channel to 200,000+ subscribers on top of a busy day job, learning a suite of creative 
            and digital marketing skills from scratch (video editing, SEO, SM engagement strategies)"""
        
        # Remove markdown formatting and clean bullet points
        clean_bio = re.sub(r'\*\*', '', raw_bio)
        clean_bio = re.sub(r'\n+', ' ', clean_bio).strip()
        
        # Clean bullet points - convert "- Item:" to "Item:"
        clean_bio = re.sub(r'-\s*([^:]+:)', r'\1', clean_bio)
        # Clean remaining standalone hyphens
        clean_bio = re.sub(r'\s-\s', ' ', clean_bio)
        
        # Convert to HTML paragraphs if needed
        sentences = re.split(r'[.!?]+', clean_bio)
        
        # Group sentences into logical paragraphs (2-3 sentences each)
        paragraphs = []
        current_paragraph = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                current_paragraph.append(sentence)
                if len(current_paragraph) >= 2:
                    paragraphs.append('. '.join(current_paragraph) + '.')
                    current_paragraph = []
        
        # Add any remaining sentences
        if current_paragraph:
            paragraphs.append('. '.join(current_paragraph) + '.')
        
        # Join paragraphs with HTML line breaks
        return '<br><br>'.join(paragraphs[:2])  # Limit to 2 paragraphs for space
    
    def _process_strengths_for_html(self, raw_strengths: str) -> List[Dict[str, str]]:
        """Process strengths into structured format for HTML"""
        if not raw_strengths:
            return [
                {
                    "title": "PUZZLES, NOT PROBLEMS",
                    "description": """Problem-solving has been an integral aspect of my career to date, 
                    whether it be understanding a particular legal issue, collaborating with stakeholders 
                    to adapt the wording on marketing material, or developing innovative ways to generate 
                    an ideal outcome for a prospective client."""
                },
                {
                    "title": "CONNECTING THE DOTS", 
                    "description": """I am skilled at understanding complex ideas and filtering key points 
                    from large amounts of information, understanding my audience, and individualising my 
                    messaging to ensure it is delivered clearly and concisely."""
                }
            ]
        
        strengths = []
        lines = raw_strengths.split('\n')
        current_strength = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('- **') and '**' in line:
                # Save previous strength
                if current_strength:
                    strengths.append(current_strength)
                
                # Extract title
                title_match = re.search(r'\*\*(.+?)\*\*', line)
                if title_match:
                    title = title_match.group(1).upper()
                    description = line.split('**', 2)[-1].strip().rstrip(':')
                    current_strength = {"title": title, "description": description}
            elif line and current_strength and not line.startswith('- **'):
                # Add to description
                current_strength["description"] += " " + line
        
        # Add final strength
        if current_strength:
            strengths.append(current_strength)
        
        # Clean up descriptions and limit to 2 strengths
        for strength in strengths[:2]:
            strength["description"] = re.sub(r'\s+', ' ', strength["description"]).strip()
            if len(strength["description"]) > 200:
                strength["description"] = strength["description"][:197] + "..."
        
        return strengths[:2]
    
    def _process_education_for_html(self, raw_education: str) -> List[Dict[str, str]]:
        """Process education into structured format"""
        if not raw_education:
            return [{"degree": "Bachelor of Science in Real Estate (BSRE)", "institution": "Temple University"}]
        
        education = []
        lines = raw_education.split('\n')
        current_degree = ""
        current_institution = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith('**') and line.endswith('**'):
                current_degree = line[2:-2]
            elif line and not line.startswith('_') and not line.startswith('**'):
                current_institution = line
                
        if current_degree and current_institution:
            education.append({"degree": current_degree, "institution": current_institution})
        elif current_degree:
            education.append({"degree": current_degree, "institution": ""})
        
        return education
    
    def _process_languages_for_html(self, raw_languages: str) -> List[Dict[str, str]]:
        """Process languages into structured format"""
        if not raw_languages:
            return [
                {"name": "ENGLISH", "level": "Native"},
                {"name": "SPANISH", "level": "Beginner"}
            ]
        
        languages = []
        lines = raw_languages.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('- '):
                lang_info = line[2:].strip()
                # Try to split on common patterns
                if '(' in lang_info and ')' in lang_info:
                    parts = lang_info.split('(')
                    name = parts[0].strip()
                    level = parts[1].replace(')', '').strip()
                    languages.append({"name": name.upper(), "level": level})
                else:
                    languages.append({"name": lang_info.upper(), "level": ""})
        
        return languages[:3]  # Limit to 3 languages
    
    def _process_technical_for_html(self, raw_technical: str) -> List[Dict[str, str]]:
        """Process technical skills as tools list - following v1JSON.json format"""
        # Extract tools from Technical Skills section - present as simple list
        tools = []
        if raw_technical:
            lines = raw_technical.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('- '):
                    tool = line[2:].strip()
                    # Clean markdown formatting
                    tool = tool.replace('**', '').replace('*', '')
                    if tool.endswith(':'):
                        tool = tool[:-1]
                    tools.append(tool)
        
        # Default tools from source resume if none found
        if not tools:
            tools = [
                "Claude Code Fluency", "Make.com Automation", "Python", "SQL", "Linux", 
                "Google Analytics Certification", "Google Ads Search Certification", 
                "Scrum Master Certified™", "Six Sigma Certified™"
            ]
        
        # Return as single tools list (not categorized) per v1JSON.json spec
        return [{"title": "TOOLS", "skills": ", ".join(tools)}]
    
    def _process_experiences_for_html(self, raw_experience: str) -> List[Dict[str, any]]:
        """Process work experience into structured format"""
        if not raw_experience:
            return []
        
        experiences = []
        # Split by job sections
        job_sections = re.split(r'###\s+', raw_experience)[1:]  # Skip empty first element
        
        for job in job_sections[:3]:  # Limit to top 3 jobs
            lines = job.strip().split('\n')
            if not lines:
                continue
            
            # Extract job title
            title = lines[0].strip()
            title = re.sub(r'\*\*', '', title)  # Remove markdown
            
            # Extract company info and dates
            company = ""
            dates = ""
            achievements = []
            
            for line in lines[1:]:
                line = line.strip()
                if line.startswith('**') or '|' in line:
                    # This is company info
                    company_line = re.sub(r'\*\*', '', line)
                    if '|' in company_line:
                        parts = company_line.split('|')
                        company = parts[0].strip()
                        dates = parts[1].strip() if len(parts) > 1 else ""
                    else:
                        company = company_line
                elif line.startswith('_') and line.endswith('_'):
                    # This is a date line in italic markdown format
                    dates = line
                elif line.startswith('- '):
                    # Achievement bullet point
                    achievement = line[2:].strip()
                    # Clean markdown formatting from achievements
                    achievement = re.sub(r'\*\*', '', achievement)  # Remove bold markdown
                    achievement = re.sub(r'\*', '', achievement)    # Remove italic markdown
                    # Prioritize achievements with metrics
                    if re.search(r'\d+[%KMB$]|\$[\d,]+|\d+\+', achievement):
                        achievements.insert(0, achievement)
                    else:
                        achievements.append(achievement)
            
            # Clean dates - remove markdown italic formatting (underscores)
            dates = re.sub(r'_([^_]+)_', r'\1', dates).strip()  # Remove _text_ patterns
            dates = re.sub(r'_', '', dates).strip()  # Remove any remaining underscores
            
            experiences.append({
                "title": title,
                "company": company,
                "dates": dates,
                "achievements": achievements  # Keep all achievements, will trim in post-processing if needed
            })
        
        return experiences
    
    def _process_professional_development(self, raw_sections: Dict[str, str]) -> List[str]:
        """Extract professional development/training information"""
        dev_items = []
        
        # Look for courses/training section
        for section_key in raw_sections:
            if 'course' in section_key.lower() or 'training' in section_key.lower():
                content = raw_sections[section_key]
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith('- '):
                        dev_items.append(line[2:].strip())
        
        # Default professional development items if none found
        if not dev_items:
            dev_items = [
                "Rob Lennon – Next-Level Prompt Engineering with AI",
                "Leila Gharani - Advanced Excel Functions in Office 365 & Office 2021", 
                "Jon Loomer - GTM/Meta Pixel Custom Event Mastery",
                "Certified Six Sigma™"
            ]
        
        return dev_items[:5]  # Limit to 5 items
    
    def optimize_for_single_page(self, content: StructuredContent) -> StructuredContent:
        """
        Post-process content to ensure it fits on a single page by intelligently trimming
        achievements while preserving the most impactful ones selected by the original prompt
        """
        print("[OPTIMIZE] Optimizing content for single-page layout...")
        
        # Calculate approximate content length for single-page estimation
        total_content_estimate = 0
        
        # Header content (name, tagline, contact)
        total_content_estimate += len(content.name) + len(content.tagline)
        total_content_estimate += sum(len(contact) for contact in content.contact_parts)
        
        # Sidebar content  
        total_content_estimate += len(content.bio)
        for strength in content.strengths:
            total_content_estimate += len(strength.get('title', '')) + len(strength.get('description', ''))
        
        # Main content - experiences are the main variable
        experience_content = 0
        for exp in content.experiences:
            experience_content += len(exp.get('title', '')) + len(exp.get('company', ''))
            for achievement in exp.get('achievements', []):
                experience_content += len(achievement)
        
        total_content_estimate += experience_content
        
        # Dynamic single-page limits and font scaling (adjusted for better page fitting)
        SINGLE_PAGE_LIMIT = 4300  # More conservative limit for trimming
        OPTIMAL_CONTENT_MIN = 3300  # Minimum for large fonts
        OPTIMAL_CONTENT_MAX = 4000  # Maximum for standard fonts
        
        print(f"[OPTIMIZE] Estimated content length: {total_content_estimate} chars")
        print(f"[OPTIMIZE] Single-page target: {SINGLE_PAGE_LIMIT} chars")
        
        # Calculate font scale factor based on content density (more conservative scaling)
        if total_content_estimate <= OPTIMAL_CONTENT_MIN:
            # Low content - scale up fonts moderately
            content.font_scale_factor = 1.2
            print(f"[OPTIMIZE] Low content density - scaling fonts to {content.font_scale_factor}x")
        elif total_content_estimate <= OPTIMAL_CONTENT_MAX:
            # Medium content - scale up fonts slightly
            content.font_scale_factor = 1.1
            print(f"[OPTIMIZE] Medium content density - scaling fonts to {content.font_scale_factor}x")
        elif total_content_estimate <= SINGLE_PAGE_LIMIT:
            # Standard content - use normal fonts
            content.font_scale_factor = 1.0
            print("[OPTIMIZE] Content fits with standard fonts")
        else:
            # Over limit - use smaller fonts and trim content
            content.font_scale_factor = 0.92
            print(f"[OPTIMIZE] High content density - scaling fonts to {content.font_scale_factor}x and trimming")
        
        if total_content_estimate <= SINGLE_PAGE_LIMIT:
            print("[OPTIMIZE] Content fits on single page with dynamic font scaling")
            return content
        
        # Need to trim - reduce achievements per job progressively
        print("[OPTIMIZE] Content exceeds single page, trimming achievements...")
        
        # Try different achievement limits until we fit
        for max_achievements in [4, 3, 2]:
            trimmed_experiences = []
            for exp in content.experiences:
                trimmed_exp = exp.copy()
                trimmed_exp['achievements'] = exp.get('achievements', [])[:max_achievements]
                trimmed_experiences.append(trimmed_exp)
            
            # Recalculate with trimmed content
            trimmed_experience_content = 0
            for exp in trimmed_experiences:
                trimmed_experience_content += len(exp.get('title', '')) + len(exp.get('company', ''))
                for achievement in exp.get('achievements', []):
                    trimmed_experience_content += len(achievement)
            
            trimmed_total = total_content_estimate - experience_content + trimmed_experience_content
            
            print(f"[OPTIMIZE] With {max_achievements} achievements per job: {trimmed_total} chars")
            
            if trimmed_total <= SINGLE_PAGE_LIMIT:
                print(f"[OPTIMIZE] Optimized to {max_achievements} achievements per job")
                content.experiences = trimmed_experiences
                
                # Recalculate font scaling for trimmed content (more conservative)
                if trimmed_total <= OPTIMAL_CONTENT_MIN:
                    content.font_scale_factor = 1.15
                    print(f"[OPTIMIZE] Trimmed content allows larger fonts: {content.font_scale_factor}x")
                elif trimmed_total <= OPTIMAL_CONTENT_MAX:
                    content.font_scale_factor = 1.05
                    print(f"[OPTIMIZE] Trimmed content allows moderate font scaling: {content.font_scale_factor}x")
                else:
                    content.font_scale_factor = 1.0
                    print("[OPTIMIZE] Using standard fonts for trimmed content")
                
                return content
        
        # If still too long, trim to 2 achievements and reduce professional development
        print("[OPTIMIZE] Final trim: 2 achievements + reduced professional development")
        for exp in content.experiences:
            exp['achievements'] = exp.get('achievements', [])[:2]
        content.professional_development = content.professional_development[:3]
        
        return content

def main():
    """Test the HTML content processor"""
    processor = HTMLContentProcessor()
    
    try:
        # Test with the resume markdown file
        structured_content = processor.process_for_html_template("cetola_resume.md")
        
        print("[OK] HTML Content Processing Complete")
        print(f"[DATA] Name: {structured_content.name}")
        print(f"[DATA] Tagline: {structured_content.tagline}")
        print(f"[DATA] Contact Parts: {len(structured_content.contact_parts)}")
        print(f"[DATA] Photo: {structured_content.photo_path or 'None found'}")
        print(f"[DATA] Strengths: {len(structured_content.strengths)}")
        print(f"[DATA] Education: {len(structured_content.education)}")
        print(f"[DATA] Languages: {len(structured_content.languages)}")
        print(f"[DATA] Technical: {len(structured_content.technical)}")
        print(f"[DATA] Experiences: {len(structured_content.experiences)}")
        print(f"[DATA] Professional Development: {len(structured_content.professional_development)}")
        
    except Exception as e:
        print(f"[ERROR] Error processing content: {e}")

if __name__ == "__main__":
    main()