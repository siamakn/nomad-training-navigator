import streamlit as st
import pandas as pd
from nomad_navigator.data_loader import CSV_FILE

def preview_csv():
    st.header("📄 Preview CSV File")
    try:
        df = pd.read_csv(CSV_FILE)
        if not df.empty:
            # Convert URL column to markdown links
            if "url" in df.columns and "title" in df.columns:
                df["title"] = df.apply(lambda row: f"[{row['title']}]({row['url']})", axis=1)

            columns_to_display = [
                "resource_type",
                "resource_subtype",
                "format",
                "title",
                "topics",
                "keywords",
                "status_tag",
                "difficulty"
            ]
            existing_columns = [col for col in columns_to_display if col in df.columns]

            st.write("### Resources:")
            st.dataframe(df[existing_columns])
        else:
            st.warning("resources.csv is empty.")
    except FileNotFoundError:
        st.warning("resources.csv file not found.")
    except pd.errors.EmptyDataError:
        st.warning("resources.csv is empty.")