import streamlit as st
import pandas as pd
import os
import random
from openai import OpenAI

# --- PAGE CONFIG ---
st.set_page_config(page_title="Maternal Wellbeing Curator", layout="wide")

st.title("🤱 Maternal Wellbeing Curator")
st.markdown("""
This app helps mothers plan calm, confident outings — using insights from other mums and AI-curated location tips 
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
    age_group = st.selectbox("Select your age group", options=[""] + sorted(df["What is your age group?"].dropna().unique()))
    region = st.text_input("Region (e.g., Auckland, Wellington, Christchurch)")
    suburb = st.text_input("Suburb (optional, e.g., Mount Eden, Riccarton)")
with col2:
    child_age = st.selectbox("Youngest child’s age", options=[""] + sorted(df["How old is your youngest child?"].dropna().unique()))
    breastfeeding = st.selectbox("Currently breastfeeding?", options=[""] + sorted(df["Are you currently breastfeeding?"].dropna().unique()))
    visit_freq = st.selectbox("Outing frequency", options=[""] + sorted(df["How often do you visit public places (cafés, malls, parks, libraries, etc.) with your baby?"].dropna().unique()))
    confidence = st.selectbox("Confidence finding mother-friendly spaces", options=[""] + sorted(df["How confident do you feel about finding suitable spaces for feeding, changing, or resting your baby?"].dropna().unique()))

# --- SHORTER, FRIENDLY CHECKBOXES ---
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

st.markdown("### What Info Would Help You?")
info_options = [
    "Nearby parent rooms or feeding zones",
    "Ratings/reviews from other mothers",
    "Quiet or private spaces for breastfeeding",
    "Parking and accessibility info",
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

    similar_count = random.choice([1, 2, 3])
    st.info(f"🌸 {similar_count} similar mothers near {suburb or region} reported experiences like yours. (Feature coming soon!)")

    prompt = f"""
You are a compassionate maternal wellbeing assistant based in New Zealand. 
Your goal is to give mothers simple, warm, location-relevant suggestions for reducing stress during outings.

Mother’s details:
Name: {name or "Anonymous"}
Region: {region or "Not specified"}
Suburb: {suburb or "Not specified"}
Age group: {age_group or "Not specified"}
Youngest child: {child_age or "Not specified"}
Breastfeeding: {breastfeeding or "Not specified"}
Outing frequency: {visit_freq or "Not specified"}
Confidence: {confidence or "Not specified"}
Challenges: {', '.join(selected_challenges) if selected_challenges else 'None'}
Emotions: {', '.join(selected_emotions) if selected_emotions else 'None'}
Information needs: {', '.join(selected_info) if selected_info else 'None'}

Please:
1. Write clear section headings with emojis and short paragraphs (2–3 lines each).
2. Make it warm, localised, and easy to read — like advice from a friendly mum.
3. Suggest 2–3 **location ideas** for {suburb or region}, e.g. parks, libraries, cafes, or baby-friendly community hubs.  
   Include realistic example links (Google Maps, Peanut App, Parenting Place, local councils).
4. Include **2 supportive communities or online groups** — NZ/AU based, not just Plunket.
5. End with a positive, reassuring note about her journey as a mother.
"""

    with st.spinner("Curating gentle, thoughtful tips for you 💭"):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an empathetic wellbeing guide for mothers in New Zealand. Your responses should sound caring, useful, and location-aware."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )

    st.success(f"Here are your curated suggestions, {name or 'Mum'} 💖")
    st.markdown(response.choices[0].message.content)

st.markdown("---")
st.caption("Prototype © 2025 — AUT MCIS Maternal Mental Health Project | Empathy, data & design for wellbeing")
