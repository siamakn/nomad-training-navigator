import streamlit as st
from nomad_navigator.models import Resource
from nomad_navigator.data_loader import load_resources_from_csv, save_resources_to_csv

def input_form():
    st.header("➕ Add a New Resource")

    title = st.text_input("Title")
    url = st.text_input("URL")
    resource_type = st.selectbox("Type", ["Video", "Page", "Misc"])
    topics = st.text_input("Topics (separate with ;)")
    keywords = st.text_input("Keywords (separate with ;)")
    status_tag = st.selectbox("Status", ["up-to-date", "deprecated-but-still-useful", "fully-deprecated"])
    difficulty = st.selectbox("Difficulty", [
        "basic usage",
        "customization level 1",
        "customization level 2",
        "configuration level 1",
        "configuration level 2",
    ])

    if st.button("Submit"):
        if title and url:
            new_resource = Resource(
                title=title,
                url=url,
                resource_type=resource_type,
                topics=[t.strip() for t in topics.split(";") if t.strip()],
                keywords=[k.strip() for k in keywords.split(";") if k.strip()],
                status_tag=status_tag,
                difficulty=difficulty
            )
            resources = load_resources_from_csv()
            resources.append(new_resource)
            save_resources_to_csv(resources)
            st.success("Resource added!")
        else:
            st.warning("Title and URL are required.")