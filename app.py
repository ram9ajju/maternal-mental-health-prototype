import streamlit as st
import pandas as pd
import random

# --- Load Survey CSV ---
@st.cache_data
def load_data():
    df = pd.read_csv("data/maternal_wellbeing_survey.csv")
    df.columns = df.columns.str.strip().str.replace("√©", "é", regex=False)
    return df

df = load_data()

# --- Page setup ---
st.set_page_config(page_title="Maternal Wellbeing App", layout="wide")
st.title("🤱 Maternal Wellbeing Curator")
st.markdown("""
This prototype helps mothers find supportive environments and plan outings based on shared experiences from other mums.
""")

# --- Mother Input Form ---
st.header("Your Profile")

age_group = st.selectbox("What is your age group?", df["What is your age group?"].dropna().unique())
region = st.selectbox("Which region of New Zealand do you live in?", df["Which region of New Zealand do you live in?"].dropna().unique())
child_age = st.selectbox("How old is your youngest child?", df["How old is your youngest child?"].dropna().unique())
breastfeeding = st.selectbox("Are you currently breastfeeding?", df["Are you currently breastfeeding?"].dropna().unique())
visit_freq = st.selectbox("How often do you visit public places?", df["How often do you visit public places (cafés, malls, parks, libraries, etc.) with your baby?"].dropna().unique())
confidence = st.selectbox("How confident do you feel about finding suitable spaces?", df["How confident do you feel about finding suitable spaces for feeding, changing, or resting your baby?"].dropna().unique())
challenges = st.multiselect("Which challenges do you face?", df["Which of the following challenges do you face most often when you go out?"].dropna().unique())
emotions = st.multiselect("What emotions do you most often experience?", df["What emotions do you most often experience before or during outings with your baby?"].dropna().unique())
info_needed = st.multiselect("What information would make outings easier?", df["What type of information would make your outings easier or less stressful? (Select up to 3)"].dropna().unique())

# --- Submit ---
if st.button("Get Curated Suggestions"):
    st.header("🌿 AI-Curated Suggestions for You")

    # Filter similar mothers by demographics
    similar = df[
        (df["What is your age group?"] == age_group) &
        (df["Which region of New Zealand do you live in?"] == region)
    ]
    
    if len(similar) > 0:
        st.success(f"Found {len(similar)} mothers in similar age and region profiles.")
    else:
        st.warning("No exact matches found, showing general insights.")

    # --- Generate simple curated suggestions ---
    tips = [
        "Look for shopping centres that provide parent rooms with enclosed play areas.",
        "Check council websites for libraries with baby-friendly reading zones.",
        "Use Google Maps reviews to spot parent facilities and changing stations.",
        "Join local parenting Facebook groups for live facility updates.",
        "Schedule shorter outings first to build confidence over time."
    ]

    # Match info preferences to boost relevance
    if "Live info on baby facilities nearby" in info_needed:
        tips.append("Try apps that list parent rooms and feeding zones in real-time.")
    if "Quiet or breastfeeding-friendly zones" in info_needed:
        tips.append("Look for mall maps that mark quiet lounges or parents' suites.")
    if "Ratings/reviews from other parents" in info_needed:
        tips.append("Use crowdsourced reviews to choose comfortable cafés and parks.")

    st.subheader("💡 Suggested Actions:")
    for tip in random.sample(tips, min(5, len(tips))):
        st.write(f"- {tip}")

    # Emotional recommendations
    if "Stressed or overwhelmed" in emotions:
        st.info("Try pre-packing essentials and using checklists before leaving home.")
    elif "Mildly anxious" in emotions:
        st.info("Start with small, familiar locations before longer trips.")
    else:
        st.info("You're doing great! Keep sharing experiences to support other mothers.")

st.markdown("---")
st.caption("Prototype © 2025 — AUT MCIS Maternal Mental Health Project")
