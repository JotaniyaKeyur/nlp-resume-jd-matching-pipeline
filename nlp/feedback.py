class FeedbackGenerator:

    def generate(self, skill_match: dict, exp_match: dict) -> dict:

        overlap = skill_match["skill_overlap"]
        gap = exp_match["gap_years"]

        # fit-classification
        if overlap >= 0.7 and gap == 0:
            fit = "Strong Fit"
        elif overlap >= 0.4 or gap <= 1:
            fit = "Partial Fit"
        else:
            fit = "Not a Fit"

        # skill-feedback
        skill_feedback = []
        if skill_match["missing_skills"]:
            skill_feedback.append(f"Missing required skills: {', '.join(skill_match['missing_skills'])}")
        else:
            skill_feedback.append("All required skills are present.")

        # experience-feedback
        if gap > 0:
            experience_feedback = (f"Candidate lacks {gap} years of required experience.")
        else:
            experience_feedback = "Experience requirement is satisfied."

        # suggestions
        suggestions = []

        if skill_match["missing_skills"]:
            suggestions.append("Focus on acquiring missing technical skills.")

        if gap > 0:
            suggestions.append("Gain additional hands-on industry experience.")

        if not suggestions:
            suggestions.append("Profile is well aligned with the job description.")

        return {
            "fit_status": fit,
            "skill_feedback": skill_feedback,
            "experience_feedback": experience_feedback,
            "suggestions": suggestions
        }
