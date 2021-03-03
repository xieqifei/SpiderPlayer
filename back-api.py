# -*- coding:utf-8 -*-
'''
@file_name    :back-api.py
@description  :后端api程序，接收请求爬取数据并返回
@time         :2021/02/25 01:15:48
@author       :Qifei
@version      :1.0
'''
import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urlparse, parse_qs,quote
import base64
from io import BytesIO
import os
import datetime
import pafy


def main_handler(event, context):
    query = event['queryString']
    resp = Response()
    if('src' in query):
        if(query['src'] == 'bilibili'):
            return do_query(BiliBili(), query)
        elif (query['src'] == 'youtube'):
            return do_query(Youtube(), query)
        else:
            return resp.error("请求出错，无此源")
    else:
        return resp.error("参数错误")


def do_query(platform_obj, query):
    resp = Response()
    if('kw' in query):
        kw=query['kw']
        videos = platform_obj.search_keyword(kw)
        return resp.json(videos)

    elif('id' in query):
        music = platform_obj.get_music(query['id'])
        return resp.json(music)

    elif ('rc' in query):
        videos = platform_obj.get_recommendation()
        return resp.json(videos)

    else:
        return resp.error("暂无此功能")

# B站类
class BiliBili:
    def get_music(self, bv):
        videourl = "https://www.bilibili.com/video/"+bv
        rep = requests.get(videourl)
        if (rep.status_code == 200):
            reg = r"audio.*baseUrl\":\"(.*?)\".*backupUrl"
            reg_url = re.findall(reg, rep.text)
            url = reg_url[0] if len(reg_url) else ""
            reg_cover = re.findall(r'"face":"(.*?)"},"stat":{"aid"', rep.text)
            cover1 = (reg_cover[0] if len(reg_cover) else "").encode(
                "utf-8").decode("unicode_escape")
            cover = self._get_base64(cover1)
            reg_artist = re.findall(r'"name":"(.*?)","face":"', rep.text)
            artist = reg_artist[0] if len(reg_artist) else ""
            soup = BeautifulSoup(rep.text, "html.parser")
            name = soup.select("#viewbox_report > h1 > span")[0].string
            parse = urlparse(url)
            query = parse_qs(parse.query)
            music = Music("bilibili", bv, url, name, artist,
                          cover, "", ''.join(query['deadline']))
            return music.__dict__

    def search_keyword(self, kw):
        url = "https://search.bilibili.com/all?keyword=" + \
            kw+"&order=totalrank&duration=1&tids_1=3"
        rep = requests.get(url)
        videos = []
        if(rep.status_code == 200):
            soup = BeautifulSoup(rep.text, "html.parser")
            video_dom = soup.find_all("li", {"class": "video-item matrix"})
            for i in range(len(video_dom)):
                bvurl = "https:"+video_dom[i].a['href']
                bv = urlparse(bvurl).path.split('/')[-1]
                duration = video_dom[i].a.find(
                    "span", {"class": "so-imgTag_rb"}).string
                name = video_dom[i].a['title']
                music = Music('bilibili', bv, "", name, "", "", duration, "")
                videos.append(music.__dict__.copy())
            return videos
        else:
            return []

    def get_recommendation(self):
        today = datetime.date.today()
        formatted_today = today.strftime('%Y%m%d')
        before30days = (datetime.date.today() +
                        datetime.timedelta(days=-30)).strftime('%Y%m%d')
        url = "https://s.search.bilibili.com/cate/search?main_ver=v3&search_type=video&view_type=hot_rank&order=click&copy_right=-1&cate_id=193&page=1&pagesize=20&jsonp=jsonp&time_from=" + \
            before30days+"&time_to="+formatted_today+"&keyword=%E5%8D%8E%E8%AF%ADMV"
        rep = requests.get(url)
        if(rep.status_code == 200):
            data = rep.json()['result']
            videos = []
            for i in range(len(data)):
                name = data[i]['title']
                duration = self._sec2MinSec(data[i]['duration'])
                id = data[i]['bvid']
                music = Music('bilibili', id, '', name, '', '', duration, '')
                videos.append(music.__dict__.copy())
            return videos
        else:
            return []

    def get_playlist(self, pl):
        return []

    # 秒转分秒
    def _sec2MinSec(self, sec):
        return str(int(sec)//60)+':'+(str(int(sec) % 60 if(int(sec) % 60 >= 10) else '0'+str(int(sec) % 60)))

    def _get_base64(self, img_url):
        resp = requests.get(img_url)
        img_bytes = base64.b64encode(BytesIO(resp.content).read())
        img_str = img_bytes.decode()
        return 'data:image/'+os.path.basename(img_url)+';base64,'+img_str

# Youtube类


class Youtube:
    def get_music(self, id):
        videoUrl = 'https://www.youtube.com/watch?v='+id
        video = pafy.new(videoUrl)
        parse = urlparse(video.audiostreams[-1].url)
        query = parse_qs(parse.query)
        music = Music("youtube", id, video.audiostreams[-1].url, video.title,
                      video.author, self._get_base64(video.thumb), video.duration, ''.join(query['expire']))
        return music.__dict__

    def search_keyword(self, kw):
        #如果是一个播放列表链接，则提取listid
        if(len(re.findall(r'[&?]list=([^&]+)',kw))):
            return self.get_playlist(re.findall(r'[&?]list=([^&]+)',kw)[0])
        url = "https://m.youtube.com/results?search_query="+kw
        resp = requests.get(url)
        if resp.status_code == 200:
            result_json = re.findall(
                r'ytInitialData = (.*);</script>', resp.text)[0]
            result_obj = json.loads(result_json)
            musiclist = []
            
            kwIsList=True
            for i in result_obj['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']:
                if "videoRenderer" in i:
                    kwIsList=False
                    item = i["videoRenderer"]
                    musicBuffer = Music('youtube', item['videoId'], "", item['title']['runs'][0]['text'],
                                        item['ownerText']['runs'][0]['text'], "", item['lengthText']['simpleText'], "")
                    musiclist.append(musicBuffer.__dict__.copy())
                #如果是listid
                elif "playlistRenderer" in i and kwIsList:
                    musiclist += self.get_playlist(
                        i['playlistRenderer']['playlistId'])
            return musiclist
        else:
            return []

    def get_playlist(self, listid):
        baseUrl = "https://www.youtube.com/playlist?app=desktop&list="+listid
        resp = requests.get(baseUrl)
        if(resp.status_code == 200):
            reg = r'ytInitialData =(.*?);</script>'
            dataStr = re.findall(reg, resp.text)[0]
            data = json.loads(dataStr)
            videos = []
            for item in data['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['playlistVideoListRenderer']['contents']:
                try:
                    item = item['playlistVideoRenderer']
                    id = item['videoId']
                    name = item['title']['runs'][0]['text']
                    duration = item['lengthText']['simpleText']
                    music = Music('youtube', id, "", name,
                                  "", "", duration, "")
                    videos.append(music.__dict__.copy())
                except KeyError:
                    pass
            return videos
        else:
            print(resp.status_code)
            return []

    def get_recommendation(self):
        return []

    def _get_base64(self, img_url):
        resp = requests.get(img_url)
        img_bytes = base64.b64encode(BytesIO(resp.content).read())
        img_str = img_bytes.decode()
        return 'data:image/'+os.path.basename(img_url)+';base64,'+img_str


class Music:
    def __init__(self, source, id, url, name, artist, cover, duration, expire):
        self.source = source
        self.url = url
        self.name = name
        self.artist = artist
        self.cover = cover
        self.id = id
        self.duration = duration
        self.expire = expire

#响应类，返回一个http响应格式字典
class Response:
    def error(self, msg):
        return {
            "isBase64Encoded": False,
            "statusCode": 400,
            "headers": {'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'},
            "body": '{"error":1,"msg":"'+msg+'}'
        }

    def html(self, html):
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {'Content-Type': 'text/html',
                        'Access-Control-Allow-Origin': '*'},
            "body": html
        }

    def json(self, jsonObj):
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'},
            "body": json.dumps(jsonObj)
        }

