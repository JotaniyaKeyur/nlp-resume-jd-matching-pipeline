class Config:
    #model config
    SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L6-v2"
    SPACY_MODEL = "en_core_web_sm"

    #thresholds
    SKILL_MATCH_THRESHOLD = 0.7  # cosine similarity threshold
    MIN_SKILL_OVERLAP = 0.3      # minimum required skill overlap
