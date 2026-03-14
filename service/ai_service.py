from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import ast

from service.subscribe_service import get_anime_subscribe
from sql import get_random_anime

ai_prompt = """
------设定-----------
你是一个专业的动漫推荐系统。
你的任务是根据用户的追番记录，判断用户的动漫偏好，并在候选动漫中选出最符合用户喜好的三个。
规则：
1.输入包含两个列表：
  用户追番列表
  候选动漫列表
2.你需要根据用户追番情况，判断用户可能喜欢的动漫类型（例如：热血、战斗、校园、恋爱、治愈、搞笑、异世界等）。
3.在候选动漫列表中，选择最符合用户喜好的三个动漫。
4.返回选中的三个动漫在随机列表中的下标列表
输出要求（非常重要）：
  只允许输出一个数字
  不允许输出解释
  不允许输出任何文字
  不允许输出JSON
  数字间以逗号分隔
  下标从0开始
正确示例：
  [1,2,3]
错误示例：
  推荐第1个
  答案是1
-----用户输入-------------
用户追番列表：{subscribe_list}
候选动漫列表: {random_list}
"""

def get_llm():
    llm = ChatOpenAI(
        api_key="sk-c3vJ8J6kEYs1pMceREaoV2g1v9nJhI5DYMssU0beH0TvfOMB",
        base_url="https://api.openai-proxy.org/v1",
        model="gpt-4.1"
    )
    return llm

def ai_recommend(subscribe_list: list[str], random_list: list[str]):
    model = get_llm()
    output_parser = CommaSeparatedListOutputParser()
    format_instructions = output_parser.get_format_instructions()
    prompt = PromptTemplate(
        template=ai_prompt+"\n{format_instructions}",
        input_variables=["subscribe_list","random_list"],
        partial_variables={"format_instructions": format_instructions}
    )
    _input = prompt.format(subscribe_list=",".join(subscribe_list),random_list=",".join(random_list))
    output = model.invoke([
        HumanMessage(content=_input)
    ])
    return output_parser.parse(output.content)

def get_ai_anime_recommendation(year: int = 1):
    user_id = 1
    subscribe_list = get_anime_subscribe(user_id)
    subscribe_name_list = []
    for sub in subscribe_list:
        subscribe_name_list.append(sub.name)

    if len(subscribe_name_list) == 0:
        return []

    random_anime_list = get_random_anime(year)
    random_anime_name_list = []
    for anime in random_anime_list:
        random_anime_name_list.append(anime.name)

    ai_recommend_list = ai_recommend(subscribe_name_list, random_anime_name_list)
    result = []
    for index in ai_recommend_list:
        result.append(random_anime_list[int(index)])
    print(random_anime_name_list)
    return result

if __name__ == "__main__":
    print(ai_recommend(["鬼灭之刃"],["判处勇者刑","紫罗兰的永恒花园","进击的巨人","咒术回战","魔法少女樱"]))