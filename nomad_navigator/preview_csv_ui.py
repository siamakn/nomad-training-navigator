import streamlit as st
import pandas as pd
from nomad_navigator.data_loader import CSV_FILE

def preview_csv():
    st.header("📄 Preview CSV File")
    try:
        df = pd.read_csv(CSV_FILE)
        if not df.empty:
            # Convert URL column to markdown links
            if "url" in df.columns:
                df["title"] = df.apply(lambda row: f"[{row['title']}]({row['url']})", axis=1)
            st.write("### Resources:")
            st.write(df.drop(columns=["url"]))
        else:
            st.warning("resources.csv is empty.")
    except FileNotFoundError:
        st.warning("resources.csv file not found.")
    except pd.errors.EmptyDataError:
        st.warning("resources.csv is empty.")
