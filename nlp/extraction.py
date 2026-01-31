import re
import spacy
from datetime import datetime
from config import Config
from nlp.normalization import normalize_skill

nlp = spacy.load(Config.SPACY_MODEL)


class InfoExtractor:

    ALLOWED_POS = {"NOUN", "PROPN"}

    TECH_KEYWORDS = {
        "python", "java", "sql", "docker", "fastapi", "django", "aws",
        "machine learning", "deep learning", "nlp", "rag",
        "pytorch", "tensorflow", "mongodb", "postgresql"
    }

    MONTHS = {
        "jan": 1, "january": 1,
        "feb": 2, "february": 2,
        "mar": 3, "march": 3,
        "apr": 4, "april": 4,
        "may": 5,
        "jun": 6, "june": 6,
        "jul": 7, "july": 7,
        "aug": 8, "august": 8,
        "sep": 9, "september": 9,
        "oct": 10, "october": 10,
        "nov": 11, "november": 11,
        "dec": 12, "december": 12,
    }

    def extract_skills(self, text: str) -> list[str]:
        doc = nlp(text)
        skills = set()

        for chunk in doc.noun_chunks:
            # reject long phrases
            if len(chunk) > 4:
                continue

            # reject verbs
            if any(tok.pos_ not in self.ALLOWED_POS for tok in chunk):
                continue

            candidate = normalize_skill(chunk.text)
            if not candidate:
                continue

            # keyword validation
            if any(k in candidate for k in self.TECH_KEYWORDS):
                skills.add(candidate)

        return sorted(skills)

    def extract_resume_experience(self, text: str) -> dict:
        pattern = re.findall(
            r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+(\d{4})\s*[-–]\s*"
            r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)?[a-z]*\s*(\d{4}|present)",
            text.lower()
        )

        total_months = 0
        ranges = []

        for sm, sy, em, ey in pattern:
            start = datetime(int(sy), self.MONTHS[sm], 1)

            if ey == "present":
                end = datetime.now()
            else:
                end_month = self.MONTHS.get(em, 1)
                end = datetime(int(ey), end_month, 1)

            months = (end.year - start.year) * 12 + (end.month - start.month)
            total_months += max(months, 0)

            ranges.append(f"{sm.title()} {sy} - {em.title() if em else ''} {ey}")

        return {"date_ranges": ranges, "total_experience_years": round(total_months / 12, 2)}

    def extract_jd_experience(self, text: str) -> dict:
        matches = re.findall(r"(\d+)\s*(?:\+|–|-)?\s*(\d+)?\s*years?", text.lower())

        years = set()

        for start, end in matches:
            years.add(int(start))
            if end:
                years.add(int(end))

        return {"type": "required_years", "values": sorted(years)}
