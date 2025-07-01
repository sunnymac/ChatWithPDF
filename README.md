# PDF Question Answering Chatbot (Fully Local & Offline)

A fully local, free, and offline chatbot that allows you to upload PDF files and ask questions about their content.  
Built using **Ollama (Llama 3)**, **FAISS**, **FastAPI**, and **Streamlit** with **no internet required, no API keys, and no chat limits.**

---

## Features

- 📂 Upload any **PDF file**
- 💬 Ask unlimited questions about the uploaded PDF
- 🧐 Uses **local Llama 3 model** via Ollama
- ⚡ Fast search with **FAISS vector store**
- 🔐 100% offline and fully local
- ✅ Works without API keys or rate limits

---

## Project Structure

```text
pdf_chatbot/
├── venv/                   # Python virtual environment
├── app/                    # FastAPI backend
│   ├── __init__.py
│   ├── main.py             # Backend server
│   ├── vector_store.index  # Saved FAISS index
│   ├── embeddings.npy      # Saved embeddings
│   ├── chunks.pkl          # Saved text chunks
│   └── extracted_text.pkl  # Saved extracted text
├── streamlit_app.py        # Frontend UI
└── sample.pdf              # Example PDF
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/sunnymac/ChatWithPDF.git
cd ChatWithPDF
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** If you don’t have a `requirements.txt` file, here are the libraries:

```bash
pip install fastapi uvicorn streamlit faiss-cpu sentence-transformers pymupdf python-multipart requests ollama
```

### 4. Start Ollama

```bash
ollama serve
ollama pull llama3  # Download Llama 3 model
```

---

## Running the Project

### Start Backend (FastAPI)

```bash
uvicorn app.main:app --reload
```

### Start Frontend (Streamlit)

```bash
streamlit run streamlit_app.py
```

---

## Usage Flow

1. Upload PDF using the sidebar in the Streamlit UI.
2. System extracts text, chunks it, and saves embeddings.
3. Ask any question based on the uploaded PDF.
4. The system retrieves relevant chunks using FAISS and sends them to the local Llama 3 model via Ollama.
5. Answers are displayed in real-time in the chat interface.

---

## Tech Stack

- **Frontend:** Streamlit
- **Backend:** FastAPI, Uvicorn
- **Vector Database:** FAISS
- **Embedding Model:** SentenceTransformers (all-MiniLM-L6-v2)
- **PDF Processing:** PyMuPDF (fitz)
- **LLM:** Ollama (Llama 3)

---

## Common Errors & Fixes

| Problem                 | Solution                                                                         |
| ----------------------- | -------------------------------------------------------------------------------- |
| `ModuleNotFoundError`   | Run: `pip install <module-name>` inside virtual env                              |
| Ollama connection error | Make sure Ollama is running: `ollama serve`                                      |
| File upload error       | Run: `pip install python-multipart`                                              |
| FastAPI not loading     | Ensure you are in the correct directory and use: `uvicorn app.main:app --reload` |

---

## Quick Setup Command

```bash
pip install -r requirements.txt
```

Use this to install all required packages in one go.

---

## Contribution

If you want to improve this project, feel free to fork it, create pull requests, or report issues.

---

## License

This project is completely free and open-source.

---

## Contact

If you need help or have questions, feel free to reach out via GitHub issues.
