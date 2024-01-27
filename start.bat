@echo off

if not exist .venv (
    echo Creating .venv directory...
    python -m venv .venv
    call .venv\Scripts\activate
    echo Installing dependencies...
    set CMAKE_ARGS=-DLLAMA_CUBLAS=OFF
    set FORCE_CMAKE=1
    python.exe -m pip install --upgrade pip setuptools wheel
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error happens. Deleting .venv directory...
        rmdir /s /q .venv
        exit
    )
) else (
    call .venv\Scripts\activate
)
streamlit run "🧑‍🏫 Main.py"
deactivate