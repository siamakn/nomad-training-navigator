import streamlit as st
from nomad_navigator.data_loader import load_resources_from_csv
from nomad_navigator.resource_manager import filter_resources
from nomad_navigator.models import Resource
from typing import List

def multi_filter_resources(resources: List[Resource], topics: List[str], keywords: List[str], tags: List[str], difficulties: List[str]) -> List[Resource]:
    filtered = resources
    if topics:
        filtered = [r for r in filtered if any(t in r.topics for t in topics)]
    if keywords:
        filtered = [r for r in filtered if any(k in r.keywords for k in keywords)]
    if tags:
        filtered = [r for r in filtered if r.status_tag in tags]
    if difficulties:
        filtered = [r for r in filtered if r.difficulty in difficulties]
    return filtered

def filter_view():
    st.header("🔎 Browse and Filter Resources")
    resources = load_resources_from_csv()

    all_topics = sorted(set(t for r in resources for t in r.topics))
    all_keywords = sorted(set(k for r in resources for k in r.keywords))
    all_tags = sorted(set(r.status_tag for r in resources))
    all_difficulties = sorted(set(r.difficulty for r in resources))

    selected_topics = st.multiselect("Filter by Topics", all_topics)
    selected_keywords = st.multiselect("Filter by Keywords", all_keywords)
    selected_tags = st.multiselect("Filter by Status Tag", all_tags)
    selected_difficulties = st.multiselect("Filter by Difficulty", all_difficulties)

    filtered = multi_filter_resources(resources, selected_topics, selected_keywords, selected_tags, selected_difficulties)

    st.write(f"Showing {len(filtered)} result(s):")
    for r in filtered:
        st.markdown(f"### [{r.title}]({r.url})")
        st.markdown(f"**Type**: {r.resource_type} | **Tags**: {r.status_tag}, {r.difficulty}")
        st.markdown(f"**Topics**: {', '.join(r.topics)}")
        st.markdown(f"**Keywords**: {', '.join(r.keywords)}")
        st.markdown("---")
