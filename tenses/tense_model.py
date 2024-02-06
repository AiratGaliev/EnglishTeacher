from dataclasses import dataclass
from typing import Dict

from spacy.tokens import token as spacy_token

from tenses.tense_patterns import TensePattern

tense_patterns = [TensePattern.PRESENT_SIMPLE_NEGATIVE, TensePattern.PRESENT_SIMPLE_POSITIVE,
                  TensePattern.PRESENT_SIMPLE_QUESTION]


@dataclass
class TenseModel:
    tokens: list[Dict[str, spacy_token.Token]] = None

    def get_tenses(self) -> list[str]:
        """Method for finding all grammatical tenses from tokens"""
        tenses = []

        for pattern_dicts in tense_patterns:
            if self.match_pattern(pattern_dicts.value):
                tenses.append(pattern_dicts.name)

        return tenses

    def match_pattern(self, pattern):
        for token, pattern_token in zip(self.tokens, pattern):
            if token["dep"] in pattern_token["dep"] and token["pos"] in pattern_token["pos"]:
                continue
            else:
                return False
        return True
