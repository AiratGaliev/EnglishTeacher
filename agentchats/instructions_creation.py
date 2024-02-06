# import json

import autogen
from autogen import config_list_from_json

llm = config_list_from_json(env_or_file="OAI_CONFIG_LIST.json", filter_dict={"model": {"starling"}})


def get_instructions(message: str = "", seed: int = 0) -> dict[str, list]:
    user_proxy_config = {
        "request_timeout": 600,
        "seed": seed,
        "config_list": llm,
        "temperature": 0
    }

    manager_config = {
        "request_timeout": 600,
        "seed": seed,
        "config_list": llm,
        "temperature": 0
    }

    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        llm_config=user_proxy_config,
        is_termination_msg=lambda x: x.get("content", "") and (
                "TERMINATE" or "APPROVED" in x.get("content", "").rstrip()),
        code_execution_config={"work_dir": ".", "use_docker": False},
        system_message="""Don't write anything!
        """
    )

    manager = autogen.AssistantAgent(
        name="manager",
        llm_config=manager_config,
        is_termination_msg=lambda x: x.get("content", "") and "TERMINATE" in x.get("content", "").strip(),
        system_message="""As a manager, your role is to oversee content_creator, content_editor and critic 
        agents working together to create text content. You're not a content creation expert, so don't show examples of 
        how to solve the task, just delegate the task to the agents! Create very detailed step by step instructions
         what are they need to do, and make sure that their instructions are strictly related. 
        Don't write examples! Each of the agents must do their part of the task! 
        The critic should check the content_editor's work, don't do his work for him!
        Return step by step instructions for the agents only this format:
        content_creator:
        1. ...
        2. ...
        3. ...
        ...
        content_editor:
        1. ...
        2. ...
        3. ...
        ...
        critic:
        1. ...
        2. ...
        3. ...
        ...
        """
    )

    user_proxy.initiate_chat(manager, message=message)
    instructions_text = str(manager.last_message()["content"]).strip()
    sections = ["content_creator", "content_editor", "critic"]
    instructions_json = {}

    current_section = None
    for line in instructions_text.splitlines():
        if line.startswith(tuple(sections)):
            current_section = line.split(':')[0].strip()
            instructions_json[current_section] = []
        elif current_section:
            line = line.strip()
            if len(line.strip()) > 0:
                instructions_json[current_section].append(line.strip())

    return instructions_json
