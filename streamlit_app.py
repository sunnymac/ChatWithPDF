import streamlit as st
import requests

import requests
import streamlit as st

st.title("📄 PDF Chatbot")

# ✅ File Upload Section
st.subheader("📤 Upload a new PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    with st.spinner("Uploading PDF..."):
        response = requests.post(
            "http://127.0.0.1:8000/upload_pdf",
            files={"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        )
        if response.status_code == 200:
            st.success("✅ PDF uploaded and processed successfully!")
        else:
            st.error("❌ Failed to upload PDF.")



st.set_page_config(page_title="Local PDF Chatbot", layout="wide")

st.title("📄 Local PDF Chatbot (Fully Offline)")

# Session for chat history
if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("Ask a question about the PDF:")

if st.button("Ask"):
    if query:
        with st.spinner("Generating answer..."):
            response = requests.post("http://127.0.0.1:8000/chat", data={"query": query})
            answer = response.json()['answer']
            st.session_state.history.append((query, answer))

# Display chat history
for q, a in st.session_state.history[::-1]:
    st.markdown(f"**You:** {q}")
    st.markdown(f"**Chatbot:** {a}")
    st.markdown("---")
