import streamlit as st
from PyPDF2 import PdfReader
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

st.title("AI PDF Summarizer")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

text = ""

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    # st.subheader("Extracted Text")
    # st.write(text[:2000])

if st.button("Generate Summary"):
    if not text.strip():
        st.warning("Please upload a PDF first.")
    else:
        prompt = f"""
Summarize the following study material.

Also provide:
1. Short summary
2. Key concepts
3. Possible exam questions

Text:
{text[:6000]}
"""

        with st.spinner("Generating summary..."):
            response = model.generate_content(prompt)

        st.subheader("AI Summary")
        st.write(response.text)