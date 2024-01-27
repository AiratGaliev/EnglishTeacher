from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough


def chat_ml_template(system_prompt: str = ""):
    template_str = "<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
    if system_prompt != "":
        template_str = "<|im_start|>system\n{system_prompt}<|im_end|>\n".format(
            system_prompt=system_prompt) + template_str
    return {"prompt": RunnablePassthrough()} | ChatPromptTemplate.from_template(template_str)


def alpaca_template(system_prompt: str = ""):
    template_str = "### Instruction:\n{prompt}\n\n### Response:\n"
    if system_prompt != "":
        template_str = "{system_prompt}\n\n".format(system_prompt=system_prompt) + template_str
    return {"prompt": RunnablePassthrough()} | ChatPromptTemplate.from_template(template_str)
