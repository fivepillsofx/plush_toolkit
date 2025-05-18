import streamlit as st
from plush_utils import find_cliches, load_docx, rtf_to_text

st.set_page_config(page_title="Cliché Buster", layout="wide")
st.title("💣 Cliché Buster")

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

if st.button("💣 Find Clichés"):
    report = find_cliches(raw)
    st.subheader("💣 Clichés Found")
    st.text_area("", report, height=300)
    st.download_button("Download .txt", report, "cliches.txt")