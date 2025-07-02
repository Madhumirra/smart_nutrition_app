
import streamlit as st
import pandas as pd
import time
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Set up the page
st.set_page_config(page_title="Smart Nutrition Recommender", layout="centered")

# Load data
try:
    df = pd.read_csv("smart_nutrition_data.csv")
except FileNotFoundError:
    st.error("❗ CSV file not found. Please make sure 'smart_nutrition_data.csv' is in your project folder.")
    st.stop()

# Custom style
st.markdown("""
    <style>
        body, .stApp {
            background-color: white;
            color: #6A0DAD;
            font-family: 'Segoe UI', sans-serif;
        }
        .stTextInput input {
            color: #6A0DAD !important;  /* Violet text */
            background-color: white !important;
            border: 2px solid #6A0DAD;
            border-radius: 10px;
            padding: 10px;
            font-size: 18px;
        }
        .stButton > button {
            background-color: #6A0DAD;
            color: white;
            padding: 10px 20px;
            border-radius: 10px;
            border: none;
            font-weight: bold;
        }
        .stButton > button:hover {
            background-color: #8A2BE2;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center;'>Smart Nutrition Recommender</h1>", unsafe_allow_html=True)

# User input
user_input = st.text_input("Enter the symptom or condition:").strip().lower()
st.write(f"You typed: {user_input}")

# Button click
if st.button("Get Recommendations"):
    with st.spinner("🔍 Searching..."):
        time.sleep(1)

        # Combine condition, gene, and recommended food into a list for matching
        match_list = df['condition'].astype(str).tolist() + \
                     df['gene'].astype(str).tolist() + \
                     df['recommended food'].astype(str).tolist()

        match_list = [item.lower() for item in match_list if str(item).strip() != ""]

        # Find best match
        best_match, score = process.extractOne(user_input, match_list, scorer=fuzz.partial_ratio)

        if score >= 70:
            result_row = df[
                (df['condition'].str.lower() == best_match) |
                (df['gene'].str.lower() == best_match) |
                (df['recommended food'].str.lower() == best_match)
            ].iloc[0]

            st.success("✅ Match Found!")
            st.dataframe(pd.DataFrame({
                "Condition": [result_row["condition"]],
                "Gene": [result_row["gene"]],
                "Foods to Avoid": [result_row["avoid food"]],
                "Foods to Recommend": [result_row["recommended food"]],
                "Why Recommended": [result_row["why_recommended"]]
            }))
        else:
            st.error("❗ No match found. Try using broader or simpler words like 'heart', 'thyroid', 'BRCA1'.")


