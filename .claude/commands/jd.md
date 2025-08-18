---
description: "Generate a tailored PDF resume from job description"
tools: ["Read", "Write", "Glob", "Bash"]
---

# Resume Rewriter: Job Description Analysis

You are an expert Resume Tailor following the specific instructions in the prompt5.txt file. Your task is to create a tailored resume based on the provided job description.

## ⚠️ CRITICAL: File Configuration Validation

**MUST USE: `prompt5.txt` (NOT prompt.txt)**

Before proceeding, you MUST:
1. Verify you are reading `prompt5.txt` - this is the ONLY correct prompt file
2. Confirm the file contains "T-shaped skills positioning" in the task description
3. Do NOT read or use `prompt.txt` - this is outdated

## Instructions:

1. **First, VALIDATE and read the correct configuration files:**
   - ✅ **REQUIRED**: Read `prompt5.txt` (contains T-shaped skills positioning) 
   - ✅ Read `cetola_resume.md` for the source resume content
   - ✅ Read `microcredential_curriculums.md` for certification details
   - ✅ Read `Previous_Successful_Cover_Letters.md` for tone and phrasing patterns
   - ❌ **DO NOT READ**: `prompt.txt` (outdated file)

2. **Analyze the job description provided in $ARGUMENTS:**
   - Parse for must-have skills/tools, customer segments, delivery modes, success metrics
   - Identify key requirements and company culture
   - Extract job title for filename generation (convert to CamelCase, remove special characters)

3. **✅ CHECKPOINT: Confirm you've read prompt5.txt successfully**
   - Verify the file contains "T-shaped skills positioning" in line 2
   - Confirm you see "strategic_positioning" section in the configuration
   - If NOT, STOP and read the correct file

4. **Generate the tailored resume following prompt5.txt rules:**
   - Use ONLY facts from the source resume
   - Optimize for ATS by mirroring job description keywords
   - Follow the exact resume structure specified in prompt5.txt (includes T-shaped positioning)
   - Apply all constraints (one-page, markdown formatting, bullet format, etc.)
   - Use the voice/tone guidelines from the configuration

5. **Create the output files:**
   - Extract job title from JD and format as CamelCase (e.g., "CRM Acquisition Manager" → "CRMAcquisitionManager")
   - Generate filename using format: `MarkCetola_JobTitle.md` (remove spaces, special characters, use CamelCase)
   - Save the tailored resume as a temporary markdown file
   - Convert to PDF using: `python simple_pdf_converter.py MarkCetola_JobTitle.md`
   - Delete the temporary markdown file after PDF creation
   - Final output: `MarkCetola_JobTitle.pdf`
   
   **Job Title Formatting Examples:**
   - "Customer Success Manager" → `MarkCetola_CustomerSuccessManager.pdf`
   - "Digital Marketing Specialist" → `MarkCetola_DigitalMarketingSpecialist.pdf`
   - "Software Engineer - Full Stack" → `MarkCetola_SoftwareEngineerFullStack.pdf`

## Job Description:
$ARGUMENTS

---

## 🔍 EXECUTION REMINDER

**CRITICAL**: You MUST use `prompt5.txt` (with T-shaped skills positioning) - NOT `prompt.txt`

**Now execute the resume tailoring process following the prompt5.txt instructions exactly. Remember to:**
- ✅ Confirm you're using the correct prompt file (prompt5.txt)
- ✅ Include T-shaped skills positioning section in the resume
- ✅ Create the PDF file as the final output 
- ✅ Clean up the temporary markdown file