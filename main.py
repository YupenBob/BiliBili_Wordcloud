from wordcloud import ImageColorGenerator
from wordcloud import WordCloud
from lxml import etree
from PIL import Image
import requests, jieba, re
import numpy as np

# http请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}

danmu_list = []  # 定义弹幕列表
txt = ""  # 定义弹幕文本
# 需要爬取的视频BV
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


# 解析视频弹幕xml地址
def DanmuURL_get(bv):
    print("解析视频弹幕xml地址")
    video_url = bv
    print("BV:" + video_url)
    response = requests.get(video_url, headers=headers)  # 获取信息
    html = response.content.decode()
    cid = re.findall(r'("cid":)([0-9]+)', html)  # 获取cid
    xml_url = "http://comment.bilibili.com/" + str(cid[0][1]) + ".xml"
    return xml_url


# 获取弹幕信息
def Danmu_get(xml_url):
    print("获取弹幕信息")
    print("XML:" + xml_url)
    response = requests.get(xml_url, headers=headers)  # 获取信息
    html = etree.HTML(response.content)
    danmu_list = html.xpath("//d/text()")  # 解析xml
    return danmu_list

# 词云生成
def WordCloud_make(danmuimg, txt):
    mask = np.array(Image.open(danmuimg))  # 导入背景图片
    color = ImageColorGenerator(mask, default_color=None)  # 分析背景文字颜色
    wordcloud = WordCloud(  # 都可以随便修改
        background_color="white",  # 背景颜色
        max_words=114514,  # 最大词量（喜）
        mask=mask,  # 导入图片
        color_func=color,  # 文字颜色
        max_font_size=120,  # 最大文字大小
        font_path="msyhbd.ttc"  # 字体
    ).generate(txt)
    wordcloud.to_file('out.jpg')  # 输出图片
    print("生成完毕，输出图片out.jpg")


# 程序开始
if __name__ == '__main__':
    # 开始调用
    for i in bv:
        xml_url = DanmuURL_get(i)
        danmu_list = Danmu_get(xml_url)
        # 拼接danmu_list
        for a in danmu_list:
            txt = txt + a

    # 生成
    print("获取完成,正在生成词云")
    WordCloud_make("back.jpg", txt)
