# 📄 Chat with PDF and ask questions using Streamlit + Ollama + LangChain + DeepSeek

This project allows you to **chat with the contents of a PDF** using `LangChain`, `Streamlit`, and an **Ollama local LLM**, specifically the `deepseek-r1:8b` model.

## ⚙️ Features

- Upload a PDF and ask questions about its content
- Uses `LangChain` for document loading, splitting, embedding, and retrieval
- Powered by `Ollama` to run the `deepseek-r1:8b` LLM locally
- Interactive UI with `Streamlit`
- No external APIs required — all runs locally

---

## 📦 Requirements

- Python 3.10+
- [Ollama](https://ollama.com) installed
- `deepseek-r1:8b` model pulled via Ollama

### 🧪 Python Dependencies

Install required Python packages with:

```bash
pip install -r requirements.txt
```

## ▶️ How to Run the App

To simplify setup, the project includes two startup scripts that automatically launch Ollama (if not running) and then open the app in your browser.

### 🪟 For Windows users
Double-click or run from a terminal:

```bash
start.bat
```

### 🐧 For Linux/macOS users
Make the script executable first:

```bash
chmod +x start.sh
start.sh
```

