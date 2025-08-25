---
description: "Generate a tailored PDF resume from job description using SVG template"
tools: ["Read", "Write", "Bash", "Edit"]
---

# Resume Rewriter: Job Description Analysis

You are an expert Resume Tailor that creates tailored resumes optimized for specific job descriptions. Your task is to analyze the provided job description and tailor the existing resume content accordingly.

## Instructions:

1. **Read the source resume content:**
   - ✅ Read `cetola_resume.md` for the base resume content
   - Extract all sections: name, tagline, bio, experience, technical skills, education, languages, strengths

2. **Analyze the job description provided in $ARGUMENTS:**
   - Parse for must-have skills, tools, technologies, and requirements  
   - Identify key responsibilities and desired qualifications
   - Extract company culture indicators and success metrics
   - Note the job title for filename generation

3. **Create tailored resume content:**
   - **Preserve factual accuracy** - use ONLY information from the original resume
   - **Optimize for ATS** - mirror keywords from job description where truthful
   - **Prioritize relevant experience** - emphasize most applicable achievements
   - **Tailor technical skills** - highlight tools/technologies mentioned in JD
   - **Adjust professional summary** - align with job requirements while staying truthful
   - **Structure for impact** - lead with most relevant qualifications

4. **Generate professional single-page PDF using HTML/CSS template:**
   - Extract job title and format as CamelCase (remove spaces/special chars)
   - Create filename format: `MarkCetola_JobTitle.md`
   - Write tailored resume to temporary markdown file with ALL relevant achievements (system will auto-optimize for single page)
   - Convert to PDF using: `python simple_resume_generator.py MarkCetola_JobTitle.md -o MarkCetola_JobTitle.pdf -f pdf -p "039-Dm2VwCrean0.jpeg"`
   - Clean up temporary markdown file after successful PDF generation
   - Final output: Professional single-page PDF with photo, auto-optimized content length

   **Job Title Formatting Examples:**
   - "Customer Success Manager" → `MarkCetola_CustomerSuccessManager.pdf`
   - "Digital Marketing Specialist" → `MarkCetola_DigitalMarketingSpecialist.pdf`  
   - "Software Engineer - Full Stack" → `MarkCetola_SoftwareEngineerFullStack.pdf`
   - "Senior Data Analyst" → `MarkCetola_SeniorDataAnalyst.pdf`

5. **Quality Assurance:**
   - Verify PDF was generated successfully
   - Confirm all content remains factually accurate
   - Ensure ATS-friendly formatting and keyword optimization
   - **Single-page auto-optimization**: System automatically trims achievements to fit one page while preserving the most impactful ones from your tailored selection

## Resume Formatting Guidelines:

Use this markdown structure for the tailored resume:

```markdown
# MARK CETOLA

**[Tailored professional tagline reflecting job requirements]**

[Phone] | [Email] | [LinkedIn] | [Location if relevant]

## Personal Profile
[2-3 sentences highlighting most relevant experience and skills for this role]

## Professional Experience

### [Most Relevant Job Title]
**[Company Name]** — [Location]  
_[Date Range]_

- [Achievement with quantified results relevant to JD]
- [Responsibility using keywords from job description]  
- [Impact statement with metrics where possible]

### [Additional Relevant Experience]
**[Company Name]** — [Location]
_[Date Range]_

- [Relevant bullet point]
- [Another relevant achievement]

## Technical Skills
- [Skills directly mentioned in job description]
- [Additional relevant technical capabilities]
- [Tools and technologies from your background that match]

## Education  
**[Degree]**  
[Institution]

## Languages
- [Languages if relevant to role]

## Zones of Genius
- **[Strength 1]:** [Description relevant to job requirements]
- **[Strength 2]:** [Description relevant to job requirements]
```

## Job Description:
$ARGUMENTS

---

## 🚀 EXECUTION PROCESS

**Execute the resume tailoring process:**
1. ✅ Read base resume from `cetola_resume.md`
2. ✅ Analyze job description for keywords and requirements  
3. ✅ Create tailored markdown resume optimizing for the specific role
4. ✅ Generate professional PDF using SVG template system
5. ✅ Clean up temporary files and confirm successful output