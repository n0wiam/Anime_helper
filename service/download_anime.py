import requests
from lxml import etree
from playwright.sync_api import sync_playwright
import subprocess
import json
import sys
from service.path_service import get_video_path, get_ffmpeg_path


def get_anime_episode_link(anime_web, anime_episode):
    web_data = requests.get(anime_web).text
    web_tree = etree.HTML(web_data)
    all_episode = web_tree.xpath(r'//*[@id="bofy"]/div[2]/div[@class="play_list_box hide show"]/div[@class="playlist_full"]/ul/li/a/@href')
    episode_number = len(all_episode)
    if episode_number < anime_episode:
        return None
    if anime_episode < 1:
        return None
    link = all_episode[anime_episode-1]
    return link

def download_video(anime_link,file_name):
    target_keywords = ["m3u8"]
    captured_urls = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        def on_request(request):
            url = request.url
            if any(k in url for k in target_keywords):
                captured_urls.append(url)

        page.on("request", on_request)

        page.goto(anime_link)

        page.wait_for_timeout(2000)

        browser.close()

    # print(captured_urls[1])
    # ffmpeg_path = r"C:/Afolder/software/ffmpeg/ffmpeg-8.0.1-essentials_build/bin/ffmpeg.exe"
    ffmpeg_path = get_ffmpeg_path()
    m3u8_url = captured_urls[1]
    output = get_video_path()+"/"+file_name+".mp4"
    subprocess.run(
        [ffmpeg_path, "-n", "-i", m3u8_url, "-c", "copy", output],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def download(anime_web,anime_episode,file_name):
    try:
        url = get_anime_episode_link(anime_web, int(anime_episode))
        if url is None:
            return {"success": False,"error": "unfound anime link!"}
        anime_link = "https://skr.skr2.cc:666"+url
        # print(anime_link)
        download_video(anime_link,file_name)
        return {"success": True}
    except Exception as e:
        return {"success": False,"error": str(e)}



# output=download("https://skr.skr2.cc:666/voddetail/216387/",1,"test")
# print(json.dumps(output, ensure_ascii=False))

if __name__ == "__main__":
    # 从命令行获取参数
    # x = sys.argv[1]
    # y = sys.argv[2]
    # z = sys.argv[3]
    x="https://skr.skr2.cc:666/voddetail/12425/"
    y=1
    z="test1"

    output = download(x,y,z)
    print(json.dumps(output, ensure_ascii=False))
