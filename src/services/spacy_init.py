# # src/services/spacy_init.py

# import spacy
# from spacy.pipeline import EntityRuler
# import json
# import os
# from typing import Any

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Path to src/services
# MODEL_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../nlp_custom_model"))
# JSON_PATH = os.path.join(BASE_DIR, "value_field_map.json")

# def build_custom_nlp() -> Any:
#     nlp = spacy.load("en_core_web_sm")
#     ruler = EntityRuler(nlp)

#     try:
#         if not os.path.exists(JSON_PATH) or os.path.getsize(JSON_PATH) == 0:
#             raise ValueError("value_field_map.json is missing or empty. Please generate it first.")
#         with open(JSON_PATH, "r", encoding="utf-8") as f:
#             value_field_map = json.load(f)
#     except Exception as e:
#         print(f"Error loading value_field_map.json: {e}")
#         raise

#     patterns = []
#     for value, meta in value_field_map.items():
#         label = meta["field"].upper()
#         patterns.append({"label": label, "pattern": value})

#     ruler.add_patterns(patterns)
#     nlp.add_pipe(ruler, before="ner")
#     try:
#         nlp.to_disk(MODEL_PATH)
#     except Exception as e:
#         print(f"Error saving spaCy model: {e}")
#         raise
#     return nlp

# def load_custom_nlp() -> Any:
#     if not os.path.exists(MODEL_PATH):
#         return build_custom_nlp()
#     try:
#         return spacy.load(MODEL_PATH)
#     except Exception as e:
#         print(f"Error loading spaCy model from disk: {e}")
#         return build_custom_nlp()
