# Dynamic Resume Generation System

A fully functional, AI-powered resume tailoring system that generates job-specific PDF resumes using advanced v1JSON dynamic analysis. The system automatically adapts content, job titles, achievements, and emphasis based on job description requirements while maintaining single-page optimization.

## Core System

### Main Components
- `generate_dynamic_resume.py` - Core dynamic resume generation with automatic PDF output
- `modules/html_content_processor.py` - Advanced v1JSON content processing and JD analysis
- `modules/html_pdf_generator.py` - WeasyPrint PDF generation with Chrome fallback
- `templates/resume_template.html` - HTML template with Option 2 font scaling (1.0x)
- `MarkCetola_CSM.md` - Source resume content (Mark Cetola)
- `v1JSON.json` - Complete systematic job description analysis instructions

### Claude Code Integration
- `/jd` command - **Fully functional** dynamic resume generation
- Automatic PDF generation with intelligent fallback system
- Located in `.claude/commands/jd.md`

## Usage

### Via Claude Code Command (Primary)
```
/jd "Job description text here..."
```
Automatically generates `MarkCetola_XXX.pdf` where XXX is job title abbreviation.

### Direct Python Usage
```python
from generate_dynamic_resume import generate_dynamic_resume

generate_dynamic_resume("Job description text", "output_filename.pdf")
```

## How It Works

### v1JSON Dynamic Analysis Engine
The system implements a complete v1JSON methodology that:

1. **Dynamic JD Parsing** - Extracts must-have skills, customer segments, success metrics, cross-functional requirements, and platform technologies
2. **Intelligent Content Adaptation** - Uses "action+scope+what+how+impact" formula for all achievements
3. **Contextual Keyword Integration** - Naturally mirrors JD terminology throughout all sections
4. **Single-Page Optimization** - Maintains perfect single-page layout with Option 2 font scaling (1.0x)
5. **Automatic PDF Generation** - Chrome headless with WeasyPrint fallback for reliable output

### Advanced Dynamic Transformations
- **Job Title Intelligence**: "SaaS Success Specialist" vs "Publisher Success Manager" based on JD context
- **Bio Personalization**: Adapts professional summary to match JD requirements and industry
- **Dynamic Strengths**: Generates contextual strengths based on JD priorities (not static)
- **Achievement Scoring**: AI-powered selection of most relevant achievements per JD
- **Tools Prioritization**: Intelligent filtering and ordering of technical skills
- **Content Density Management**: Automatic trimming while preserving high-impact content

## System Status - FULLY OPERATIONAL ✅

### Complete Features
- **✅ v1JSON Dynamic Analysis** - Full implementation with intelligent JD parsing
- **✅ Automatic PDF Generation** - Chrome headless with WeasyPrint fallback
- **✅ Dynamic Job Titles** - Context-aware title transformation per industry/role
- **✅ Content Personalization** - Bio, strengths, and achievements tailored per JD
- **✅ Single-Page Optimization** - Perfect formatting with Option 2 font scaling (1.0x)
- **✅ Achievement Intelligence** - JD-specific scoring and selection system
- **✅ Tools Prioritization** - Dynamic filtering based on JD requirements
- **✅ Claude Code Integration** - `/jd` command ready for production use

### Recent Enhancements
- Fixed automatic PDF generation (no manual steps required)
- Implemented Option 2 font scaling as default for consistent output
- Enhanced v1JSON processing for superior content adaptation
- Added robust fallback system for PDF generation across environments

## File Structure

```
├── generate_dynamic_resume.py          # Core system with automatic PDF generation
├── MarkCetola_CSM.md                   # Source resume content (Mark Cetola)
├── v1JSON.json                         # Complete v1JSON analysis instructions  
├── 039-Dm2VwCrean0.jpeg               # Profile photo
├── modules/
│   ├── html_content_processor.py       # Advanced v1JSON processing engine
│   └── html_pdf_generator.py           # WeasyPrint + Chrome PDF generation
├── templates/
│   └── resume_template.html            # Production template with Option 2 scaling
├── .claude/commands/
│   └── jd.md                           # Fully functional /jd command
├── requirements.txt                    # All dependencies
├── archive/                            # Legacy files (unused)
└── README.md                           # This documentation
```

## Dependencies

```bash
pip install -r requirements.txt
```

**Core Dependencies:**
- **Jinja2** - HTML templating engine
- **WeasyPrint** - Primary PDF generation (with Windows fallback)
- **Chrome/Chromium** - Fallback PDF generation (headless mode)

## Production Examples

Recent successful outputs demonstrate full v1JSON functionality:

### Customer Success Roles
- **Orum Senior CSM**: Dynamic title → "SaaS Success Specialist" with conversation platform focus
- **Agiloft Mid-Market CSM**: Emphasis on contract lifecycle management and enterprise accounts
- **GumGum Publisher Success**: Ad tech terminology with publisher partnership focus

### Key Features Demonstrated
- **Dynamic Job Titles**: Each JD produces contextually appropriate role positioning
- **Industry Adaptation**: SaaS vs Ad Tech vs CLM terminology automatically applied
- **Achievement Selection**: Most relevant bullets highlighted per JD requirements
- **Tool Prioritization**: Salesforce, Zendesk, analytics tools ordered by JD relevance
- **Single-Page Perfection**: All outputs maintain optimal layout with Option 2 scaling

## Status: Production Ready ✅

The `/jd` command is fully operational for end-to-end resume generation with automatic PDF output.

---

*System Status: Fully Operational | Last Updated: August 27, 2025*