import streamlit as st
import os

from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

# === Initialize session state ===
if "messages" not in st.session_state:
    st.session_state["messages"] = []  # List to store chat messages

if "pending_question" not in st.session_state:
    st.session_state["pending_question"] = None  # Question waiting for response

# === Prompt template ===
template = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {question} 
Context: {context} 
Answer:
"""

# === Define file paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pdfs_directory = os.path.join(BASE_DIR, "uploaded_files", "pdfs")
os.makedirs(pdfs_directory, exist_ok=True)

# === Load Ollama model and embeddings ===
# Make sure `ollama run deepseek-r1:8b` is running in background
embeddings = OllamaEmbeddings(model="deepseek-r1:8b")
vector_store = InMemoryVectorStore(embeddings)
model = OllamaLLM(model="deepseek-r1:8b")

# === Utility functions ===

# Save uploaded PDF file to local directory
def upload_pdf(file):
    with open(os.path.join(pdfs_directory, file.name), "wb") as f:
        f.write(file.getbuffer())

# Load PDF content using PDFPlumber
def load_pdf(file_path):
    loader = PDFPlumberLoader(file_path)
    return loader.load()

# Split PDF content into chunks for processing
def split_text(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    return splitter.split_documents(documents)

# Add chunked documents to vector store
def index_docs(documents):
    vector_store.add_documents(documents)

# Retrieve similar documents from vector store
def retrieve_docs(query):
    return vector_store.similarity_search(query)

# Generate response from documents
def answer_question(question, documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return chain.invoke({"question": question, "context": context})

# Generate response when no documents are uploaded
def answer_question_no_docs_uploaded(question):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return chain.invoke({"question": question, "context": ""})

# === Streamlit UI ===

st.title("Chat with your PDF")

# File uploader widget
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

# If file uploaded, process and index it
if uploaded_file:
    upload_pdf(uploaded_file)
    path = os.path.join(pdfs_directory, uploaded_file.name)
    documents = load_pdf(path)
    chunked_docs = split_text(documents)
    index_docs(chunked_docs)

# Chat input field
question = st.chat_input("Ask a question about the PDF...")

# On new user question, save it to session state
if question:
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    st.session_state["messages"].append({"role": "user", "content": question})
    st.session_state["pending_question"] = question

# If a pending question exists, generate a response
if st.session_state.get("pending_question"):
    pending = st.session_state["pending_question"]

    if uploaded_file:
        docs = retrieve_docs(pending)
        answer = answer_question(pending, docs)
    else:
        answer = answer_question_no_docs_uploaded(pending)

    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    st.session_state["messages"].append({"role": "assistant", "content": answer})

    # Clear pending question after responding
    st.session_state["pending_question"] = None

# Display all messages in chat
if "messages" in st.session_state:
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])
