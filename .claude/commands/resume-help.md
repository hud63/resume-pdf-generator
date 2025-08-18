---
description: "Help and examples for the resume rewriter commands"
---

# Resume Rewriter Help

This project contains a custom `/jd` command for generating tailored PDF resumes from job descriptions.

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

## What Happens

1. Claude reads your job description
2. Analyzes it against your source resume and supporting files
3. Follows the detailed instructions in `prompt5.txt`
4. Generates a tailored resume optimized for the specific job
5. Creates a temporary markdown file
6. Converts to professional PDF format using Python
7. Final output: `MarkCetola_JobTitle.pdf`

## Source Files Used

- `cetola_resume.md` - Your base resume content
- `microcredential_curriculums.md` - Your certifications and training
- `Previous_Successful_Cover_Letters.md` - Tone and phrasing patterns
- `prompt5.txt` - Detailed tailoring instructions and constraints

## Model Selection

You can change Claude models anytime with:
```
/model
```

## Features

- ✅ Professional PDF output
- ✅ ATS-optimized formatting
- ✅ Keyword matching from job descriptions  
- ✅ Bold company names in PDF
- ✅ One-page resume constraint
- ✅ Truthful content only (no fabrication)
- ✅ Professional tone and structure
- ✅ Automatic filename generation

## Tips

- Copy the entire job description for best results
- Include clear job title in the job description for better filename generation
- The more detailed the job description, the better the tailoring
- Generated resumes follow your prompt5.txt configuration exactly