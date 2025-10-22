import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# --- Page Setup ---
st.set_page_config(page_title="Maternal Wellbeing Curator", layout="wide")

st.title("🤱 Maternal Wellbeing Curator")
st.markdown("""
Welcome! This prototype uses real survey data and AI reasoning to help mothers like you 
discover friendly, supportive public places based on shared experiences in New Zealand.
""")

# --- Load Dataset ---
@st.cache_data
def load_data():
    df = pd.read_csv("data/maternal_wellbeing_survey.csv")
    df.columns = df.columns.str.strip().str.replace("√©", "é", regex=False)
    return df

df = load_data()

# --- Basic Info ---
st.header("Your Details")

name = st.text_input("What’s your first name?")
age_group = st.selectbox("Your age group", df["What is your age group?"].dropna().unique())
region = st.selectbox("Which region of New Zealand do you live in?", df["Which region of New Zealand do you live in?"].dropna().unique())
child_age = st.selectbox("How old is your youngest child?", df["How old is your youngest child?"].dropna().unique())
breastfeeding = st.selectbox("Are you currently breastfeeding?", df["Are you currently breastfeeding?"].dropna().unique())
visit_freq = st.selectbox("How often do you visit public places (cafés, malls, parks, libraries, etc.) with your baby?", 
                          df["How often do you visit public places (cafés, malls, parks, libraries, etc.) with your baby?"].dropna().unique())
confidence = st.selectbox("How confident do you feel about finding suitable spaces for feeding/changing/resting your baby?", 
                          df["How confident do you feel about finding suitable spaces for feeding, changing, or resting your baby?"].dropna().unique())
challenges = st.multiselect("Which challenges do you face most often when you go out?", 
                            df["Which of the following challenges do you face most often when you go out?"].dropna().unique())
emotions = st.multiselect("What emotions do you most often experience before or during outings with your baby?", 
                          df["What emotions do you most often experience before or during outings with your baby?"].dropna().unique())
info_needed = st.multiselect("What type of information would make your outings easier or less stressful?",
                             df["What type of information would make your outings easier or less stressful? (Select up to 3)"].dropna().unique())

# --- OpenAI Setup (Free API key input) ---
api_key = st.text_input("🔑 Enter your OpenAI API key (kept private)", type="password")

# --- Curate Suggestions ---
if st.button("✨ Get AI-Curated Suggestions"):
    if not api_key:
        st.error("Please enter your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=api_key)

    # Filter similar mothers
    similar = df[
        (df["What is your age group?"] == age_group) &
        (df["Which region of New Zealand do you live in?"] == region)
    ]
    count = len(similar)

    # Build AI prompt
    prompt = f"""
You are a digital wellbeing assistant helping postpartum mothers plan stress-free outings.

Mother's details:
- Name: {name}
- Age group: {age_group}
- Region: {region}
- Child age: {child_age}
- Breastfeeding: {breastfeeding}
- Visit frequency: {visit_freq}
- Confidence level: {confidence}
- Challenges: {', '.join(challenges) if challenges else 'None'}
- Emotions: {', '.join(emotions) if emotions else 'None'}
- Information preferences: {', '.join(info_needed) if info_needed else 'None'}

Based on this profile and insights from similar mothers ({count} records found),
suggest 3 to 5 personalized tips or location-based strategies that can improve her confidence, 
reduce anxiety, and help her find mother-friendly spaces in New Zealand (cafés, malls, parks, libraries, etc.). 
Be specific but empathetic and supportive.
"""

    st.info("Generating personalized insights... please wait ⏳")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an empathetic maternal wellbeing assistant for postpartum mothers."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8
    )

    st.success(f"Here are your insights, {name or 'Mother'} 🌷")
    st.write(response.choices[0].message.content)

    st.markdown("---")
    st.caption("Prototype © 2025 — AUT MCIS Maternal Wellbeing Project")

