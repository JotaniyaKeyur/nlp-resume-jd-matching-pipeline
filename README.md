# 📄 Resume Analyzer API (Pure NLP Project)

A **Resume vs Job Description Analyzer** built using **classical NLP techniques** (spaCy + sentence-transformers).
This project performs **skill extraction, experience parsing, semantic matching, and candidate fit analysis** — **without using any LLMs**.

> 🎯 Built as a **practice + portfolio project** to demonstrate NLP, backend, and ATS-style logic.

---

## 🚀 Features

- Upload Resume (PDF) and Job Description (TXT)
- Text preprocessing (cleaning, tokenization, lemmatization, POS tagging)
- Skill extraction using spaCy noun chunks
- Real-world **skill normalization**
- Resume experience extraction (date ranges → total years)
- JD experience extraction (e.g. `2+ years`, `3–5 years`)
- Semantic skill matching using cosine similarity
- Experience gap analysis
- Final **candidate fit feedback**
- REST API using FastAPI

---

## 🧠 Tech Stack (No LLMs)

- Python
- FastAPI
- spaCy
- Sentence Transformers (MiniLM)
- Regex
- Pure NLP + rule-based logic

> ❌ No GPT / LLM / Generative AI  
> ✅ Fully explainable & deterministic NLP pipeline

---

## 📁 Project Structure

```
resume-analyzer/
│
├── app.py
├── config.py
├── requirements.txt
├── setup_nlp.py
│
├── nlp/
│   ├── preprocessing.py
│   ├── extraction.py
│   ├── normalization.py
│   ├── matching.py
│   └── feedback.py
│
├── utils/
│   └── doc_reader.py
│
├── uploads/
└── README.md
```

---

## ⚙️ How to Run This Project

### 1️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate    # Windows
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Download spaCy Model

```bash
python -m spacy download en_core_web_sm
```

### 4️⃣ Setup NLP Models

```bash
python setup_nlp.py
```

### 5️⃣ Run the Server

```bash
uvicorn app:app --reload
```

---

## 🌐 API Access

- Base URL: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs

---

## 🔌 API Endpoints

### Upload
- POST `/upload/resume`
- POST `/upload/jd`

### Preprocess
- POST `/preprocess/resume`
- POST `/preprocess/jd`

### Extract
- POST `/extract/resume`
- POST `/extract/jd`
- POST `/extract/resume/experience`
- POST `/extract/jd/experience`

### Match
- GET `/match`

### Final Feedback
- GET `/report/feedback`

---

## 📊 Sample Feedback Output

```json
{
  "fit_status": "Partial Fit",
  "skill_feedback": [
    "Missing required skills: docker, aws"
  ],
  "experience_feedback": "Candidate lacks 1.0 years of required experience.",
  "suggestions": [
    "Improve missing technical skills",
    "Gain additional hands-on experience"
  ]
}
```

---

## 🎯 Why This Project Is Valuable

- Demonstrates core NLP fundamentals
- Mimics real ATS resume screening
- Fully explainable & rule-based
- Clean backend architecture
- Easy to extend with ML or LLMs later

---

## 🔮 Future Enhancements

- Resume scoring system
- Role-based skill weighting
- Resume ranking
- Visualization dashboard
- Unit tests

---

## 👨‍💻 Author

Built as a learning and portfolio project to showcase  
**NLP • Backend • System Design • ATS Logic**
