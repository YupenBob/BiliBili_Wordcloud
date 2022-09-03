import requests
import re
from lxml import etree
import jieba
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
import numpy as np
from PIL import Image

#http请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}

#解析视频弹幕xml地址
def DanmuURL_get(bv):
    print("解析视频弹幕xml地址")
    video_url = "https://bilibili.com/video/BV" + bv
    print("BV:"+video_url)
    response = requests.get(video_url, headers=headers)
    html = response.content.decode()
    cid = re.findall(r'("cid":)([0-9]+)', html)
    xml_url = "http://comment.bilibili.com/" + str(cid[0][1]) + ".xml"
    return xml_url

#获取弹幕信息
def Danmu_get(xml_url):
    print("获取弹幕信息")
    print("XML:"+xml_url)
    response = requests.get(xml_url, headers=headers)
    html = etree.HTML(response.content)
    danmu_list = html.xpath("//d/text()")
    return danmu_list


danmu_list = []
bv = [
    "1Qd4y1d7px",
    "1gG411b7Pk",
    "1FN4y1c7xp",
    "1Jd4y1A7vs",
    "1d14y1W7Xd",
    "1Ve4y1X7TY",
    "1EN4y1V7MB",
    "1dB4y1k7nB",
    "1kT411F7v1",
    "1ae4y1f7aB",
    "1eW4y1t7TG",
    "1va411G7Fy",
    "1LG4y1k7Es",
    "1gG411b7Pk",

]
txt = ""

#循环
for i in bv:
    xml_url = DanmuURL_get(i)
    danmu_list = Danmu_get(xml_url)
    #拼接danmu_list
    for a in danmu_list:
        txt = txt + a

#分词
words = jieba.lcut(txt)

#空格拼接
wordtxt = ''.join(words)

#词云生成
mask = np.array(Image.open("back.png"))
color = ImageColorGenerator(mask, default_color=None)
wordcloud = WordCloud(
                        background_color="white",
                        max_words = 900000,
                        mask = mask,
                        color_func = color,
                        max_font_size=120,
                        font_path =  "msyhbd.ttc"
                      ).generate(txt)
wordcloud.to_file('out.jpg')