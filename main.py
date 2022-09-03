from wordcloud import ImageColorGenerator
from wordcloud import WordCloud
from lxml import etree
from PIL import Image
import requests,jieba,re
import numpy as np

#http请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}

#解析视频弹幕xml地址
def DanmuURL_get(bv):
    print("解析视频弹幕xml地址")
    video_url = bv
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
    "https://www.bilibili.com/video/BV1HL4y1577D",
    "https://www.bilibili.com/video/BV1dr4y1H77b",
    "https://www.bilibili.com/video/BV1h34y1k7m1",
    "https://www.bilibili.com/video/BV14P4y1A7UG",
    "https://www.bilibili.com/video/BV1ES4y1y7K1",
    "https://www.bilibili.com/video/BV1tL4y1c7hj",
    "https://www.bilibili.com/video/BV1LB4y1X7Nj",
    "https://www.bilibili.com/video/BV1ya411W7Lv",
    "https://www.bilibili.com/video/BV1aa411Z7U2",
    "https://www.bilibili.com/video/BV1Qd4y1d7px",
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
                        max_words = 9000,
                        mask = mask,
                        color_func = color,
                        max_font_size=120,
                        font_path =  "msyhbd.ttc"
                      ).generate(txt)
wordcloud.to_file('out.jpg')