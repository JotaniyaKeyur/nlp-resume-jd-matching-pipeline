from config import Config


class FitReportGenerator:
    def generate(self, skill_match: dict, exp_match: dict) -> dict:

        skill_overlap = skill_match["skill_overlap"]
        meets_skill = skill_match["meets_threshold"]
        meets_exp = exp_match["meets_requirement"]

        #fit-decision
        if meets_skill and meets_exp:
            fit = "Strong Fit"
        elif skill_overlap >= 0.5:
            fit = "Partial Fit"
        else:
            fit = "Not a Fit"

        #feedback messages
        feedback = []

        if not meets_skill:
            feedback.append(f"Missing key skills: {', '.join(skill_match['missing_skills'])}")

        if not meets_exp:
            feedback.append(f"Experience gap of {exp_match['gap_years']} years")

        if not feedback:
            feedback.append("Profile aligns well with the job description.")

        # ats style score
        skill_score = skill_overlap * 70
        exp_score = 30 if meets_exp else max(0, 30 - exp_match["gap_years"] * 5)

        final_score = round(skill_score + exp_score, 2)

        return {
            "fit_status": fit,
            "final_score": final_score,
            "summary": feedback,
            "improvements": {
                "skills_to_improve": skill_match["missing_skills"],
                "experience_gap_years": exp_match["gap_years"]
            }
        }
