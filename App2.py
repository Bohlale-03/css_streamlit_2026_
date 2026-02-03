import streamlit as st
import pandas as pd

# ----------------------------
# Page configuration
# ----------------------------
st.set_page_config(page_title="Mini Data Dashboard", layout="wide")

st.title("Mini Streamlit Dashboard")
st.markdown("This dashboard uses a public dataset and demonstrates multi-page navigation without plots. It focuses on data overview, filtering, and summary tables.")

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
    ["Dataset Overview", "Column Description", "Grouped Summary", "Key Insights"]
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
# PAGE 1: Dataset Overview
# ----------------------------
if page == "Dataset Overview":
    st.header("Dataset Overview")
    st.write("This page shows the raw dataset after applying filters.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", len(filtered_df))
    col2.metric("Unique Species", filtered_df["species"].nunique())
    col3.metric("Islands Covered", filtered_df["island"].nunique())

    st.dataframe(filtered_df)

# ----------------------------
# PAGE 2: Column Description
# ----------------------------
elif page == "Column Description":
    st.header(" Column Description")

    description = pd.DataFrame({
        "Column": filtered_df.columns,
        "Description": [
            "Penguin species",
            "Island where penguin was observed",
            "Bill length in millimeters",
            "Bill depth in millimeters",
            "Flipper length in millimeters",
            "Body mass in grams",
            "Sex of the penguin"
        ]
    })

    st.table(description)

# ----------------------------
# PAGE 3: Grouped Summary
# ----------------------------
elif page == "Grouped Summary":
    st.header("Grouped Summary Statistics")

    summary_df = filtered_df.groupby("species", as_index=False).agg(
        count=("species", "count"),
        avg_body_mass_g=("body_mass_g", "mean"),
        avg_bill_length_mm=("bill_length_mm", "mean"),
        avg_flipper_length_mm=("flipper_length_mm", "mean")
    )

    st.write("Summary statistics grouped by species:")
    st.dataframe(summary_df)

# ----------------------------
# PAGE 4: Key Insights
# ----------------------------
elif page == "Key Insights":
    st.header(" Key Insights")

    st.markdown(
        """
        - The dataset contains observations of penguins from multiple islands.
        - Species show noticeable differences in body mass and flipper length.
        - Filtering allows focused inspection of specific species or islands.
        - This structure is useful for exploratory data analysis before visualization or modeling.
        """
    )






