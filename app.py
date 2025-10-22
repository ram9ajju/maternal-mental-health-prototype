import streamlit as st
import pandas as pd

# --- Load CSVs from GitHub ---
# Replace these URLs with the raw GitHub URLs of your CSV files
SURVEY_CSV_URL = "https://raw.githubusercontent.com/yourusername/yourrepo/main/maternal_streamlit_project/maternal_wellbeing_survey.csv"
PLOS_CSV_URL = "https://raw.githubusercontent.com/yourusername/yourrepo/main/maternal_streamlit_project/plos_breastfeeding_mental_health.csv"

@st.cache_data
def load_csv(url):
    df = pd.read_csv(url)
    # Clean column names: strip spaces, replace special characters
    df.columns = df.columns.str.strip().str.replace('√©', 'é', regex=False)
    return df

survey_df = load_csv(SURVEY_CSV_URL)
plos_df = load_csv(PLOS_CSV_URL)

st.title("Maternal Mental Health Curator App")
st.markdown("""
This app uses survey and published dataset information to help mothers anticipate and manage stress during outings.
""")

# --- Mother Profile Input ---
st.header("Mother Profile")

age_group = st.selectbox("Select your age group:", survey_df["What is your age group?"].unique())
region = st.selectbox("Select your region:", survey_df["Which region of New Zealand do you live in?"].unique())
child_age = st.selectbox("How old is your youngest child?", survey_df["How old is your youngest child?"].unique())
breastfeeding_status = st.selectbox("Are you currently breastfeeding?", survey_df["Are you currently breastfeeding?"].unique())
visit_freq = st.selectbox("How often do you visit public places with your baby?", 
                         survey_df["How often do you visit public places (cafés, malls, parks, libraries, etc.) with your baby?"].unique())
confidence = st.selectbox("How confident do you feel about finding suitable spaces for feeding/changing/resting your baby?",
                          survey_df["How confident do you feel about finding suitable spaces for feeding, changing, or resting your baby?"].unique())
challenges = st.multiselect("Which challenges do you face most often when you go out?", 
                            survey_df["Which of the following challenges do you face most often when you go out?"].dropna().unique())
emotions = st.multiselect("What emotions do you most often experience before or during outings with your baby?", 
                          survey_df["What emotions do you most often experience before or during outings with your baby?"].dropna().unique())
info_needed = st.multiselect("What type of information would make your outings easier or less stressful?",
                             survey_df["What type of information would make your outings easier or less stressful? (Select up to 3)"].dropna().unique())
use_app = st.radio("Would you be comfortable with an app using location data (anonymously) to recommend nearby mother-friendly places?",
                   survey_df["Would you be comfortable with an app using location data (anonymously) to recommend nearby mother-friendly places?"].unique())

# --- Placeholder AI Curation ---
st.header("Curated Suggestions")

if st.button("Get Curated Recommendations"):
    st.markdown("**Based on your profile and the survey/plos dataset, here are some insights:**")
    
    # Example logic: you can replace this with ML/AI predictions later
    st.write(f"- Since you are in **{region}**, frequenting public places **{visit_freq}**, we suggest checking facilities that have breastfeeding-friendly zones and quiet areas.")
    st.write(f"- Challenges like {', '.join(challenges)} may be mitigated by planning your route using crowdsourced parent ratings and live facility info.")
    st.write(f"- Emotional pattern: {', '.join(emotions)} — consider reminders and checklists to reduce anxiety.")
    st.write(f"- Additional info requested: {', '.join(info_needed)}")

st.markdown("---")
st.markdown("**Data sources:** Survey dataset & PLOS breastfeeding mental health dataset (Figshare)")

