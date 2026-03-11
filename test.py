import re

from playwright.sync_api import sync_playwright
import subprocess
import requests

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

    page.goto("https://skr.skr2.cc:666/vodplay/216387-7-7/")

    page.wait_for_timeout(2000)

    browser.close()

print(captured_urls[1])
# res = requests.get(captured_urls[1])
# ts_list = re.findall("https.*ts",res.text)
# for url in ts_list:
#     print(url)
#     page = requests.get(url)
#     data = requests.get(url)
#     file_name = 'C:/Afolder/项目/AnimeHelper/video/'+url.split('/')[-1]
#     with open(file_name, 'wb') as f:
#         f.write(data.content)
ffmpeg_path = r"C:/Afolder/software/ffmpeg/ffmpeg-8.0.1-essentials_build/bin/ffmpeg.exe"
m3u8_url = captured_urls[1]
output = "C:/Afolder/项目/AnimeHelper/video/video.mp4"

subprocess.run([ffmpeg_path, "-i", m3u8_url, "-c", "copy", output], check=True)