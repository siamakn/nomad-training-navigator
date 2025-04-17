# ui_components/table_header.py
import streamlit as st


def render_table_header():
    header_cols = st.columns([0.5, 0.7, 2, 2, 1, 2, 2, 2, 1, 1])
    headers = ["Select", "ID", "Type", "Subtype", "Format", "Title", "Topics", "Keywords", "Status", "Difficulty"]
    for col, header in zip(header_cols, headers):
        col.markdown(f"**{header}**")