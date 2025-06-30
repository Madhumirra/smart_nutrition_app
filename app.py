import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="Smart Nutrition Recommender", layout="centered")

# 💅 CSS Styling
st.markdown("""
    <style>
    .stApp {
        background-color: white;
        color: #6a1b9a;
    }
    .main-title {
        font-size: 34px;
        font-weight: bold;
        color: #6a1b9a;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtext {
        font-size: 17px;
        color: #6a1b9a;
        text-align: center;
        margin-bottom: 25px;
    }
    .section {
        font-size: 20px;
        color: #6a1b9a;
        font-weight: 600;
        margin-top: 20px;
    }
    .content {
        font-size: 17px;
        color: #6a1b9a;
        margin-left: 10px;
    }
    .custom-input input {
        width: 300px !important;
        height: 36px !important;
        font-size: 15px !important;
        border: 1px solid #6a1b9a !important;
        border-radius: 5px !important;
        padding-left: 10px !important;
        color: #6a1b9a !important;
    }
    .stButton > button {
        background-color: white;
        color: #6a1b9a;
        border: 2px solid #6a1b9a;
        border-radius: 8px;
        padding: 6px 16px;
        font-size: 15px;
        font-weight: bold;
        transition: 0.3s ease-in-out;
    }
    .stButton > button:hover {
        background-color: #f3e5f5;
        color: #4a148c;
        border-color: #4a148c;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# 🟣 Title and Subtitle
st.markdown('<div class="main-title">Smart Nutrition Recommender</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">Enter any disease, gene, or symptom below</div>', unsafe_allow_html=True)

# Load data
df = pd.read_csv("smart_nutrition_data.csv")

# Smaller input box
with st.container():
    st.markdown('<div class="custom-input">', unsafe_allow_html=True)
    user_input = st.text_input("", placeholder="Enter a condition, gene or symptom")
    st.markdown('</div>', unsafe_allow_html=True)

# 🔍 Logic
if st.button("Get Recommendation"):
    user_input_lower = user_input.lower().strip()
    found = False

    for _, row in df.iterrows():
        keywords = [k.strip().lower() for k in row["Keywords"].split(',')]
        if any(k in user_input_lower or user_input_lower in k for k in keywords):
            st.markdown(f'<div class="section">Condition</div><div class="content">{row["Condition Name"]} ({row["Type"]})</div>', unsafe_allow_html=True)

            if pd.notna(row['Gene']) and row['Gene'].strip().lower() != "n/a":
                st.markdown(f'<div class="section">Gene Involved</div><div class="content">{row["Gene"]}</div>', unsafe_allow_html=True)

            st.markdown(f'<div class="section">Foods to Avoid</div><div class="content">{row["Avoid Food"]}</div>', unsafe_allow_html=True)

            st.markdown(f'<div class="section">Foods to Recommend</div><div class="content">{row["Recommend Food"]}</div>', unsafe_allow_html=True)

            st.markdown(f'<div class="section">Reason</div><div class="content">{row["Why_Recommended"]}</div>', unsafe_allow_html=True)

            found = True
            break

    if not found:
        st.markdown('<div class="section">No exact match found in the database.</div>', unsafe_allow_html=True)
