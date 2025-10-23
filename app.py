import streamlit as st
import pandas as pd
import os
import random
from openai import OpenAI

# --- PAGE CONFIG ---
st.set_page_config(page_title="Maternal Wellbeing Curator", layout="wide")

st.title("🤱 Maternal Wellbeing Curator")
st.markdown("""
Welcome! This app helps mothers find calm, confidence, and community while planning outings.  
It uses real feedback from other mums and AI to curate warm, practical suggestions —  
tailored to your region and suburb.
""")

# --- LOAD SURVEY DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv("data/maternal_wellbeing_survey.csv")
    df.columns = df.columns.str.strip().str.replace("√©", "é", regex=False)
    return df

df = load_data()

# --- INPUT SECTION ---
st.header("👩 Your Details")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Your first name (optional)")
    age_group = st.selectbox("Age group", sorted(df["What is your age group?"].dropna().unique()))
    region = st.text_input("Region (e.g., Auckland, Wellington, Christchurch)")
    suburb = st.text_input("Suburb (optional, e.g., Ponsonby, Mount Eden, Riccarton)")
with col2:
    child_age = st.selectbox("Youngest child’s age", sorted(df["How old is your youngest child?"].dropna().unique()))
    breastfeeding = st.selectbox("Currently breastfeeding?", sorted(df["Are you currently breastfeeding?"].dropna().unique()))
    visit_freq = st.selectbox("How often do you go out with your baby?", sorted(df["How often do you visit public places (cafés, malls, parks, libraries, etc.) with your baby?"].dropna().unique()))
    confidence = st.selectbox("Confidence finding mother-friendly spaces", sorted(df["How confident do you feel about finding suitable spaces for feeding, changing, or resting your baby?"].dropna().unique()))

# --- BRIEF CHECKBOX OPTIONS ---
st.markdown("### Common Challenges")
challenge_options = [
    "Finding clean baby rooms",
    "Few breastfeeding-friendly areas",
    "Limited seating or rest spots",
    "Unclear info on facilities",
    "Judgement from others",
]
selected_challenges = [opt for opt in challenge_options if st.checkbox(opt)]

st.markdown("### Emotions Before or During Outings")
emotion_options = ["Calm", "Mildly anxious", "Stressed", "Overwhelmed", "Confident"]
selected_emotions = [opt for opt in emotion_options if st.checkbox(opt)]

st.markdown("### Information That Would Help You")
info_options = [
    "Nearby parent rooms or feeding zones",
    "Ratings/reviews from other mothers",
    "Quiet or private spaces for breastfeeding",
    "Parking or pram-friendly routes",
    "Pre-outing checklists or reminders",
]
selected_info = [opt for opt in info_options if st.checkbox(opt)]

# --- API KEY INPUT ---
api_key = st.text_input("🔑 Enter your OpenAI API key (kept private)", type="password")

# --- GENERATE AI RECOMMENDATIONS ---
if st.button("✨ Get Curated Suggestions"):
    if not api_key:
        st.error("Please enter your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=api_key)

    # Simulated “similar mums near you” future feature
    similar_count = random.choice([1, 2, 3])
    st.info(f"🌸 {similar_count} similar mothers near {suburb or region} reported experiences like yours. (Feature coming soon!)")

    # --- BUILD AI PROMPT ---
    prompt = f"""
You are a compassionate maternal wellbeing coach in New Zealand. 
Use empathy and practical understanding to guide a mother planning local outings.

Mother’s details:
Name: {name or "Anonymous"}
Region: {region}
Suburb: {suburb or "Not specified"}
Age group: {age_group}
Child age: {child_age}
Breastfeeding: {breastfeeding}
Outing frequency: {visit_freq}
Confidence: {confidence}
Challenges: {', '.join(selected_challenges) if selected_challenges else 'None'}
Emotions: {', '.join(selected_emotions) if selected_emotions else 'None'}
Information needs: {', '.join(selected_info) if selected_info else 'None'}

Please:
1. Provide clear sectioned suggestions with short, mother-friendly headings.  
2. Make the tone warm, conversational, and localised to her region/suburb.  
3. Include 2-3 **location-type ideas** (parks, cafés, libraries, community hubs) that might exist in that area, with realistic example links (e.g. Google Maps, Peanut App, council or mum groups).  
4. Avoid obvious suggestions like "Plunket NZ" unless it’s uniquely contextual.  
5. Ensure the content is calming and inclusive — assume this mum is doing her best and needs reassurance.
"""

    with st.spinner("Gathering thoughtful recommendations for you... 💭"):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an empathetic maternal wellbeing advisor for mothers in New Zealand."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )

    st.success(f"Here are your personalised insights, {name or 'Mum'} 💖")
    st.markdown(response.choices[0].message.content)

st.markdown("---")
st.caption("Prototype © 2025 — AUT MCIS Maternal Mental Health Project | Empathy, data & design for wellbeing")
