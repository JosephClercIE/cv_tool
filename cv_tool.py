import os
import spacy
import re
from collections import Counter
import streamlit as st

# Ensure the SpaCy model is downloaded at runtime (if not already installed)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Function to extract keywords
def extract_keywords(text):
    """Extract keywords from text using SpaCy."""
    doc = nlp(text)
    keywords = [token.text for token in doc if token.is_alpha and token.pos_ in {"NOUN", "PROPN", "ADJ"}]
    return Counter(keywords).most_common()

# Function to calculate match score
def calculate_match_score(cv_keywords, job_keywords):
    """Calculate match score based on keyword overlap."""
    cv_keywords_set = set(cv_keywords)
    job_keywords_set = set(job_keywords)
    matched_keywords = cv_keywords_set.intersection(job_keywords_set)
    match_score = (len(matched_keywords) / len(job_keywords_set)) * 100 if job_keywords_set else 0
    return match_score, matched_keywords

# Streamlit Interface
st.title("ATS-Optimized CV Tool")

st.header("Upload Job Description and CV")
job_description = st.text_area("Paste the job description here:")
candidate_cv = st.text_area("Paste the candidate CV here:")

if st.button("Analyze"):
    if job_description.strip() and candidate_cv.strip():
        # Extract keywords
        job_keywords = [kw[0] for kw in extract_keywords(job_description)]
        cv_keywords = [kw[0] for kw in extract_keywords(candidate_cv)]

        # Calculate match score
        score, matched_keywords = calculate_match_score(cv_keywords, job_keywords)

        # Display results
        st.subheader("Results")
        st.write(f"**Job Keywords:** {', '.join(job_keywords)}")
        st.write(f"**CV Keywords:** {', '.join(cv_keywords)}")
        st.write(f"**Match Score:** {score:.2f}%")
        st.write(f"**Matched Keywords:** {', '.join(matched_keywords)}")
    else:
        st.error("Please enter both the job description and CV.")

