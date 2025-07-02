import streamlit as st
import pandas as pd
import time
import difflib

# Page config
st.set_page_config(page_title="Smart Nutrition Recommender", layout="centered")

# Light theme & input styling
st.markdown("""
    <style>
    .stApp { background-color: white; color: #6A0DAD; font-family: 'Segoe UI', sans-serif; }
    .stTextInput input { color: #6A0DAD !important; background-color: white; border: 2px solid #6A0DAD; border-radius: 10px; padding: 12px; }
    .stButton > button { background-color: #6A0DAD; color: white; border-radius: 8px; padding: 10px 24px; font-weight: bold; }
    .stButton > button:hover { background-color: #8A2BE2; }
    .stDataFrame table { background-color: white !important; color: #6A0DAD !important; }
    thead tr th { background-color: #f3e5f5 !important; color: #6A0DAD; }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center;'>Smart Nutrition Recommender</h1>", unsafe_allow_html=True)

# Load data
try:
    df = pd.read_csv("smart_nutrition_data.csv")
except FileNotFoundError:
    st.error("CSV not found. Upload `smart_nutrition_data.csv` alongside `app.py`.")
    st.stop()

# Symptom-to-disease map
symptom_map = {
    "left hand pain": "heart disease",
    "chest pain": "heart disease",
    "breathlessness": "heart disease",
    "hair fall": "hair loss",
    "rash": "skin allergy",
    "itchy skin": "skin allergy",
    "fatigue": "iron deficiency",
    "baldness": "hair loss",
    "acne": "hormonal imbalance",
}

# Input
user_input = st.text_input("Enter symptom or condition:", key="main_input").strip().lower()
if user_input in symptom_map:
    user_input = symptom_map[user_input]

# Button
if st.button("Get Recommendation"):
    with st.spinner("Searching..."):
        time.sleep(0.8)

        # Build list of possible matches
        candidates = (
            df['condition'].astype(str).str.lower().tolist()
            + df['gene'].astype(str).str.lower().tolist()
        )
        # Remove empty strings
        candidates = [c for c in candidates if c]

        # Use difflib to find best close match
        matches = difflib.get_close_matches(user_input, candidates, n=1, cutoff=0.6)
        if matches:
            best = matches[0]
            # locate the row
            row = df[
                (df['condition'].str.lower() == best) |
                (df['gene'].str.lower() == best)
            ].iloc[0]
            st.success("Match found:")
            st.dataframe(pd.DataFrame({
                "Condition": [row["condition"]],
                "Gene": [row["gene"]],
                "Foods to Avoid": [row["avoid food"]],
                "Foods to Recommend": [row["recommended food"]],
                "Why Recommended": [row["why_recommended"]],
            }))
        else:
            st.warning("No match found. Try simpler terms like 'heart disease' or 'BRCA1'.")

# Footer
st.markdown("<hr><p style='text-align:center;font-size:13px;'>Built by Madhumirra R</p>", unsafe_allow_html=True)

