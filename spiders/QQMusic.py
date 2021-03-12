import requests
from .base import Music,Playlist,Userlist

class QQMusic:

    cookie = ''
    
    #官方的请求地址，香港以及海外服务器无法请求
    # def get_music(self,id):
    #     baseUrl = r'https://u.y.qq.com/cgi-bin/musicu.fcg?format=json'
    #     data = r'{"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"126548448","songmid":["'+id+r'"],"songtype":[0],"uin":"1443481947","loginflag":1,"platform":"20"}},"comm":{"uin":"18585073516","format":"json","ct":24,"cv":0}}'
    #     resp = requests.post(baseUrl,data=data)
    #     m={}
    #     if(resp.status_code==200):
    #         try:
    #             music_data = (resp.json())['req_0']['data']
    #             if(len(music_data['midurlinfo'][0]['purl'])!=0):
    #                 url = music_data['sip'][0]+music_data['midurlinfo'][0]['purl']
    #             else:
    #                 url = ''
    #             m = Music('qqmusic',id,url,'','','','','').__dict__
    #         except:
    #             pass
    #     return m
    
    #非官方api，在网上找的一个api
    def get_music(self,id):
        baseUrl = 'https://api.zsfmyz.top/music/song?songmid='+id+'&guid=126548448'
        resp = requests.get(baseUrl)
        m={}
        if (resp.status_code==200):
            try:
                m = Music('qqmusic',id,resp.json()['data']['musicUrl'],'','','','','').__dict__
            except Exception:
                pass
        return m
        
    def search_keyword(self,kw):
        baseUrl = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?p=1&n=30&w="+kw+"&format=json"
        resp = requests.get(baseUrl)
        musiclist = []
        if(resp.status_code==200):
            try:
                musics = resp.json()['data']['song']['list']
                for music in musics:
                    if(music['isonly']==0):
                        cover = self.get_pic(music['albummid'])
                        m = Music('qqmusic',music['songmid'],'',music['songname'],music['singer'][0]['name'],cover,self._sec2MinSec(music['interval']),'',albummid=music['albummid'],albumname = music['albumname'],)
                        musiclist.append(m.__dict__.copy())
            except:
                pass
            return musiclist
        else:
            return []

    # 秒转分秒
    def _sec2MinSec(self, sec):
        return str(int(sec)//60)+':'+(str(int(sec) % 60 if(int(sec) % 60 >= 10) else '0'+str(int(sec) % 60)))

    def get_playlist(self,id):
        baseUrl = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_playlist_cp.fcg?newsong=1&id='+id+'&format=json'
        resp = requests.get(baseUrl)
        if(resp.status_code ==200):
            try:
                data = resp.json()['data']['cdlist'][0]
                pl_name = data['dissname']
                pl_cover = data['logo'].replace('http:','https:')
                creatername = data['nickname']
                creatercover = ''
                musics = []
                for music in data['songlist']:
                    if(music['isonly']==0):
                        mid = music['mid']
                        name = music['name']
                        artist = music['singer'][0]['name']
                        cover = self.get_pic(music['album']['mid'])
                        m = Music('qqmusic',mid,'',name,artist,cover,'','').__dict__
                        musics.append(m.copy())
                playlist = Playlist('qqmusic',id,pl_name,pl_cover,creatername,creatercover,musics).__dict__
            except Exception:
                pass
        return playlist
    #获取歌词
    def get_lyric(self,id):
        headers = {'Referer':'https://y.qq.com/portal/player.html'}
        baseUrl = "https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg?songmid="+id+"&format=json&nobase64=1"
        resp = requests.get(baseUrl,headers=headers)
        if(resp.status_code==200):
            lyric = ''
            try:
                lyric = resp.json()['lyric']
            except:
                pass
        return {'source':'qqmusic','id':id,'lyric':lyric}

    #获取专辑图片
    def get_pic(self,albummid):
        cover = 'https://y.gtimg.cn/music/photo_new/T002R180x180M000'+albummid+'.jpg'
        return cover
    
    #设置cookie
    def set_cookie(self,cookie):
       self.cookie = cookie

    #通过qq号搜索用户歌单
    #此功能要实现，必须提供qq音乐cookie
    def get_userlist(self,qq):
        baseUrl = 'https://c.y.qq.com/rsc/fcgi-bin/fcg_get_profile_homepage.fcg?format=json&cid=205360838&userid='+qq+'&reqfrom=1'
        header = {'cookie':self.cookie}
        resp = requests.get(baseUrl,headers=header)
        userlist = {}
        if(resp.status_code==200):
            try:
                data = resp.json()['data']
                creatername = data['creator']['nick']
                creatercover = data['creator']['headpic']
                playlist = []
                for pl in data['mydiss']['list']:
                    pid = pl['dissid']
                    pname = pl['title']
                    playlist.append(Playlist('qqmusic',pid,pname,'','','',[]).__dict__.copy())
                userlist = Userlist('qqmusic',200,qq,creatername,creatercover,playlist).__dict__
            except Exception:
                pass
        return userlist