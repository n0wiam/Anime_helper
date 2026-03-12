from service.path_service import get_web_url
from sql import insert_anime_information
from anime import Anime
from informate import *
from log import logger
from path_service import get_web_url


# link_list = get_all_anime_link()
# for link in link_list:
#     # 随机睡眠避免反爬
#     time.sleep(random.uniform(0.5, 1))
#     # 获取每个番剧链接里的信息
#     anime = get_anime_information(link)
#     # 将内容写入数据库
#     insert_anime_information(anime)
#     print(link)

def update_anime():
    print("update!")
    # size = get_pages_size()
    # for page in range(1, size + 1):
    #     url = f'https://skr.skr2.cc:666/vodshow/46--------{page}---/'
    #     link_list = get_page_anime_link(url)
    #     for link in link_list:
    #         time.sleep(random.uniform(0.5, 1))
    #         anime = get_anime_information(link)
    #         # print(anime)
    #         try:
    #             insert_anime_information(anime)
    #         except Exception as e:
    #             logger.error("[插入番剧异常]：%s %s", e, anime.link, exc_info=True)


size = get_pages_size()
for page in range(1, size+1):
    url = get_web_url()+ f'/vodshow/46--------{page}---/'
    time.sleep(random.uniform(3, 5))
    link_list = get_page_anime_link(url)
    for link in link_list:
        anime = get_anime_information(link)
        # print(anime)
        try:
            insert_anime_information(anime)
        except Exception as e:
            logger.error("[插入番剧异常]：%s %s", e,anime.link, exc_info=True)
        # print(link)