import streamlit as st
import pandas as pd
import os
from openai import OpenAI
import random

# --- Page Setup ---
st.set_page_config(page_title="Maternal Wellbeing Curator", layout="wide")

st.title("🤱 Maternal Wellbeing Curator")
st.markdown("""
Welcome! This app uses AI and real experiences from mothers in New Zealand to provide 
personalised suggestions for stress-free outings and community connections.
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
    name = st.text_input("Your name (optional)")
    age_group = st.selectbox("Age group", df["What is your age group?"].dropna().unique())
    region = st.selectbox("Region", df["Which region of New Zealand do you live in?"].dropna().unique())
    child_age = st.selectbox("Youngest child’s age", df["How old is your youngest child?"].dropna().unique())
with col2:
    breastfeeding = st.selectbox("Currently breastfeeding?", df["Are you currently breastfeeding?"].dropna().unique())
    visit_freq = st.selectbox("Outing frequency", df["How often do you visit public places (cafés, malls, parks, libraries, etc.) with your baby?"].dropna().unique())
    confidence = st.selectbox("Confidence finding mother-friendly spaces", df["How confident do you feel about finding suitable spaces for feeding, changing, or resting your baby?"].dropna().unique())

# --- Clean, brief checkbox sections ---
st.markdown("### 🌼 Common Challenges")
challenge_options = [
    "Finding clean baby rooms", "Few breastfeeding-friendly spots", 
    "Limited resting areas", "Hard to locate change tables", 
    "Judgment from others", "Parking or accessibility issues"
]
selected_challenges = [opt for opt in challenge_options if st.checkbox(opt)]

st.markdown("### 💭 Emotions Before/During Outings")
emotion_options = ["Calm", "Mildly anxious", "Stressed", "Overwhelmed", "Confident"]
selected_emotions = [opt for opt in emotion_options if st.checkbox(opt)]

st.markdown("### 💡 Helpful Information")
info_options = [
    "Nearby baby-friendly cafés", "Ratings from other parents",
    "Quiet or feeding zones", "Live facility updates", 
    "Checklists before leaving", "Parking and toilet info"
]
selected_info = [opt for opt in info_options if st.checkbox(opt)]

# --- API Key ---
api_key = st.text_input("🔑 Enter your OpenAI API key (kept private)", type="password")

# --- AI Suggestions ---
if st.button("✨ Get AI-Curated Suggestions"):
    if not api_key:
        st.error("Please enter your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=api_key)

    # Simulated “similar mothers nearby” message
    similar_count = random.choice([1, 2, 3])
    st.info(f"🌸 {similar_count} similar mothers near you reported similar experiences. (Feature coming soon!)")

    # Build the AI prompt
    prompt = f"""
You are a friendly, empathetic assistant helping mothers in New Zealand plan relaxing outings.

Mother’s details:
Name: {name or "Anonymous"}
Age group: {age_group}
Region: {region}
Child age: {child_age}
Breastfeeding: {breastfeeding}
Visit frequency: {visit_freq}
Confidence: {confidence}
Challenges: {', '.join(selected_challenges) or 'None'}
Emotions: {', '.join(selected_emotions) or 'None'}
Information needs: {', '.join(selected_info) or 'None'}

Generate warm, evidence-based advice that includes:
1. 3-5 actionable, realistic tips to reduce stress during outings.
2. 2-3 location or activity ideas suited to mothers in NZ (cafés, malls, parks, etc.).
3. Links to trusted mum communities or resources (e.g. Plunket NZ, The Parenting Place, Peanut App).
Use bullet points and short, readable paragraphs.
Highlight key emotions and confidence level visually.
"""

    with st.spinner("Creating personalised insights..."):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an empathetic maternal wellbeing coach for mothers in New Zealand."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )

    st.success(f"Here are your insights, {name or 'Mum'} 💖")
    st.markdown(response.choices[0].message.content)

# --- Footer ---
st.markdown("---")
st.caption("Prototype © 2025 — AUT MCIS Maternal Mental Health Project")
