import streamlit as st

# session state initialization (api keys)
if "key_openai_proxy" not in st.session_state:
    st.session_state.key_openai_proxy = {
        "OPENAI_API_KEY": "",
        "BASE_URL": ""
    }

if "key_xunfei" not in st.session_state:
    st.session_state.keys_xunfei = {
        "APPID": "",
        "API_SECRET": "",
        "API_KEY": ""
    }

if "key_zhipuai" not in st.session_state:
    st.session_state.keys_zhipuai = {
        "API_KEY": ""
    }

# session state initialization (user)
if "user" not in st.session_state:
    st.session_state.user = {
        "name": "",
        "gender": ""
    }


def get_user_name():
    st.title("Who are you?")
    name = st.text_input("Please enter your name")
    gender = st.radio(
        "Please select your gender",
        ["Secret", "Male", "Female"],
        index=0
    )

    submit_user_name = st.button("Submit user name")
    if submit_user_name:
        st.session_state.user["name"] = name
        st.session_state.user["gender"] = gender


def get_key_config():
    st.title("Key Configuration")
    key_type = st.selectbox(
        "Please select your key type",
        ["openai-proxy", "xunfei", "zhipuai"],
        index=0
    )
    if key_type == "openai-proxy":
        openai_api_key = st.text_input("OpenAI API Key")
        # base_url = st.text_input("Base URL")

        submit_key_config_openai_proxy = st.button("Submit key config for OpenAI proxy")
        if submit_key_config_openai_proxy:
            st.session_state.key_openai_proxy["OPENAI_API_KEY"] = openai_api_key
            st.session_state.key_openai_proxy["BASE_URL"] = "https://api.aigc369.com/v1"
            print(st.session_state.key_openai_proxy)

    elif key_type == "xunfei":
        app_id = st.text_input("APP ID")
        api_secret = st.text_input("API Secret")
        api_key = st.text_input("API Key")

        submit_key_config_xunfei = st.button("Submit key config for Xunfei")
        if submit_key_config_xunfei:
            st.session_state.keys_xunfei["APPID"] = app_id
            st.session_state.keys_xunfei["API_SECRET"] = api_secret
            st.session_state.keys_xunfei["API_KEY"] = api_key
            print(st.session_state.keys_xunfei)

    elif key_type == "zhipuai":
        api_key = st.text_input("API Key")

        submit_key_config_zhipuai = st.button("Submit key config for Zhipuai")
        if submit_key_config_zhipuai:
            st.session_state.keys_zhipuai["API_KEY"] = api_key
            print(st.session_state.keys_zhipuai)
