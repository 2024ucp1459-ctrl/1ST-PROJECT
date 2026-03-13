import streamlit as st
from PyPDF2 import PdfReader

st.title("AI PDF Summarizer")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file is not None:

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    st.subheader("Extracted Text")

    st.write(text[:2000])