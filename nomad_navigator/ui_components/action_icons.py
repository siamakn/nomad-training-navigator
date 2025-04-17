# ui_components/action_icons.py
import streamlit as st
from nomad_navigator.data_loader import load_resources_from_csv, save_resources_to_csv

def render_action_icons(row_id):
    icon_cols = st.columns([0.15, 0.15, 0.15])
    if icon_cols[0].button("\u270F\ufe0f", key=f"icon_edit_{row_id}", help="Edit this row", use_container_width=True):
        st.session_state.edit_mode[row_id] = True
        st.rerun()
    if icon_cols[1].button("\U0001F5D1\ufe0f", key=f"icon_delete_{row_id}", help="Delete this row", use_container_width=True):
        delete_row(row_id)
    if icon_cols[2].button("\u2795", key=f"icon_add_{row_id}", help="Insert a new row below", use_container_width=True):
        st.session_state.insert_below[row_id] = True
        st.rerun()

def delete_row(row_id):
    resources = load_resources_from_csv(convert_lists=True)
    updated = [r for r in resources if r.id != row_id]
    save_resources_to_csv(updated, convert_lists=True)
    st.session_state.selected_row_id = None
    st.rerun()