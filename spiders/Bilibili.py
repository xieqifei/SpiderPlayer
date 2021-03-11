# -*- encoding: utf-8 -*-
'''
@file_name    :Bilibili.py
@description  :B站爬虫程序，通过b站bvid获取播放列表、视频的音频链接、视频信息等资源
@time         :2021/03/11 01:56:19
@author       :Qifei
@version      :1.0
'''


import json
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, parse_qs
import base64
from io import BytesIO
import os
import datetime
from .base import Music,Playlist


# B站类
class BiliBili:
    '''
        B站视频id对应的不仅仅是一个视频，有的可能有多个视频，也就是视频列表
        如果这个列表里只有一个视频，那么bvid就对应一个视频，如果有多个，
        在请求url中，用了一个参数p用以区分。
        为了请求方便，这里的bv可以是原来的12位bv，也可能是bv+p构成的十三位或者更多位的新bv
        通过程序，将bv与p分开
        return Music类的字典
    '''
    def get_music(self, bv):
        if(len(bv)==12):
            videourl = "https://www.bilibili.com/video/"+bv
        else:
            videourl = "https://www.bilibili.com/video/"+bv[0:12]+"?p="+bv[12:]
        rep = requests.get(videourl)
        if (rep.status_code == 200):
            jsonstr = re.findall(r'<script>window.__playinfo__=(.*?)</script><script>', rep.text)[0]
            data1 = json.loads(jsonstr)
            url = data1['data']['dash']['audio'][0]['baseUrl']
            duration = data1['data']['dash']['duration']
            jsonstr2 = re.findall(r'<script>window.__INITIAL_STATE__=(.*?);\(function\(\){',rep.text)[0]
            data2 = json.loads(jsonstr2)['videoData']
            cover_url = data2['pic']
            cover = self._get_base64(cover_url)
            artist = data2['owner']['name']
            name = data2['title']
            parse = urlparse(url)
            query = parse_qs(parse.query)
            music = Music("bilibili", bv, url, name, artist,
                          cover, duration, ''.join(query['deadline']),'')
            return music.__dict__

    
    def search_keyword(self, kw):
        '''
        kw：搜索关键词
        return：一个列表，列表的每个元素是一个Music对象的字典形式
        '''
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
                music = Music('bilibili', bv, "", name, "", "", duration, "",'')
                videos.append(music.__dict__.copy())
            return videos
        else:
            return []

    def get_recommendation(self):
        '''
        获取一个推荐列表
        return Music对象的字典格式列表
        '''
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
                music = Music('bilibili', id, '', name, '', '', duration, '','')
                videos.append(music.__dict__.copy())
            return videos
        else:
            return []

    #B站播放列表和视频在同页面下
    def get_playlist(self, bvid):
        '''
        bvid：B站视频id
        return 一个Playlist对象的字典形式
        '''
        videourl = "https://www.bilibili.com/video/"+bvid
        rep = requests.get(videourl)
        playlist = {}
        if (rep.status_code == 200):
            # try:
                jsonstr = re.findall(r'<script>window.__INITIAL_STATE__=(.*?);\(function\(\){',rep.text)[0]
                data = json.loads(jsonstr)['videoData']
                id = data['bvid']
                cover_url = data['pic']
                cover = self._get_base64(cover_url)
                creatername = data['owner']['name']
                face = data['owner']['face']
                creatrecover = self._get_base64(face)
                name = data['title']
                items = []
                for item in data['pages']:
                    music = Music('bilibili',id+str(item['page']),'',item['part'],creatername,'',str(item['duration']),'','')
                    items.append(music.__dict__)
                playlist = Playlist('bilibili',id,name,cover,creatername,creatrecover,items).__dict__
                
            # except Exception:
            #     pass
        return playlist

    # 秒转分秒
    def _sec2MinSec(self, sec):
        return str(int(sec)//60)+':'+(str(int(sec) % 60 if(int(sec) % 60 >= 10) else '0'+str(int(sec) % 60)))

    def _get_base64(self, img_url):
        '''
        img_url：图片链接
        return base64编码后的图片
        '''
        resp = requests.get(img_url)
        img_bytes = base64.b64encode(BytesIO(resp.content).read())
        img_str = img_bytes.decode()
        return 'data:image/'+os.path.basename(img_url)+';base64,'+img_str