import streamlit as st
import subprocess
import os

from docu_mentor.ai.rag import run_llm
from docu_mentor.types.enums import SessionStateEnum, ComponentsKeyEnum
from docu_mentor.utils import get_main_doc_name_from_url


def chat_interface():
    st.header("DocuMentor - Documentation Assistant Bot")

    # Display the documentation URL if available
    if SessionStateEnum.documentation_url in st.session_state:
        doc_url = st.session_state[SessionStateEnum.documentation_url]
        doc_name = get_main_doc_name_from_url(doc_url)
        st.write(f"🔗 **Working with {doc_name} docs**: {doc_url}")

    # Disable prompt input while generating the response
    is_generating = st.session_state.get(SessionStateEnum.generating_response, False)

    # Show chat input only if not generating a response
    prompt = st.chat_input(
        placeholder=f"What would you like to explore in the {doc_name} docs today?",
        key=ComponentsKeyEnum.chat_prompt,
        disabled=is_generating  # Disable input while generating response
    )

    if prompt:
        # Store prompt in session state and set generating flag
        st.session_state[SessionStateEnum.generating_response] = True
        generate_results(prompt)


def generate_results(prompt: str):
    if prompt:
        with st.spinner("Generating response..."):
            response = run_llm(
                query=prompt,
                chat_history=st.session_state[SessionStateEnum.chat_history],
                faiss_index=st.session_state[SessionStateEnum.faiss_index],
            )

            # Append the user's query and AI's response to history
            st.session_state[SessionStateEnum.user_prompt_history].append(prompt)
            st.session_state[SessionStateEnum.chat_answer_history].append(
                response.formatted_response
            )
            st.session_state[SessionStateEnum.chat_history].append(("human", prompt))
            st.session_state[SessionStateEnum.chat_history].append(
                ("ai", response.result)
            )

        # Reset the generating state after response is generated
        st.session_state[SessionStateEnum.generating_response] = False

    # Display chat history (user and assistant messages)
    if st.session_state[SessionStateEnum.chat_answer_history]:
        for user_query, generated_response in zip(
            st.session_state[SessionStateEnum.user_prompt_history],
            st.session_state[SessionStateEnum.chat_answer_history],
        ):
            st.chat_message("user").write(user_query)
            st.chat_message("assistant").write(generated_response)


def main():
    # Check if we're running inside Streamlit by setting and checking an environment variable
    if not os.getenv("STREAMLIT_RUNNING", "false") == "true":
        # Set the environment variable to prevent recursive running
        os.environ["STREAMLIT_RUNNING"] = "true"
        # Run Streamlit via subprocess if not already running
        subprocess.run(["streamlit", "run", os.path.abspath(__file__)]) 


if __name__ == "__main__":
    main()
