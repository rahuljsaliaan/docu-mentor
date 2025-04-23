import streamlit as st
import subprocess
import os

from docu_mentor.rag import run_llm

st.header("DocuMentor - Documentation Assistant Bot")

prompt = st.text_input("Prompt", placeholder="Enter your prompt")


if prompt:
    with st.spinner("Generating response..."):
        generated_response = run_llm(query=prompt)
        formatted_response = generated_response.formatted_response
        st.text(formatted_response)


def main():
    # Check if we're running inside Streamlit by setting and checking an environment variable
    if not os.getenv("STREAMLIT_RUNNING", "false") == "true":
        # Set the environment variable to prevent recursive running
        os.environ["STREAMLIT_RUNNING"] = "true"
        # Run Streamlit via subprocess if not already running
        subprocess.run(["streamlit", "run", os.path.abspath(__file__)])


if __name__ == "__main__":
    main()
