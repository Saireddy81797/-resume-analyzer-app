import streamlit as st
import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string

# Download stopwords if not already
nltk.download('stopwords')

st.title("📄 Resume Analyzer & Improved ATS Checker")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
jd_text = st.text_area("Paste the Job Description (JD) here:")

if uploaded_file is not None and jd_text:
    # Extract text from PDF
    reader = PyPDF2.PdfReader(uploaded_file)
    resume_text = ""
    for page in reader.pages:
        resume_text += page.extract_text()

    # Initialize tools
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()

    def clean_text(text):
        # Lowercase, remove punctuation
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        words = text.split()
        # Remove stopwords, keep words > 2 letters, stem
        cleaned = [ps.stem(w) for w in words if w not in stop_words and len(w) > 2]
        return set(cleaned)

    resume_cleaned = clean_text(resume_text)
    jd_cleaned = clean_text(jd_text)

    # Compare
    common = resume_cleaned.intersection(jd_cleaned)
    missing = jd_cleaned - resume_cleaned

    # ATS score: percentage of important JD words present
    ats_score = int(len(common) / len(jd_cleaned) * 100)

    # Display
    st.subheader("✅ Improved ATS Score:")
    st.write(f"**{ats_score} %**")

    st.subheader("✔ Matching keywords in resume:")
    st.write(', '.join(common))

    st.subheader("❌ Keywords missing from resume:")
    st.write(', '.join(missing))

else:
    st.info("📌 Please upload your resume PDF and paste JD to start analysis.")
