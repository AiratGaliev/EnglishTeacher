import json
import shutil

from agentchats.content_creation import get_sentence_list
from prompts.lists import get_present_simple_sentence_list
from tools.nlp_tools import sentence_to_lemmas, check_sentence

text = """
I understand that you are eager to type some code in your editor and run it to see your first Java application in action! Do not worry, your expectation will be fulfilled by the end of this tutorial. But before we move on, I would like to do through several elements that you need to know to fully understand what you are doing.

Even if you are familiar with some other programming language, know about compilation, know what an executable file is you may be interested in the following because Java works in a way that differs from C or C++.

There are several steps that you need to follow to create a Java application. This tutorial shows you how to create a very simple Java application. If you need to create an enterprise application, the creation process is more complex but at its core you will find these simple steps.

The first of these steps is to write some Java code in a text editor.

Then this code has to be transformed to another format, which can be executed by your computer. This transformation is conducted by a special piece of software called a compiler. Some languages do not have a compiler; Java does. Every compiler is specific to a language.

The file produced by a compiler is often called a binary file or an executable file. Whereas you can read a source code and understand it, binary or executable files are not meant to be read by a human person. Only your computer can make sense of it.

This code contains special binary codes called byte code. This is a technical term that you may come across. The precise description of what is this byte code is beyond the scope of this tutorial.

Compiling some code may fail; your code has to be correct for the compiler to produce an executable version of it. Do not worry, this page gives you the code you are going to compile. All you need to do is copy it and paste it in your text editor.

Once the compiler produced the binary file that you need, you can execute this binary file, that will your program.

These two steps: compilation and execution require two specific pieces of software that are part of the Java Development Kit, also known as the JDK. You will see how to download the JDK for free and how to install it later in this tutorial.

Note that starting with Java SE 11 you can also merge these two steps into one, by executing a .java file directly. You can use these feature only if you are executing a program that is written in a single file. This way of executing your java application does not work if your java code spans more than one file.
"""

prompt = get_present_simple_sentence_list()

temp_sentence_list: list[str] = []

if __name__ == '__main__':
    list_length = 5
    seed = 0
    while len(temp_sentence_list) < list_length:
        word_list = sentence_to_lemmas(text)
        sentence_list = get_sentence_list(topic="Java Programming", word_list=word_list, tense="Present Simple",
                                          list_length=list_length, seed=seed)
        shutil.rmtree(".cache", ignore_errors=True)
        if len(sentence_list) > 0:
            for sentence in sentence_list:
                if len(sentence) > 5:
                    if check_sentence(sentence, word_list=word_list):
                        temp_sentence_list.append(sentence)
        seed += 1
    print(json.dumps(temp_sentence_list, indent=2))
