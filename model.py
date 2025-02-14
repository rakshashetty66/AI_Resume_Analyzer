import pdfplumber
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

# Extract text from resume (supports PDFs)
def process_resume(file):
    with pdfplumber.open(file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text.lower()

# Extract skills from text
def extract_skills(text):
    doc = nlp(text)
    skills = set()
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"]:  # Extract nouns (potential skills)
            skills.add(token.text.lower())
    return skills

# Match resume with job description
def match_resume_with_job(resume_text, job_description):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    # Calculate similarity score
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_description])
    similarity_score = cosine_similarity(vectors[0], vectors[1])[0][0] * 100

    # Identify missing skills
    missing_skills = job_skills - resume_skills

    return round(similarity_score, 2), list(missing_skills)
