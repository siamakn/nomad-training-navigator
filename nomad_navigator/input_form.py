import streamlit as st
import json
import os
from nomad_navigator.models import Resource
from nomad_navigator.data_loader import load_resources_from_csv, save_resources_to_csv

VOCAB_FILE = "vocabulary.json"

DEFAULT_TOPICS = [
    "GeneralNOMAD", "Publish", "Explore", "Analyze", "ELN",
    "API", "OasisCustomization", "OasisInstallation", "OasisConficuration"
]

DEFAULT_KEYWORDS = [
    "login", "register", "Introduction", "UploadData", "CreateDataset", "GetDOI",
    "ManageMembers", "SupportedFiles", "FilterMenu", "Widgets", "Dashboard",
    "NORTH", "BuiltinSchema", "CustomYAMLSchema", "TabularParserYAML", "BaseSection",
    "NeXusDataConverter", "WriteApp", "WriteExampleUpload", "WriteNormalizer",
    "WriteParser", "WriteSchemaPackage", "DevelopPlugin", "InstallPlugin",
    "InstallOasis", "ConfigureOasis"
]

def load_vocab():
    if not os.path.exists(VOCAB_FILE):
        return {"topics": DEFAULT_TOPICS.copy(), "keywords": DEFAULT_KEYWORDS.copy()}
    with open(VOCAB_FILE, "r") as f:
        return json.load(f)

def save_vocab(vocab):
    with open(VOCAB_FILE, "w") as f:
        json.dump(vocab, f, indent=2)

def input_form():
    st.header("➕ Add a New Resource")

    vocab = load_vocab()
    title = st.text_input("Title")
    url = st.text_input("URL")
    resource_type = st.selectbox("Type", ["Video", "Page", "Misc"])

    existing_resources = load_resources_from_csv()
    existing_topics = sorted(set(t for r in existing_resources for t in r.topics))
    existing_keywords = sorted(set(k for r in existing_resources for k in r.keywords))

    suggested_topics = sorted(set(vocab["topics"] + existing_topics))
    suggested_keywords = sorted(set(vocab["keywords"] + existing_keywords))

    selected_topics = st.multiselect("Topics", options=suggested_topics)
    new_topic = st.text_input("Add a new topic (optional)")
    if new_topic and new_topic not in selected_topics:
        selected_topics.append(new_topic)
        if new_topic not in vocab["topics"]:
            vocab["topics"].append(new_topic)

    selected_keywords = st.multiselect("Keywords", options=suggested_keywords)
    new_keyword = st.text_input("Add a new keyword (optional)")
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
                title=title,
                url=url,
                resource_type=resource_type,
                topics=[t.strip() for t in selected_topics if t.strip()],
                keywords=[k.strip() for k in selected_keywords if k.strip()],
                status_tag=status_tag,
                difficulty=difficulty
            )
            existing_resources.append(new_resource)
            save_resources_to_csv(existing_resources)
            save_vocab(vocab)  # Save the updated vocab permanently
            st.success("Resource added!")
        else:
            st.warning("Title and URL are required.")