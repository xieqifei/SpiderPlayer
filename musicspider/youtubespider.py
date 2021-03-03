import requests
import json
import re
import pafy


class Youtube():
    def __init__(self):
        self.listUrl = "https://www.youtube.com/playlist?list="
        self.watchUrl = "https://www.youtube.com/embed/"

        
    def getList(self,listid):
        url = self.listUrl+listid
        resp = requests.get(url)
        reg = r'ytInitialData = \'(.*?)\';</script>'
        data = re.findall(reg,resp.text)[0]
        #十六进制转ascii

        return 0
    
    def getMusic(self,musicid):
        url = self.watchUrl+musicid
        resp = requests.get(url)
        abc = resp.content.decode("utf-8")
        reg = r'INNERTUBE_API_KEY":"(.*?)\"'
        api_key = re.findall(reg,abc)[0]
        print(api_key)
        music_info_url = "https://www.youtube.com/youtubei/v1/player?key="+api_key
        headers={"user-agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Mobile Safari/537.36"}
        resp2 = requests.post(music_info_url,headers=headers)
        print(resp2.text)
        data = resp2.json()
        music = Music('youtube',data['videoDetails']['videoId'],data['streamingData']['adaptiveFormats'][-1]['url'],data['videoDetails']['title'],data['videoDetails']['author'],data['videoDetails']['thumbnail']['thumbnails'][0]['url'],data['videoDetails']['lengthSeconds'])
        return music


class Music:
    def __init__(self, source, id, url, name, artist, cover,duration):
        self.source = source
        self.url = url
        self.name = name
        self.artist = artist
        self.cover = cover
        self.id = id
        self.duration = duration

    def getName(self):
        return self.name

    def getUrl(self):
        return self.url

    def getArtist(self):
        return self.artist

    def getCover(self):
        return self.cover

    def getSource(self):
        return self.source

    def getId(self):
        return self.id


url = "https://www.youtube.com/watch?v=VVuRaPvHlj4"
video = pafy.new(url)
for s in video:
    print(s.resolution, s.extension, s.get_filesize(), s.url)
# youtubemusic = Youtube().getMusic("VVuRaPvHlj4")
# print(youtubemusic.url)
