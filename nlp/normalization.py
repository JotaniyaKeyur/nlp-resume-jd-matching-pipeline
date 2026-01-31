import re
from typing import Optional

SKILL_NORMALIZATION_MAP = {
    # auth/security
    "jwt-based": "jwt",
    "jwt authentication": "jwt",
    "jwt-based authentication": "jwt",
    "oauth2": "oauth",
    "auth": "authentication",

    # aiml
    "machine learning": "machine learning",
    "ml models": "machine learning",
    "deep-learning": "deep learning",
    "neural networks": "deep learning",
    "llm": "large language models",
    "llm models": "large language models",
    "rag architectures": "rag",
    "retrieval augmented generation": "rag",
    "nlp": "natural language processing",
    "transformer models": "transformers",

    # dsv
    "data analysis": "data analytics",
    "exploratory data analysis": "eda",
    "statistical learning": "statistics",

    # backend&web
    "fastapi backend": "fastapi",
    "django rest framework": "django rest framework",
    "rest apis": "rest api",
    "microservices architecture": "microservices",
    "backend services": "backend development",

    # databases
    "sqlalchemy orm": "sqlalchemy",
    "postgres": "postgresql",
    "mongo db": "mongodb",
    "mysql database": "mysql",

    # cloud&devops
    "dockerized services": "docker",
    "containerization": "docker",
    "ci/cd pipelines": "ci cd",
    "aws services": "aws",
    "gcp cloud": "gcp",

    # tools
    "hugging face": "huggingface",
    "git github": "git",
    "jupyter notebooks": "jupyter",
}

GENERIC_PHRASES_TO_REMOVE = {
    "the system", "the model", "the database", "things", "users",
    "responsibilities", "experience", "projects", "development",
    "this role", "our clients", "the job"
}


def normalize_skill(skill: str) -> Optional[str]:
    skill = skill.lower().strip("-• ")

    if skill in GENERIC_PHRASES_TO_REMOVE:
        return None

    for k, v in SKILL_NORMALIZATION_MAP.items():
        if k in skill:
            return v

    # remove trailing noise
    skill = skill.replace(" experience", "").replace(" projects", "")

    # remove articles (a, an, the)
    skill = re.sub(r"\b(a|an|the)\b", "", skill)

    # final cleanup
    skill = re.sub(r"\s+", " ", skill).strip()

    return skill if len(skill) > 2 else None
