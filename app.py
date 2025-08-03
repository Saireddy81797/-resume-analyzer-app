import streamlit as st
import PyPDF2

st.title("📄 Resume Analyzer & ATS Score Checker")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
jd_text = st.text_area("Paste the Job Description (JD) here:")

if uploaded_file is not None and jd_text:
    # Extract text from PDF
    reader = PyPDF2.PdfReader(uploaded_file)
    resume_text = ""
    for page in reader.pages:
        resume_text += page.extract_text()

    # Tokenize words (very simple split)
    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_text.lower().split())

    # Find common & missing keywords
    common = resume_words.intersection(jd_words)
    missing = jd_words - resume_words

    # ATS score (very simple): % of JD words present
    ats_score = int(len(common) / len(jd_words) * 100)

    st.subheader("✅ ATS Score:")
    st.write(f"{ats_score} %")

    st.subheader("✔ Keywords found in your resume:")
    st.write(list(common))

    st.subheader("❌ Keywords missing from your resume:")
    st.write(list(missing))

else:
    st.info("📌 Please upload PDF and paste JD to start analysis.")
