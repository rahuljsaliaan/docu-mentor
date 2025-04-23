import streamlit as st

from docu_mentor.types.enums import SessionStateEnum


def init_session_state():
    if SessionStateEnum.user_prompt_history not in st.session_state:
        st.session_state[SessionStateEnum.user_prompt_history] = []

    if SessionStateEnum.chat_answer_history not in st.session_state:
        st.session_state[SessionStateEnum.chat_answer_history] = []

    if SessionStateEnum.chat_history not in st.session_state:
        st.session_state[SessionStateEnum.chat_history] = []
