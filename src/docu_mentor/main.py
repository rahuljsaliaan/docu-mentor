import streamlit as st
import os
import subprocess

from docu_mentor.ui.helpers.session import init_session_state
from docu_mentor.ui.setup import setup_url_input
from docu_mentor.ui.chat import chat_interface
from docu_mentor.types.enums import SessionStateEnum, ComponentsKeyEnum


def main():
    if not os.getenv("STREAMLIT_RUNNING", "false") == "true":
        os.environ["STREAMLIT_RUNNING"] = "true"
        subprocess.run(["streamlit", "run", os.path.abspath(__file__), "--server.port", "8000"])


    st.set_page_config(
        page_title="DocuMentor – AI-Powered Documentation Assistant", 
        page_icon="static/favicon.png",
        initial_sidebar_state="collapsed"
    )

    if SessionStateEnum.documentation_url in st.session_state:
        chat_interface()
    else:
        # Initialize session state
        init_session_state()

        # Show setup URL input
        setup_url_input()

    # Show chat interface


if __name__ == "__main__":
    main()
