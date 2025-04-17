# compact_edit_insert_form.py
import streamlit as st
import json
from nomad_navigator.models import Resource
from nomad_navigator.data_loader import save_resources_to_csv
from nomad_navigator.utils import generate_sequential_id

VOCAB_FILE = "vocabulary.json"

def update_vocab(vocab, new_topic, new_keyword):
    if new_topic and new_topic not in vocab["topics"]:
        vocab["topics"].append(new_topic)
    if new_keyword and new_keyword not in vocab["keywords"]:
        vocab["keywords"].append(new_keyword)
    with open(VOCAB_FILE, "w") as f:
        json.dump(vocab, f, indent=2)

def render_edit_form(resource, row_id, resources, vocab):
    with st.form(f"edit_form_{row_id}"):
        st.markdown("🔧 **Edit Resource**")

        format = st.selectbox(
            "Format",
            options=sorted(vocab.get("formats", [])),
            index=sorted(vocab.get("formats", [])).index(resource.format)
                if resource.format in vocab.get("formats", []) else 0,
            key=f"edit_format_{row_id}"
        )

        title = st.text_input("Title", value=resource.title)
        url = st.text_input("URL", value=resource.url)

        topic_cols = st.columns([3, 1])
        topics = topic_cols[0].multiselect("Topics", options=sorted(vocab.get("topics", [])),
                                           default=[t for t in resource.topics if t in vocab.get("topics", [])])
        new_topic = topic_cols[1].text_input("Add new topic", key=f"edit_new_topic_{row_id}", value="")

        keyword_cols = st.columns([3, 1])
        keywords = keyword_cols[0].multiselect("Keywords", options=sorted(vocab.get("keywords", [])),
                                               default=[k for k in resource.keywords if k in vocab.get("keywords", [])])
        new_keyword = keyword_cols[1].text_input("Add new keyword", key=f"edit_new_keyword_{row_id}", value="")

        status_cols = st.columns(2)
        status_tag = status_cols[0].selectbox("Status",
                                              ["up-to-date", "deprecated-but-still-useful", "fully-deprecated"],
                                              index=["up-to-date", "deprecated-but-still-useful", "fully-deprecated"]
                                              .index(resource.status_tag))
        difficulty = status_cols[1].selectbox("Difficulty",
                                              ["basic usage", "customization level 1", "customization level 2",
                                               "configuration level 1", "configuration level 2"],
                                              index=["basic usage", "customization level 1", "customization level 2",
                                                     "configuration level 1", "configuration level 2"]
                                              .index(resource.difficulty))

        col_submit, col_cancel = st.columns(2)
        if col_submit.form_submit_button("✅ Save"):
            if new_topic and new_topic not in topics:
                topics.append(new_topic)
            if new_keyword and new_keyword not in keywords:
                keywords.append(new_keyword)
            update_vocab(vocab, new_topic, new_keyword)

            resource.format = format
            resource.title = title
            resource.url = url
            resource.topics = topics
            resource.keywords = keywords
            resource.status_tag = status_tag
            resource.difficulty = difficulty

            save_resources_to_csv(resources, convert_lists=True)
            st.session_state.edit_mode[row_id] = False
            st.session_state.pop(f"initial_values_{row_id}", None)
            st.success("Changes saved.")
            st.rerun()
        if col_cancel.form_submit_button("❌ Cancel"):
            st.session_state.edit_mode[row_id] = False
            st.rerun()

def render_insert_form(row_id, resources, vocab):
    with st.form(f"insert_form_{row_id}"):
        st.markdown("🔻 **Insert New Resource Below**")

        st.info("Adding new resources is disabled. Please use the Add Resource page.")

        col_cancel = st.columns(1)[0]
        if col_cancel.form_submit_button("❌ Cancel"):
            st.session_state.insert_below[row_id] = False
            st.rerun()