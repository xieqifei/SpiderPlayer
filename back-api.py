# -*- coding:utf-8 -*-
'''
@file_name    :back-api.py
@description  :提供api服务
@time         :2021/02/25 01:15:48
@author       :Qifei
@version      :1.0
'''

import json
from spiders.Bilibili import BiliBili
from spiders.Youtube import Youtube
from spiders.QQMusic import QQMusic

def main_handler(event, context):
  
    #获取get请求的参数
    query = event['queryString']

    #新建一个响应对象
    resp = Response()

    #src为请求必填参数
    if('src' in query):
        
        if(query['src'] == 'bilibili'): #请求资源为bilibili
            return do_query(BiliBili(), query)
        elif (query['src'] == 'youtube'):   #请求资源为youtube
            return do_query(Youtube(), query)
        elif (query['src']=='qqmusic'):
            return do_query(QQMusic(),query)
        else:
            return resp.error("请求出错，暂不支持此源")
    else:
        return resp.error("src为必填参数")



#根据请求参数，对指定平台进行操作
def do_query(platform_obj, query):
    resp = Response()
    #关键词搜索
    if('kw' in query):
        kw=query['kw']
        musics = platform_obj.search_keyword(kw)
        return resp.json(musics)

    #通过id获取音乐信息，比如播放链接，封面等
    elif('id' in query):
        music = platform_obj.get_music(query['id'])
        return resp.json(music)

    #获取一个平台推荐歌单
    elif ('rc' in query):
        musics = platform_obj.get_recommendation()
        return resp.json(musics)
    
    #根据歌单id获取歌单信息
    elif('gd' in query):
        playlist =  platform_obj.get_playlist(query['gd'])
        return resp.json(playlist)
    
    elif('lrc' in query):
        lyric = platform_obj.get_lyric(query['lrc'])
        return resp.json(lyric)
    
    elif('uid' in query):
        userlist = platform_obj.get_userlist(query['uid'])
        return resp.json(userlist)

    #上述参数未被包含，返回错误响应
    else:
        return resp.error("暂无此功能")

#响应类，返回一个http响应格式字典
class Response:
    #错误相应
    def error(self, msg):
        return {
            "isBase64Encoded": False,
            "statusCode": 400,
            "headers": {'Content-Type': 'application/json'},
            "body": '{"error":1,"msg":"'+msg+'}'
        }

    #返回一个html页面
    def html(self, html):
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {'Content-Type': 'text/html'},
            "body": html
        }
    #返回json格式数据
    def json(self, jsonObj):
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {'Content-Type': 'application/json'},
            "body": json.dumps(jsonObj)
        }

