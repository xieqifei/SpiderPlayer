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

