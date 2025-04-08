import streamlit as st
from nomad_navigator.data_loader import load_resources_from_csv
from nomad_navigator.resource_manager import filter_resources

def filter_view():
    st.header("🔎 Browse and Filter Resources")
    resources = load_resources_from_csv()

    topics = sorted(set(t for r in resources for t in r.topics))
    keywords = sorted(set(k for r in resources for k in r.keywords))
    tags = sorted(set(r.status_tag for r in resources))
    difficulties = sorted(set(r.difficulty for r in resources))

    topic_filter = st.selectbox("Topic", [None] + topics)
    keyword_filter = st.selectbox("Keyword", [None] + keywords)
    tag_filter = st.selectbox("Status Tag", [None] + tags)
    diff_filter = st.selectbox("Difficulty", [None] + difficulties)

    filtered = filter_resources(resources, topic_filter, keyword_filter, tag_filter, diff_filter)

    st.write(f"Showing {len(filtered)} result(s):")
    for r in filtered:
        st.markdown(f"### [{r.title}]({r.url})")
        st.markdown(f"**Type**: {r.resource_type} | **Tags**: {r.status_tag}, {r.difficulty}")
        st.markdown(f"**Topics**: {', '.join(r.topics)}")
        st.markdown(f"**Keywords**: {', '.join(r.keywords)}")
        st.markdown("---")
