from sentence_transformers import SentenceTransformer, util
from config import Config


class SkillMatcher:
    def __init__(self):
        self.model = SentenceTransformer(Config.SENTENCE_TRANSFORMER_MODEL)

    def match_skills(self, resume_skills: list[str], jd_skills: list[str]) -> dict:
        if not resume_skills or not jd_skills:
            return {
                "matched_skills": [],
                "missing_skills": jd_skills,
                "extra_skills": resume_skills,
                "skill_overlap": 0.0,
                "meets_threshold": False
            }

        resume_embeddings = self.model.encode(resume_skills, convert_to_tensor=True)
        jd_embeddings = self.model.encode(jd_skills, convert_to_tensor=True)

        matched = set()
        missing = set(jd_skills)

        for i, jd_skill in enumerate(jd_skills):
            similarities = util.cos_sim(jd_embeddings[i], resume_embeddings)[0]
            max_score = similarities.max().item()

            if max_score >= Config.SKILL_MATCH_THRESHOLD:
                matched.add(jd_skill)
                missing.discard(jd_skill)

        overlap = len(matched) / len(jd_skills)

        return {
            "matched_skills": sorted(matched),
            "missing_skills": sorted(missing),
            "extra_skills": sorted(set(resume_skills) - matched),
            "skill_overlap": round(overlap, 2),
            "meets_threshold": overlap >= Config.MIN_SKILL_OVERLAP
        }


class ExperienceMatcher:
    def match_experience(self, resume_years: float, required_years: int) -> dict:
        return {
            "resume_experience_years": resume_years,
            "required_experience_years": required_years,
            "meets_requirement": resume_years >= required_years,
            "gap_years": round(max(required_years - resume_years, 0), 2)
        }
