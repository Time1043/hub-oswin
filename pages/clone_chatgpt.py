import sys

import streamlit as st
from langchain.memory import ConversationBufferMemory

sys.path.append("..")
from service.to_openai_proxy import get_chat_response

# sidebar
with st.sidebar:
    openai_proxy_key = st.text_input("Enter your OpenAI API keys:", type="password")
    st.markdown("[Get the OpenAI API key](https://platform.openai.com/account/api-keys)")

# memory message (session state)
st.title("💬 clone ChatGPT")
if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
    st.session_state["messages"] = [
        {"role": "ai", "content": "你好，我是你的AI助手，有什么可以帮你的吗？"}
    ]

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

# user input
prompt = st.chat_input()
if prompt:
    if not openai_proxy_key:
        st.info("Please enter your OpenAI API keys in the sidebar to use this feature.")
        st.stop()
    st.session_state["messages"].append({"role": "human", "content": prompt})
    st.chat_message("human").write(prompt)

    with st.spinner("AI is thinking, please hold on..."):
        try:
            response = get_chat_response(prompt, st.session_state["memory"], openai_proxy_key)
        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

    msg = {"role": "ai", "content": response}
    st.session_state["messages"].append(msg)
    st.chat_message("ai").write(response)
