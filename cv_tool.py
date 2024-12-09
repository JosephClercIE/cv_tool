import streamlit as st
from collections import Counter
from PyPDF2 import PdfReader
from transformers import pipeline

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
st.title("CV Tool : ATS Scorer & Cover Letter Generator")

st.header("Step 1: Upload Job Description and CV")
job_description = st.text_area("Paste the job description here:")

# CV input options
cv_input_type = st.radio(
    "How would you like to input your CV?",
    ("Paste CV as text", "Upload CV as a PDF")
)

candidate_cv = None
if cv_input_type == "Paste CV as text":
    candidate_cv = st.text_area("Paste your CV here:")
elif cv_input_type == "Upload CV as a PDF":
    uploaded_file = st.file_uploader("Upload your CV as a PDF", type=["pdf"])
    if uploaded_file:
        candidate_cv = extract_text_from_pdf(uploaded_file)

if st.button("Analyze CV"):
    if job_description.strip() and candidate_cv:
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
        st.error("Please enter the job description and upload or paste a CV.")

# Cover Letter Generator
st.header("Step 2: Generate a Cover Letter")

if st.button("Generate Cover Letter"):
    if job_description.strip() and candidate_cv:
        # Load a text generation pipeline
        generator = pipeline("text-generation", model="distilgpt2")
        # Generate a cover letter
        cover_letter = generator(
            f"Generate a professional cover letter based on this CV: {candidate_cv} and this job description: {job_description}",
            max_length=300,
            num_return_sequences=1
        )[0]["generated_text"]

        st.subheader("Generated Cover Letter")
        st.text_area("Generated Cover Letter", cover_letter, height=300)
    else:
        st.error("Please provide both a job description and a CV to generate a cover letter.")

