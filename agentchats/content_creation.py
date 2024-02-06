# based on https://github.com/microsoft/autogen/blob/main/notebook/agentchat_groupchat.ipynb
import ast
import re

import autogen
from autogen import config_list_from_json

from agentchats.instructions_creation import get_instructions

dolphin_llm = config_list_from_json(env_or_file="OAI_CONFIG_LIST.json", filter_dict={"model": {"dolphin"}})
westlake_llm = config_list_from_json(env_or_file="OAI_CONFIG_LIST.json", filter_dict={"model": {"westlake"}})
starling_llm = config_list_from_json(env_or_file="OAI_CONFIG_LIST.json", filter_dict={"model": {"starling"}})
openchat_llm = config_list_from_json(env_or_file="OAI_CONFIG_LIST.json", filter_dict={"model": {"openchat"}})


def format_instructions(instructions: list[str]) -> str:
    return "\n".join([item for item in instructions])


def get_sentence_list(topic: str = "", word_list: list[str] = None, tense: str = "Present Simple",
                      list_length: int = 5, seed: int = 0) -> list[str]:
    seed_idx = f"get_sentence_list_{seed}"
    json_list_template = str([f"sentence{i}" for i in range(1, list_length + 1)]).replace("'", '"')

    message = f"""Strictly return only a list of {list_length} sentences in the {tense} tense!
    Use only {tense} tense markers in sentences! The sentences in the list should not
    be сompound and сomplex sentences and should not include other grammatical tenses! The length of the list
    should be strictly no more than {list_length} elements, but don't write any other text and code. Make sure that sentence
    tenses are written in {tense} only!
    Return a list of sentences only json list format {json_list_template}
    The topic for sentences: {topic}.
    Use only this list to create sentences: {word_list}.
    Don't use any other words!
    """

    instructions = get_instructions(message=message, seed=seed)
    content_creator_instructions = format_instructions(instructions["content_creator"])
    content_editor_instructions = format_instructions(instructions["content_editor"])
    critic_instructions = format_instructions(instructions["critic"])

    manager_config = {
        "request_timeout": 600,
        "seed": seed_idx,
        "config_list": dolphin_llm,
        "temperature": 0
    }

    user_proxy_config = {
        "request_timeout": 600,
        "seed": seed_idx,
        "config_list": dolphin_llm,
        "temperature": 0
    }

    content_creator_config = {
        "request_timeout": 600,
        "seed": seed_idx,
        "config_list": dolphin_llm,
        "temperature": 0.3
    }

    content_editor_config = {
        "request_timeout": 600,
        "seed": seed_idx,
        "config_list": starling_llm,
        "temperature": 0.3
    }

    critic_config = {
        "request_timeout": 600,
        "seed": seed_idx,
        "config_list": openchat_llm,
        "temperature": 0.2
    }

    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        llm_config=user_proxy_config,
        is_termination_msg=lambda x: x.get("content", "") and (
                "TERMINATE" or "APPROVED" in x.get("content", "").rstrip()),
        code_execution_config={"work_dir": ".", "use_docker": False},
        system_message="""
        Don't write anything! Return only one of two words: 'TERMINATE' or 'CONTINUE'.
        Strictly follow this pseudocode instruction:
        if content form critic agent contains has 'APPROVED' word:
            return 'TERMINATE'
        else:
            return 'CONTINUE'
        """
    )

    content_creator = autogen.AssistantAgent(
        name="content_creator",
        llm_config=content_creator_config,
        is_termination_msg=lambda x: x.get("content", "") and "TERMINATE" in x.get("content", "").strip(),
        system_message=f"""As a content creator, who is very strong on grammar, you are required to create textual content.
        Strictly return only a list of sentences in the {tense} tense! Don't write nonsense, only sentences that make 
        sense, facts about {topic}, or {topic} terminology.
        Use only {tense} tense markers in every sentences! You must use topic to figure out in what topic to use the words in the list, but no more!
        You must strictly follow these instructions:
        {content_creator_instructions}
        Follow the critic's "recommendations" or "improvements" to correct your response! Your content must be edited
        by the content_editor agent.
        Strictly reply with a list of {list_length} sentences only in json list format {json_list_template}
        """
    )

    content_editor = autogen.AssistantAgent(
        name="content_editor",
        llm_config=content_editor_config,
        is_termination_msg=lambda x: x.get("content", "") and "TERMINATE" in x.get("content", "").strip(),
        system_message=f"""As a content editor, who is very strong on grammar, you need to fix textual content created by
        a content writer. Correct every sentence in the list in {tense} tense! Don't write nonsense, only sentences that make
        sense, facts about {topic}, or {topic} terminology. Check {tense} tense markers
        in every sentences! Rewrite all the sentences in the list so that they are correct not only grammatically but also in meaning.
        You must strictly follow these instructions:
        {content_editor_instructions}
        Follow the critic's "recommendations" or "improvements" to correct your answer!
        Check the length of the list, delete extra sentences and fix json list format {json_list_template}
        Always reply with a list of {list_length} sentences only in json list format {json_list_template}
        """
    )

    critic = autogen.AssistantAgent(
        name="critic",
        llm_config=critic_config,
        is_termination_msg=lambda x: x.get("content", "") and "TERMINATE" in x.get("content", "").strip(),
        system_message=f"""As a critic, who is very strong on grammar, it is your responsibility to check the textual
        content created by the content_creator agent and edited by the content_editor agent.
        Follow these task requirements:
        {critic_instructions}
        If all is well, add the word "APPROVED" at the end of the answer, otherwise write lists recommendations or improvements.
        In other words follow this pseudocode instruction:
        ```
        sentence_list = content_editor_content()
        is_approved = check_list_of_sentences(sentence_list)
        length = len(sentence_list)
        if is_approved is True and length <= {list_length}:
            return "APPROVED"
        else:
            return lists recommendations or improvements
        ```
        """
    )
    extracted_list: list[str] = []
    try:
        groupchat = autogen.GroupChat(agents=[user_proxy, content_creator, content_editor, critic],
                                      messages=[], max_round=50)
        manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=manager_config)

        user_proxy.initiate_chat(manager, message=message)
        content_creator_contents = [str(item['content']).strip() for item in groupchat.messages if
                                    item['name'] == 'content_editor']
        content_creator_last_content = content_creator_contents[-1].replace('".', '"').replace(',"', '",').replace('\n',
                                                                                                                   '')
        if content_creator_last_content[-1] != "]":
            content_creator_last_content = content_creator_last_content + "]"
        pattern = r"\[([^\]]*)\]"
        matches = re.findall(pattern, content_creator_last_content)

        if matches:
            extracted_list = list(ast.literal_eval(matches[0]))
    except Exception as e:
        print(f"Error: {e}")
    return extracted_list
