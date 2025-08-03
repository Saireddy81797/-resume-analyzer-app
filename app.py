import streamlit as st
import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('stopwords')

st.title("📄 Resume Analyzer - Skill based ATS Checker")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
jd_text = st.text_area("Paste the Job Description (JD) here:")

# ✅ Define a list of common skills / keywords to check
skills_list = [
    'python', 'java', 'c++', 'c', 'flask', 'django', 'html', 'css', 'javascript', 'sql',
    'machine learning', 'deep learning', 'nlp', 'data analysis', 'pandas', 'numpy', 'tensorflow',
    'keras', 'git', 'github', 'docker', 'linux', 'aws', 'azure', 'react', 'angular', 'cloud',
    'microservices', 'rest api', 'oop', 'agile', 'scrum', 'jira', 'communication', 'teamwork'
]

ps = PorterStemmer()

# Preprocess skills list: stem them
skills_stemmed = set([ps.stem(skill.replace(' ', '')) for skill in skills_list])

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def clean_and_stem(text):
    text = text.lower()
    words = text.split()
    stop_words = set(stopwords.words('english'))
    cleaned = [ps.stem(w) for w in words if w not in stop_words and len(w) > 2]
    return set(cleaned)

if uploaded_file is not None and jd_text:
    resume_text = extract_text_from_pdf(uploaded_file)
    
    # Clean and stem
    resume_words = clean_and_stem(resume_text)
    jd_words = clean_and_stem(jd_text)
    
    # ✅ Focus only on matching skills from skills_list
    resume_skills = resume_words.intersection(skills_stemmed)
    jd_skills = jd_words.intersection(skills_stemmed)
    
    common = resume_skills.intersection(jd_skills)
    missing = jd_skills - resume_skills

    if len(jd_skills) > 0:
        ats_score = int(len(common) / len(jd_skills) * 100)
    else:
        ats_score = 0

    st.subheader("✅ ATS Score (Skill-focused):")
    st.write(f"**{ats_score}%**")

    st.subheader("✔ Skills found in resume:")
    st.write(', '.join(common))

    st.subheader("❌ Skills missing:")
    st.write(', '.join(missing))
else:
    st.info("📌 Upload your resume and paste JD to start analysis.")
