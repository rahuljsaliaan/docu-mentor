import os
import subprocess

from docu_mentor.ui.helpers.session import init_session_state
from docu_mentor.ui.setup import setup_url_input
from docu_mentor.ui.chat import chat_interface


def main():
    if not os.getenv("STREAMLIT_RUNNING", "false") == "true":
        os.environ["STREAMLIT_RUNNING"] = "true"
        subprocess.run(["streamlit", "run", os.path.abspath(__file__)])
        return

    # Initialize session state
    init_session_state()

    # Show setup URL input
    setup_url_input()

    # Show chat interface
    chat_interface()


if __name__ == "__main__":
    main()
