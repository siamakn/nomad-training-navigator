# preview_csv_ui.py
import streamlit as st
from nomad_navigator.data_loader import load_resources_from_csv, save_resources_to_csv
from nomad_navigator.models import Resource
from nomad_navigator.utils import generate_sequential_id
import json
import os

from ui_components.table_header import render_table_header
from ui_components.resource_row import render_resource_row
from ui_components.action_icons import render_action_icons
from ui_components.compact_edit_insert_form import render_edit_form, render_insert_form

VOCAB_FILE = "vocabulary.json"

def load_vocab():
    if not os.path.exists(VOCAB_FILE):
        return {"topics": [], "keywords": [], "formats": [], "resource_types": [], "resource_subtypes": []}
    with open(VOCAB_FILE, "r") as f:
        return json.load(f)

def preview_csv():
    for k in list(st.session_state.keys()):
        if k.startswith("edit_new_topic_") or k.startswith("edit_new_keyword_"):
            del st.session_state[k]

    st.header("📄 Preview & Manage Resources")

    resources = load_resources_from_csv(convert_lists=True)
    vocab = load_vocab()

    if not resources:
        st.info("No resources found. Add new resources first.")
        return

    if "edit_mode" not in st.session_state:
        st.session_state.edit_mode = {}
    if "insert_below" not in st.session_state:
        st.session_state.insert_below = {}

    def has_unsaved_changes(row_id):
        if row_id and st.session_state.get(f"initial_values_{row_id}"):
            initial = st.session_state[f"initial_values_{row_id}"]
            form_inputs = {
                "title": st.session_state.get("title", ""),
                "url": st.session_state.get("url", ""),
                "topics": st.session_state.get("topics", []),
                "keywords": st.session_state.get("keywords", []),
                "status_tag": st.session_state.get("status_tag", ""),
                "difficulty": st.session_state.get("difficulty", "")
            }
            return any([
                form_inputs["title"] != initial.get("title"),
                form_inputs["url"] != initial.get("url"),
                form_inputs["topics"] != initial.get("topics"),
                form_inputs["keywords"] != initial.get("keywords"),
                form_inputs["status_tag"] != initial.get("status_tag"),
                form_inputs["difficulty"] != initial.get("difficulty")
            ])
        return False

    selected_id = st.session_state.get("selected_row_id")

    render_table_header()

    for idx, resource in enumerate(resources):
        row_id = resource.id
        with st.container():
            render_resource_row(resource, selected_id, has_unsaved_changes)
            if resource.id == selected_id:
                render_action_icons(row_id)

        if st.session_state.edit_mode.get(row_id, False):
            render_edit_form(resource, row_id, resources, vocab)

        if st.session_state.insert_below.get(row_id, False):
            render_insert_form(row_id, resources, vocab)

def delete_row(row_id):
    resources = load_resources_from_csv(convert_lists=True)
    updated = [r for r in resources if r.id != row_id]
    save_resources_to_csv(updated, convert_lists=True)
    st.session_state.selected_row_id = None
    st.rerun()
