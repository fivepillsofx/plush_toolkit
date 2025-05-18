
import streamlit as st
from plush_utils import analyze_text, STYLE_PRESETS, load_docx, rtf_to_text, generate_docx, generate_pdf

st.set_page_config(page_title="Analyze Text")
st.title("Analyze Analyze Text")

uploaded = st.file_uploader("Upload .txt, .docx, or .rtf", type=["txt","docx","rtf"])
if uploaded:
    ext=uploaded.name.split(".")[-1].lower()
    if ext=="txt": raw=uploaded.read().decode()
    elif ext=="docx": raw=load_docx(uploaded)
    else: raw=rtf_to_text(uploaded.read().decode())
else:
    raw=st.text_area("Or paste here", height=300)

if st.button("Analyze"):
    report=analyze_text(raw, style)
    st.text_area('', report, height=400)
