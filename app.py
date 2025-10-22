import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Maternal Wellbeing AI Curator", layout="wide")

# ---- LOAD SURVEY DATA ----
@st.cache_data
def load_data():
    df = pd.read_csv("maternal_wellbeing_survey.csv")
    df.columns = df.columns.str.strip().str.replace("√©", "é", regex=False)
    return df

survey_df = load_data()

st.title("🤱 Maternal Wellbeing Curator")
st.write("""
This prototype uses real survey data from mothers in New Zealand to suggest friendly places and stress-reduction ideas based on your experiences.
""")

# ---- USER INPUT ----
st.header("Tell us about yourself")

age = st.selectbox("Your age group:", sorted(survey_df["What is your age group?"].dropna().unique()))
region = st.selectbox("Region:", sorted(survey_df["Which region of New Zealand do you live in?"].dropna().unique()))
child_age = st.selectbox("Youngest child's age:", sorted(survey_df["How old is your youngest child?"].dropna().unique()))
breastfeeding = st.selectbox("Are you currently breastfeeding?", sorted(survey_df["Are you currently breastfeeding?"].dropna().unique()))
visit_freq = st.selectbox("How often do you visit public places?", sorted(survey_df.filter(like="public places").dropna().squeeze().unique()))
confidence = st.selectbox("Confidence in finding suitable spaces:", sorted(survey_df.filter(like="confident").dropna().squeeze().unique()))
challenges = st.multiselect("Common challenges you face:", survey_df["Which of the following challenges do you face most often when you go out?"].dropna().unique())
emotions = st.multiselect("Emotions you often feel during outings:", survey_df["What emotions do you most often experience before or during outings with your baby?"].dropna().unique())
info_needed = st.multiselect("Information that would help you:", survey_df.filter(like="make your outings easier").dropna().squeeze().unique())

# ---- SIMPLE CURATION ENGINE ----
if st.button("✨ Get AI-Curated Suggestions"):
    st.subheader("Personalised Insights")

    # Find similar mothers
    mask = (
        (survey_df["What is your age group?"] == age) &
        (survey_df["Which region of New Zealand do you live in?"] == region)
    )
    similar = survey_df[mask]

    if len(similar) > 0:
        common_challenges = (
            similar["Which of the following challenges do you face most often when you go out?"]
            .value_counts().head(3).index.tolist()
        )
        st.write(f"🧩 Mothers like you often report these top challenges: {', '.join(common_challenges)}")
    else:
        st.write("No exact matches, showing general insights instead.")

    # AI-style heuristic curation
    if "Difficulty finding clean baby rooms" in challenges:
        st.info("Try malls like **Westfield Albany** or **Sylvia Park** — both have clean, rated parent rooms.")
    if "Lack of breastfeeding-friendly spaces" in challenges:
        st.info("Cafés such as **The Shelf Café (Auckland CBD)** and **Crave Café (Morningside)** are known to be friendly for breastfeeding.")
    if "Inadequate seating/resting spots" in challenges:
        st.info("Libraries and community centres often provide calm, air-conditioned rest areas.")

    if len(emotions) > 0:
        st.success("You’re not alone — many mothers experience similar emotions. A short walk, flexible plans, and supportive places help reduce anxiety.")

    st.write("💡 Based on your info preferences, the app could recommend routes with:")
    for i in info_needed:
        st.write(f"• {i}")

st.markdown("---")
st.caption("Prototype © 2025 – AUT MCIS Maternal Mental Health Research")
