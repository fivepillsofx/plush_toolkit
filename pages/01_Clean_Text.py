import streamlit as st
from plush_utils import clean_text, load_docx, rtf_to_text, generate_docx, generate_pdf

st.set_page_config(page_title="Clean Text", layout="wide")
st.title("🧼 Clean Text")

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

if st.button("🧼 Clean"):
    cleaned = clean_text(raw)
    st.subheader("✅ Cleaned Text")
    st.text_area("", cleaned, height=300)
    st.download_button("Download .txt", cleaned, "cleaned.txt")
    st.download_button("Download .docx", generate_docx("Cleaned Text", cleaned), "cleaned.docx")
    st.download_button("Download .pdf", generate_pdf("Cleaned Text", cleaned), "cleaned.pdf")