from enum import Enum


class TensePattern(Enum):
    PRESENT_SIMPLE_POSITIVE = [
        {"pos": ["PRON", "PROPN"], "dep": "nsubj"},
        {"pos": "VERB", "dep": ["ROOT", "conj"]}
    ]

    PRESENT_SIMPLE_NEGATIVE = [
        {"pos": ["PRON", "PROPN"], "dep": "nsubj"},
        {"pos": "AUX", "lemma": "do", "dep": "aux"},
        {"pos": "PART", "lemma": "not", "dep": "neg"},
        {"pos": "VERB", "dep": ["ROOT", "conj"]}
    ]

    PRESENT_SIMPLE_QUESTION = [
        {"pos": "AUX", "lemma": "do", "dep": "aux"},
        {"pos": "PRON", "dep": "nsubj"},
        {"pos": "VERB", "dep": "ROOT"}
    ]
