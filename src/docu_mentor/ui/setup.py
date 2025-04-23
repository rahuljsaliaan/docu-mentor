import streamlit as st
import time

from docu_mentor.utils import is_valid_url
from docu_mentor.types.enums import SessionStateEnum, ComponentsKey
from docu_mentor.ai import ingest_docs_from_url


def setup_url_input():
    url_setup_title = st.title("🔗 DocuMentor Setup")

    url_input_container = st.empty()

    # Render the URL input field inside the container
    url = url_input_container.text_input(
        "Enter the documentation URL",
        placeholder="https://example.com/docs",
        key=ComponentsKey.url_input,
    )

    if url:
        if is_valid_url(url):
            success_message_url = st.success("✅ Valid URL")

            with st.spinner("Ingesting documents..."):

                faiss_index = ingest_docs_from_url(url=url)
                st.session_state[SessionStateEnum.faiss_index] = faiss_index

            success_message_ingestion = st.success(
                "✅ Documents ingested successfully!"
            )

            # Add a delay of 2 seconds before clearing the message
            time.sleep(2)
            st.session_state[SessionStateEnum.documentation_url] = url
            success_message_url.empty()
            url_setup_title.empty()
            url_input_container.empty()
            success_message_ingestion.empty()
        else:
            st.error("❌ Please enter a valid URL starting with http:// or https://")
            st.stop()
    else:
        st.warning("⚠️ Please enter a documentation URL to start.")
        st.stop()
