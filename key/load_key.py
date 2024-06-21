import yaml

# open or no
openai_proxy_or = False
moonshot_ai_or = True
check_or = True

# read the key file
key_file_path = "key.yaml"
with open(key_file_path, 'r') as file:
    key_data = yaml.safe_load(file)

openai_proxy = key_data.get('openai-proxy') if openai_proxy_or else None
moonshot_ai = key_data.get('moonshot-ai') if moonshot_ai_or else None


def get_openai_proxy_key():
    openai_proxy_key = openai_proxy.get('OPENAI_API_KEY')
    base_url = "https://api.aigc369.com/v1"

    if check_or:
        print('openai_proxy: key is set')
        print(openai_proxy_key, base_url)

    return openai_proxy_key, base_url


def get_moonshot_key():
    kimi_api_key = moonshot_ai.get("KIMI_API_KEY")
    base_url = "https://api.moonshot.cn/v1"

    if check_or:
        print('moonshot_ai: key is set')
        print(kimi_api_key, base_url)

    return kimi_api_key, base_url


def test_openai_proxy():
    from openai import OpenAI

    openai_proxy_key, base_url = get_openai_proxy_key()
    client = OpenAI(api_key=openai_proxy_key, base_url=base_url)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一个热爱好故事的文学家，同时也是有着深厚的文学功底的作家。"},
            {"role": "user", "content": "给我推荐一个影视作品吧"},
            {"role": "assistant",
             "content": "好的，我将给您推荐《doctor who》，并且我有足够打动你的理由！我最喜欢其中的一句话，他有着直击灵魂的力量，相信这也能鼓动你！"},
            {"role": "user", "content": "是吗？我很期待你的理由和你喜欢的那句话！"},
        ],
        max_tokens=300
    )

    print(response)

    """
    ChatCompletion(
      id='chatcmpl-9OaB6MjBAJUCPAfXcIwsQqvY8cLwa', 
      choices=[
        Choice(
          finish_reason='stop', 
          index=0, 
          logprobs=None, 
          message=ChatCompletionMessage(
            content=
              "当然！《doctor who》是一部英国科幻电视剧，已经播出了多个季度。这部剧讲述了一个神秘的时间领主“博士”（The Doctor）
              和他的伙伴们在时间和空间中历险的故事。剧中融合了科幻、冒险、幽默等元素，而博士的心灵与智慧更是整个系列的核心所在。\n\n
              我的最爱的一句经典台词是：“We're all stories in the end. Just make it a good one, eh?”
              （最后我们都只是故事，那就让它成为一个美好的故事，好吗？）这句话深刻表达了人生的意义，
              也传达了《doctor who》对于故事和人生的独特见解。希望你能喜欢并感受到它所带来的魅力！", 
            role='assistant', 
            function_call=None, 
            tool_calls=None
          )
        )
      ], 
      created=1715645968, 
      model='gpt-3.5-turbo-0125', 
      object='chat.completion', 
      system_fingerprint=None, 
      usage=CompletionUsage(completion_tokens=266, prompt_tokens=163, total_tokens=429)
    )
    """


def test_moonshot_ai():
    from openai import OpenAI

    kimi_api_key, base_url = get_moonshot_key()
    client = OpenAI(api_key=kimi_api_key, base_url=base_url)

    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {
                "role": "system",
                "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"
            },
            {
                "role": "user",
                "content": "你好，我叫李雷，1+1等于多少？"
            }
        ],
        temperature=0.3,
    )

    print(completion.choices[0].message)

    """
    ChatCompletionMessage(
      content='你好，李雷！1+1等于2。这是一个基本的数学加法运算。如果你有任何其他问题，欢迎随时提问。', 
      role='assistant', 
      function_call=None, 
      tool_calls=None
      )
    """


if __name__ == '__main__':
    print("start test")
    # test_openai_proxy()  # ok
    # test_moonshot_ai()  # ok
