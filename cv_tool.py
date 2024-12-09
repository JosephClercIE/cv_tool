import streamlit as st
from collections import Counter

# Keyword extraction function (simplified)
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
st.title("ATS-Optimized CV Tool (Minimal Version)")

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



