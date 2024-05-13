from openai import OpenAI
import streamlit as st
from pages_common import get_user_name, get_key_config


def init_sidebar():
    # sidebar
    with st.sidebar:
        get_user_name()
        st.divider()
        get_key_config()


def init_welcome_title():
    # Welcome message

    if 'user' not in st.session_state:
        st.session_state.user = None

    if not st.session_state.user:
        st.title("Welcome!")
    elif st.session_state.user["gender"] == "Male":
        st.title(f"Welcome Mr. {st.session_state.user['name']}! ")
    elif st.session_state.user["gender"] == "Female":
        st.title(f"Welcome Mrs. {st.session_state.user['name']}! ")


def chat_openai_proxy(openai_api_key, base_url, user_input):
    if not openai_api_key:
        st.error("Please provide OpenAI API Key")
        return

    try:
        client = OpenAI(api_key=openai_api_key, base_url=base_url)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个热爱好故事的文学家，同时也是有着深厚的文学功底的作家。"},
                {"role": "user", "content": "给我推荐一个影视作品吧"},
                {"role": "assistant", "content": "好的，猜测您喜欢的是有关科幻的、文学的！"},
                {"role": "user", "content": user_input},
            ],
            max_tokens=300
        )

        print(response)
        output = response.choices[0].message.content
        st.write(output)

    except Exception as err:
        st.error(err)


def chat_get_start():
    user_input = st.text_area(
        "Let's talk about movies with me: ",
        value="你最喜欢《三体》中的哪一句话？"
    )
    submit_chat_start = st.button("Submit chat start")

    if submit_chat_start:
        st.write(user_input)

        openai_api_key = st.session_state.key_openai_proxy["OPENAI_API_KEY"]
        base_url = st.session_state.key_openai_proxy["BASE_URL"]

        chat_openai_proxy(openai_api_key, base_url, user_input)


def chat_adjusting_parameter():
    model = [
        "babbage-002", "code-davinci-edit-001", "dall-e-2", "davinci-002",
        "gpt-3.5-turbo", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-1106",
        "gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613", "gpt-3.5-turbo-instruct",
        "text-ada-001", "text-babbage-001", "text-curie-001", "text-davinci-002",
        "text-davinci-003", "text-davinci-edit-001", "text-embedding-v1",
        "text-moderation-latest", "text-moderation-stable",
        "tts-1", "tts-1-1106", "tts-1-hd", "tts-1-hd-1106",
        "whisper-1",
    ]
    pass


def chat_qualified_output_format():
    pass


init_sidebar()
init_welcome_title()

tab_get_start, tab_adjusting_parameter, tab_qualified_output_format = st.tabs(
    ["Get start", "Adjusting parameter", "Qualified output format"]
)

with tab_get_start:
    st.header("Get start")
    chat_get_start()

with tab_adjusting_parameter:
    st.header("Adjusting parameter")

with tab_qualified_output_format:
    st.header("Qualified output format")
