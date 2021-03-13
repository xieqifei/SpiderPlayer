class Music:
    def __init__(self, source, id, url, name, artist, cover, duration, expire,**kv):
        self.source = source
        self.url = url
        self.name = name
        self.artist = artist
        self.cover = cover
        self.id = id
        self.duration = duration
        self.expire = expire
        for k,v in kv.items():
            setattr(self, k, v)


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

class Userlist:
    def __init__(self,source,code,uid,creatername,creatercover,playlist) -> None:
        self.code = code 
        self.source = source
        self.uid = uid
        self.creatername = creatername
        self.creatercover = creatercover
        self.playlist = playlist

class MVideo:
    def __init__(self, source,vid,name,urls,cover,**kv) -> None:
        self.source = source
        self.vid = vid
        self.name = name
        self.urls = urls
        self.cover = cover
        for k,v in kv.items():
            setattr(self,k,v)