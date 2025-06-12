import streamlit as st
import fitz  # PyMuPDF
import openai
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="ClearText AI", layout="centered")

st.title("🧠 ClearText AI")
st.write("Nahraj dokument alebo napíš text a vyber typ analýzy.")
# Výber typu analýzy
typ = st.selectbox("Vyber typ analýzy", [
    "Zhrnutie obsahu",
    "Vysvetlenie pre študenta",
    "Kontrola zmluvy"
])
# Nahrať súbor alebo manuálny text
uploaded_file = st.file_uploader("Nahraj súbor (.pdf alebo .txt)", type=["pdf", "txt"])
manual_input = st.text_area("Alebo vlož text ručne")

text = ""
if uploaded_file is not None:
    if uploaded_file.name.endswith(".pdf"):
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()
    elif uploaded_file.name.endswith(".txt"):
        text = uploaded_file.read().decode("utf-8")

elif manual_input:
    text = manual_input
# Spustiť analýzu
if st.button("Analyzovať") and text:
    with st.spinner("Spracúvam text pomocou AI..."): 
#Skladanie promtu
        user_prompt = f"{typ}:\n\n{text}"

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You simplify and explain documents based on context."},
                {"role": "user", "content": user_prompt}
],
            temperature=0.5
        )

        result = response["choices"][0]["message"]["content"]
        st.subheader("📝 Výstup:")
        st.write(result) 
elif st.button ("Analyzovať", key="analyzuj_btn") and not text:
    st.warning("Najprv nahraj súbor alebo zadaj text.")
