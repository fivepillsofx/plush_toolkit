import streamlit as st
from plush_utils import generate_names

st.set_page_config(page_title="Character Name Generator", layout="wide")
st.title("🎲 Character Name Generator")

gender = st.selectbox("Gender", ["Any", "Male", "Female"])
rarity = st.selectbox("Rarity", ["Common", "Rare"])
count  = st.number_input("How many names?", 1, 10, 5)

if st.button("🎲 Generate Names"):
    names = generate_names(gender, rarity, count)
    st.subheader("🎲 Generated Names")
    for n in names:
        st.write(f"- {n}")