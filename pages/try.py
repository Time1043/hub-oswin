import streamlit as st


def init_welcome_title():
    if st.session_state.user["gender"] == "Male":
        st.title(f"Welcome Mr. {st.session_state.user['name']}! ")
    elif st.session_state.user["gender"] == "Female":
        st.title(f"Welcome Mrs. {st.session_state.user['name']}! ")
    else:
        st.title(f"Welcome {st.session_state.user['name']}! ")
