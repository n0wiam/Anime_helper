import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://skr.skr2.cc:666/vodtype/22/"
data = urlopen(url).read().decode('utf-8')

# 格式化并写入html
soup = BeautifulSoup(data, "html.parser")
pretty_html = soup.prettify()   # 自动缩进 + 换行
with open('content.html', mode="w", encoding="utf-8") as f:
    f.write(pretty_html)

# 原格式
# obj = re.compile(r"<a class=\"ranklist_thumb lazyload\" href=\"/voddetail/(?P<id>.*?)/\" alt=\"(?P<name>.*?)\" data-original=\"(?P<picture>.*?)\">")
obj = re.compile(r"<a alt=\"(?P<name>.*?)\" class=\"ranklist_thumb lazyload\" data-original=\"(?P<picture>.*?)\" href=\"/voddetail/(?P<id>.*?)/\"")

# result = obj.finditer(data)
# result = obj.finditer(pretty_html)
# for item in result:
#     print(item.group("id"))
#     print(item.group("name"))
#     print(item.group("picture"))

# 按时间进行区分
result = {}
parts = re.split(r'(?=<h2 class="title")', pretty_html)
for block in parts:
    m = re.search(r'<h2 class="title">\s*(周[一二三四五六日])\s*</h2>', block)
    if m:
        title = m.group(1)
        result[title]=[]
        content = obj.finditer(block)
        # 解析对应时间段的更新内容
        for item in content:
            result[title].append(item.group("name"))
print(result)



