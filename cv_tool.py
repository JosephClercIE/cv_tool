import streamlit as st
from collections import Counter
from PyPDF2 import PdfReader

# Function to extract text from a PDF file
def extract_text_from_pdf(uploaded_file):
    """Extract text from an uploaded PDF file."""
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Keyword extraction function
def extract_keywords(text):
    """Extract keywords by splitting on spaces."""
    words = text.split()
    return Counter(words).most_common()

# Match score calculation
def calculate_match_score(cv_keywords, job_keywords):
    """Calculate match score based on keyword overlap."""
    cv_keywords_set = set(cv_keywords)
    job_keywords_set = set(job_keywords)
    matched_keywords = cv_keywords_set.intersection(job_keywords_set)
    match_score = (len(matched_keywords) / len(job_keywords_set)) * 100 if job_keywords_set else 0
    return match_score, matched_keywords

# Streamlit Interface
st.title("PDF CV ATS Scorer")

st.header("Upload Job Description and CV")
job_description = st.text_area("Paste the job description here:")
uploaded_file = st.file_uploader("Upload your CV as a PDF", type=["pdf"])

if st.button("Analyze"):
    if job_description.strip() and uploaded_file:
        # Extract text from the uploaded PDF
        candidate_cv = extract_text_from_pdf(uploaded_file)
        st.text_area("Extracted CV Text (Preview)", candidate_cv, height=200)

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

        # Grade based on ATS score
        st.subheader("ATS Grade")
        if score >= 80:
            st.success("Your CV is ATS-optimized! Great match!")
        elif score >= 50:
            st.warning("Your CV is moderately optimized. Consider improving the keyword alignment.")
        else:
            st.error("Your CV is not well-optimized. Improve the alignment with job description keywords.")
    else:
        st.error("Please enter the job description and upload a CV.")




