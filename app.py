import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
from pypdf import PdfReader

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("📚 Raiki AI")
st.caption("PDF学習・試験対策アシスタント")

st.info(
    "📚 PDFをアップロードして、要約・試験対策・レポート作成・PDF比較ができます"
)

st.sidebar.title("📚 Raiki AI")

st.sidebar.markdown("---")
st.sidebar.write("🧑‍💻 Created by Raiki")

uploaded_files = st.file_uploader(
    "PDFをアップロードしてください",
    type="pdf",
    accept_multiple_files=True
)

pdf_text = ""

question = ""

if uploaded_files:
    st.sidebar.write(f"📄 PDF数: {len(uploaded_files)}")

if uploaded_files:
    for uploaded_file in uploaded_files:

        pdf_text += f"\n\n===== ファイル名: {uploaded_file.name} =====\n\n"

        reader = PdfReader(uploaded_file)

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pdf_text += text + "\n"

if uploaded_files:
    st.success(f"{len(uploaded_files)}個のPDFを読み込みました")

    st.write("アップロード中のPDF")

    for uploaded_file in uploaded_files:
        st.write(f"✅ {uploaded_file.name}")

        if st.button(f"📄 {uploaded_file.name} を要約"):
            question = f"{uploaded_file.name} の内容だけを3点にまとめて要約してください"

if pdf_text:

    st.subheader("📚 学習モード")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📄 要約"):
            question = "この資料を3点にまとめて要約してください"

    with col2:
        if st.button("⭐ 重要ポイント"):
            question = "この資料の重要ポイントを5つ挙げてください"

    with col3:
        if st.button("📚 単語帳"):
            question = """
この資料から重要語句を20個抽出してください。

以下の形式で出力してください。

用語：
説明：

試験前に暗記しやすいように簡潔にまとめてください。
"""

    with col4:
        if st.button("⚡ 試験直前"):
            question = """
この資料について試験直前用のまとめを作成してください。

以下の形式で出力してください。

1. 絶対覚えるべき内容5個
2. 頻出キーワード10個
3. 3分で読める超要約
4. テストで引っかかりやすいポイント

できるだけ短く実践的にまとめてください。
"""

    st.subheader("🎓 試験対策モード")

    col5, col6 = st.columns(2)

    with col5:
        if st.button("🎓 予想問題"):
            question = "この資料から試験に出そうな問題を5問作成してください"

    with col6:
        if st.button("🧠 完全試験対策"):
            question = """
この資料をもとに試験対策を作成してください。

以下を出力してください。

1. 重要語句20個
2. 一問一答10問
3. 記述問題5問
4. 試験に出そうなポイント5個
5. 最後に3分で復習できる要約

見やすく整理して日本語で出力してください。
"""

    st.subheader("📝 レポートモード")

    col7, col8 = st.columns(2)

    with col7:
        if st.button("📝 レポート"):
            question = "この資料をもとに、大学提出用の500字程度のレポートを作成してください。単なる要約ではなく、内容の考察や重要性にも触れてください。"

    with col8:
        if st.button("✍️ 自然なレポート"):
            question = "この資料をもとに、大学提出用の500字程度のレポートを作成してください。AIが書いたような硬すぎる文章ではなく、大学生が自分で書いたような自然で少し口語的な文体にしてください。ただし内容は薄くせず、単なる要約ではなく、自分の経験や具体例、考察も含めてください。"

    st.subheader("🔍 分析モード")

    if st.button("🔍 PDF比較"):
        question = "アップロードされた複数のPDFを比較してください。それぞれのPDFごとの内容、共通点、違い、重要な変化をわかりやすく整理してください。最後に、試験やレポートで重要になりそうな観点もまとめてください。"


if "messages" not in st.session_state:
    st.session_state.messages = []

st.sidebar.write(f"💬 チャット数: {len(st.session_state.messages)}")

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

    with st.spinner("AIが考えています..."):

       response = client.responses.create(
           model="gpt-5-mini",
           input=prompt
    )

    answer = response.output_text

    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.write(answer)
       