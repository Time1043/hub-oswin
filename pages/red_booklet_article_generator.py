import streamlit as st
import sys

sys.path.append("..")
from service.to_openai_proxy import generate_red_booklet_article

# sidebar
with st.sidebar:
    openai_proxy_key = st.text_input("Enter your OpenAI API keys:", type="password")
    st.markdown("[Get the OpenAI API key](https://platform.openai.com/account/api-keys)")

# user input
st.header("AI writing assistant for red booklet ✏️")
theme = st.text_input("theme")
submit = st.button("start writing")

# service call (openai_proxy_key, theme)
if submit and not openai_proxy_key:
    st.info("Please enter your OpenAI API keys in the sidebar to use this feature.")
    st.stop()
if submit and not theme:
    st.info("Please enter the theme of the red booklet to generate the article.")
    st.stop()
if submit:
    with st.spinner("AI writing assistant is generating the article..."):
        try:
            result = generate_red_booklet_article(theme, openai_proxy_key)
        except Exception as err:
            st.error(f"Error: {err}")
            st.stop()

    st.success("AI writing assistant has generated the article!")
    st.divider()
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown("##### title1")
        st.write(result.titles[0])
        st.markdown("##### title2")
        st.write(result.titles[1])
        st.markdown("##### title3")
        st.write(result.titles[2])
        st.markdown("##### title4")
        st.write(result.titles[3])
        st.markdown("##### title5")
        st.write(result.titles[4])
    with right_column:
        st.markdown("##### content")
        st.write(result.content)
