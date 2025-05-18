import streamlit as st
import os
import re
import random
from io import BytesIO
from collections import Counter
from datetime import datetime
import nltk
from nltk.data import find
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
import textstat
from docx import Document as DocxDocument
from striprtf.striprtf import rtf_to_text
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from plush_utils import (
    clean_text, analyze_text, extract_dialogue, dialogue_by_character,
    find_cliches, export_full_report, generate_names,
    load_docx, generate_docx, generate_pdf, STYLE_PRESETS
)

# ── Ensure NLTK Data ────────────────────────────────────────
def ensure_nltk_data():
    try:
        find("tokenizers/punkt")
    except:
        nltk.download("punkt", quiet=True)
    try:
        find("corpora/stopwords")
    except:
        nltk.download("stopwords", quiet=True)

ensure_nltk_data()

# ── Last-name support ────────────────────────────────────────
COMMON_LAST_NAMES = [
    "Smith","Johnson","Williams","Brown","Jones","Miller","Davis",
    "Garcia","Rodriguez","Wilson","Martinez","Anderson","Taylor"
]
RARE_LAST_NAMES = [
    "Hawthorne","Lockwood","Fairchild","Blackwood","Ashford",
    "Everhart","Sterling","Winslow","Briarwood","Thornfield"
]
def generate_last_names(rarity, count):
    pool = RARE_LAST_NAMES if rarity == "Rare" else COMMON_LAST_NAMES
    return random.sample(pool, min(count, len(pool)))

# ── Main App ────────────────────────────────────────────────
def main():
    st.set_page_config(page_title="Plush Toolkit", layout="wide")

    tools = [
        "Home",
        "Clean Text",
        "Analyze Text",
        "Extract Dialogue",
        "Dialogue by Character",
        "Cliché Buster",
        "Full Report",
        "Character Name Generator",
        "Templates"
    ]

    # Initialize session state
    if "active_tool" not in st.session_state:
        st.session_state.active_tool = "Home"

    # Sidebar buttons
    for t in tools:
        if st.sidebar.button(t):
            st.session_state.active_tool = t

    choice = st.session_state.active_tool
    c = st.container()

    # ── HOME ───────────────────────────────────────────────
    if choice == "Home":
        # If you have a logo file in your repo, uncomment next line:
        # c.image("plush-logo.png", width=200)

        c.markdown("## Plush: Your Storytelling Sidekick")
        c.markdown("> *Soft on the surface, sharp on the scene.*")

        c.markdown("**What you can do with Plush:**")
        c.markdown("""
         🧼  **Clean Text** — Strip out noise and normalize quotes  
         🔍  **Analyze Text** — Readability, passive-voice, long-sentence alerts  
         🗣  **Extract Dialogue** — Pull every line of spoken text  
         💣  **Cliché Buster** — Hunt down tired clichés  
         🎲  **Name Generator** — Instant first & last names (10 by default!)  
         📦  **Full Report** — All of the above in one handy download  
        """)

        c.markdown("**Quick Start:**")
        c.markdown("""
        1. Click **Clean Text** and upload or paste your manuscript.  
        2. Head to **Analyze Text** for deep stats & suggestions.  
        3. Export your files or explore names & templates!
        """)

        c.markdown(
            "---\n"
            "[🔗 Visit writtenbybc.com](https://www.writtenbybc.com) • "
            "[🐙 GitHub](https://github.com/fivepillsofx/plush_toolkit)"
        )

    # ── CLEAN TEXT ────────────────────────────────────────
    elif choice == "Clean Text":
        c.title("🧼 Clean Text")
        f = c.file_uploader("Upload `.txt`, `.docx`, or `.rtf`", type=["txt","docx","rtf"])
        if f:
            ext = f.name.split(".")[-1].lower()
            raw = (
                f.read().decode("utf-8")
                if ext == "txt"
                else load_docx(f)
                if ext == "docx"
                else rtf_to_text(f.read().decode("utf-8"))
            )
        else:
            raw = c.text_area("Or paste your text here:", height=300)
        if c.button("🧼 Clean", key="clean"):
            out = clean_text(raw)
            c.subheader("✅ Cleaned Text")
            c.text_area("", out, height=300)
            c.download_button("Download .txt", out, "cleaned.txt")
            c.download_button("Download .docx", generate_docx("Cleaned Text", out), "cleaned.docx")
            c.download_button("Download .pdf", generate_pdf("Cleaned Text", out), "cleaned.pdf")

    # ── ANALYZE TEXT ───────────────────────────────────────
    elif choice == "Analyze Text":
        c.title("🔍 Analyze Text")
        f = c.file_uploader("Upload `.txt`, `.docx`, or `.rtf`", type=["txt","docx","rtf"])
        if f:
            ext = f.name.split(".")[-1].lower()
            raw = (
                f.read().decode("utf-8")
                if ext == "txt"
                else load_docx(f)
                if ext == "docx"
                else rtf_to_text(f.read().decode("utf-8"))
            )
        else:
            raw = c.text_area("Or paste your text here:", height=300)
        style = c.selectbox("Style Preset", list(STYLE_PRESETS.keys()))
        if c.button("🔍 Analyze", key="analyze"):
            rpt = analyze_text(raw, style)
            c.subheader("📊 Analysis Report")
            c.text_area("", rpt, height=400)
            c.download_button("Download .txt", rpt, "report.txt")
            c.download_button("Download .docx", generate_docx("Analysis Report", rpt), "analysis.docx")
            c.download_button("Download .pdf", generate_pdf("Analysis Report", rpt), "analysis.pdf")

    # ── EXTRACT DIALOGUE ───────────────────────────────────
    elif choice == "Extract Dialogue":
        c.title("🗣 Extract Dialogue")
        f = c.file_uploader("Upload `.txt`, `.docx`, or `.rtf`", type=["txt","docx","rtf"])
        if f:
            ext = f.name.split(".")[-1].lower()
            raw = (
                f.read().decode("utf-8")
                if ext == "txt"
                else load_docx(f)
                if ext == "docx"
                else rtf_to_text(f.read().decode("utf-8"))
            )
        else:
            raw = c.text_area("Or paste your text here:", height=300)
        if c.button("🗣 Extract", key="extract"):
            dlg = extract_dialogue(raw)
            c.subheader("🗣 Extracted Dialogue")
            c.text_area("", dlg, height=300)
            c.download_button("Download .txt", dlg, "dialogue.txt")

    # ── DIALOGUE BY CHARACTER ─────────────────────────────
    elif choice == "Dialogue by Character":
        c.title("🧍 Dialogue by Character")
        f = c.file_uploader("Upload `.txt`, `.docx`, or `.rtf`", type=["txt","docx","rtf"])
        if f:
            ext = f.name.split(".")[-1].lower()
            raw = (
                f.read().decode("utf-8")
                if ext == "txt"
                else load_docx(f)
                if ext == "docx"
                else rtf_to_text(f.read().decode("utf-8"))
            )
        else:
            raw = c.text_area("Or paste your text here:", height=300)
        if c.button("🧍 Show", key="by_char"):
            rep = dialogue_by_character(raw)
            c.subheader("🧍 Dialogue by Character")
            c.text_area("", rep, height=300)
            c.download_button("Download .txt", rep, "by_character.txt")

    # ── CLICHÉ BUSTER ─────────────────────────────────────
    elif choice == "Cliché Buster":
        c.title("💣 Cliché Buster")
        f = c.file_uploader("Upload `.txt`, `.docx`, or `.rtf`", type=["txt","docx","rtf"])
        if f:
            ext = f.name.split(".")[-1].lower()
            raw = (
                f.read().decode("utf-8")
                if ext == "txt"
                else load_docx(f)
                if ext == "docx"
                else rtf_to_text(f.read().decode("utf-8"))
            )
        else:
            raw = c.text_area("Or paste your text here:", height=300)
        if c.button("💣 Bust", key="bust"):
            rep = find_cliches(raw)
            c.subheader("💣 Clichés Found")
            c.text_area("", rep, height=300)
            c.download_button("Download .txt", rep, "cliches.txt")

    # ── FULL REPORT ────────────────────────────────────────
    elif choice == "Full Report":
        c.title("📦 Full Report")
        f = c.file_uploader("Upload `.txt`, `.docx`, or `.rtf`", type=["txt","docx","rtf"])
        if f:
            ext = f.name.split(".")[-1].lower()
            raw = (
                f.read().decode("utf-8")
                if ext == "txt"
                else load_docx(f)
                if ext == "docx"
                else rtf_to_text(f.read().decode("utf-8"))
            )
        else:
            raw = c.text_area("Or paste your text here:", height=300)
        style = c.selectbox("Style Preset", list(STYLE_PRESETS.keys()))
        if c.button("Generate Report", key="full_report"):
            fr = export_full_report(raw, style)
            c.subheader("📦 Full Report")
            c.text_area("", fr, height=400)
            c.download_button("Download .txt", fr, "full_report.txt")
            c.download_button("Download .docx", generate_docx("Full Report", fr), "full_report.docx")
            c.download_button("Download .pdf", generate_pdf("Full Report", fr), "full_report.pdf")

    # ── CHARACTER NAME GENERATOR ───────────────────────────
    elif choice == "Character Name Generator":
        c.title("🎲 Character Name Generator")
        gender = c.selectbox("Gender", ["Any", "Male", "Female"])
        rarity = c.selectbox("Rarity", ["Common", "Rare"])
        count = c.number_input("How many names?", 1, 10, 10)
        if c.button("🎲 Generate Names", key="make_names"):
            firsts = generate_names(gender, rarity, count)
            lasts = generate_last_names(rarity, count)
            fullns = [f"{f} {l}" for f, l in zip(firsts, lasts)]
            c.subheader("🎲 Generated Names")
            for name in fullns:
                c.write(f"- {name}")

    # ── TEMPLATES ──────────────────────────────────────────
    elif choice == "Templates":
        c.title("📑 Templates Library")
        tpl_choice = c.selectbox("Pick a template", list(templates.keys()))
        if c.button("Show Template", key="show_tpl"):
            t = templates[tpl_choice]
            c.subheader(f"📑 {tpl_choice}")
            c.text_area("", t, height=400)
            c.download_button("Download .txt", t, f"{tpl_choice}.txt")
            c.download_button("Download .docx", generate_docx(tpl_choice, t), f"{tpl_choice}.docx")
            c.download_button("Download .pdf", generate_pdf(tpl_choice, t), f"{tpl_choice}.pdf")

if __name__ == "__main__":
    main()
