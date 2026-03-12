import re
import requests
from log import logger
from lxml import etree
import time
import random
from anime import Anime
from service.path_service import get_web_url


# TODO 爬取全部番剧
# TODO 爬取各个番剧对应的内容，状态
# TODO 爬取番剧视频保存到本地

#获取总页数
def get_pages_size():
    try:
        # url = 'https://skr.skr2.cc:666/vodshow/46-----------/'
        url = get_web_url()+'/vodshow/46-----------/'
        # url = 'https://skr.skr2.cc:666/vodshow/46--------70---/'
        data = requests.get(url).text
        tree = etree.HTML(data)
        pages = tree.xpath('//*[@id="show_page"]/div[2]/div/div[2]/ul[2]/li[@class="hidden_mb"]')[1]
        total = pages.xpath('./a/@href')[0]
        pattern = re.compile(r'/vodshow/46--------(?P<number>\d+)---/', re.S)
        result = int(re.search(pattern, total)[1])
        return result
    except Exception as e:
        logger.error("[获取总页数异常]：%s",e, exc_info=True)
        return 0

# 获取全部番剧的link
def get_all_anime_link():
    size = get_pages_size()
    # url = 'https://skr.skr2.cc:666/vodshow/46--------1---/'
    link_list = []
    try:
        for page in range(1, size + 1):

            # 随机睡眠避免反爬
            # TODO 考虑是否缩小间隔或删除
            time.sleep(random.uniform(0.5, 1))

            # 爬取每个分页所展示的链接，加入到列表中
            # url = f'https://skr.skr2.cc:666/vodshow/46--------{page}---/'
            url = get_web_url()+f'/vodshow/46--------{page}---/'
            # prefix_url = 'https://skr.skr2.cc:666'
            prefix_url = get_web_url()
            data = requests.get(url).text
            tree = etree.HTML(data)
            content = tree.xpath('//*[@id="show_page"]/div[2]/div/div[2]/ul[1]/li')
            for item in content:
                suffix_url = item.xpath('./a/@href')[0]
                link_list.append(prefix_url + suffix_url)
    except Exception as e:
        logger.error("[获取全部番剧的link异常]：%s",e, exc_info=True)
    return link_list

def get_page_anime_link(url):
    link_list = []
    try:
        # 爬取分页所展示的链接，加入到列表中
        # prefix_url = 'https://skr.skr2.cc:666'
        prefix_url = get_web_url()
        data = requests.get(url).text
        tree = etree.HTML(data)
        content = tree.xpath('//*[@id="show_page"]/div[2]/div/div[2]/ul[1]/li')
        for item in content:
            suffix_url = item.xpath('./a/@href')[0]
            link_list.append(prefix_url + suffix_url)
    except Exception as e:
        logger.error("[获取全部番剧的link异常]：%s", e, exc_info=True)
    return link_list

# class Anime(object):
#     def __init__(self, id, name, status, info, total_number, update_time, image_url, link):
#         self.id = id
#         self.name = name
#         self.status = status
#         self.info = info
#         self.total_number = total_number
#         self.update_time = update_time
#         self.image_url = image_url
#         self.link = link

# 获取单个链接中番剧的信息
def get_anime_information(url):
    try:
        data = requests.get(url).text
        tree = etree.HTML(data)

        anime_id = re.search(r'https://(.*?)/voddetail/(?P<id>\d+)',url).group('id')

        # 获取名字，状态，简介
        anime_name = tree.xpath('/html/body/div[2]/div/div/div/div[2]/div[1]/h1/text()')[0]
        anime_status = tree.xpath('/html/body/div[2]/div/div/div/div[3]/ul/li[2]/span/span/text()')[0]
        anime_info = tree.xpath('/html/body/div[3]/div[1]/div[1]/div/div/section[1]/div[1]/span/text()')[0]
        # print(anime_name)
        # print(anime_status)
        # print(anime_info)

        # 获取最新集数
        # pattern = re.compile(r'(.*?)(?P<number>\d+)集', re.S)
        # result = re.search(pattern, anime_status)
        # last_number = int(result.group('number'))

        episodes = tree.xpath('//*[@id="bofy"]/div[2]/div[2]/div[3]/ul/li')
        last_number = len(episodes)
        # print(last_number)

        # 获取更新时间
        year = tree.xpath('/html/body/div[2]/div/div/div/div[3]/ul/li[1]/a[1]/text()')[0]
        date = tree.xpath('/html/body/div[2]/div/div/div/div[3]/ul/li[2]/span/text()')[1]
        try :
            year = int(year)
        except ValueError:
            year = 1999
        update_time = str(year)+'-'+re.search(r'\d{2}-\d{2}', date).group()
        # print(update_time)

        # 获取封面图片
        image_url = tree.xpath('/html/body/div[2]/div/div/div/div[1]/a/@data-original')[0]
        # image_name = image_url.split('/')[-1]
        # download_image(image_url, image_name)
        anime = Anime(anime_id, anime_name, anime_status, anime_info, last_number, update_time, image_url, url)
        return anime
    except Exception as e:
        logger.error("[获取单个链接中番剧的信息异常]：%s [link = %s]",e,url, exc_info=True)
        return None


# def download_image(url,image_name):
#     try:
#         target_path = 'C:/Afolder/项目/AnimeHelper/pic/' + image_name
#         response = requests.get(url)
#         with open(target_path, 'wb') as f:
#             f.write(response.content)
#     except Exception as e:
#         logger.error("[下载番剧图片异常]：%s",e, exc_info=True)

# log_name = log_filename = datetime.now().strftime("%Y_%m_%d") + ".log"
# logging.basicConfig(
#     level=logging.ERROR,
#     format="%(asctime)s [%(levelname)s] %(message)s",
#     filename="C:/Afolder/项目/AnimeHelper/log/"+log_name,  # 写入文件，如果不想写文件就删掉这个参数
# )

def get_weekly_list():
    data = requests.get(get_web_url()+"/vodtype/22/").text
    tree = etree.HTML(data)
    days = tree.xpath('//*[@id="day1"]/div[2]/div/div/div[@class="vodlist_smt clearfix"]')
    result = []
    pattern = re.compile(r'/voddetail/(?P<id>\d+)/')
    for i in range(0,7):
        day = days[i]
        anime_list = day.xpath('./ul/li/a/@href')
        value = re.search(pattern, anime_list[0]).group('id')
        for j in range(1,len(anime_list)):
            anime = re.search(pattern, anime_list[j]).group('id')
            value+= ','+anime
        result.append(value)
    return result

# anime = get_anime_information("https://skr.skr2.cc:666/voddetail/214895/")
# print(anime.update_time)
# try:
#     get_anime_information("https://skr.skr2.cc:666/voddetail/214895/")
# except Exception as e:
#     logging.error("发生异常：%s", e, exc_info=True)