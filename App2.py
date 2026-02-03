import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# Page configuration
# ----------------------------
st.set_page_config(page_title="Mini Data Dashboard", layout="wide")

st.title("📊 Mini Streamlit Dashboard (Public Dataset)")
st.markdown("This dashboard uses a **public dataset** and demonstrates **multi-page navigation** with **static Matplotlib plots**.")

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

    fig, ax = plt.subplots()
    for sp in filtered_df["species"].dropna().unique():
        subset = filtered_df[filtered_df["species"] == sp]
        ax.scatter(subset["bill_length_mm"], subset["flipper_length_mm"], label=sp)

    ax.set_xlabel("Bill Length (mm)")
    ax.set_ylabel("Flipper Length (mm)")
    ax.set_title("Bill Length vs Flipper Length")
    ax.legend()

    st.pyplot(fig)

    st.markdown("**Insight:** Different species form distinct clusters.")

# ----------------------------
# PAGE 3: Distribution Analysis
# ----------------------------
elif page == "Distribution Analysis":
    st.header("📊 Distribution Analysis")

    fig, ax = plt.subplots()
    for sp in filtered_df["species"].dropna().unique():
        subset = filtered_df[filtered_df["species"] == sp]
        ax.hist(subset["body_mass_g"].dropna(), alpha=0.6, label=sp)

    ax.set_xlabel("Body Mass (g)")
    ax.set_ylabel("Frequency")
    ax.set_title("Body Mass Distribution by Species")
    ax.legend()

    st.pyplot(fig)

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

    fig, ax = plt.subplots()
    ax.bar(summary_df["species"], summary_df["avg_body_mass"])
    ax.set_xlabel("Species")
    ax.set_ylabel("Average Body Mass (g)")
    ax.set_title("Average Body Mass by Species")

    st.pyplot(fig)

    st.dataframe(summary_df)

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.caption("Built with Streamlit • Public dataset: Palmer Penguins")
