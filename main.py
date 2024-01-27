from langchain.chains import LLMChain

from prompts.lists import get_sentence_list
from tools.nlp_tools import sentence_to_lemmas
from utils.loaders import load_dolphin_dpo_laser_llm

llm = load_dolphin_dpo_laser_llm()

sentence = """When I was a child, I often played in the park near our house. One day, while playing there, I found a strange key. I knew it was a key to something important, but I didn't know exactly what.

My parents had bought this house many years ago, and perhaps this key belonged to something they had just acquired. I decided to ask them what the key was for.

When I approached my parents and showed them the key, they were surprised. My mom said she had already forgotten about that key and didn't know where it could have been lost.

We are figuring out the mystery of the key together. It turns out it's the key to a safe in the old room in the attic. When we open the safe, there will be an old family photograph that my parents had long given up hope of finding."""

words_list = sentence_to_lemmas(sentence)

prompt = get_sentence_list()

chain = LLMChain(llm=llm, prompt=prompt, verbose=True)

if __name__ == '__main__':
    print(chain.run({"input": words_list, "context": sentence}))
