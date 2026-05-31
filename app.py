import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
from pypdf import PdfReader

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("Raiki AI")

uploaded_files = st.file_uploader(
    "PDFをアップロードしてください",
    type="pdf",
    accept_multiple_files=True
)

pdf_text = ""

if uploaded_files:
    for uploaded_file in uploaded_files:

        pdf_text += f"\n\n===== ファイル名: {uploaded_file.name} =====\n\n"

        reader = PdfReader(uploaded_file)

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pdf_text += text + "\n"

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

    if pdf_text:
        prompt = f"""
あなたはPDF資料を読む専門アシスタントです。
必ず以下のPDF内容だけを根拠にして答えてください。
PDFに書かれていないことは、推測せず「PDF内には明記されていません」と答えてください。

回答ルール:
- まず結論を短く答える
- 次に根拠をPDF内容に沿って説明する
- 箇条書きでわかりやすくする
- 日本語で答える

PDF内容:
{pdf_text}

ユーザーの質問:
{question}
"""
    else:
        prompt = f"""
あなたは親切なAIアシスタントです。
日本語でわかりやすく答えてください。

ユーザーの質問:
{question}
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    answer = response.output_text

    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.write(answer)
       