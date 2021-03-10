# -*- coding:utf-8 -*-
'''
@file_name    :index.py
@description  :云函数入口程序，带参数时作为api服务器，不带参数或参数错误时，返回html网页
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
    # query = event('queryStringParameters')
    #静态资源
    js = ['/js/ajax.js','/js/lyric.js','/js/musicList.js','/js/functions.js','/js/player.js','/js/jquery.mCustomScrollbar.concat.min.js','/js/background-blur.min.js']
    css = ['/css/jquery.mCustomScrollbar.min.css','/css/player.css','/css/small.css']
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
        with open('./index.html') as f:
            html = f.read()
        for j in js:
            html = html.replace("${"+j+"}",read_statics(j))
        for cs in css:
            html = html.replace("${"+cs+"}",read_statics(cs))
        return resp.html(html)

def read_statics(key):
    with open('./cdn'+key) as f:
        staticsstr = f.read()
    return staticsstr

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
    
    elif('gd' in query):
        playlist =  platform_obj.get_playlist(query['gd'])
        return resp.json(playlist)

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
                          cover, "", ''.join(query['deadline']),'')
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
                music = Music('bilibili', bv, "", name, "", "", duration, "",'')
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
                music = Music('bilibili', id, '', name, '', '', duration, '','')
                videos.append(music.__dict__.copy())
            return videos
        else:
            return []

    def get_playlist(self, pl):
        return {}

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
                      video.author, self._get_base64(video.thumb), video.duration, ''.join(query['expire']),'')
        return music.__dict__

    def search_keyword(self, kw):
        #如果是一个播放列表链接，则提取listid
        if(len(re.findall(r'[&?]list=([^&]+)',kw))):
            return self.get_playlist(re.findall(r'[&?]list=([^&]+)',kw)[0])['items']
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
                                        item['ownerText']['runs'][0]['text'], "", item['lengthText']['simpleText'], "",'')
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
            playlist = {}
            try:
                for item in data['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['playlistVideoListRenderer']['contents']: 
                    item = item['playlistVideoRenderer']
                    id = item['videoId']
                    name = item['title']['runs'][0]['text']
                    duration = item['lengthText']['simpleText']
                    music = Music('youtube', id, "", name,
                                "", "", duration, "",'')
                    videos.append(music.__dict__.copy())
                name = data['microformat']['microformatDataRenderer']['title']
                cover_url = data['microformat']['microformatDataRenderer']['thumbnail']['thumbnails'][-1]['url']
                cover = self._get_base64(cover_url)
                creatername = data['sidebar']['playlistSidebarRenderer']['items'][-1]['playlistSidebarSecondaryInfoRenderer']['videoOwner']['videoOwnerRenderer']['title']['runs'][0]['text']
                creatercover_url = data['sidebar']['playlistSidebarRenderer']['items'][-1]['playlistSidebarSecondaryInfoRenderer']['videoOwner']['videoOwnerRenderer']['thumbnail']['thumbnails'][-1]['url']
                creatercover = self._get_base64(creatercover_url)
                playlist=Playlist('youtube',listid,name,cover,creatername,creatercover,videos).__dict__
            except KeyError:
                    pass    
            
            return playlist
        else:
            print(resp.status_code)
            return {}

    def get_recommendation(self):
        return []

    def _get_base64(self, img_url):
        resp = requests.get(img_url)
        img_bytes = base64.b64encode(BytesIO(resp.content).read())
        img_str = img_bytes.decode()
        return 'data:image/'+os.path.basename(img_url)+';base64,'+img_str

class QQMusic:

    def get_music(self,id):
        baseUrl = r'https://u.y.qq.com/cgi-bin/musicu.fcg?format=json&data={"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"126548448","songmid":["'+id+r'"],"songtype":[0],"uin":"1443481947","loginflag":1,"platform":"20"}},"comm":{"uin":"18585073516","format":"json","ct":24,"cv":0}}'
        resp = requests.get(baseUrl)
        if(resp.status_code==200):
            try:
                data = resp.json()['req_0']['data']
                if(len(data['midurlinfo'][0]['purl'])!=0):
                    url = data['sip'][0]+data['midurlinfo'][0]['purl']
                else:
                    url = ''
                m = Music('qqmusic',id,url,)
            except:
                pass
        return 0
    
    def search_keyword(self,kw):
        baseUrl = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?p=1&n=20&w="+kw+"&format=json"
        resp = requests.get(baseUrl)
        musiclist = []
        if(resp.status_code==200):
            try:
                musics = resp.json()['data']['song']['list']
                for music in musics:
                    if(music['isonly']==0):
                        m = Music('qqmusic',music['songmid'],'',music['songname'],music['singer'][0]['name'],'',self._sec2MinSec(music['interval']),'','')
                        musiclist.append(m.__dict__.copy())
                
            except:
                pass
            return musiclist
        else:
            return []

    # 秒转分秒
    def _sec2MinSec(self, sec):
        return str(int(sec)//60)+':'+(str(int(sec) % 60 if(int(sec) % 60 >= 10) else '0'+str(int(sec) % 60)))

    #获取歌词
    def get_lyric(self,id):
        headers = {'Referer':'https://y.qq.com/portal/player.html'}
        baseUrl = "https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg?songmid="+id+"&format=json&nobase64=1"
        resp = requests.get(baseUrl,headers=headers)
        if(resp.status_code==200):
            lyric = ''
            try:
                lyric = resp.json()['lyric']
            except :
                pass
        return lyric
    
    #获取歌曲信息
    def get_info(self,id):
        return 


class Music:
    def __init__(self, source, id, url, name, artist, cover, duration, expire,lrc):
        self.source = source
        self.url = url
        self.name = name
        self.artist = artist
        self.cover = cover
        self.id = id
        self.duration = duration
        self.expire = expire
        self.lrc = lrc

#歌单
class Playlist:
    def __init__(self,source,id,name,cover,creatername,creatercover,items):
        self.source = source
        self.name = name
        self.id = id
        self.cover = cover
        self.creatername = creatername
        self.creatercover = creatercover
        self.items = items


#响应类，返回一个http响应格式字典
class Response:
    def error(self, msg):
        return {
            "isBase64Encoded": False,
            "statusCode": 400,
            "headers": {'Content-Type': 'application/json'},
            "body": '{"error":1,"msg":"'+msg+'}'
        }

    def html(self, html):
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {'Content-Type': 'text/html'},
            "body": html
        }

    def json(self, jsonObj):
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {'Content-Type': 'application/json'},
            "body": json.dumps(jsonObj)
        }


