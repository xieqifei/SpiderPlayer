import requests
from .base import Music,Playlist,Userlist
import json

class QQMusic:
    cookie = 'pgv_pvi=8608630784; RK=UKpl0yStED; ptcz=fbb88170fafd2ed95d5d3b653c7f180d5d916823e72e04a44454e12fc0772bb7; tvfe_boss_uuid=41ec9918a7abd703; eas_sid=T1q5E9j7O1B5K7i5O1b9U8f162; ied_qq=o0975322731; pac_uid=1_975322731; iip=0; _ga=GA1.2.984015091.1601553199; ts_uid=7486175980; pgv_pvid=5602168404; fqm_pvqid=955e6bfd-c610-4384-b3c0-0afef3ae4b61; pgv_info=ssid=s257455772; userAction=1; _qpsvr_localtk=0.8074091033690896; euin=NKSkoi-A7io5; tmeLoginType=2; ts_refer=www.google.com/; yqq_stat=0; ts_last=y.qq.com/portal/profile.html; psrf_qqaccess_token=BD8A28A11DF77AD5905C5428ADF9F8C3; psrf_qqunionid=; qm_keyst=Q_H_L_2m0WA160eaxm3LzECdv3z_BX0Zt3qVJRER9gaSMYSvK6Tyfxge0_8pRSj-xYah8; psrf_qqrefresh_token=E8EAB1E0F4135D94809D75593B5F0333; qqmusic_key=Q_H_L_2m0WA160eaxm3LzECdv3z_BX0Zt3qVJRER9gaSMYSvK6Tyfxge0_8pRSj-xYah8; uin=975322731; psrf_access_token_expiresAt=1623271180; psrf_musickey_createtime=1615495180; psrf_qqopenid=E9376778794A0D6CB151A392F60AB3A2'
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
   
    #通过qq号搜索用户歌单
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