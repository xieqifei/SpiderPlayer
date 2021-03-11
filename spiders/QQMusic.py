import requests
from .base import Music,Playlist

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

