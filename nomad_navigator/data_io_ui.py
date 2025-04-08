import streamlit as st
import pandas as pd
from nomad_navigator.data_loader import load_resources_from_csv, save_resources_to_csv


def data_io():
    st.header("📁 Import / Export Resources")

    if st.button("📤 Export CSV"):
        resources = load_resources_from_csv()
        df = pd.DataFrame([r.__dict__ for r in resources])
        df["topics"] = df["topics"].apply(lambda x: ";".join(x))
        df["keywords"] = df["keywords"].apply(lambda x: ";".join(x))
        st.download_button("Download resources.csv", df.to_csv(index=False), file_name="resources.csv")

    uploaded_file = st.file_uploader("📥 Import CSV", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)
        if st.button("Replace existing data"):
            from nomad_navigator.models import Resource
            resources = [
                Resource(
                    title=row["title"],
                    url=row["url"],
                    resource_type=row["resource_type"],
                    topics=row["topics"].split(";"),
                    keywords=row["keywords"].split(";"),
                    status_tag=row["status_tag"],
                    difficulty=row["difficulty"]
                ) for _, row in df.iterrows()
            ]
            save_resources_to_csv(resources)
            st.success("Data replaced!")