import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Maternal Mental Health Assistant", layout="wide")

st.title("🤱 Maternal Mental Health & Breastfeeding Assistant")
st.write("Input your details to receive curated guidance based on survey data and research findings.")

# -----------------------------
# Load CSVs
# -----------------------------
@st.cache_data
def load_data():
    survey_df = pd.read_csv("data/maternal_wellbeing_survey.csv")
    plos_df = pd.read_csv("data/plos_breastfeeding_mental_health.csv")
    return survey_df, plos_df

survey_df, plos_df = load_data()

# -----------------------------
# Sidebar: Mother input form
# -----------------------------
st.sidebar.header("Input Your Details")
age_group = st.sidebar.selectbox("What is your age group?", survey_df['What is your age group?'].unique())
region = st.sidebar.selectbox("Which region of New Zealand do you live in?", survey_df['Which region of New Zealand do you live in?'].unique())
child_age = st.sidebar.selectbox("How old is your youngest child?", survey_df['How old is your youngest child?'].unique())
breastfeeding = st.sidebar.selectbox("Are you currently breastfeeding?", survey_df['Are you currently breastfeeding?'].unique())
outings_freq = st.sidebar.selectbox("How often do you visit public places with your baby?", survey_df['How often do you visit public places (caf√©s, malls, parks, libraries, etc.) with your baby?'].unique())
confidence = st.sidebar.selectbox("How confident do you feel about finding suitable spaces for feeding, changing, or resting your baby?", survey_df['How confident do you feel about finding suitable spaces for feeding, changing, or resting your baby?'].unique())
challenges = st.sidebar.multiselect("Which challenges do you face most often when you go out?", 
                                    survey_df['What challenges do you face most often when you go out?'].dropna().unique())
emotions = st.sidebar.multiselect("What emotions do you most often experience before or during outings?", 
                                 survey_df['What emotions do you most often experience before or during outings with your baby?'].dropna().unique())

# Submit button
if st.sidebar.button("Get Recommendations"):

    st.subheader("Your Curated Recommendations")

    # -----------------------------
    # Simple AI-style curation logic
    # -----------------------------
    recs = []

    # Use breastfeeding info from PLOS dataset
    if breastfeeding.lower().startswith("yes"):
        avg_anxiety = plos_df[plos_df['Any Breastfeeding']=='Yes']['Anxiety'].mean()
        recs.append(f"Average anxiety reported among breastfeeding mothers: {avg_anxiety:.2f}/5")
    else:
        avg_anxiety = plos_df[plos_df['Any Breastfeeding']=='No']['Anxiety'].mean()
        recs.append(f"Average anxiety reported among non-breastfeeding mothers: {avg_anxiety:.2f}/5")

    # Use survey data to tailor advice
    if 'Difficulty finding clean baby rooms' in challenges:
        recs.append("Consider using apps or resources that provide live info and ratings for baby-friendly facilities nearby.")
    if 'Inadequate seating/resting spots' in challenges:
        recs.append("Plan outings to cafes or libraries with dedicated parent rooms or resting areas.")
    if 'Stressed or overwhelmed' in emotions or 'Midly anxious' in emotions:
        recs.append("Prepare a checklist before leaving home and set realistic expectations to reduce stress.")
    
    # General tips
    recs.append("Remember: every mother’s needs are unique. Adjust planning according to your comfort and child’s age.")

    # Display recommendations
    for r in recs:
        st.info(r)

# -----------------------------
# Optional: Show datasets for transparency
# -----------------------------
with st.expander("View Survey Dataset"):
    st.dataframe(survey_df.head())

with st.expander("View PLOS Breastfeeding Dataset"):
    st.dataframe(plos_df.head())

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("📊 Prototype developed for Master's thesis research on maternal mental health and breastfeeding.")
