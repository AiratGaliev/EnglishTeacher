import re

import spacy


def is_word(token):
    return bool(re.match("^[a-zA-Z]+$", token))


def sentence_to_lemmas(sentence: str) -> list[str]:
    nlp = spacy.load("en_core_web_lg")
    nlp.get_pipe("lemmatizer")
    doc = nlp(sentence)
    lemmas: set = set()
    for token in doc:
        if is_word(token.text):
            lemmas.add(token.lemma_)
    return list(lemmas)


def sentence_to_tense(sentence: str):
    """Not implemented yet"""
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(sentence)
    print([(ent.text, ent.tag_) for ent in doc])
    print([(ent.text, ent.morph) for ent in doc])
    print("\n")
