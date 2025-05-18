
import streamlit as st
from plush_utils import dialogue_by_character, load_docx, rtf_to_text

st.set_page_config(page_title="Dialogue by Character")
st.title("Show Dialogue by Character")

uploaded = st.file_uploader("Upload .txt, .docx, or .rtf", type=["txt","docx","rtf"])
if uploaded:
    ext=uploaded.name.split(".")[-1].lower()
    if ext=="txt": raw=uploaded.read().decode()
    elif ext=="docx": raw=load_docx(uploaded)
    else: raw=rtf_to_text(uploaded.read().decode())
else:
    raw=st.text_area("Or paste here", height=300)

if st.button("Show Dialogue"):
    r=dialogue_by_character(raw)
    st.text_area('', r, height=300)
