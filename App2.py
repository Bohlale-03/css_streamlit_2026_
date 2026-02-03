# -*- coding: utf-8 -*-
"""
Created on Tue Feb  3 10:52:00 2026

@author: 202158511
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# Page configuration
# ----------------------------
st.set_page_config(page_title="Mini Data Dashboard", layout="wide")

st.title("📊 Mini Streamlit Dashboard (Public Dataset)")
st.markdown("This dashboard uses a **public dataset** and demonstrates **multi-page navigation** with different plots.")

# ----------------------------
# Load public dataset (Penguins)
# ----------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv"
    return pd.read_csv(url)

df = load_data()

# ----------------------------
# Sidebar Navigation
# ----------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Overview", "Scatter Analysis", "Distribution Analysis", "Summary Insights"]
)

st.sidebar.header("Global Filters")

species = st.sidebar.multiselect(
    "Select Species",
    options=df["species"].dropna().unique(),
    default=df["species"].dropna().unique()
)

islands = st.sidebar.multiselect(
    "Select Island",
    options=df["island"].dropna().unique(),
    default=df["island"].dropna().unique()
)

filtered_df = df[
    (df["species"].isin(species)) &
    (df["island"].isin(islands))
]

# ----------------------------
# PAGE 1: Overview
# ----------------------------
if page == "Overview":
    st.header("📌 Dataset Overview")
    st.dataframe(filtered_df)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Penguins", len(filtered_df))
    col2.metric("Avg Bill Length (mm)", round(filtered_df["bill_length_mm"].mean(), 2))
    col3.metric("Avg Flipper Length (mm)", round(filtered_df["flipper_length_mm"].mean(), 2))

# ----------------------------
# PAGE 2: Scatter Analysis
# ----------------------------
elif page == "Scatter Analysis":
    st.header("📈 Scatter Plot Analysis")

    fig1 = px.scatter(
        filtered_df,
        x="bill_length_mm",
        y="flipper_length_mm",
        color="species",
        size="body_mass_g",
        title="Bill Length vs Flipper Length"
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("**Insight:** Different species show clear clustering patterns.")

# ----------------------------
# PAGE 3: Distribution Analysis
# ----------------------------
elif page == "Distribution Analysis":
    st.header("📊 Distribution Analysis")

    fig2 = px.histogram(
        filtered_df,
        x="body_mass_g",
        color="species",
        barmode="overlay",
        title="Body Mass Distribution by Species"
    )
    st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# PAGE 4: Summary Insights
# ----------------------------
elif page == "Summary Insights":
    st.header("🧠 Summary Insights")

    summary_df = filtered_df.groupby("species", as_index=False).agg(
        avg_body_mass=("body_mass_g", "mean"),
        avg_bill_length=("bill_length_mm", "mean"),
        avg_flipper_length=("flipper_length_mm", "mean")
    )

    fig3 = px.bar(
        summary_df,
        x="species",
        y="avg_body_mass",
        title="Average Body Mass by Species"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.dataframe(summary_df)

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.caption("Built with Streamlit • Public dataset: Palmer Penguins")


