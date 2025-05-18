import streamlit as st
from plush_utils import export_full_report, STYLE_PRESETS, load_docx, rtf_to_text, generate_docx, generate_pdf

st.set_page_config(page_title="Full Report", layout="wide")
st.title("📦 Full Report")

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

style = st.selectbox("Style Preset", list(STYLE_PRESETS.keys()))
if st.button("📦 Generate Full Report"):
    full = export_full_report(raw, style)
    st.subheader("📦 Full Report")
    st.text_area("", full, height=400)
    st.download_button("Download .txt", full, "full_report.txt")
    st.download_button("Download .docx", generate_docx("Full Report", full), "full_report.docx")
    st.download_button("Download .pdf", generate_pdf("Full Report", full), "full_report.pdf")