import requests
import re
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44"
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


xml_url = DanmuURL_get("1Qd4y1d7px")
list = Danmu_get(xml_url)
print(list)
