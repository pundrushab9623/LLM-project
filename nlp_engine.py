import spacy
from sentence_transformers import SentenceTransformer, util

# Load SpaCy for Entity Recognition (Name, Email, etc.)
nlp = spacy.load("en_core_web_sm")

# Load HuggingFace Transformer for high-accuracy semantic matching
model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_entities(text):
    doc = nlp(text)
    entities = {"name": None, "skills": []}
    # Basic logic to find Proper Nouns as potential names
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            entities["name"] = ent.text
    return entities

def get_semantic_score(resume_text, jd_text):
    # This understands that "Cloud" and "Azure" are related
    embeddings = model.encode([resume_text, jd_text])
    score = util.cos_sim(embeddings[0], embeddings[1])
    return float(score) * 100
