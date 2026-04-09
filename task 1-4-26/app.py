#turn this code to Add PDF Upload Support Hint: pip install PyPDF2 Extract text from PDF and analyze.



import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PyPDF2 import PdfReader
from utils import preprocess_text

st.set_page_config(page_title="Resume Analyser", page_icon=":briefcase:", layout="centered")
st.title("AI Resume Analyser")

resume_file = st.file_uploader("Upload your resume (.txt or .pdf)", type=["txt", "pdf"])

job_description = st.text_area("Paste the job description here")


def extract_text_from_pdf(uploaded_file):
    uploaded_file.seek(0)
    reader = PdfReader(uploaded_file)
    text = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)
    return "\n".join(text)


if resume_file and job_description:
    if resume_file.type == "application/pdf" or resume_file.name.lower().endswith(".pdf"):
        resume_text = extract_text_from_pdf(resume_file)
    else:
        resume_file.seek(0)
        resume_text = resume_file.read().decode("utf-8")
    
    # Preprocess the texts
    processed_resume = preprocess_text(resume_text)
    processed_job_description = preprocess_text(job_description)
    

    # Vectorize the texts using TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([processed_resume , processed_job_description])
    
    # Calculate cosine similarity
    similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    similarity_score = round(similarity_score * 100, 2)

    st.subheader("Similarity Score")

    if similarity_score > 70:
        st.success("Your resume is a good match for the job description!")
    elif similarity_score > 40:
        st.warning("Your resume is a moderate match for the job description. Consider improving it.")
    else:
        st.error("Your resume is a poor match for the job description. Consider revising it significantly.")

    st.subheader("Top keywords")
    feature_names = vectorizer.get_feature_names_out()
    resume_vector = tfidf_matrix[0].toarray()[0]
    top_indices = sorted(range(len(resume_vector)), key=lambda i: resume_vector[i], reverse=True)[:10]
    top_keywords = [feature_names[i] for i in top_indices if resume_vector[i] > 0]
    st.write(", ".join(top_keywords) if top_keywords else "No keywords found.")


