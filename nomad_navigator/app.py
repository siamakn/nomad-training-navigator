import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from nomad_navigator.filter_ui import filter_view
from nomad_navigator.input_form import input_form
from nomad_navigator.data_io_ui import data_io
from nomad_navigator.preview_csv_ui import preview_csv
from nomad_navigator.manage_vocab_ui import manage_vocab


st.set_page_config(page_title="NOMAD Training Navigator", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "🔎 Filter View",
    "➕ Add Resource",
    "📁 Import/Export",
    "📄 Preview CSV",
    "🛠️ Manage Vocabulary"  # ← New tab
])


if page == "🔎 Filter View":
    filter_view()
elif page == "🛠️ Manage Vocabulary":
    manage_vocab()
elif page == "➕ Add Resource":
    input_form()
elif page == "📁 Import/Export":
    data_io()
elif page == "📄 Preview CSV":
    preview_csv()
