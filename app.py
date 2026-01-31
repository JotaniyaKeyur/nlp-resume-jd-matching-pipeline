from fastapi import FastAPI, HTTPException
from fastapi import UploadFile, File
import os
import shutil

from utils.doc_reader import DocLoader
from nlp.preprocessing import TextPreprocessor
from nlp.extraction import InfoExtractor
from nlp.matching import SkillMatcher, ExperienceMatcher
from nlp.report import FitReportGenerator
from nlp.feedback import FeedbackGenerator

app = FastAPI(title="Resume Analyzer API")

doc_loader = DocLoader()
preprocessor = TextPreprocessor()
extractor = InfoExtractor()
skill_matcher = SkillMatcher()
experience_matcher = ExperienceMatcher()
report_generator = FitReportGenerator()
feedback_generator = FeedbackGenerator()

RESUME_TEXT = None
JD_TEXT = None

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/upload/resume")
def upload_resume(file: UploadFile = File(...)):
    global RESUME_TEXT

    # validation
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid resume format. Only PDF files are allowed.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        RESUME_TEXT = doc_loader.extract_resume_text(file_path)

        return {
            "message": "Resume uploaded & processed successfully",
            "filename": file.filename
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload/jd")
def upload_jd(file: UploadFile = File(...)):
    global JD_TEXT

    # validation
    if not file.filename.lower().endswith(".txt"):
        raise HTTPException(status_code=400, detail="Invalid JD format. Only TXT files are allowed.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        JD_TEXT = doc_loader.extract_jd_text(file_path)

        return {
            "message": "JD uploaded & processed successfully",
            "filename": file.filename
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/preprocess/resume")
def preprocess_resume():
    if not RESUME_TEXT:
        raise HTTPException(status_code=400, detail="resume not loaded")

    clean_text = preprocessor.clean_text(RESUME_TEXT)
    sen_tokens = preprocessor.tokenize_sentences(clean_text)
    tokens = preprocessor.tokenize_words(clean_text)
    lemmas = preprocessor.lemmatize_tokens(tokens)
    pos_tags = preprocessor.get_pos_tags(clean_text)

    return {
        "clean_text": clean_text,
        "sen_tokens": sen_tokens,
        "tokens": tokens,
        "lemmas": lemmas,
        "pos_tags": pos_tags
        }

@app.post("/preprocess/jd")
def preprocess_jd():
    if not JD_TEXT:
        raise HTTPException(status_code=400, detail="jd not loaded")

    clean_text = preprocessor.clean_text(JD_TEXT)
    sen_tokens = preprocessor.tokenize_sentences(clean_text)
    tokens = preprocessor.tokenize_words(clean_text)
    lemmas = preprocessor.lemmatize_tokens(tokens)
    pos_tags = preprocessor.get_pos_tags(clean_text)

    return {
        "clean_text": clean_text,
        "sen_tokens": sen_tokens,
        "tokens": tokens,
        "lemmas": lemmas,
        "pos_tags": pos_tags
        }

@app.post("/extract/resume")
def extract_resume_info():
    if not RESUME_TEXT:
        raise HTTPException(status_code=400, detail="resume not loaded")

    clean_text = preprocessor.clean_text(RESUME_TEXT)

    skills = extractor.extract_skills(clean_text)

    return {
        "skills": skills
    }

@app.post("/extract/jd")
def extract_jd_info():
    if not JD_TEXT:
        raise HTTPException(status_code=400, detail="jd not loaded")

    clean_text = preprocessor.clean_text(JD_TEXT)

    skills = extractor.extract_skills(clean_text)

    return {
        "skills": skills
    }

@app.post("/extract/resume/experience")
def extract_resume_experience():
    if not RESUME_TEXT:
        raise HTTPException(status_code=400, detail="resume not loaded")

    clean_text = preprocessor.clean_text(RESUME_TEXT)

    experience = extractor.extract_resume_experience(clean_text)

    return experience

@app.post("/extract/jd/experience")
def extract_jd_experience():
    if not JD_TEXT:
        raise HTTPException(status_code=400, detail="jd not loaded")

    clean_text = preprocessor.clean_text(JD_TEXT)

    experience = extractor.extract_jd_experience(clean_text)

    return experience

@app.get("/match")
def match_resume_jd():
    if not RESUME_TEXT or not JD_TEXT:
        raise HTTPException(status_code=400, detail="Resume and JD must be loaded")

    resume_skills = extractor.extract_skills(RESUME_TEXT)
    jd_skills = extractor.extract_skills(JD_TEXT)

    resume_exp = extractor.extract_resume_experience(RESUME_TEXT)
    jd_exp = extractor.extract_jd_experience(JD_TEXT)

    required_years = max(jd_exp["values"]) if jd_exp["values"] else 0

    skill_match = skill_matcher.match_skills(resume_skills, jd_skills)
    exp_match = experience_matcher.match_experience(resume_exp["total_experience_years"], required_years)

    return {
        "skills": skill_match,
        "experience": exp_match
    }

@app.get("/report/final")
def final_report():
    if not RESUME_TEXT or not JD_TEXT:
        raise HTTPException(status_code=400, detail="Resume and JD must be loaded")

    resume_skills = extractor.extract_skills(RESUME_TEXT)
    jd_skills = extractor.extract_skills(JD_TEXT)

    resume_exp = extractor.extract_resume_experience(RESUME_TEXT)
    jd_exp = extractor.extract_jd_experience(JD_TEXT)

    required_years = max(jd_exp["values"]) if jd_exp["values"] else 0

    skill_match = skill_matcher.match_skills(resume_skills, jd_skills)
    exp_match = experience_matcher.match_experience(resume_exp["total_experience_years"],required_years)

    report = report_generator.generate(skill_match, exp_match)

    return {"final_report": report}

@app.get("/report/feedback")
def feedback_report():
    if not RESUME_TEXT or not JD_TEXT:
        raise HTTPException(status_code=400, detail="Resume and JD must be loaded")

    resume_skills = extractor.extract_skills(RESUME_TEXT)
    jd_skills = extractor.extract_skills(JD_TEXT)

    resume_exp = extractor.extract_resume_experience(RESUME_TEXT)
    jd_exp = extractor.extract_jd_experience(JD_TEXT)

    required_years = max(jd_exp["values"]) if jd_exp["values"] else 0

    skill_match = skill_matcher.match_skills(resume_skills, jd_skills)
    exp_match = experience_matcher.match_experience(resume_exp["total_experience_years"], required_years)

    feedback = feedback_generator.generate(skill_match, exp_match)

    return {"feedback": feedback}
