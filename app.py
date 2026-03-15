# Action	Command
# Activate venv	: venv/Scripts/activate
# Exit venv: deactivate
# Run Streamlit	: streamlit run app.py
# Stop Streamlit : CTRL + C



import streamlit as st
from PyPDF2 import PdfReader
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not found in .env file")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

st.title("AI PDF Summarizer")

def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""
    return text

def chunk_text(text, chunk_size=4000):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    return chunks

def summarize_chunk(chunk, chunk_number):
    prompt = f"""
You are helping a student study.

Summarize this PDF chunk clearly.

Give:
1. Short summary
2. Key concepts
3. Important points
4. Possible exam questions

Chunk {chunk_number}:
{chunk}
"""
    response = model.generate_content(prompt)
    return response.text

def final_summary(chunk_summaries):
    combined = "\n\n".join(chunk_summaries)

    prompt = f"""
Below are summaries of different chunks of a PDF.

Create a final combined result in this format:

1. Short Summary
2. Key Concepts
3. Important Points
4. Possible Exam Questions

Chunk summaries:
{combined}
"""
    response = model.generate_content(prompt)
    return response.text

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if st.button("Generate Summary"):
    if uploaded_file is None:
        st.warning("Please upload a PDF first.")
    else:
        with st.spinner("Extracting text from PDF..."):
            text = extract_text_from_pdf(uploaded_file)

        if not text.strip():
            st.warning("No readable text found in this PDF.")
        else:
            chunks = chunk_text(text)

            chunk_summaries = []
            with st.spinner("Summarizing PDF in chunks..."):
                for i, chunk in enumerate(chunks, start=1):
                    summary = summarize_chunk(chunk, i)
                    chunk_summaries.append(summary)

            with st.spinner("Creating final summary..."):
                result = final_summary(chunk_summaries)

            st.subheader("AI Summary")
            st.write(result)