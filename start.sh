#!/bin/bash

# Move to the script's directory
cd "$(dirname "$0")"

echo "Checking if Ollama is running..."
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
  echo "Ollama is not running. Starting it..."
  nohup ollama serve > ollama.log 2>&1 &
  sleep 3
else
  echo "Ollama is already running."
fi

# Ensure the model is pulled
echo "Checking if 'deepseek-r1:8b' model is available..."
if ! ollama list | grep -q "deepseek-r1:8b"; then
  echo "Model not found. Pulling 'deepseek-r1:8b'..."
  ollama pull deepseek-r1:8b
fi

# Start the model in the background
echo "Running deepseek-r1:8b in background..."
nohup ollama run deepseek-r1:8b > model.log 2>&1 &

# Give it a moment to spin up
sleep 5

# Run the Streamlit app
echo "Starting Streamlit app..."
streamlit run app.py
