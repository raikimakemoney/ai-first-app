import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
from pypdf import PdfReader

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("Raiki AI")

uploaded_file = st.file_uploader(
    "PDFをアップロードしてください",
    type="pdf"
)

pdf_text = ""

if uploaded_file:
    reader = PdfReader(uploaded_file)

    for page in reader.pages:
        pdf_text += page.extract_text() + "\n"

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("履歴を削除"):
    st.session_state.messages = []
    st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("質問してください")

if question:
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.write(question)

    response = client.responses.create(
    model="gpt-5-mini",
    input=f"""
以下のPDF内容を参考にして回答してください。

PDF内容:
{pdf_text}

質問:
{question}
"""
)

    answer = response.output_text

    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.write(answer)
       