import streamlit as st
from plush_utils import dialogue_by_character, load_docx, rtf_to_text

st.set_page_config(page_title="Dialogue by Character", layout="wide")
st.title("🧍 Dialogue by Character")

uploaded = st.file_uploader("Upload `.txt`, `.docx`, or `.rtf`", type=["txt","docx","rtf"])
if uploaded:
    ext = uploaded.name.split(".")[-1].lower()
    raw = (
        uploaded.read().decode("utf-8")
        if ext=="txt" else
        load_docx(uploaded)
        if ext=="docx" else
        rtf_to_text(uploaded.read().decode("utf-8"))
    )
else:
    raw = st.text_area("Or paste your text here:", height=300)

if st.button("🧍 Show Dialogue by Character"):
    report = dialogue_by_character(raw)
    st.subheader("🧍 Dialogue by Character")
    st.text_area("", report, height=300)
    st.download_button("Download .txt", report, "by_character.txt")