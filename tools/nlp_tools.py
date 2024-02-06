import re
from typing import Dict

import spacy
from spacy.tokens import token as spacy_token


def is_word(token):
    return bool(re.match("^[a-zA-Z]+$", token))


def sentence_to_lemmas(sentence: str) -> list[str]:
    """used this glossary https://github.com/explosion/spaCy/blob/master/spacy/glossary.py
    MD: verb, modal auxiliary (will, would, can, could, etc.)
    DATE: Absolute or relative dates or periods
    TIME: Times smaller than a day
    """
    nlp = spacy.load("en_core_web_lg")
    nlp.get_pipe("lemmatizer")
    doc = nlp(sentence)
    lemmas: set = set()
    filtered_lemmas = [token.lemma_ for token in doc if token.ent_type_ not in ["DATE", "TIME"] and token.tag_ != "MD"]
    for lemma in filtered_lemmas:
        if is_word(lemma):
            lemmas.add(lemma)
    return list(lemmas)


def check_sentence(sentence: str, word_list: list[str]) -> bool:
    sentence_lemmas = sentence_to_lemmas(sentence)
    for word in sentence_lemmas:
        if word not in word_list:
            return False
    return True


def sentence_to_tokens(sentence: str) -> list[Dict[str, spacy_token.Token]]:
    """used https://universaldependencies.org/guidelines.html"""
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(sentence)
    tokens_j = doc.to_json()["tokens"]
    for token_j in tokens_j:
        print(token_j)
    print("\n")
    dep_list = ["nsubj", "aux", "ROOT", "advcl", "relcl", "ccomp", "xcomp", "acl", "expl", "neg", "conj"]
    tokens_list: list = []
    token_id: int = 0
    for token_j in tokens_j:
        if token_j["dep"] in dep_list:
            token_j["id"] = token_id
            tokens_list.append(token_j)
            token_id += 1
    return tokens_list

# if __name__ == '__main__':
#     sentence = "My parents had bought this house many years ago and could have visited it last summer."
#     lemmas = sentence_to_lemmas(sentence)
#     print(lemmas)
# tokens = sentence_to_tokens(sentence)
# for token in tokens:
#     print(token)
# tenses = TenseModel(tokens).get_tenses()
# print(tenses)
