#!/bin/bash

if [ ! -d ".venv" ]; then
    echo "Creating .venv directory..."
    python3 -m venv .venv
    source .venv/bin/activate
    echo "Installing dependencies..."
    export CUDACXX=/usr/local/cuda/bin/nvcc
    export CMAKE_ARGS="-DLLAMA_CUBLAS=on"
    export FORCE_CMAKE=1
    pip install -U pip setuptools wheel
    pip install -r requirements.txt
    python -m spacy download en_core_web_lg
    if [ $? -ne 0 ]; then
        echo "Error happens. Deleting .venv directory..."
        rm -rf .venv
        exit 1
    fi
else
    source .venv/bin/activate
fi
streamlit run "🧑‍🏫 Main.py"
deactivate