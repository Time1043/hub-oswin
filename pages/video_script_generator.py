import sys

import streamlit as st

sys.path.append("..")
from service.to_openai_proxy import generate_video_script

# sidebar
with st.sidebar:
    openai_proxy_key = st.text_input("Enter your OpenAI API keys:", type="password")
    st.markdown("[Get the OpenAI API key](https://platform.openai.com/account/api-keys)")

# user input
st.title("🎬 video script generator")
subject = st.text_input("💡 Enter the subject of the video")
video_length = st.number_input("⏰ Enter the length of the video in minutes", min_value=0.5, value=0.6, step=0.1)
creativity = st.slider(
    "✨ Enter your creativity level (Smaller numbers indicate rigor, larger numbers indicate variety)",
    min_value=0.0, max_value=1.2, value=0.2, step=0.1
)
submit = st.button("Generate Video Script")

# service call (openai_proxy_key, subject)
if submit and not openai_proxy_key:
    st.info("Please enter your OpenAI API keys in the sidebar to use this feature.")
    st.stop()
if submit and not subject:
    st.info("Please enter the subject of the video.")
    st.stop()
if submit:
    with st.spinner("AI is thinking, please hold on..."):
        try:
            search_results, title, script = generate_video_script(subject, video_length, creativity, openai_proxy_key)
        except Exception as err:
            st.error(f"An error occurred: {err}")
            st.stop()

    st.success("Done!")
    st.subheader("🔥 Title")
    st.write(title)
    st.subheader("📝 Script")
    st.write(script)
    with st.expander("Search Results of Wikipedia 👀"):
        st.write(search_results)
