from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import faiss
import numpy as np
import pickle
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import ollama

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load saved data
print("🔵 Loading vector store and data...")
index = faiss.read_index('app/vector_store.index')

with open('app/embeddings.npy', 'rb') as f:
    embeddings = np.load(f)

with open('app/chunks.pkl', 'rb') as f:
    chunks = pickle.load(f)

with open('app/extracted_text.pkl', 'rb') as f:
    extracted_text = pickle.load(f)

print("✅ Vector store and data loaded successfully.")

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!"}

@app.post("/chat")
async def chat(query: str = Form(...)):
    print(f"\n🟢 Received query: {query}")

    # Step 1: Create embedding for the query
    query_embedding = embedding_model.encode([query])

    # Step 2: Search in vector store
    distances, indices = index.search(np.array(query_embedding).astype('float32'), k=3)

    print("\n🔍 Top 3 most relevant chunks found:")

    context = ""
    for i, idx in enumerate(indices[0]):
        print(f"\n🔹 Result {i+1}:")
        print(f"📏 Distance: {distances[0][i]}")
        print(f"📝 Chunk:\n{chunks[idx]}")
        context += chunks[idx] + "\n"

    # Step 3: Query local LLM via Ollama
    print("\n⏳ Querying local model via Ollama...")
    ollama_response = ollama.chat(model='llama3', messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
    ])
    answer = ollama_response['message']['content']

    print(f"\n🟢 Final Answer: {answer}")
    return {"answer": answer}

# ✅ PDF Upload and Auto-Processing
@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    print(f"\n📥 Received file: {file.filename}")

    # Read PDF content
    pdf_bytes = await file.read()
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")

    full_text = ""
    for page in pdf_document:
        full_text += page.get_text()

    # Save the extracted text
    with open("app/extracted_text.pkl", "wb") as f:
        pickle.dump(full_text, f)

    print("📦 Starting text chunking...")
    chunk_size = 500
    chunk_overlap = 50
    words = full_text.split()
    chunks_local = []

    for i in range(0, len(words), chunk_size - chunk_overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks_local.append(chunk)

    print(f"✅ Chunking completed. Total chunks created: {len(chunks_local)}")

    # Save the chunks
    with open('app/chunks.pkl', 'wb') as f:
        pickle.dump(chunks_local, f)

    print("🔵 Creating embeddings for each chunk...")
    embeddings_local = embedding_model.encode(chunks_local, show_progress_bar=True)

    # Save embeddings
    with open('app/embeddings.npy', 'wb') as f:
        np.save(f, embeddings_local)

    print("✅ Embeddings created. Shape:", embeddings_local.shape)

    # Build and save FAISS index
    new_index = faiss.IndexFlatL2(embeddings_local.shape[1])
    new_index.add(np.array(embeddings_local).astype('float32'))
    faiss.write_index(new_index, 'app/vector_store.index')

    print("✅ Vector store updated and saved successfully.")

    # ✅ Refresh the in-memory variables
    global index, embeddings, chunks
    index = new_index
    embeddings = embeddings_local
    chunks = chunks_local

    return {"message": "PDF uploaded and fully processed successfully."}
