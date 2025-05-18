import streamlit as st
from plush_utils import extract_dialogue, load_docx, rtf_to_text

st.set_page_config(page_title="Extract Dialogue", layout="wide")
st.title("🗣 Extract Dialogue")

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

if st.button("🗣 Extract Dialogue"):
    dialogue = extract_dialogue(raw)
    st.subheader("🗣 Extracted Dialogue")
    st.text_area("", dialogue, height=300)
    st.download_button("Download .txt", dialogue, "dialogue.txt")