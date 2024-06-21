import sys

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI

sys.path.append("..")
from model_langchain.DMAnalyse import DMAnalyse
from prompt_template.dameng_template import system_template_text, user_template_text


def generate_dm(
        task_content, task_reference, student_answer, student_submit_time, student_online_time, student_course_list,
        openai_proxy_key
):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template_text),
        ("user", user_template_text)
    ])

    model = ChatOpenAI(model="gpt-3.5-turbo", api_key=openai_proxy_key, openai_api_base="https://api.aigc369.com/v1")
    output_parser = PydanticOutputParser(pydantic_object=DMAnalyse)

    chain = prompt | model | output_parser
    result = chain.invoke({
        "parser_instructions": output_parser.get_format_instructions(),
        "task_content": task_content,
        "task_reference": task_reference,
        "student_answer": student_answer,
        "student_submit_time": student_submit_time,
        "student_online_time": student_online_time,
        "student_course_list": student_course_list,
    })
    return result


def test_generate_dm():
    # 本次实训
    task_content = "完成达梦数据库的安装"
    task_reference = """
    cd /opt/software
    docker load -i dm8_20230808_rev197096_x86_rh6_64_single.tar
    docker images
    docker run -d \
      -p 30236:5236 \
      --restart=always \
      --name dm8_24 \
      --privileged=true \
      -e PAGE_SIZE=16 \
      -e LD_LIBRARY_PATH=/opt/dmdbms/bin \
      -e EXTENT_SIZE=32 \
      -e BLANK_PAD_MODE=1 \
      -e LOG_SIZE=1024 \
      -e UNICODE_FLAG=1 \
      -e LENGTH_IN_CHAR=1 \
      -e INSTANCE_NAME=dm8_test \
      -v /data/dm8_24:/opt/dmdbms/data \
      dm8_single:dm8_20230808_rev197096_x86_rh6_64
    docker logs -f dm8_24 
    docker inspect dm8_24 
    docker stop dm8_24
    docker start dm8_24
    docker restart dm8_24 
    docker exec -it dm8_24 bash
    source /etc/profile
    cd /opt/dmdbms
    ls  # bin  bin2  data  log
    cd /opt/dmdbms/bin
    ./disql SYSDBA/SYSDBA001
    create user DM identified by "dameng123"; 
    grant resource to dm; 
    conn dm/dameng123;  
    select user from dual; 
    """
    student_answer = """
    cd /opt/software
    docker load -i dm8_20230808_rev197096_x86_rh6_64_single.tar
    docker images
    docker run -d \
      -p 30236:5236 \
      --restart=always \
      --name dm8_24 \
      --privileged=true \
      -e PAGE_SIZE=16 \
      -e LD_LIBRARY_PATH=/opt/dmdbms/bin \
      -e EXTENT_SIZE=32 \
      -e BLANK_PAD_MODE=1 \
      -e LOG_SIZE=1024 \
      -e UNICODE_FLAG=1 \
      -e LENGTH_IN_CHAR=1 \
      -e INSTANCE_NAME=dm8_test \
      -v /data/dm8_24:/opt/dmdbms/data \
      dm8_single:dm8_20230808_rev197096_x86_rh6_64
    docker logs -f dm8_24 
    docker inspect dm8_24 
    docker stop dm8_24
    docker start dm8_24
    docker restart dm8_24 
    docker exec -it dm8_24 bash
    source /etc/profile
    cd /opt/dmdbms
    ls  # bin  bin2  data  log
    cd /opt/dmdbms/bin
    ./disql SYSDBA/SYSDBA001
    create user DM identified by "dameng123"; 
    grant resource to dm; 
    conn dm/dameng123;  
    select user from dual; 
    """
    student_submit_time = "3"  # 分钟
    # 画像信息
    student_online_time = "2"
    student_course_list = ['java基础语法', 'java面向对象', 'DM数据库基础使用',
                           'SpringBoot企业级开发教程', 'docker入门与实践']

    api_key = input("Please enter your OpenAI API key: ")
    print(generate_dm(
        task_content, task_reference, student_answer, student_submit_time,
        student_online_time, student_course_list,
        api_key,
    ))


if __name__ == '__main__':
    print("start")
    test_generate_dm()
