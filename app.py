import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Maternal Mental Health Prototype", layout="wide")

st.title("🧠 Maternal Mental Health Prototype")
st.write("""
This prototype integrates real-world survey data with open research datasets 
to explore relationships between maternal wellbeing and breastfeeding patterns.
""")

# File upload or default sample data
st.sidebar.header("📂 Upload or use demo data")

uploaded_survey = st.sidebar.file_uploader("Upload Maternal Wellbeing Survey CSV", type=["csv"])
uploaded_plos = st.sidebar.file_uploader("Upload PLOS Breastfeeding Dataset CSV", type=["csv"])

# Load data (use defaults if not uploaded)
if uploaded_survey is not None and uploaded_plos is not None:
    survey_df = pd.read_csv(uploaded_survey)
    plos_df = pd.read_csv(uploaded_plos)
else:
    st.info("Using example data since no files uploaded.")
    survey_df = pd.read_csv("data/maternal_wellbeing_survey.csv")
    plos_df = pd.read_csv("data/plos_breastfeeding_mental_health.csv")

# Show dataset previews
st.subheader("Survey Dataset (Maternal Wellbeing)")
st.dataframe(survey_df.head())

st.subheader("PLOS Dataset (Breastfeeding and Parenting Behaviours)")
st.dataframe(plos_df.head())

# Summary statistics
st.subheader("📊 Summary Statistics")
col1, col2 = st.columns(2)

with col1:
    st.write("**Survey Dataset Summary**")
    st.write(survey_df.describe())

with col2:
    st.write("**PLOS Dataset Summary**")
    st.write(plos_df.describe())

# Correlation visualization
st.subheader("📈 Correlation Visualization")

num_cols = [c for c in survey_df.columns if survey_df[c].dtype != 'object']
if len(num_cols) >= 2:
    x_var = st.selectbox("Select X variable", num_cols)
    y_var = st.selectbox("Select Y variable", num_cols, index=1)
    fig, ax = plt.subplots()
    ax.scatter(survey_df[x_var], survey_df[y_var], alpha=0.7)
    ax.set_xlabel(x_var)
    ax.set_ylabel(y_var)
    ax.set_title(f"Correlation between {x_var} and {y_var}")
    st.pyplot(fig)
else:
    st.info("Not enough numeric columns to visualize correlations.")

st.markdown("---")
st.caption("Prototype © 2025 – AUT MCIS Maternal Mental Health Project")
