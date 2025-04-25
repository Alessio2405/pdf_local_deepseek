@echo off
setlocal

:: Ensure we're in the current script directory
cd /d %~dp0

:: Check if Ollama is running by pinging the API
echo Checking if Ollama is running...
curl http://localhost:11434/api/tags >nul 2>&1

IF %ERRORLEVEL% NEQ 0 (
    echo Ollama is not running. Starting it...
    start "" /B ollama serve
    timeout /t 3 >nul
) ELSE (
    echo Ollama is already running.
)

:: Check if deepseek-r1:8b model is pulled
echo Ensuring deepseek-r1:8b is available...
ollama list | findstr /C:"deepseek-r1:8b" >nul
IF %ERRORLEVEL% NEQ 0 (
    echo Model not found. Pulling deepseek-r1:8b...
    ollama pull deepseek-r1:8b
)

:: Start the model in background
echo Running deepseek-r1:8b in background...
start "" /B ollama run deepseek-r1:8b

:: Wait a few seconds for the model to spin up
timeout /t 5 >nul

:: Start the Streamlit app
echo Starting Streamlit app...
streamlit run app.py

endlocal
