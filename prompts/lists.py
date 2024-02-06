from langchain.prompts import PromptTemplate, FewShotPromptTemplate


def get_present_simple_prompt(context: str, word_list: [str]) -> str:
    present_simple_template = """
    I want you to act as an English teacher to create educational content in this context:
    {context}
    
    Return only a list of short sentences in Present Simple like on the example for this words list: {word_list}.
    
    Please ensure that sentences are grammatically correct, logically coherent and laconic.
    Do not return sentences from the examples.
    Like this example:
    
    Words list example: [I, know, see, it, you, work, every, day, we, understand, also, think, so, usually, buy, there, 
    speak, English, they, like, this, language, often, go]
    List of sentences list example (don"t return any these sentences): ["I know","I see it","You work every day","We 
    understand you","I also think so","We usually buy it there","I speak English","They also think so","I like this 
    language","We often go there"]
   """

    prompt = PromptTemplate(
        input_variables=["context", "word_list"],
        template=present_simple_template,
    )

    return prompt.format(context=context, word_list=word_list)


def get_present_simple_sentence_list():
    examples = [
        {"word_list": ["work", "study", "speak", "you", "also", "it", "I", "help", "this", "to", "like", "want",
                       "think", "English", "language", "understand", "know", "see", "and", "go", "so"],
         "sentences": ["I know", "I see it", "I understand you", "I want to help you", "I also think so", "I know it",
                       "I speak English", "I go to work", "I like this language", "I study and work"]},
        {"word_list": ["know", "you", "and", "it", "very", "understand", "New", "year", "travel", "speak", "like",
                       "this", "Russian", "I", "learn", "in", "Russia", "live", "country", "English", "York", "every",
                       "well", "They"],
         "sentences": ["I know it very well", "I live in New York", "I understand it", "I learn English",
                       "I live in Russia", "They live in this country", "I travel every year",
                       "I understand you very well", "I speak English and Russian", "I like English"]},
        {"word_list": ["English", "want", "You", "my", "understand", "I", "program", "every", "and", "you", "learn",
                       "online", "city", "study", "like", "work", "it", "this", "We", "day", "see", "result"],
         "sentences": ["I learn English online", "I like this city", "I want it", "You work every day",
                       "I see my results", "I study every day", "We understand you", "I work and study",
                       "I like this program", "I see you"]},
        {"word_list": ["my", "English", "lesson", "that", "video", "me", "this", "very", "We", "see", "place", "city",
                       "in", "can", "like", "You", "I", "live", "well", "know", "result", "speak", "help",
                       "understand"],
         "sentences": ["I understand", "I like this video", "I know that place", "I see my result",
                       "I understand this lesson", "You help me", "I can speak English", "I like this place",
                       "We live in this city", "You speak English very well"]},
    ]

    example_formatter_template = """
    Word List: {word_list}
    Sentences: {sentences}\n
   """
    example_prompt = PromptTemplate(
        input_variables=["word_list", "sentences"],
        template=example_formatter_template,
    )

    return FewShotPromptTemplate(
        validate_template=True,
        examples=examples,
        example_prompt=example_prompt,
        prefix="""Follow the context: {context}. Strictly return only a list of sentences in the 
        Present Simple tense, don't return сompound and сomplex sentences with other grammatical tenses. The length of 
        the list should be strictly no more than 5 elements and in json list format ['sentence1', 'sentence2', etc].
        Strictly use words only from the "Word List", not more.
        Strictly make sure that every sentence as grammatically correct as in "Sentences" list examples, as logically 
        coherent, laconic as possible.""",
        suffix="Word List: {input}\nSentences: ",
        input_variables=["input", "context"],
        example_separator="\n"
    )
