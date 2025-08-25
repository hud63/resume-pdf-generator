#!/usr/bin/env python3
"""
Content Processor Module
Processes resume markdown content and optimizes it for SVG template placement
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import markdown

@dataclass
class ProcessedContent:
    """Represents processed content ready for SVG placement"""
    region_type: str
    content: str
    char_count: int
    truncated: bool

class ContentProcessor:
    """
    Processes resume markdown content according to the mapping specifications
    from the process document
    """
    
    def __init__(self):
        # Content mapping rules optimized based on testing
        self.region_specs = {
            'name': {'max_chars': 25, 'priority': 1},
            'tagline': {'max_chars': 85, 'priority': 2},  # Increased slightly
            'contact': {'max_chars': 90, 'priority': 3},
            'bio': {'max_chars': 350, 'priority': 4},     # Reduced for better fitting
            'experience': {'max_chars': 500, 'priority': 5},
            'strengths': {'max_chars': 200, 'priority': 6},
            'technical': {'max_chars': 150, 'priority': 7},
            'education': {'max_chars': 100, 'priority': 8},
            'languages': {'max_chars': 50, 'priority': 9} # Increased slightly
        }
        
    def parse_markdown_resume(self, md_file_path: str) -> Dict[str, str]:
        """Parse markdown resume file and extract sections"""
        try:
            with open(md_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            return self._extract_sections(content)
            
        except Exception as e:
            print(f"Error reading markdown file: {e}")
            return {}
    
    def _extract_sections(self, content: str) -> Dict[str, str]:
        """Extract resume sections from markdown content"""
        sections = {}
        
        # Extract name (first # heading)
        name_match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
        if name_match:
            sections['raw_name'] = name_match.group(1).strip()
            
        # Extract tagline (first **bold** text after name)
        tagline_match = re.search(r'\*\*(.+?)\*\*', content)
        if tagline_match:
            sections['raw_tagline'] = tagline_match.group(1).strip()
            
        # Extract contact info (look for email/phone/linkedin)
        contact_info = []
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', content)
        phone_match = re.search(r'\(\d{3}\)\s*\d{3}-\d{4}', content)
        linkedin_match = re.search(r'linkedin\.com/in/[\w-]+', content)
        
        if phone_match:
            contact_info.append(phone_match.group(0))
        if email_match:
            contact_info.append(email_match.group(0))
        if linkedin_match:
            contact_info.append(linkedin_match.group(0))
            
        sections['raw_contact'] = ' | '.join(contact_info)
        
        # Extract Personal Profile/Bio
        bio_match = re.search(r'## Personal Profile\s*\n(.*?)(?=##|$)', content, re.DOTALL)
        if not bio_match:
            bio_match = re.search(r'## Profile\s*\n(.*?)(?=##|$)', content, re.DOTALL)
        if bio_match:
            sections['raw_bio'] = bio_match.group(1).strip()
            
        # Extract Professional Experience  
        exp_start = content.find('## Professional Experience')
        if exp_start != -1:
            # Find the next ## section (not ###)
            next_section = re.search(r'\n## [^#]', content[exp_start + 25:])
            if next_section:
                exp_end = exp_start + 25 + next_section.start()
                exp_content = content[exp_start + 25:exp_end].strip()
            else:
                exp_content = content[exp_start + 25:].strip()
            sections['raw_experience'] = exp_content
            
        # Extract Technical Skills
        tech_match = re.search(r'## Technical Skills\s*\n(.*?)(?=##|$)', content, re.DOTALL)
        if tech_match:
            sections['raw_technical'] = tech_match.group(1).strip()
            
        # Extract Education
        edu_match = re.search(r'## Education\s*\n(.*?)(?=##|$)', content, re.DOTALL)
        if edu_match:
            sections['raw_education'] = edu_match.group(1).strip()
            
        # Extract Languages
        lang_match = re.search(r'## Languages\s*\n(.*?)(?=##|$)', content, re.DOTALL)
        if lang_match:
            sections['raw_languages'] = lang_match.group(1).strip()
            
        # Extract Zones of Genius for strengths
        zones_match = re.search(r'## Zones of Genius\s*\n(.*?)(?=##|$)', content, re.DOTALL)
        if zones_match:
            sections['raw_strengths'] = zones_match.group(1).strip()
            
        return sections
    
    def process_content_for_regions(self, raw_sections: Dict[str, str]) -> Dict[str, ProcessedContent]:
        """Process raw sections into optimized content for each region"""
        processed = {}
        
        # Process each section according to specifications
        if 'raw_name' in raw_sections:
            processed['name'] = self._process_name(raw_sections['raw_name'])
            
        if 'raw_tagline' in raw_sections:
            processed['tagline'] = self._process_tagline(raw_sections['raw_tagline'])
            
        if 'raw_contact' in raw_sections:
            processed['contact'] = self._process_contact(raw_sections['raw_contact'])
            
        if 'raw_bio' in raw_sections:
            processed['bio'] = self._process_bio(raw_sections['raw_bio'])
            
        if 'raw_experience' in raw_sections:
            processed.update(self._process_experience(raw_sections['raw_experience']))
            
        if 'raw_technical' in raw_sections:
            processed['technical'] = self._process_technical(raw_sections['raw_technical'])
            
        if 'raw_education' in raw_sections:
            processed['education'] = self._process_education(raw_sections['raw_education'])
            
        if 'raw_languages' in raw_sections:
            processed['languages'] = self._process_languages(raw_sections['raw_languages'])
            
        if 'raw_strengths' in raw_sections:
            processed['strengths'] = self._process_strengths(raw_sections['raw_strengths'])
            
        return processed
    
    def _process_name(self, raw_name: str) -> ProcessedContent:
        """Process name - remove markdown, ensure character limit"""
        clean_name = re.sub(r'\*\*', '', raw_name).strip()
        
        if len(clean_name) > self.region_specs['name']['max_chars']:
            # Try to abbreviate middle name or use initials
            parts = clean_name.split()
            if len(parts) > 2:
                clean_name = f"{parts[0]} {parts[-1]}"
                
        truncated = len(clean_name) > self.region_specs['name']['max_chars']
        if truncated:
            clean_name = clean_name[:self.region_specs['name']['max_chars']]
            
        return ProcessedContent('name', clean_name, len(clean_name), truncated)
    
    def _process_tagline(self, raw_tagline: str) -> ProcessedContent:
        """Process professional tagline"""
        # Remove markdown formatting
        clean_tagline = re.sub(r'\*\*', '', raw_tagline).strip()
        
        # Ensure it starts with capital and ends with period for consistency
        if not clean_tagline.endswith('.') and not clean_tagline.endswith('!'):
            clean_tagline += '.'
            
        truncated = len(clean_tagline) > self.region_specs['tagline']['max_chars']
        if truncated:
            # Truncate at word boundary
            words = clean_tagline.split()
            result = ""
            for word in words:
                if len(result + word) + 1 <= self.region_specs['tagline']['max_chars'] - 3:
                    result += word + " "
                else:
                    break
            clean_tagline = result.strip() + "..."
            
        return ProcessedContent('tagline', clean_tagline, len(clean_tagline), truncated)
    
    def _process_contact(self, raw_contact: str) -> ProcessedContent:
        """Process contact information"""
        # Clean up URLs
        clean_contact = raw_contact.replace('https://', '').replace('http://', '')
        clean_contact = clean_contact.replace('www.', '')
        
        truncated = len(clean_contact) > self.region_specs['contact']['max_chars']
        if truncated:
            # Prioritize phone and email over LinkedIn
            parts = clean_contact.split(' | ')
            essential = []
            for part in parts:
                if '@' in part or '(' in part:  # email or phone
                    essential.append(part)
                    
            if essential:
                clean_contact = ' | '.join(essential)
                
        return ProcessedContent('contact', clean_contact, len(clean_contact), truncated)
    
    def _process_bio(self, raw_bio: str) -> ProcessedContent:
        """Process bio/personal profile section"""
        # Remove markdown and clean up
        clean_bio = re.sub(r'\*\*', '', raw_bio)
        clean_bio = re.sub(r'\n+', ' ', clean_bio).strip()
        
        # Extract first 2-3 sentences if too long
        sentences = re.split(r'[.!?]+', clean_bio)
        if len(sentences) > 3:
            sentences = sentences[:3]
            
        result = '. '.join(s.strip() for s in sentences if s.strip()) + '.'
        
        truncated = len(result) > self.region_specs['bio']['max_chars']
        if truncated:
            # Keep first 2 sentences
            sentences = sentences[:2]
            result = '. '.join(s.strip() for s in sentences if s.strip()) + '.'
            
        return ProcessedContent('bio', result, len(result), truncated)
    
    def _process_experience(self, raw_experience: str) -> Dict[str, ProcessedContent]:
        """Process professional experience - return top 3 jobs"""
        # Extract job sections
        job_sections = re.split(r'###\s+', raw_experience)[1:]  # Skip empty first element
        
        processed_jobs = {}
        
        for i, job in enumerate(job_sections[:3]):  # Top 3 jobs
            lines = job.strip().split('\n')
            if not lines:
                continue
                
            # Extract job title and company info
            title_line = lines[0].strip()
            company_info = ""
            bullets = []
            
            for line in lines[1:]:
                line = line.strip()
                if line.startswith('**') or '|' in line:
                    company_info = line
                elif line.startswith('- '):
                    bullet = line[2:].strip()
                    # Prioritize bullets with numbers/metrics
                    if re.search(r'\d+[%KMB]|\$[\d,]+|\d+\+', bullet):
                        bullets.insert(0, bullet)
                    else:
                        bullets.append(bullet)
            
            # Process job title
            clean_title = re.sub(r'\*\*', '', title_line)
            if len(clean_title) > 40:
                clean_title = clean_title[:37] + "..."
                
            # Process bullets (max 3-4, ~100 chars each)
            processed_bullets = []
            for bullet in bullets[:4]:
                if len(bullet) > 100:
                    # Truncate at word boundary
                    words = bullet.split()
                    truncated = ""
                    for word in words:
                        if len(truncated + word) + 1 <= 97:
                            truncated += word + " "
                        else:
                            break
                    bullet = truncated.strip() + "..."
                processed_bullets.append(bullet)
                
            # Combine job content
            job_content = f"{clean_title}\n{company_info}\n" + "\n".join(f"• {bullet}" for bullet in processed_bullets)
            
            processed_jobs[f'experience_{i+1}'] = ProcessedContent(
                'experience', 
                job_content, 
                len(job_content), 
                len(job_content) > 500
            )
            
        return processed_jobs
    
    def _process_technical(self, raw_technical: str) -> ProcessedContent:
        """Process technical skills section"""
        # Extract skill items
        skills = []
        lines = raw_technical.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('- '):
                skill = line[2:].strip()
                skills.append(skill)
                
        # Group similar skills and limit to top skills
        top_skills = skills[:8]  # Limit to most important
        result = ', '.join(top_skills)
        
        truncated = len(result) > self.region_specs['technical']['max_chars']
        if truncated:
            # Keep reducing skills until it fits
            while len(result) > self.region_specs['technical']['max_chars'] and top_skills:
                top_skills.pop()
                result = ', '.join(top_skills)
                
        return ProcessedContent('technical', result, len(result), truncated)
    
    def _process_education(self, raw_education: str) -> ProcessedContent:
        """Process education section"""
        # Extract degree and university
        lines = raw_education.split('\n')
        degree = ""
        university = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith('**') and line.endswith('**'):
                degree = line[2:-2]
            elif line and not line.startswith('_'):
                university = line
                
        result = f"{degree}\n{university}" if degree and university else degree or university
        
        truncated = len(result) > self.region_specs['education']['max_chars']
        if truncated:
            # Abbreviate degree if needed
            result = result[:self.region_specs['education']['max_chars']-3] + "..."
            
        return ProcessedContent('education', result, len(result), truncated)
    
    def _process_languages(self, raw_languages: str) -> ProcessedContent:
        """Process languages section"""
        # Extract language entries
        languages = []
        lines = raw_languages.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('- '):
                lang_info = line[2:].strip()
                languages.append(lang_info)
                
        # Limit to top 2 languages
        result = '\n'.join(languages[:2])
        
        return ProcessedContent('languages', result, len(result), False)
    
    def _process_strengths(self, raw_strengths: str) -> ProcessedContent:
        """Process strengths/zones of genius section"""
        # Extract first 2-3 strength items
        strength_items = []
        lines = raw_strengths.split('\n')
        current_strength = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith('- **'):
                if current_strength:
                    strength_items.append(current_strength)
                # Extract strength title
                title_match = re.search(r'\*\*(.+?)\*\*', line)
                if title_match:
                    current_strength = title_match.group(1)
            elif line and current_strength:
                # Add description
                clean_desc = line[:60] + "..." if len(line) > 60 else line
                current_strength += f": {clean_desc}"
                strength_items.append(current_strength)
                current_strength = ""
                
        if current_strength:
            strength_items.append(current_strength)
            
        # Take top 2 strengths
        result = '\n\n'.join(strength_items[:2])
        
        truncated = len(result) > self.region_specs['strengths']['max_chars']
        if truncated:
            result = strength_items[0] if strength_items else ""
            
        return ProcessedContent('strengths', result, len(result), truncated)

def main():
    """Test the content processor"""
    processor = ContentProcessor()
    
    # Test with the resume markdown file
    raw_sections = processor.parse_markdown_resume("cetola_resume.md")
    print(f"📝 Extracted {len(raw_sections)} sections from markdown")
    
    processed = processor.process_content_for_regions(raw_sections)
    print(f"✅ Processed {len(processed)} content regions:")
    
    for region_type, content in processed.items():
        status = "⚠️ TRUNCATED" if content.truncated else "✅"
        print(f"  - {region_type}: {content.char_count} chars {status}")
        print(f"    {content.content[:100]}...")
        print()

if __name__ == "__main__":
    main()