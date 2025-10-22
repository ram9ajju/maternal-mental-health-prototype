import streamlit as st
import pandas as pd
from openai import OpenAI

# --- CONFIG ---
st.set_page_config(page_title="Maternal Mental Health AI Prototype", layout="wide")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    survey_df = pd.read_csv("data/maternal_wellbeing_survey.csv")
    plos_df = pd.read_csv("data/plos_breastfeeding_mental_health.csv")
    return survey_df, plos_df

survey_df, plos_df = load_data()

# --- INTRO ---
st.title("🤱 Maternal Mental Health AI Curator")
st.write("""
Welcome! This prototype combines breastfeeding & maternal wellbeing data to provide **personalized insights**.
Please fill in the fields below to get curated suggestions.
""")

# --- USER INPUT ---
st.header("Your Information")
age_group = st.selectbox("What is your age group?", survey_df["What is your age group?"].unique())
region = st.selectbox("Which region of New Zealand do you live in?", survey_df["Which region of New Zealand do you live in?"].unique())
child_age = st.selectbox("How old is your youngest child?", survey_df["How old is your youngest child?"].unique())
breastfeeding_status = st.selectbox("Are you currently breastfeeding?", survey_df["Are you currently breastfeeding?"].unique())
visit_freq = st.selectbox("How often do you visit public places with your baby?", survey_df["How often do you visit public places (caf√©s, malls, parks, libraries, etc.) with your baby?"].unique())
confidence = st.slider("How confident are you about finding suitable spaces?", 0, 10, 5)
challenges = st.multiselect(
    "Which challenges do you face most often when going out?",
    survey_df["What challenges do you face most often when you go out?"].dropna().str.split(';').explode().unique()
)
emotions = st.multiselect(
    "What emotions do you most often experience before/during outings?",
    survey_df["What emotions do you most often experience before or during outings with your baby?"].dropna().str.split(';').explode().unique()
)
info_preferences = st.multiselect(
    "What type of information would make your outings easier?",
    survey_df["What type of information would make your outings easier or less stressful? (Select up to 3)"].dropna().str.split(';').explode().unique()
)

if st.button("Get AI-Curated Suggestions"):
    st.info("Generating insights...")

    # --- SIMPLE RULE-BASED CURATION EXAMPLE ---
    # Match survey data patterns and PLOS trends
    matched_rows = plos_df[
        (plos_df["Any Breastfeeding"].str.lower().str.contains("yes" if "Yes" in breastfeeding_status else "no"))
    ]
    avg_anxiety = matched_rows["Anxiety"].mean()
    
    st.subheader("📊 Curated Insights")
    st.write(f"Based on your profile, mothers with similar breastfeeding status show an average anxiety score of **{avg_anxiety:.2f}** in the PLOS dataset.")
    
    st.write("Based on your challenges and preferences, here are some tips:")
    for pref in info_preferences:
        st.write(f"- {pref}")

   # --- AI-based example (optional, OpenAI LLM) ---
# Uncomment below and provide OPENAI_API_KEY as environment variable for GPT suggestions

import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

prompt = f"""
Mother profile:
Age group: {age_group}
Region: {region}
Child age: {child_age}
Breastfeeding: {breastfeeding_status}
Challenges: {', '.join(challenges) if challenges else 'None'}
Emotions: {', '.join(emotions) if emotions else 'None'}
Info preferences: {', '.join(info_preferences) if info_preferences else 'None'}

Provide 3 actionable suggestions for her to reduce anxiety and make outings easier based on maternal mental health studies.
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7
)
st.write(response.choices[0].message["content"])

