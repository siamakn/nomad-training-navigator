# ui_components/resource_row.py
import streamlit as st

def render_resource_row(resource, selected_id, has_unsaved_changes_callback):
    row_id = resource.id
    cols = st.columns([0.5, 0.7, 2, 2, 1, 2, 2, 2, 1, 1])
    with cols[0]:
        if st.button("\U0001F518" if resource.id == selected_id else "\u25CB", key=f"radio_{resource.id}", use_container_width=True):
            if not st.session_state.edit_mode.get(selected_id, False) or not has_unsaved_changes_callback(selected_id):
                st.session_state.selected_row_id = resource.id
                st.rerun()
            else:
                st.toast(f"\u26A0\uFE0F Unsaved changes in row {selected_id}. Please save or cancel before switching.")
    cols[1].markdown(f"`{str(resource.id)[:6]}`")
    cols[2].markdown(f"**{resource.resource_type}**")
    cols[3].markdown(f"{resource.resource_subtype}")
    cols[4].markdown(f"{resource.format}")
    cols[5].markdown(f"[{resource.title}]({resource.url})")
    cols[6].markdown(f"{', '.join(resource.topics)}")
    cols[7].markdown(f"{', '.join(resource.keywords)}")
    cols[8].markdown(f"`{resource.status_tag}`")
    cols[9].markdown(f"_{resource.difficulty}_")