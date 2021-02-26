# -*- encoding: utf-8 -*-
'''
@file_name    :back-api.py
@description  :
@time         :2021/02/24 18:38:35
@author       :Qifei
@version      :1.0
'''

import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urlparse
import base64
from io import BytesIO
import os

def main_handler(event,context):
    if('kw' in event['queryString']):
        videos = SerchResult(event['queryString']['kw']).videos
        videosjson = json.dumps(videos)
        return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {'Content-Type': 'application/json','Access-Control-Allow-Origin':'*'},
        "body": videosjson
        }
    elif('bv' in event['queryString']):
        music = Music(event['queryString']['bv'])
        return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {'Content-Type': 'application/json','Access-Control-Allow-Origin':'*'},
        "body": '{"url":"'+music.url+'","name":"'+music.name+'","cover":"'+music.cover+'","artist":"'+music.artist+'"}'
        }
    else:
        return {
        "isBase64Encoded": False,
        "statusCode": 404,
        "headers": {'Content-Type': 'application/json','Access-Control-Allow-Origin':'*'},
        "body": "{'msg':'query incorrect'}"
        }

class Music:
    def __init__(self, bv:str):
        self.videourl = "https://www.bilibili.com/video/"+bv
        self.url = ""
        self.name = ""
        self.artist = ""
        self.cover = ""
        self._getMusic()
    
    def _getMusic(self):
        rep = requests.get(self.videourl)
        if (rep.status_code ==200):
            reg = r"audio.*baseUrl\":\"(.*?)\".*backupUrl"
            reg_url  =re.findall(reg,rep.text)
            self.url = reg_url[0] if len(reg_url)  else ""
            reg_cover = re.findall(r'"face":"(.*?)"},"stat":{"aid"',rep.text)
            cover=(reg_cover[0] if len(reg_cover) else "").encode("utf-8").decode("unicode_escape")
            self.cover = self._getImgtoBase64(cover)
            reg_artist = re.findall(r'"name":"(.*?)","face":"',rep.text)
            self.artist = reg_artist[0] if len(reg_artist) else ""
            soup = BeautifulSoup(rep.text,"html.parser")
            self.name = soup.select("#viewbox_report > h1 > span")[0].string
    
    def _getImgtoBase64(self,img_url):
        resp = requests.get(img_url)
        img_bytes=base64.b64encode(BytesIO(resp.content).read())
        img_str = img_bytes.decode()
        return 'data:image/'+os.path.basename(img_url)+';base64,'+img_str

class SerchResult:
    def __init__(self, keyword:str) -> None:
        self.keyword = keyword
        self.videos = self._getVideos()

    def _getVideos(self):
        url = "https://search.bilibili.com/all?keyword=" + \
            self.keyword+"&order=totalrank&duration=1&tids_1=3"
        rep = requests.get(url)
        videos = []
        video = {}
        if(rep.status_code == 200):
            soup = BeautifulSoup(rep.text, "html.parser")
            video_dom = soup.find_all("li", {"class": "video-item matrix"})
            for i in range(len(video_dom)):
                video['bvurl'] = "https:"+video_dom[i].a['href']
                video['bv']= urlparse(video['bvurl']).path.split('/')[-1]
                video['name'] = video_dom[i].a['title']
                video['duration'] = video_dom[i].a.find(
                    "span", {"class": "so-imgTag_rb"}).string
                # video['img'] = "https:"+video_dom[i].a.img["src"]
                videos.append(video.copy())
            return videos
        else:
            return []

