import streamlit as st
import pandas as pd
import os
from openai import OpenAI
import random

# --- Page Setup ---
st.set_page_config(page_title="Maternal Wellbeing Curator", layout="wide")

st.title("🤱 Maternal Wellbeing Curator")
st.markdown("""
This app helps mothers find confidence and supportive environments for outings, 
using real survey data and AI to suggest helpful communities, locations, and habits.
""")

# --- Load Dataset ---
@st.cache_data
def load_data():
    df = pd.read_csv("data/maternal_wellbeing_survey.csv")
    df.columns = df.columns.str.strip().str.replace("√©", "é", regex=False)
    return df

df = load_data()

# --- Mother Input ---
st.header("👩 Your Profile")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Your name (optional, for a personal touch)")
    age_group = st.selectbox("Age group", df["What is your age group?"].dropna().unique())
    region = st.selectbox("Region", df["Which region of New Zealand do you live in?"].dropna().unique())
    child_age = st.selectbox("Youngest child’s age", df["How old is your youngest child?"].dropna().unique())
with col2:
    breastfeeding = st.selectbox("Currently breastfeeding?", df["Are you currently breastfeeding?"].dropna().unique())
    visit_freq = st.selectbox("Outing frequency", df["How often do you visit public places (cafés, malls, parks, libraries, etc.) with your baby?"].dropna().unique())
    confidence = st.selectbox("Confidence finding mother-friendly spaces", df["How confident do you feel about finding suitable spaces for feeding, changing, or resting your baby?"].dropna().unique())

st.markdown("### Common Challenges")
challenge_options = df["Which of the following challenges do you face most often when you go out?"].dropna().unique()
selected_challenges = [opt for opt in challenge_options if st.checkbox(opt)]

st.markdown("### Emotions Before/During Outings")
emotion_options = df["What emotions do you most often experience before or during outings with your baby?"].dropna().unique()
selected_emotions = [opt for opt in emotion_options if st.checkbox(opt)]

st.markdown("### Helpful Information")
info_options = df["What type of information would make your outings easier or less stressful? (Select up to 3)"].dropna().unique()
selected_info = [opt for opt in info_options if st.checkbox(opt)]

# --- API Setup ---
api_key = st.text_input("🔑 Enter your OpenAI API key (kept private)", type="password")

# --- Generate AI Suggestions ---
if st.button("✨ Get AI-Curated Suggestions"):
    if not api_key:
        st.error("Please enter your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=api_key)

    # Simulate “similar mothers nearby” message (future feature)
    similar_count = random.choice([1, 2, 3])
    st.info(f"🌸 {similar_count} similar mothers near you reported similar experiences. (Feature coming soon!)")

    # Create prompt for AI
    prompt = f"""
You are a digital wellbeing assistant supporting mothers in New Zealand.

Mother's profile:
Name: {name or "Anonymous"}
Age group: {age_group}
Region: {region}
Child age: {child_age}
Breastfeeding: {breastfeeding}
Visit frequency: {visit_freq}
Confidence level: {confidence}
Challenges: {', '.join(selected_challenges) if selected_challenges else 'None'}
Emotions: {', '.join(selected_emotions) if selected_emotions else 'None'}
Information preferences: {', '.join(selected_info) if selected_info else 'None'}

Provide 3-5 actionable, empathetic suggestions for this mother. Include:
1. Tips to manage anxiety or stress during outings.
2. Types of NZ or AU local places that may suit her needs (e.g., malls, cafes, libraries).
3. 2–3 community groups or websites she can explore (give real, relevant links).
Be warm, encouraging, and realistic — short paragraphs or bullet points are preferred.
"""

    with st.spinner("Curating personalized insights..."):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an empathetic maternal wellbeing coach for postpartum mothers in New Zealand."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )

    st.success(f"Here are your insights, {name or 'Mum'} 💖")
    st.markdown(response.choices[0].message.content)

st.markdown("---")
st.caption("Prototype © 2025 — AUT MCIS Maternal Mental Health Project")
