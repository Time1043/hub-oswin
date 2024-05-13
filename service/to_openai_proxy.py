import sys

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI

sys.path.append("..")
from model_langchain.RedBooklet import RedBookletArticle
from prompt_template.red_booklet_article_template import system_template_text, user_template_text


def generate_video_script(
        subject, video_length, creativity,
        key_openai_proxy
):
    """
    Get video title (Prompt Template)
    Call the Wikipedia API to get the relevant information
    Get the script content of the video (Prompt Template)
    :param subject:
    :param video_length:
    :param creativity:
    :param key_openai_proxy:
    :return:
    """

    # Prompt Templates
    title_template = ChatPromptTemplate.from_messages(
        [
            (
                "human",
                "请为'{subject}'这个主题的视频想一个吸引人的标题（记住专有名词我希望你用英文的）"
            )
        ]
    )

    script_template = ChatPromptTemplate.from_messages(
        [
            (
                "human",
                """你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。（记住专有名词我希望你用英文的）
                视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
                要求开头抓住限球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间，结尾】分隔。
                整体内容的表达方式要尽量轻松有趣，吸引年轻人。
                脚本内容可以结合以下维基百科搜索出的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略：
                ```{wikipedia_search}```"""
            )
        ]
    )

    # Call the OpenAI API
    model = ChatOpenAI(
        openai_api_key=key_openai_proxy,
        openai_api_base="https://api.aigc369.com/v1",
        temperature=creativity
    )

    # Generate the title and script (Chains)
    title_chain = title_template | model
    script_chain = script_template | model
    title = title_chain.invoke({"subject": subject}).content

    # Call the Wikipedia API (proxy 7890)
    search = WikipediaAPIWrapper(lang="zh")
    search_result = search.run(subject)

    script = script_chain.invoke(
        {
            "title": title,
            "duration": video_length,
            "wikipedia_search": search_result
        }
    ).content

    return search_result, title, script


def generate_red_booklet_article(
        theme,
        key_openai_proxy
):
    """
    Generate a red booklet article and 5 titles (Prompt Template)
    :param theme:
    :param key_openai_proxy:
    :return:
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template_text),
        ("user", user_template_text)
    ])

    model = ChatOpenAI(model="gpt-3.5-turbo", api_key=key_openai_proxy, openai_api_base="https://api.aigc369.com/v1")
    output_parser = PydanticOutputParser(pydantic_object=RedBookletArticle)

    chain = prompt | model | output_parser
    result = chain.invoke({
        "parser_instructions": output_parser.get_format_instructions(),
        "theme": theme
    })
    return result


def get_chat_response(
        prompt, memory,
        key_openai_proxy
):
    """
    Conversations with memories
    :param prompt:
    :param memory:
    :param key_openai_proxy:
    :return:
    """
    model = ChatOpenAI(
        model="gpt-3.5-turbo",
        openai_api_key=key_openai_proxy,
        openai_api_base="https://api.aigc369.com/v1"
    )
    chain = ConversationChain(llm=model, memory=memory)

    response = chain.invoke({"input": prompt})
    return response["response"]


def test_generate_video_scrip():
    api_key = input("Please enter your OpenAI API key: ")
    print(generate_video_script("sora模型", 1, 0.7, api_key))

    """
    (
      'Page: 
        Sora (人工智能模型)\n
      Summary: 
        Sora是一个能以文本描述生成视频的人工智能模型，由美国人工智能研究机构OpenAI开发。\n
        Sora这一名称源于日文“空”（そら sora），即天空之意，以示其无限的创造潜力。其背后的技术是在OpenAI的文本到图像生成模型DALL-E基础上开发而成的。
        模型的训练数据既包含公开可用的视频，也包括了专为训练目的而获授权的版权视频，但OpenAI没有公开训练数据的具体数量与确切来源。
        \nOpenAI于2024年2月15日向公众展示了由Sora生成的多个高清视频，称该模型能够生成长达一分钟的视频。
        同时，OpenAI也承认了该技术的一些缺点，包括在模拟复杂物理现象方面的困难。
        《麻省理工科技评论》的报道称演示视频令人印象深刻，但指出它们可能是经精心挑选的，并不一定能代表Sora生成视频的普遍水准。\n
        由于担心Sora可能被滥用，OpenAI表示目前没有计划向公众发布该模型，而是给予小部分研究人员有限的访问权限，以理解模型的潜在危害。
        Sora生成的视频带有C2PA元数据标签，以表示它们是由人工智能模型生成的。OpenAI还与一小群创意专业人士分享了Sora，以获取对其实用性的反馈。\n\n
      Page: 
        東北俊子\n
      Summary: 
        東北俊子、俊达萌Project（日语：東北ずん子・ずんだもんプロジェクト），简称Zunzun Project（ずんずんプロジェクト），
        是日本SSS合同会社建立的跨媒体特许经营项目。此项目始于SSS在2011年10月27日公布的虚构人物「東北俊子」，
        她是为了鼓舞東日本大震災后的东北地方，由日本插画师江户村Ninico（江戸村ににこ）根据东北地方特产毛豆麻糬为题材而设计的美少女人物，
        之后延伸出「东北伊达子」「东北切蒲英」「尊达萌」等相關配角。SSS允许总部注册在东北地方的公司免费商用此项目中角色们的图像。
        自从建立以来，已经开展至包括小说、動畫、语音合成软件及相關產品。', '"探索未来的Sora模型：科技与创新的结合"', '【开头】\n
        大家好，欢迎来到我们的短视频频道！今天我们将探索未来的Sora模型：科技与创新的结合。你一定听说过Sora，一个能以文本描述生成视频的人工智能模型，
        让我们一起来看看它到底有多厉害吧！\n\n【中间】\n
        Sora这一名称源自日文“空”，意为天空，象征着无限的创造潜力。它的背后技术是在OpenAI的文本到图像生成模型DALL-E基础上开发而成的。
        虽然Sora能生成长达一分钟的高清视频，但也有一些缺点，比如在模拟复杂物理现象方面存在困难。不过，演示视频仍然令人印象深刻，展示了Sora的潜力。\n\n
        【结尾】\n虽然OpenAI目前没有计划向公众发布Sora模型，但仍与一小群创意专业人士分享，以获取反馈。未来，Sora可能会带来更多惊喜和创新，让我们拭目以待！
        记得关注我们的频道，了解更多有趣的科技新闻和创新技术！谢谢观看，我们下期再见！')
    """


def test_generate_red_booklet_article():
    api_key = input("Please enter your OpenAI API key: ")
    print(generate_red_booklet_article("微积分", api_key))

    """
    titles=[
      '🚀教科书般大模型，小白必看', '🔥大数据助力，打工人也能搞钱', '💥万万没想到的大模型秘方', 
      '🌟绝绝子大模型，让你破防了', '🔑高级感大模型，永远可以相信'
    ] 
    content='💡在当今大数据时代，大模型已经成为各行各业的热门话题。它们不仅教科书般强大，更能为小白们提供简单易懂的使用方法。
    利用大数据助力，即使是打工人，也能通过大模型来获得搞钱的秘诀。不得不说，大模型的神奇之处让人们万万没想到，它们的绝绝子特质真是让人破防了。
    拥有高级感的大模型让人永远可以相信，它们就像是隐藏在最深处的宝藏，等待着你的发现。'
    """

    """
    titles=[
      '微积分神器，小白必看！🔥', '停止摆烂！微积分教科书般解读！💪', '微积分绝绝子，手残党必备！😎', 
      '小红书爆款，上天在提醒你学微积分！🌟', '微积分大数据，解锁高级感！💡'
    ] 
    content='📚微积分，作为数学的重要分支之一，常常让人望而生畏。但实际上，掌握微积分可以让我们更好地理解世界的运行规律，
    应用到各个领域。不要害怕挑战，从基础开始学起，慢慢掌握微积分的奥秘，你会发现它其实并不难，甚至可以成为你的利器！
    加油学习微积分，发现数学之美！🌈#微积分#小白学习#数学奥秘'
    """


def test_get_chat_response():
    api_key = input("Please enter your OpenAI API key: ")
    memory = ConversationBufferMemory(return_messages=True)
    print(get_chat_response("牛顿提出过哪些知名的定律？", memory, api_key))
    print(get_chat_response("我上一个问题是什么？", memory, api_key))

    """
    牛顿提出了三大著名的运动定律，分别是第一定律：惯性定律，第二定律：运动定律，第三定律：作用反作用定律。这些定律被称为经典力学的基石，对于描述物体的运动和相互作用关系具有重要意义。
    你的上一个问题是"牛顿提出过哪些知名的定律？"。
    """


if __name__ == '__main__':
    print("start test")
    # test_generate_video_scrip()
    # test_generate_red_booklet_article()
    test_get_chat_response()
