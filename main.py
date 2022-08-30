import requests
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44"
}

def DanmuURL_get(bv):
    video_url = "https://bilibili.com/video/BV" + bv
    response = requests.get(video_url, headers=headers)
    html = response.content.decode()
    cid = re.findall(r'(?<=("cid":))[0-9]+(?=(,))', html)
    xml_url = "http://comment.bilibili.com/" + str(cid[0]) + ".xml"
    return xml_url

def Danmu_get(url):
    response = requests.get(url, headers=headers)
    html = response.content.decode()
    danmu = re.findall('(?<=(<d p=".*?">)).*(?=(</d>))', html)
    return danmu


url = DanmuURL_get("1Qd4y1d7px")
list = Danmu_get(url)
print(list)
