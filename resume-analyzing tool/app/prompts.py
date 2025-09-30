def ats_prompt(resume_text, jd_text):
    return f"""
Compare this resume with the job description. 
Highlight missing skills, keywords, and formatting issues. 
Generate an ATS compatibility score from 0 to 100.

Resume:
{resume_text}

Job Description:
{jd_text}
"""

def resume_rewrite_prompt(resume_text, jd_text):
    return f"""
Rewrite this resume to make it ATS-friendly for this job description.
Keep achievements factual, professional, and role-specific.

Resume:
{resume_text}

Job Description:
{jd_text}
"""

def cover_letter_prompt(resume_text, jd_text, role):
    return f"""
Generate a professional cover letter for this role using the resume and job description.
Keep it concise, impactful, and ATS-friendly.

Resume:
{resume_text}

Job Description:
{jd_text}

Role: {role}
"""
