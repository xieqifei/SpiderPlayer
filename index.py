# -*- coding:utf-8 -*-
'''
@file_name    :index.py
@description  :云函数入口程序，带参数时作为api服务器，不带参数或参数错误时，返回html网页
@time         :2021/02/25 01:15:48
@author       :Qifei
@version      :1.0
'''

import json
from spiders.Bilibili import BiliBili
from spiders.Youtube import Youtube
from spiders.QQMusic import QQMusic

def main_handler(event, context):
    # query = event('queryStringParameters')
    #将以下目录里的静态资源替换到html中
    js = ['/js/ajax.js','/js/lyric.js','/js/musicList.js','/js/functions.js','/js/player.js','/js/jquery.mCustomScrollbar.concat.min.js','/js/background-blur.min.js']
    css = ['/css/jquery.mCustomScrollbar.min.css','/css/player.css','/css/small.css']
    
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
            return resp.error("请求出错，无此源")
    else:
        with open('./index.html') as f:
            html = f.read()
        #将js代码插入html的script标签中
        for j in js:
            html = html.replace("${"+j+"}",read_statics(j))
        #将css代码插入html的style标签中
        for cs in css:
            html = html.replace("${"+cs+"}",read_statics(cs))
        return resp.html(html)

#读取jscss等静态文件为字符串
def read_statics(key):
    with open('./cdn'+key) as f:
        staticsstr = f.read()
    return staticsstr

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

