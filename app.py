import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

st.title("Raiki AI")

question = st.text_input("質問してください")

if question:
    response = client.responses.create(
        model="gpt-5-mini",
        input=question
    )

    st.write(response.output_text)