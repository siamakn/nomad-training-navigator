import streamlit as st
import json
import os

VOCAB_FILE = "vocabulary.json"


def load_vocab():
    if not os.path.exists(VOCAB_FILE):
        return {"topics": [], "keywords": []}
    with open(VOCAB_FILE, "r") as f:
        return json.load(f)


def save_vocab(vocab):
    with open(VOCAB_FILE, "w") as f:
        json.dump(vocab, f, indent=2)


def manage_vocab():
    st.header("🛠️ Manage Vocabulary")

    vocab = load_vocab()

    st.subheader("📚 Topics")
    new_topic = st.text_input("Add a new topic")
    if st.button("Add Topic"):
        if new_topic and new_topic not in vocab["topics"]:
            vocab["topics"].append(new_topic.strip())
            save_vocab(vocab)
            st.success(f"Added topic: {new_topic}")

    remove_topic = st.selectbox("Remove a topic", options=["-- select --"] + vocab["topics"])
    if st.button("Remove Topic") and remove_topic != "-- select --":
        vocab["topics"].remove(remove_topic)
        save_vocab(vocab)
        st.warning(f"Removed topic: {remove_topic}")

    st.write("Current Topics:", vocab["topics"])

    st.subheader("🔑 Keywords")
    new_keyword = st.text_input("Add a new keyword")
    if st.button("Add Keyword"):
        if new_keyword and new_keyword not in vocab["keywords"]:
            vocab["keywords"].append(new_keyword.strip())
            save_vocab(vocab)
            st.success(f"Added keyword: {new_keyword}")

    remove_keyword = st.selectbox("Remove a keyword", options=["-- select --"] + vocab["keywords"])
    if st.button("Remove Keyword") and remove_keyword != "-- select --":
        vocab["keywords"].remove(remove_keyword)
        save_vocab(vocab)
        st.warning(f"Removed keyword: {remove_keyword}")

    st.write("Current Keywords:", vocab["keywords"])
