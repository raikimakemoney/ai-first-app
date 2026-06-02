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

question = ""

if uploaded_files:
    for uploaded_file in uploaded_files:

        pdf_text += f"\n\n===== ファイル名: {uploaded_file.name} =====\n\n"

        reader = PdfReader(uploaded_file)

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pdf_text += text + "\n"

if pdf_text:

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📄 要約"):
            question = "この資料を3点にまとめて要約してください"

    with col2:
        if st.button("⭐ 重要ポイント"):
            question = "この資料の重要ポイントを5つ挙げてください"

    with col3:
        if st.button("🎓 予想問題"):
            question = "この資料から試験に出そうな問題を5問作成してください"   

    with col4:
        if st.button("📝 レポート"):
            question = "この資料をもとに、大学提出用の500字程度のレポートを作成してください。単なる要約ではなく、内容の考察や重要性にも触れてください。"                             

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("履歴を削除"):
    st.session_state.messages = []
    st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_question = st.chat_input("質問してください")

if user_question:
    question = user_question

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
       