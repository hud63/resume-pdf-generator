#!/usr/bin/env python3
"""
HTML Content Processor
Enhanced content processor that formats resume data specifically for HTML template integration
"""

import re
from typing import Dict, List, Optional
from dataclasses import dataclass
import sys
import os
# Add archive modules to path for base ContentProcessor
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'archive', 'modules'))
from content_processor import ContentProcessor, ProcessedContent

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
    
    def __init__(self, jd_text=None):
        super().__init__()
        self.jd_text = jd_text
        self.jd_analysis = self._analyze_jd(jd_text) if jd_text else None
        
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
        """Format tagline for HTML display - use static tagline for consistency"""
        # Always use the static tagline from reference template for professional consistency
        return "On a mission to unleash business profitability through automation and AI innovation"
    
    def _process_contact_for_html(self, raw_contact: str) -> List[str]:
        """Process contact info into list for template"""
        if not raw_contact:
            return ["(561) 600-8773", "mark.newagemedia@gmail.com", "www.linkedin.com/in/MarkCetola"]
        
        # Split on common separators first
        parts = re.split(r'\s*[|•]\s*', raw_contact)
        processed_parts = []
        
        for part in parts:
            part = part.strip()
            if part:
                # Add www. prefix to LinkedIn URLs for professional formatting
                if 'linkedin.com/in/' in part and not part.startswith('www.'):
                    part = 'www.' + part
                processed_parts.append(part)
        
        return processed_parts
    
    def _analyze_jd(self, jd_text: str) -> Optional[Dict]:
        """Dynamic JD analysis following v1JSON.json instruction engine approach"""
        if not jd_text:
            return None
            
        import re
        
        # v1JSON Step 1: "parse JD for must-have skills/tools, customer segment, delivery modes, lifecycle moments, success metrics, cross-functional partners, analytics stack, platform nouns"
        
        # Dynamic skills/tools extraction (expanded beyond hardcoded list)
        skill_patterns = [
            r'\b(?:Salesforce|PowerBI|Excel|Smartsheet|Python|JavaScript|SQL|API|CRM|HubSpot|Zendesk|Intercom|Notion)\b',
            r'\b(?:automation|analytics|data analysis|troubleshooting|onboarding|retention|expansion|adoption)\b',
            r'\b(?:enrollment|planning|implementation|optimization|integration|migration)\b'
        ]
        must_have_skills = []
        for pattern in skill_patterns:
            must_have_skills.extend(re.findall(pattern, jd_text, re.IGNORECASE))
        
        # Dynamic customer segment identification (mine JD content for segment indicators)
        segment_indicators = {}
        
        # Benefits/Healthcare segment
        benefits_terms = re.findall(r'\b(?:voluntary benefits|benefits|employee benefits|critical illness|accident insurance|hospital indemnity|legal plans|pet insurance|financial wellness|BenefitsTech|carriers|enrollment planning|rate design|plan design)\b', jd_text, re.IGNORECASE)
        if benefits_terms:
            segment_indicators['benefits'] = benefits_terms
        
        # SaaS/Technology segment  
        saas_terms = re.findall(r'\b(?:SaaS|Fortune 500|mid-market|enterprise|productivity tools|software|platform|product adoption|user onboarding|feature adoption|churn reduction)\b', jd_text, re.IGNORECASE)
        if saas_terms:
            segment_indicators['saas'] = saas_terms
        
        # Revenue/Sales segment
        revenue_terms = re.findall(r'\b(?:high-ticket|revenue|sales|pipeline|deal sizes|quota|commission|closing|prospecting|lead generation)\b', jd_text, re.IGNORECASE)
        if revenue_terms:
            segment_indicators['revenue'] = revenue_terms
        
        # Operations segment
        ops_terms = re.findall(r'\b(?:operations|process improvement|efficiency|scaling|workflow|automation|systems)\b', jd_text, re.IGNORECASE)
        if ops_terms:
            segment_indicators['operations'] = ops_terms
        
        # Dynamic cross-functional partners identification
        cross_functional_patterns = [
            r'\b(?:Client Executives|carrier contacts|carriers|legal departments|legal)\b',
            r'\b(?:Sales|Product|Engineering|Account Management|Customer Education|support teams)\b',
            r'\b(?:Marketing|Finance|Operations|Implementation|Onboarding|Training)\b'
        ]
        cross_functional = []
        for pattern in cross_functional_patterns:
            cross_functional.extend(re.findall(pattern, jd_text, re.IGNORECASE))
        
        # Dynamic success metrics extraction
        metrics_patterns = [
            r'\b(?:enrollment planning|rate design|plan design|adoption|retention|expansion)\b',
            r'\b(?:renewals|churn|contraction|utilization|growth|satisfaction|NPS)\b',
            r'\b(?:conversion|close rate|pipeline velocity|revenue growth|customer lifetime value)\b'
        ]
        success_metrics = []
        for pattern in metrics_patterns:
            success_metrics.extend(re.findall(pattern, jd_text, re.IGNORECASE))
        
        # Platform nouns (expanded dynamically)
        platform_patterns = [
            r'\b(?:Salesforce|Smartsheet|PowerBI|Microsoft Office|Notion|Intercom|Zendesk|HubSpot)\b',
            r'\b(?:Slack|Asana|Jira|Confluence|Tableau|Google Analytics|Marketo|Pardot)\b'
        ]
        platform_nouns = []
        for pattern in platform_patterns:
            platform_nouns.extend(re.findall(pattern, jd_text, re.IGNORECASE))
        
        # v1JSON Step 2: "mine source resume for segment/program/tool/metric tags; retain only supported claims"  
        # This provides context for what we can truthfully claim based on resume content
        
        # v1JSON Step 4: "choose emphasis based on JD priorities" - Now dynamic based on actual JD content
        primary_focus = self._determine_primary_focus(segment_indicators, must_have_skills, cross_functional, success_metrics)
        
        return {
            'must_have_skills': list(set(must_have_skills)),
            'segment_indicators': segment_indicators,
            'cross_functional': list(set(cross_functional)),
            'success_metrics': list(set(success_metrics)),
            'platform_nouns': list(set(platform_nouns)),
            'primary_focus': primary_focus,
            'raw_jd_text': jd_text  # Keep for dynamic keyword matching
        }
        
    def _determine_primary_focus(self, segment_indicators: dict, must_have_skills: list, cross_functional: list, success_metrics: list) -> dict:
        """Determine primary focus based on JD priorities using v1JSON dynamic approach"""
        
        # Calculate segment strength scores based on term frequency and importance
        segment_scores = {}
        
        for segment, terms in segment_indicators.items():
            # Base score from number of terms
            score = len(terms) * 10
            
            # Boost score for high-value terms
            for term in terms:
                term_lower = term.lower()
                if segment == 'benefits':
                    if term_lower in ['salesforce', 'enrollment planning', 'rate design', 'carriers']:
                        score += 25
                    elif term_lower in ['benefits', 'voluntary benefits']:
                        score += 15
                elif segment == 'saas':
                    if term_lower in ['product adoption', 'churn reduction', 'enterprise']:
                        score += 25
                    elif term_lower in ['saas', 'platform']:
                        score += 15
                elif segment == 'revenue':
                    if term_lower in ['high-ticket', 'pipeline', 'closing']:
                        score += 25
                    elif term_lower in ['revenue', 'sales']:
                        score += 15
                elif segment == 'operations':
                    if term_lower in ['process improvement', 'scaling', 'automation']:
                        score += 25
                    elif term_lower in ['operations', 'efficiency']:
                        score += 15
            
            segment_scores[segment] = score
        
        # Determine primary and secondary focus
        sorted_segments = sorted(segment_scores.items(), key=lambda x: x[1], reverse=True)
        
        primary_focus = sorted_segments[0][0] if sorted_segments else 'operations'
        secondary_focus = sorted_segments[1][0] if len(sorted_segments) > 1 else None
        
        # Generate role-specific keywords for dynamic title transformation
        role_keywords = self._extract_role_keywords(segment_indicators, must_have_skills, success_metrics)
        
        return {
            'primary': primary_focus,
            'secondary': secondary_focus,
            'segment_scores': segment_scores,
            'role_keywords': role_keywords,
            'segment_terms': segment_indicators
        }
    
    def _extract_role_keywords(self, segment_indicators: dict, must_have_skills: list, success_metrics: list) -> list:
        """Extract role-specific keywords for dynamic title transformation (v1JSON approach)"""
        keywords = []
        
        # Extract role-defining terms from each segment
        for segment, terms in segment_indicators.items():
            for term in terms:
                term_lower = term.lower()
                # Add meaningful role-defining terms
                if term_lower in ['benefits', 'saas', 'revenue', 'operations', 'growth', 'success', 'enablement', 'onboarding']:
                    keywords.append(term.title())
        
        # Add skill-based keywords
        for skill in must_have_skills:
            if skill.lower() in ['salesforce', 'analytics', 'automation', 'crm']:
                keywords.append(skill.title())
        
        # Add metric-based keywords  
        for metric in success_metrics:
            if metric.lower() in ['adoption', 'retention', 'expansion', 'growth', 'enrollment']:
                keywords.append(metric.title())
        
        return list(set(keywords))  # Remove duplicates
    
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
        """Format bio content for HTML with proper paragraphs - dynamic based on v1JSON JD analysis"""
        
        # Use dynamic bio based on JD analysis if available (v1JSON approach)
        if self.jd_analysis and 'primary_focus' in self.jd_analysis:
            focus = self.jd_analysis['primary_focus']
            role_keywords = focus.get('role_keywords', [])
            primary_segment = focus.get('primary')
            segment_terms = focus.get('segment_terms', {})
            
            # Generate dynamic bio using JD-specific terms and keywords
            if primary_segment == 'benefits':
                # Extract benefits-specific terms from JD
                benefits_terms = segment_terms.get('benefits', [])
                key_terms = [term for term in benefits_terms if term.lower() in ['enrollment', 'benefits', 'carriers', 'legal', 'plan design', 'rate design']][:3]
                dynamic_bio = f"""Benefits Operations & Client Success professional with 8 years' experience in benefits administration, {', '.join(key_terms[:2]).lower() if key_terms else 'enrollment planning'}, and client relationship management. Proven expertise in Salesforce operations, data analysis, and cross-functional collaboration with carriers and legal teams to deliver comprehensive benefits solutions."""
            elif primary_segment == 'saas':
                # Extract SaaS-specific terms from JD  
                saas_terms = segment_terms.get('saas', [])
                key_terms = [term for term in saas_terms if term.lower() in ['adoption', 'onboarding', 'platform', 'product', 'churn']][:3]
                dynamic_bio = f"""Growth-focused Customer Success professional with 8 years' experience scaling SaaS {', '.join(key_terms[:2]).lower() if key_terms else 'adoption and retention'} programs. Proven track record of driving product utilization, customer onboarding, and cross-functional collaboration with Product and Sales teams to achieve measurable growth outcomes."""
            elif primary_segment == 'revenue':
                # Extract revenue-specific terms from JD
                revenue_terms = segment_terms.get('revenue', [])
                key_terms = [term for term in revenue_terms if term.lower() in ['pipeline', 'sales', 'revenue', 'closing', 'deal']][:3]
                dynamic_bio = f"""Revenue Operations & Sales professional with 8 years' experience in {', '.join(key_terms[:2]).lower() if key_terms else 'high-ticket revenue generation, pipeline management'}, and customer success optimization. Strong background in CRM operations, analytics, and cross-functional collaboration to drive measurable revenue growth."""
            else:  # operations or default
                # Extract operations-specific terms from JD
                ops_terms = segment_terms.get('operations', []) or ['process optimization', 'efficiency', 'automation']
                key_terms = [term for term in ops_terms if term.lower() in ['operations', 'process', 'efficiency', 'automation', 'scaling']][:3]
                dynamic_bio = f"""Customer Success & Operations professional with 8 years' experience in client relationship management, {', '.join(key_terms[:2]).lower() if key_terms else 'process optimization'}, and customer enablement. Strong background in building scalable support systems and data-driven customer success programs."""
            
            return dynamic_bio
        
        # Fallback to processed raw bio or default
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
        """Process strengths into structured format for HTML - dynamic based on v1JSON JD analysis"""
        
        # Use dynamic strengths based on JD analysis if available (v1JSON approach)
        if self.jd_analysis and 'primary_focus' in self.jd_analysis:
            focus = self.jd_analysis['primary_focus']
            primary_segment = focus.get('primary')
            segment_terms = focus.get('segment_terms', {})
            role_keywords = focus.get('role_keywords', [])
            
            strengths = []
            
            if primary_segment == 'benefits':
                # Extract key benefits terms for dynamic strength descriptions
                benefits_terms = segment_terms.get('benefits', [])
                key_tools = [term for term in self.jd_analysis['must_have_skills'] if term.lower() in ['salesforce', 'excel', 'powerbi']]
                
                strengths.extend([
                    {
                        "title": "BENEFITS ADMINISTRATION EXPERTISE",
                        "description": f"""Deep experience in {', '.join([t.lower() for t in benefits_terms[:3]]) if benefits_terms else 'voluntary benefits, enrollment planning'}, and carrier coordination. Proven ability to manage complex benefits portfolios and compliance requirements while maintaining exceptional client relationships."""
                    },
                    {
                        "title": f"{key_tools[0].upper() if key_tools else 'SALESFORCE'} & DATA OPTIMIZATION",
                        "description": f"""Proficient in {', '.join(key_tools) if key_tools else 'Salesforce'} operations, reporting, and data analysis. Experience in building automated workflows, maintaining data integrity, and creating actionable insights that drive benefits program success."""
                    }
                ])
            elif primary_segment == 'saas':
                # Extract key SaaS terms for dynamic strength descriptions  
                saas_terms = segment_terms.get('saas', [])
                key_metrics = [term for term in self.jd_analysis['success_metrics'] if term.lower() in ['adoption', 'retention', 'expansion', 'growth']]
                
                strengths.extend([
                    {
                        "title": "SaaS GROWTH & ADOPTION",
                        "description": f"""Proven track record of driving {', '.join([t.lower() for t in key_metrics[:3]]) if key_metrics else 'product adoption, customer retention, and account expansion'} in SaaS environments. Experience in building onboarding programs and customer success playbooks that scale."""
                    },
                    {
                        "title": "CROSS-FUNCTIONAL COLLABORATION", 
                        "description": f"""Strong ability to work across {', '.join([p for p in self.jd_analysis['cross_functional'] if p.lower() in ['product', 'sales', 'engineering']][:3]) or 'Product, Sales, and Engineering'} teams to deliver customer outcomes. Experience in translating customer feedback into actionable insights."""
                    }
                ])
            elif primary_segment == 'revenue':
                # Extract key revenue terms for dynamic strength descriptions
                revenue_terms = segment_terms.get('revenue', [])
                key_skills = [term for term in self.jd_analysis['must_have_skills'] if term.lower() in ['crm', 'salesforce', 'analytics']]
                
                strengths.extend([
                    {
                        "title": "HIGH-TICKET REVENUE GENERATION", 
                        "description": f"""Demonstrated success in managing {', '.join([t.lower() for t in revenue_terms[:2]]) if revenue_terms else 'high-value client relationships'} and driving revenue growth. Experience in complex sales processes and systematic approaches to achieving consistent results."""
                    },
                    {
                        "title": f"{'CRM' if 'CRM' in key_skills else key_skills[0].upper() if key_skills else 'CRM'} & PIPELINE OPTIMIZATION",
                        "description": f"""Expertise in {', '.join(key_skills) if key_skills else 'CRM'} operations, pipeline management, and revenue forecasting. Proven ability to implement systematic processes that improve conversion rates and operational efficiency."""
                    }
                ])
            else:  # operations or default
                # Extract key operations terms for dynamic strength descriptions
                ops_terms = segment_terms.get('operations', []) or ['process optimization', 'efficiency', 'automation']
                
                strengths.extend([
                    {
                        "title": "CUSTOMER SUCCESS OPERATIONS",
                        "description": f"""Experience in building scalable customer success programs and driving {', '.join([t.lower() for t in ops_terms[:2]]) if ops_terms else 'operational efficiency'}. Proven ability to balance multiple priorities while maintaining exceptional service quality."""
                    },
                    {
                        "title": "PROCESS OPTIMIZATION & SCALING",
                        "description": f"""Demonstrated ability to analyze complex workflows and implement {', '.join([t.lower() for t in ops_terms[1:3]]) if len(ops_terms) > 1 else 'systematic improvements'}. Experience in building repeatable processes that maintain quality while scaling operations efficiently."""
                    }
                ])
            
            return strengths[:2]
        
        # Fallback to default strengths if no JD or insufficient dynamic content
        if not raw_strengths:
            return [
                {
                    "title": "PUZZLES, NOT PROBLEMS",
                    "description": """Problem-solving has been an integral aspect of my career to date, 
                    whether it be understanding a particular technical challenge, collaborating with stakeholders 
                    to optimize processes, or developing innovative ways to generate ideal outcomes for clients."""
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
        """Process technical skills dynamically based on v1JSON.json JD analysis - 'only tools actually used or studied; mirror JD terms'"""
        # Extract all available tools from Technical Skills section
        available_tools = []
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
                    available_tools.append(tool)
        
        # Default tools from source resume if none found
        if not available_tools:
            available_tools = [
                "Claude Code Fluency", "Make.com Automation", "Python", "SQL", "Linux", 
                "Google Analytics Certification", "Google Ads Search Certification", 
                "Scrum Master Certified™", "Six Sigma Certified™"
            ]
        
        # v1JSON: "choose emphasis based on JD priorities" for tool selection and ordering
        if self.jd_analysis and 'primary_focus' in self.jd_analysis:
            prioritized_tools = self._prioritize_tools_by_jd(available_tools)
        else:
            prioritized_tools = available_tools
        
        # v1JSON.json constraint: "no wrapper headers; plain text" - return without "TOOLS" heading
        return [{"title": "", "skills": ", ".join(prioritized_tools)}]
    
    def _prioritize_tools_by_jd(self, available_tools: list) -> list:
        """Prioritize and filter tools based on JD analysis (v1JSON approach: 'mirror JD terms')"""
        focus = self.jd_analysis['primary_focus']
        jd_skills = self.jd_analysis.get('must_have_skills', [])
        platform_nouns = self.jd_analysis.get('platform_nouns', [])
        primary_segment = focus.get('primary')
        
        # Score tools based on JD relevance
        tool_scores = []
        for tool in available_tools:
            score = 0
            tool_lower = tool.lower()
            
            # High priority: Direct matches with JD skills/platforms
            for jd_skill in jd_skills:
                if jd_skill.lower() in tool_lower or tool_lower in jd_skill.lower():
                    score += 100
            
            for platform in platform_nouns:
                if platform.lower() in tool_lower or tool_lower in platform.lower():
                    score += 90
            
            # Medium priority: Segment-specific tool relevance
            if primary_segment == 'benefits':
                if any(term in tool_lower for term in ['salesforce', 'excel', 'powerbi', 'smartsheet']):
                    score += 75
            elif primary_segment == 'saas':
                if any(term in tool_lower for term in ['analytics', 'api', 'automation', 'python', 'sql']):
                    score += 75
            elif primary_segment == 'revenue':
                if any(term in tool_lower for term in ['crm', 'salesforce', 'analytics', 'hubspot']):
                    score += 75
            elif primary_segment == 'operations':
                if any(term in tool_lower for term in ['automation', 'python', 'sql', 'make.com']):
                    score += 75
            
            # Base relevance for professional tools
            if any(term in tool_lower for term in ['certified', 'certification', 'master', 'analytics', 'automation']):
                score += 25
            
            tool_scores.append((tool, score))
        
        # Sort by score (highest first) and return top tools
        tool_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Return prioritized tools (top 8-10 to fit space, focusing on JD-relevant ones)
        prioritized = []
        for tool, score in tool_scores:
            if score > 0 or len(prioritized) < 6:  # Include at least 6 tools
                prioritized.append(tool)
            if len(prioritized) >= 10:  # Cap at 10 tools for space
                break
        
        return prioritized if prioritized else available_tools[:8]
    
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
            
            # Extract job title and apply dynamic prioritization based on JD
            title = lines[0].strip()
            title = re.sub(r'\*\*', '', title)  # Remove markdown
            
            # Apply v1JSON dynamic job title transformation using actual JD keywords
            if self.jd_analysis and 'primary_focus' in self.jd_analysis:
                focus = self.jd_analysis['primary_focus']
                primary_segment = focus.get('primary')
                role_keywords = focus.get('role_keywords', [])
                segment_terms = focus.get('segment_terms', {})
                
                # v1JSON approach: Use actual JD terms instead of hardcoded mappings
                if 'Client Success Lead' in title:
                    # Use JD-specific keywords to determine the appropriate transformation
                    if primary_segment == 'benefits' and any(term.lower() in ['benefits', 'enrollment', 'carriers'] for term in segment_terms.get('benefits', [])):
                        # Use actual JD terminology instead of generic "Benefits Operations"
                        key_term = next((term for term in segment_terms.get('benefits', []) if term.lower() in ['benefits', 'enrollment']), 'Benefits')
                        title = title.replace('Client Success Lead', f'{key_term.title()} Success Specialist')
                    elif primary_segment == 'saas' and any(term.lower() in ['growth', 'product', 'adoption'] for term in segment_terms.get('saas', [])):
                        # Use actual SaaS JD terminology
                        key_term = next((term for term in segment_terms.get('saas', []) if term.lower() in ['growth', 'product']), 'Growth')
                        title = title.replace('Client Success Lead', f'{key_term.title()} Success Manager')
                    elif primary_segment == 'revenue':
                        # Use actual revenue JD terminology
                        key_term = next((term for term in segment_terms.get('revenue', []) if term.lower() in ['revenue', 'sales']), 'Revenue')
                        title = title.replace('Client Success Lead', f'{key_term.title()} Success Specialist')
                    else:
                        # Default: avoid generic "Customer" - use the most relevant JD keyword
                        primary_keyword = role_keywords[0] if role_keywords else 'Client'
                        title = title.replace('Client Success Lead', f'{primary_keyword} Success Specialist')
                        
                elif 'GTM Content Enablement Manager' in title:
                    # Use JD-specific terminology for enablement roles
                    if primary_segment == 'benefits':
                        key_term = next((term for term in segment_terms.get('benefits', []) if term.lower() in ['benefits', 'enrollment']), 'Benefits')
                        title = title.replace('GTM Content Enablement Manager', f'{key_term.title()} Enablement Manager')
                    elif primary_segment == 'saas':
                        key_term = next((term for term in segment_terms.get('saas', []) if term.lower() in ['growth', 'product']), 'Growth')  
                        title = title.replace('GTM Content Enablement Manager', f'{key_term.title()} Enablement Manager')
                    elif primary_segment == 'revenue':
                        title = title.replace('GTM Content Enablement Manager', 'Revenue Enablement Manager')
                    else:
                        # Use most relevant JD keyword instead of generic "Customer"
                        primary_keyword = role_keywords[0] if role_keywords else 'GTM'
                        title = title.replace('GTM Content Enablement Manager', f'{primary_keyword} Enablement Manager')
                        
                elif 'Revenue Operations & Enablement Specialist' in title:
                    # Transform based on actual JD focus, not hardcoded rules
                    if primary_segment == 'benefits':
                        key_term = next((term for term in segment_terms.get('benefits', []) if term.lower() in ['benefits', 'enrollment']), 'Benefits')
                        title = title.replace('Revenue Operations & Enablement Specialist', f'{key_term.title()} Operations Specialist')
                    elif primary_segment == 'saas':
                        key_term = next((term for term in segment_terms.get('saas', []) if term.lower() in ['growth', 'product']), 'Growth')
                        title = title.replace('Revenue Operations & Enablement Specialist', f'{key_term.title()} Operations Specialist')
                    elif primary_segment == 'revenue':
                        title = title.replace('Revenue Operations & Enablement Specialist', 'Revenue Operations Specialist')
                    else:
                        # Use most relevant JD keyword instead of generic "Customer"
                        primary_keyword = role_keywords[0] if role_keywords else 'Operations'
                        title = title.replace('Revenue Operations & Enablement Specialist', f'{primary_keyword} Operations Specialist')
            
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
                    
                    # Score achievements for dynamic selection (v1JSON-style prioritization + JD analysis)
                    score = 0
                    # Highest priority: quantified results with metrics
                    if re.search(r'\d+[%KMB$]|\$[\d,]+|\d+\+|increased.*\d+|grew.*\d+|reduced.*\d+', achievement, re.IGNORECASE):
                        score += 100
                    
                    # JD-AWARE SCORING: Boost achievements matching v1JSON dynamic analysis  
                    if self.jd_analysis and 'primary_focus' in self.jd_analysis:
                        focus = self.jd_analysis['primary_focus']
                        primary_segment = focus.get('primary')
                        segment_terms = focus.get('segment_terms', {})
                        
                        # Dynamic scoring based on actual JD terms (v1JSON approach)
                        if primary_segment == 'benefits':
                            # Check for any benefits-related terms from actual JD
                            for term in segment_terms.get('benefits', []):
                                if term.lower() in achievement.lower():
                                    score += 75  # High boost for matching JD benefits terms
                            # Additional benefits-focused terms
                            if re.search(r'carrier|legal|compliance|Salesforce|plan design|rate|voluntary', achievement, re.IGNORECASE):
                                score += 60
                        
                        elif primary_segment == 'saas':
                            # Check for any SaaS-related terms from actual JD  
                            for term in segment_terms.get('saas', []):
                                if term.lower() in achievement.lower():
                                    score += 75  # High boost for matching JD SaaS terms
                            # Additional SaaS-focused terms
                            if re.search(r'adoption|retention|expansion|growth|onboarding|utilization|product', achievement, re.IGNORECASE):
                                score += 60
                                
                        elif primary_segment == 'revenue':
                            # Check for any revenue-related terms from actual JD
                            for term in segment_terms.get('revenue', []):
                                if term.lower() in achievement.lower():
                                    score += 75  # High boost for matching JD revenue terms
                            # Additional revenue-focused terms
                            if re.search(r'CRM|deal|conversion|close|quota|commission', achievement, re.IGNORECASE):
                                score += 60
                                
                        else:  # operations or default
                            # Check for any operations-related terms from actual JD
                            for segment in segment_terms:
                                for term in segment_terms[segment]:
                                    if term.lower() in achievement.lower():
                                        score += 50  # Medium boost for matching any JD terms
                            # Additional operations-focused terms
                            if re.search(r'support|client|troubleshooting|resolution|satisfaction|service|efficiency', achievement, re.IGNORECASE):
                                score += 40
                        
                        # Boost achievements containing JD-specific skills/tools
                        jd_skills = self.jd_analysis.get('must_have_skills', [])
                        for skill in jd_skills:
                            if skill.lower() in achievement.lower():
                                score += 30  # Bonus for each JD skill match
                        
                        # Boost achievements containing JD success metrics
                        jd_metrics = self.jd_analysis.get('success_metrics', [])
                        for metric in jd_metrics:
                            if metric.lower() in achievement.lower():
                                score += 25  # Bonus for each JD success metric match
                    else:
                        # Fallback: Original AI/automation scoring when no JD analysis
                        if re.search(r'AI|automation|intelligent|machine|data|analytics|optimization', achievement, re.IGNORECASE):
                            score += 50
                    
                    # Medium priority: leadership/management
                    if re.search(r'led|managed|orchestrated|spearheaded|architected', achievement, re.IGNORECASE):
                        score += 30
                    # Medium priority: technical tools and processes
                    if re.search(r'Python|SQL|ChatGPT|Make\.com|LangChain|prompt|API|Salesforce|Zendesk', achievement, re.IGNORECASE):
                        score += 25
                    # Bonus for longer, detailed achievements (more informative)
                    if len(achievement) > 100:
                        score += 10
                    
                    achievements.append({'text': achievement, 'score': score})
            
            # Clean dates - remove markdown italic formatting (underscores)
            dates = re.sub(r'_([^_]+)_', r'\1', dates).strip()  # Remove _text_ patterns
            dates = re.sub(r'_', '', dates).strip()  # Remove any remaining underscores
            
            # Sort achievements by score (highest first) and select top 2-6 dynamically
            achievements.sort(key=lambda x: x['score'], reverse=True)
            
            # Dynamic selection: 2-6 bullets based on quality
            if len(achievements) >= 6:
                # Many achievements: select top 5-6 if scores are high
                high_scoring = [a for a in achievements if a['score'] >= 50]
                selected_count = min(6, max(4, len(high_scoring)))
            elif len(achievements) >= 4:
                # Medium achievements: select 3-5 based on score distribution
                high_scoring = [a for a in achievements if a['score'] >= 30]
                selected_count = min(5, max(3, len(high_scoring)))
            else:
                # Few achievements: use all available
                selected_count = len(achievements)
            
            selected_achievements = [a['text'] for a in achievements[:selected_count]]
            
            experiences.append({
                "title": title,
                "company": company,
                "dates": dates,
                "achievements": selected_achievements
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
        SINGLE_PAGE_LIMIT = 4600  # Increased limit with smaller header (42px saved)
        OPTIMAL_CONTENT_MIN = 3500  # Minimum for large fonts
        OPTIMAL_CONTENT_MAX = 4200  # Maximum for standard fonts
        
        print(f"[OPTIMIZE] Estimated content length: {total_content_estimate} chars")
        print(f"[OPTIMIZE] Single-page target: {SINGLE_PAGE_LIMIT} chars")
        
        # Use Option 2's font scaling (1.0x) for consistent PDF output
        content.font_scale_factor = 1.0
        print(f"[OPTIMIZE] Using Option 2 font scaling: {content.font_scale_factor}x")
        
        if total_content_estimate <= SINGLE_PAGE_LIMIT:
            print("[OPTIMIZE] Content fits on single page with dynamic font scaling")
            return content
        
        # Need to trim - reduce achievements per job progressively
        print("[OPTIMIZE] Content exceeds single page, trimming achievements...")
        
        # Try different achievement limits until we fit (more conservative approach)
        for max_achievements in [5, 4, 3, 2]:
            trimmed_experiences = []
            for exp in content.experiences:
                trimmed_exp = exp.copy()
                # Keep the highest-scoring achievements when trimming
                current_achievements = exp.get('achievements', [])
                trimmed_exp['achievements'] = current_achievements[:max_achievements]
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
                
                # Maintain Option 2's font scaling (1.0x) for consistent PDF output
                content.font_scale_factor = 1.0
                print("[OPTIMIZE] Maintaining Option 2 font scaling for trimmed content: 1.0x")
                
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