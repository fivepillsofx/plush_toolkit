import streamlit as st
from plush_utils import templates, generate_docx, generate_pdf

st.set_page_config(page_title="Templates", layout="wide")
st.title("📑 Templates Library")

choice = st.selectbox("Pick a template", list(templates.keys()))

if st.button("Show Template"):
    tpl = templates[choice]
    st.subheader(f"📑 {choice}")
    st.text_area("", tpl, height=400)
    st.download_button("Download .txt", tpl, f"{choice}.txt")
    st.download_button("Download .docx", generate_docx(choice, tpl), f"{choice}.docx")
    st.download_button("Download .pdf", generate_pdf(choice, tpl), f"{choice}.pdf")