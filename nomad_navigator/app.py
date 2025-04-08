import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import streamlit as st
from nomad_navigator.filter_ui import filter_view
from nomad_navigator.input_form import input_form
from nomad_navigator.data_io_ui import data_io

st.set_page_config(page_title="NOMAD Training Navigator", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["🔎 Filter View", "➕ Add Resource", "📁 Import/Export"])

if page == "🔎 Filter View":
    filter_view()
elif page == "➕ Add Resource":
    input_form()
elif page == "📁 Import/Export":
    data_io()
