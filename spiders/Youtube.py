import requests
import re
import json
from urllib.parse import urlparse, parse_qs
import base64
from io import BytesIO
import os
import pafy
from .base import Music,Playlist

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

