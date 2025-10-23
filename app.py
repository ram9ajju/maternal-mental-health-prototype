import streamlit as st
import pandas as pd
import os
import random
from openai import OpenAI

# --- Page Setup ---
st.set_page_config(page_title="Maternal Wellbeing Curator", layout="wide")

st.title("🤱 Maternal Wellbeing Curator")
st.markdown("""
This app helps mothers plan comfortable outings, 
offering suggestions drawn from other mothers’ experiences and AI-curated insights 
tailored to your region and needs.
""")

# --- Load Data ---
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
    name = st.text_input("Your first name (optional)")
    age_group = st.selectbox("Age group", df["What is your age group?"].dropna().unique())
    region = st.selectbox("Region", df["Which region of New Zealand do you live in?"].dropna().unique())
    child_age = st.selectbox("Youngest child’s age", df["How old is your youngest child?"].dropna().unique())
with col2:
    breastfeeding = st.selectbox("Currently breastfeeding?", df["Are you currently breastfeeding?"].dropna().unique())
    visit_freq = st.selectbox("Outing frequency", df["How often do you visit public places (cafés, malls, parks, libraries, etc.) with your baby?"].dropna().unique())
    confidence = st.selectbox("Confidence finding mother-friendly spaces", df["How confident do you feel about finding suitable spaces for feeding, changing, or resting your baby?"].dropna().unique())

# --- Compact checkboxes (refined options) ---
st.markdown("### Common Challenges")
challenge_text = [
    "Finding clean baby rooms",
    "Few breastfeeding-friendly spots",
    "Limited seating or rest areas",
    "Judgement from others",
    "Unclear facility info online"
]
selected_challenges = [opt for opt in challenge_text if st.checkbox(opt)]

st.markdown("### Emotions Before/During Outings")
emotion_text = ["Calm", "Mildly anxious", "Stressed", "Overwhelmed", "Confident"]
selected_emotions = [opt for opt in emotion_text if st.checkbox(opt)]

st.markdown("### What Info Would Help You?")
info_text = [
    "Nearby parent rooms and feeding zones",
    "Ratings or reviews from other mothers",
    "Quiet, calm areas for breastfeeding",
    "Checklists/reminders before leaving",
    "Parking and accessibility details"
]
selected_info = [opt for opt in info_text if st.checkbox(opt)]

# --- OpenAI API ---
api_key = st.text_input("🔑 Enter your OpenAI API key (kept private)", type="password")

# --- Generate Suggestions ---
if st.button("✨ Get AI-Curated Suggestions"):
    if not api_key:
        st.error("Please enter your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=api_key)

    # Simulate “similar mothers nearby” message (future feature)
    similar_count = random.choice([1, 2, 3])
    st.info(f"🌸 {similar_count} similar mothers near you reported experiences like yours. (Feature coming soon!)")

    # --- Build AI prompt ---
    prompt = f"""
You are a compassionate maternal wellbeing assistant helping mothers in New Zealand plan calm and confident outings.

Mother's profile:
Name: {name or "Anonymous"}
Region: {region}
Age group: {age_group}
Youngest child: {child_age}
Breastfeeding: {breastfeeding}
Outing frequency: {visit_freq}
Confidence: {confidence}
Challenges: {', '.join(selected_challenges) if selected_challenges else 'None'}
Emotions: {', '.join(selected_emotions) if selected_emotions else 'None'}
Information preferences: {', '.join(selected_info) if selected_info else 'None'}

Your task:
1. Write 4–6 empathetic, practical suggestions for this mother. 
2. Make them sound warm, short, and location-relevant (in New Zealand context).
3. Include at least 2 realistic group or website links that help mothers — 
   avoid suggesting Plunket generically; mention community-level groups or digital resources (e.g., "The Parenting Place", "Peanut App", "Local Council Parenting Support").
4. Keep tone positive, conversational, and mother-centred.
5. Mention a type of place in {region} that might be family-friendly or relaxing (generic if unsure).
"""

    with st.spinner("Curating insights for you... please wait ⏳"):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an empathetic maternal wellbeing coach for mothers in New Zealand."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )

    st.success(f"Here are your suggestions, {name or 'Mum'} 💖")
    st.markdown(response.choices[0].message.content)

st.markdown("---")
st.caption("Prototype © 2025 — AUT MCIS Maternal Mental Health Project | AI-assisted wellbeing support")
