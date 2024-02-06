import json

import uvicorn
from llama_cpp.server.app import create_app
from llama_cpp.server.settings import ConfigFileSettings, ServerSettings

json_cfg = {
    "host": "localhost",
    "port": 1234,
    "models": [
        {
            "model": "https://huggingface.co/TheBloke/dolphin-2.6-mistral-7B-dpo-laser-GGUF",
            "model_alias": "dolphin",
            "chat_format": "chatml"
        },
        {
            "model": "https://huggingface.co/TheBloke/openchat-3.5-0106-GGUF",
            "model_alias": "openchat",
            "chat_format": "openchat"
        },
        {
            "model": "https://huggingface.co/TheBloke/xDAN-L1-Chat-RL-v1-GGUF",
            "model_alias": "xdan",
            "chat_format": "chatml"
        },
        {
            "model": "https://huggingface.co/TheBloke/OpenHermes-2.5-Mistral-7B-16k-GGUF",
            "model_alias": "openhermes",
            "chat_format": "chatml"
        }
    ]
}


def main():
    models_dir = "/home/airat/LLMs/"
    quant_method = "Q4_K_M"

    for models in json_cfg["models"]:
        models["model"]: str = models_dir + models["model"].split('/')[-1].lower().rstrip(
            "-gguf") + f".{quant_method}.gguf"
        models["n_gpu_layers"]: int = 33
        models["offload_kqv"]: bool = True
        models["n_threads"]: int = 12
        models["n_batch"]: int = 512
        models["n_ctx"]: int = 5120
        models["cache"]: bool = False

    # for models in json_cfg["models"]:
    #     models["model"]: str = models_dir + models["model"].split('/')[-1].lower().rstrip(
    #         "-gguf") + f".{quant_method}.gguf"
    #     models["n_gpu_layers"]: int = 33
    #     models["offload_kqv"]: bool = True
    #     models["n_threads"]: int = 12
    #     models["n_batch"]: int = 512
    #     models["n_ctx"]: int = 5120
    #     models["cache"]: bool = False

    # "https://huggingface.co/TheBloke/OpenHermes-2.5-Mistral-7B-16k-GGUF/resolve/main/openhermes-2.5-mistral-7b-16k.Q4_K_M.gguf"

    json_data = json.dumps(json_cfg)
    config_file_settings = ConfigFileSettings.model_validate_json(json_data)
    server_settings = ServerSettings.model_validate(config_file_settings)
    model_settings = config_file_settings.models

    app = create_app(
        server_settings=server_settings,
        model_settings=model_settings,
    )
    uvicorn.run(
        app,
        host=server_settings.host,
        port=server_settings.port,
        ssl_keyfile=server_settings.ssl_keyfile,
        ssl_certfile=server_settings.ssl_certfile,
    )

    print(json_cfg)


if __name__ == "__main__":
    main()
