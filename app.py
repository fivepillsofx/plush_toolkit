import os, re, random, streamlit as st
from io import BytesIO
from collections import Counter
from datetime import datetime
from nltk.data import find
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
import nltk, textstat
from docx import Document as DocxDocument
from striprtf.striprtf import rtf_to_text
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from plush_utils import (
    clean_text, analyze_text, extract_dialogue, dialogue_by_character,
    find_cliches, export_full_report, generate_names,
    load_docx, generate_docx, generate_pdf, STYLE_PRESETS, templates
)

# Ensure NLTK data
def ensure_nltk():
    try: find("tokenizers/punkt")
    except: nltk.download("punkt", quiet=True)
    try: find("corpora/stopwords")
    except: nltk.download("stopwords", quiet=True)
ensure_nltk()

def main():
    st.set_page_config(page_title="🧠 Plush Toolkit", layout="wide")
    tools = [
        "Home","Clean Text","Analyze Text","Extract Dialogue",
        "Dialogue by Character","Cliché Buster","Full Report",
        "Character Name Generator","Templates"
    ]
    choice = st.sidebar.radio("Select a tool", tools)
    c = st.container()

    if choice == "Home":
        c.title("📚 Plush: The Writer Toolkit")
        c.write("Welcome! Use the sidebar to pick a tool.")

    elif choice == "Clean Text":
        c.title("🧼 Clean Text")
        f = c.file_uploader("Upload .txt/.docx/.rtf", type=["txt","docx","rtf"])
        if f:
            ext = f.name.split(".")[-1].lower()
            raw = (f.read().decode() if ext=="txt" else load_docx(f))
        else:
            raw = c.text_area("Or paste your text here:", height=300)
        if c.button("Clean"):
            out = clean_text(raw)
            c.subheader("✅ Cleaned Text")
            c.text_area("", out, height=300)
            c.download_button("Download .txt", out, "cleaned.txt")
            c.download_button("Download .docx", generate_docx("Cleaned", out), "cleaned.docx")
            c.download_button("Download .pdf", generate_pdf("Cleaned", out), "cleaned.pdf")

    elif choice == "Analyze Text":
        c.title("🔍 Analyze Text")
        f = c.file_uploader("Upload .txt/.docx/.rtf", type=["txt","docx","rtf"])
        if f:
            ext = f.name.split(".")[-1].lower()
            raw = (f.read().decode() if ext=="txt" else load_docx(f))
        else:
            raw = c.text_area("Or paste your text here:", height=300)
        style = c.selectbox("Style Preset", list(STYLE_PRESETS.keys()))
        if c.button("Analyze"):
            rpt = analyze_text(raw, style)
            c.subheader("📊 Analysis Report")
            c.text_area("", rpt, height=400)
            c.download_button("Download .txt", rpt, "report.txt")
            c.download_button("Download .docx", generate_docx("Report", rpt), "report.docx")
            c.download_button("Download .pdf", generate_pdf("Report", rpt), "report.pdf")

    elif choice == "Extract Dialogue":
        c.title("🗣 Extract Dialogue")
        f = c.file_uploader("Upload .txt/.docx/.rtf", type=["txt","docx","rtf"])
        if f:
            ext = f.name.split(".")[-1].lower()
            raw = (f.read().decode() if ext=="txt" else load_docx(f))
        else:
            raw = c.text_area("Or paste your text here:", height=300)
        if c.button("Extract"):
            dlg = extract_dialogue(raw)
            c.subheader("🗣 Dialogue")
            c.text_area("", dlg, height=300)
            c.download_button("Download .txt", dlg, "dialogue.txt")

    elif choice == "Dialogue by Character":
        c.title("🧍 Dialogue by Character")
        f = c.file_uploader("Upload .txt/.docx/.rtf", type=["txt","docx","rtf"])
        if f:
            ext = f.name.split(".")[-1].lower()
            raw = (f.read().decode() if ext=="txt" else load_docx(f))
        else:
            raw = c.text_area("Or paste your text here:", height=300)
        if c.button("Show"):
            rep = dialogue_by_character(raw)
            c.subheader("🧍 By Character")
            c.text_area("", rep, height=300)
            c.download_button("Download .txt", rep, "by_character.txt")

    elif choice == "Cliché Buster":
        c.title("💣 Cliché Buster")
        f = c.file_uploader("Upload .txt/.docx/.rtf", type=["txt","docx","rtf"])
        if f:
            ext = f.name.split(".")[-1].lower()
            raw = (f.read().decode() if ext=="txt" else load_docx(f))
        else:
            raw = c.text_area("Or paste your text here:", height=300)
        if c.button("Bust"):
            rep = find_cliches(raw)
            c.subheader("💣 Clichés")
            c.text_area("", rep, height=300)
            c.download_button("Download .txt", rep, "cliches.txt")

    elif choice == "Full Report":
        c.title("📦 Full Report")
        f = c.file_uploader("Upload .txt/.docx/.rtf", type=["txt","docx","rtf"])
        if f:
            ext = f.name.split(".")[-1].lower()
            raw = (f.read().decode() if ext=="txt" else load_docx(f))
        else:
            raw = c.text_area("Or paste your text here:", height=300)
        style = c.selectbox("Style Preset", list(STYLE_PRESETS.keys()))
        if c.button("Generate"):
            fr = export_full_report(raw, style)
            c.subheader("📦 Report")
            c.text_area("", fr, height=400)
            c.download_button("Download .txt", fr, "full_report.txt")
            c.download_button("Download .docx", generate_docx("Full Report", fr), "full_report.docx")
            c.download_button("Download .pdf", generate_pdf("Full Report", fr), "full_report.pdf")

    elif choice == "Character Name Generator":
        c.title("🎲 Character Name Generator")
        gender = c.selectbox("Gender", ["Any", "Male", "Female"])
        rarity = c.selectbox("Rarity", ["Common", "Rare"])
        count = c.number_input("How many?", 1, 10, 5)
        if c.button("Generate"):
            names = generate_names(gender, rarity, count)
            c.subheader("🎲 Names")
            for n in names: c.write(f"- {n}")

    elif choice == "Templates":
        c.title("📑 Templates Library")
        tpl = c.selectbox("Template", list(templates.keys()))
        if c.button("Show"):
            content = templates[tpl]
            c.subheader(f"📑 {tpl}")
            c.text_area("", content, height=400)
            c.download_button("Download .txt", content, f"{tpl}.txt")
            c.download_button("Download .docx", generate_docx(tpl, content), f"{tpl}.docx")
            c.download_button("Download .pdf", generate_pdf(tpl, content), f"{tpl}.pdf")

if __name__ == "__main__":
    main()