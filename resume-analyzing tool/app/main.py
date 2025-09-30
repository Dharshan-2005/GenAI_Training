import streamlit as st
from utils import extract_text_from_pdf, extract_text_from_docx
from prompts import ats_prompt, resume_rewrite_prompt, cover_letter_prompt
from ats_logger import log_ats_score
import re
from langchain.llms.ollama import Ollama

# -------------------- Load LLaMA 3 via Ollama --------------------
# Ollama automatically runs local models (no API key needed)
llama_llm = Ollama(model="llama3")

# -------------------- Streamlit App UI --------------------
st.set_page_config(page_title="Career Copilot", layout="wide")
st.title("Career Copilot – AI Resume Tool")
st.write("Upload your resume and job description to get an ATS score, optimized resume, and cover letter.")

# --- File Uploads ---
resume_file = st.file_uploader("Upload your Resume (PDF/DOCX)", type=["pdf", "docx"])
jd_file = st.file_uploader("Upload Job Description (PDF/DOCX)", type=["pdf", "docx"])
role = st.text_input("Target Role")
optimize = st.radio("Optimize Resume for this Job?", ["Yes", "No"])

# -------------------- LLaMA 3 Call Function --------------------
def call_llama(prompt):
    return llama_llm(prompt)

# -------------------- Main Workflow --------------------
if st.button("Submit"):
    if not (resume_file and jd_file and role):
        st.warning("Please upload all files and enter a target role.")
    else:
        # --- Extract Text from Files ---
        if resume_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(resume_file)
        else:
            resume_text = extract_text_from_docx(resume_file)

        if jd_file.type == "application/pdf":
            jd_text = extract_text_from_pdf(jd_file)
        else:
            jd_text = extract_text_from_docx(jd_file)

        # --- 1. ATS Score ---
        with st.spinner("Generating ATS score..."):
            ats_result = call_llama(ats_prompt(resume_text, jd_text))
        st.subheader("ATS Score & Feedback")
        st.text(ats_result)

        # Extract numeric ATS score for logging
        ats_numeric = re.search(r"(\d+)", ats_result)
        if ats_numeric:
            ats_score = int(ats_numeric.group(1))
            log_ats_score(resume_file.name, ats_score)
            st.subheader("ATS Record Stored")
            st.text(f"Resume: {resume_file.name} | Score: {ats_score} | Remarks: {'Good' if ats_score >= 70 else 'Bad'}")

        # --- 2. Resume Optimization + Cover Letter ---
        if optimize == "Yes":
            with st.spinner("Optimizing resume..."):
                optimized_resume = call_llama(resume_rewrite_prompt(resume_text, jd_text))
            st.subheader("Optimized Resume")
            st.text(optimized_resume)

            with st.spinner("Generating cover letter..."):
                cover_letter = call_llama(cover_letter_prompt(resume_text, jd_text, role))
            st.subheader("Cover Letter")
            st.text(cover_letter)
