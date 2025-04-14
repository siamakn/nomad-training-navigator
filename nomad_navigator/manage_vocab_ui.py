import streamlit as st
import json
import os

VOCAB_FILE = "vocabulary.json"

def load_vocab():
    if not os.path.exists(VOCAB_FILE):
        return {"topics": [], "keywords": [], "formats": [], "resource_types": [], "resource_subtypes": []}
    with open(VOCAB_FILE, "r") as f:
        return json.load(f)

def save_vocab(vocab):
    with open(VOCAB_FILE, "w") as f:
        json.dump(vocab, f, indent=2)

def manage_vocab():
    st.header("🛠️ Manage Vocabulary")
    vocab = load_vocab()

    def vocab_section(title, key):
        st.subheader(title)
        new_value = st.text_input(f"Add a new {key}", key=f"add_{key}")
        if st.button(f"Add {key}", key=f"btn_add_{key}"):
            if new_value and new_value not in vocab[key]:
                vocab[key].append(new_value.strip())
                save_vocab(vocab)
                st.success(f"Added {key}: {new_value}")

        remove_value = st.selectbox(f"Remove a {key}", options=["-- select --"] + vocab[key], key=f"rm_select_{key}")
        if st.button(f"Remove {key}", key=f"btn_rm_{key}") and remove_value != "-- select --":
            vocab[key].remove(remove_value)
            save_vocab(vocab)
            st.warning(f"Removed {key}: {remove_value}")

        st.write(f"Current {key}s:", vocab[key])

    for section in [
        ("📚 Resource Types", "resource_types"),
        ("📘 Resource Subtypes", "resource_subtypes"),
        ("📦 Formats", "formats"),
        ("🏷️ Topics", "topics"),
        ("🔑 Keywords", "keywords")
    ]:
        vocab_section(*section)
