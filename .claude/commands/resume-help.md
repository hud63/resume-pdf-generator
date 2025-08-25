---
description: "Help and examples for the resume rewriter commands"
---

# Resume Rewriter Help

This project contains a custom `/jd` command for generating tailored PDF resumes from job descriptions using the SVG-to-PDF system.

## Usage

### Basic Command
```
/jd [paste your job description here]
```

### Examples

**Software Engineer Position:**
```
/jd Software Engineer at TechCorp
We're looking for a Python developer with 3+ years experience in machine learning and data analysis. Must have experience with AWS, Docker, and SQL databases. Strong communication skills required for cross-functional collaboration.
```

**Marketing Role:**
```
/jd Digital Marketing Manager at StartupCo
Seeking experienced marketer with expertise in social media, content creation, and analytics tools like Google Analytics and HubSpot. Experience with automation tools and A/B testing preferred.
```

**Data Analysis Role:**
```
/jd Senior Data Analyst at FinTech Company
Looking for experienced analyst with SQL, Python, and business intelligence tools. Must have experience with data visualization, statistical analysis, and stakeholder communication. Financial services background preferred.
```

## What Happens

1. Claude reads your job description
2. Analyzes it against your base resume (`cetola_resume.md`)
3. Identifies key requirements, skills, and keywords from the JD
4. Tailors the resume content while maintaining factual accuracy
5. Creates a temporary markdown file with optimized content
6. Generates professional PDF using SVG template system (`svg_pdf_generator.py`)
7. Cleans up temporary files
8. Final output: `MarkCetola_JobTitle.pdf` with professional SVG styling

## Source Files Used

- `cetola_resume.md` - Your base resume content (source of all facts)
- `12.svg` - Professional SVG template for layout and styling
- `svg_pdf_generator.py` - Modern PDF generation system
- Built-in resume tailoring intelligence and ATS optimization

## System Features

- ✅ **Professional SVG Template** - Consistent visual design with two-column layout
- ✅ **Intelligent Content Optimization** - Auto-adjusts text to fit regions perfectly
- ✅ **ATS-Optimized Formatting** - Keyword matching and proper structure
- ✅ **Factual Accuracy** - Only uses information from your actual resume
- ✅ **One-Page Constraint** - SVG template enforces professional length
- ✅ **Automatic Filename Generation** - Smart job title extraction and formatting
- ✅ **Professional Typography** - High-quality PDF output with proper fonts
- ✅ **Content Prioritization** - Emphasizes most relevant experience first

## Model Selection

You can change Claude models anytime with:
```
/model
```

## Tips for Best Results

- **Include full job description** - More detail = better tailoring
- **Clear job title** - Helps with automatic filename generation  
- **Specific requirements** - Technical skills, tools, years of experience
- **Company context** - Size, industry, culture indicators for better alignment
- **Key responsibilities** - Helps prioritize relevant experience from your background

## Output Quality

The updated system provides:
- **Character limits optimized** based on SVG template constraints
- **Content truncation** at word boundaries for readability
- **Professional formatting** with proper spacing and typography
- **Clean PDF output** suitable for ATS systems and human reviewers

## Technical Details

- Uses modern `svg_pdf_generator.py` system (replaces legacy converters)
- Content processing optimized for template regions (tagline: 85 chars, bio: 350 chars)
- Graceful handling of content that exceeds region limits
- Professional error handling with fallback options