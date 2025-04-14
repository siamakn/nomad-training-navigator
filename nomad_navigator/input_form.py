import streamlit as st
import json
import os
from nomad_navigator.models import Resource
from nomad_navigator.data_loader import load_resources_from_csv, save_resources_to_csv

VOCAB_FILE = "vocabulary.json"


def load_vocab():
    if not os.path.exists(VOCAB_FILE):
        return {"topics": [], "keywords": [], "formats": [], "resource_types": [], "resource_subtypes": []}
    with open(VOCAB_FILE, "r") as f:
        return json.load(f)


def save_vocab(vocab):
    with open(VOCAB_FILE, "w") as f:
        json.dump(vocab, f, indent=2)


def input_form():
    st.header("➕ Add a New Resource")

    vocab = load_vocab()
    existing_resources = load_resources_from_csv()
    existing_topics = sorted(set(t for r in existing_resources for t in r.topics))
    existing_keywords = sorted(set(k for r in existing_resources for k in r.keywords))

    suggested_types = sorted(set(vocab.get("resource_types", [])))
    suggested_subtypes = sorted(set(vocab.get("resource_subtypes", [])))
    suggested_formats = sorted(set(vocab.get("formats", [])))
    suggested_topics = sorted(set(vocab.get("topics", []) + existing_topics))
    suggested_keywords = sorted(set(vocab.get("keywords", []) + existing_keywords))

    subtype_labels = {
        "FAIRmat Tutorial": "Which Part?",
        "Documentation": "What kind of documentation (Diataxis)?",
        "Workshop": "What is the subtype of this event (optional)?"
    }

    subtype_options_map = {
        "FAIRmat Tutorial": ["Part 1", "Part 2", "Part 3", "Part 4"],
        "Documentation": ["Tutorial", "How-to", "Explanation", "Reference"],
        "Workshop": []
    }

    col1, col2, col3 = st.columns(3)
    with col1:
        resource_type = st.selectbox("Resource Type", ["- select -"] + suggested_types, index=0, help="E.g., FAIRmat Tutorial, NOMAD Documentation, Workshop/Hackathon Documentation, Other.")
        new_type = st.text_input("Add new Resource Type (optional)", value="")
        if new_type and new_type not in suggested_types:
            resource_type = new_type
            vocab["resource_types"].append(new_type)

    with col2:
        if resource_type != "- select -":
            subtype_label = subtype_labels.get(resource_type, "Subtype")
            subtype_options = subtype_options_map.get(resource_type, [])
            resource_subtype = st.selectbox(subtype_label, ["- select -"] + subtype_options, index=0)
        else:
            st.selectbox("Subtype (locked)", ["Select resource type first"], index=0, disabled=True)
            resource_subtype = ""

        new_subtype = st.text_input("Add new Subtype (optional)", value="")
        if new_subtype and new_subtype not in suggested_subtypes:
            resource_subtype = new_subtype
            vocab["resource_subtypes"].append(new_subtype)

    with col3:
        format_val = st.selectbox("Format", ["- select -"] + suggested_formats, index=0)
        new_format = st.text_input("Add new Format (optional)", value="")
        if new_format and new_format not in suggested_formats:
            format_val = new_format
            vocab["formats"].append(new_format)

    title = st.text_input("Title")
    url = st.text_input("URL")

    selected_topics = st.multiselect("Topics", options=suggested_topics)
    new_topic = st.text_input("Add a new topic (optional)", value="")
    if new_topic and new_topic not in selected_topics:
        selected_topics.append(new_topic)
        if new_topic not in vocab["topics"]:
            vocab["topics"].append(new_topic)

    selected_keywords = st.multiselect("Keywords", options=suggested_keywords)
    new_keyword = st.text_input("Add a new keyword (optional)", value="")
    if new_keyword and new_keyword not in selected_keywords:
        selected_keywords.append(new_keyword)
        if new_keyword not in vocab["keywords"]:
            vocab["keywords"].append(new_keyword)

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
                resource_type=resource_type,
                resource_subtype=resource_subtype,
                format=format_val,
                title=title,
                url=url,
                topics=[t.strip() for t in selected_topics if t.strip()],
                keywords=[k.strip() for k in selected_keywords if k.strip()],
                status_tag=status_tag,
                difficulty=difficulty
            )
            existing_resources.append(new_resource)
            save_resources_to_csv(existing_resources)
            save_vocab(vocab)
            st.success("Resource added!")
        else:
            st.warning("Title and URL are required.")
