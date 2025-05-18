import streamlit as st
from plush_utils import analyze_text, STYLE_PRESETS, load_docx, rtf_to_text, generate_docx, generate_pdf

st.set_page_config(page_title="Analyze Text", layout="wide")
st.title("🔍 Analyze Text")

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
if st.button("🔍 Analyze"):
    report = analyze_text(raw, style)
    st.subheader("📊 Analysis Report")
    st.text_area("", report, height=400)
    st.download_button("Download .txt", report, "report.txt")
    st.download_button("Download .docx", generate_docx("Analysis Report", report), "analysis.docx")
    st.download_button("Download .pdf", generate_pdf("Analysis Report", report), "analysis.pdf")