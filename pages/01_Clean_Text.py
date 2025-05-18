
import streamlit as st
from plush_utils import clean_text, load_docx, rtf_to_text, generate_docx, generate_pdf

st.set_page_config(page_title="Clean Text")
st.title("Clean Clean Text")

uploaded = st.file_uploader("Upload .txt, .docx, or .rtf", type=["txt","docx","rtf"])
if uploaded:
    ext=uploaded.name.split(".")[-1].lower()
    if ext=="txt": raw=uploaded.read().decode()
    elif ext=="docx": raw=load_docx(uploaded)
    else: raw=rtf_to_text(uploaded.read().decode())
else:
    raw=st.text_area("Or paste here", height=300)

if st.button("Clean Text"):
    out=clean_text(raw)
    st.text_area('', out, height=300)
    st.download_button('.txt',out,'cleaned.txt')
