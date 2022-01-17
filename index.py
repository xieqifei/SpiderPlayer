# -*- coding:utf-8 -*-
'''
@file_name    :index.py
@description  :云函数入口程序，带参数时作为api服务器，不带参数或参数错误时，返回html网页
@time         :2021/02/25 01:15:48
@author       :Qifei
@version      :1.0
'''

import json
import spiders as api
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

    #新建api对象
    bili = api.BiliBili()
    ytb = api.Youtube()
    qqm = api.QQMusic()

    #设置qq音乐cookie，没有cookie输入qq同步歌单功能无法使用
    qqm.set_cookie('pgv_pvi=8608630784; RK=UKpl0yStED; ptcz=fbb88170fafd2ed95d5d3b653c7f180d5d916823e72e04a44454e12fc0772bb7; tvfe_boss_uuid=41ec9918a7abd703; eas_sid=T1q5E9j7O1B5K7i5O1b9U8f162; pac_uid=1_975322731; iip=0; _ga=GA1.2.984015091.1601553199; ts_uid=7486175980; pgv_pvid=5602168404; fqm_pvqid=955e6bfd-c610-4384-b3c0-0afef3ae4b61; ts_refer=www.google.com/; yqq_stat=0; pgv_info=ssid=s208126685; ts_last=y.qq.com/; userAction=1; _qpsvr_localtk=0.8754919399439696; ptui_loginuin=975322731; psrf_access_token_expiresAt=1623414555; qqmusic_key=Q_H_L_2i1iC160emFZNG3eMDZ_aXM5rtRPXzBaWRsslN2Jau7zfn8L5iegbtip-eKzq06; uin=975322731; psrf_qqunionid=; qm_keyst=Q_H_L_2i1iC160emFZNG3eMDZ_aXM5rtRPXzBaWRsslN2Jau7zfn8L5iegbtip-eKzq06; psrf_qqopenid=E9376778794A0D6CB151A392F60AB3A2; tmeLoginType=2; psrf_qqaccess_token=BD8A28A11DF77AD5905C5428ADF9F8C3; euin=NKSkoi-A7io5; psrf_musickey_createtime=1615638555; psrf_qqrefresh_token=E8EAB1E0F4135D94809D75593B5F0333')
    
    #src为请求必填参数
    if('src' in query):
        if(query['src'] == 'bilibili'): #请求资源为bilibili
            return do_query(bili, query)
        elif (query['src'] == 'youtube'):   #请求资源为youtube
            return do_query(ytb, query)
        elif (query['src']=='qqmusic'):
            return do_query(qqm,query)
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

#读取jscss等静态文件为字符串，参数key 静态资源路径
def read_statics(key):
    with open('./cdn'+key) as f:
        staticsstr = f.read()
    return staticsstr

#根据请求参数，对指定平台进行操作， 参数platform_obj 平台的一个对象，query 请求参数字典
def do_query(platform_obj, query):
    resp = Response()
    if('type' in query):

        #关键词搜索
        if('kw' in query and query['type'] =='search'):
            kw=query['kw']
            musics = platform_obj.search_keyword(kw)
            return resp.json(musics)

        #通过id获取音乐信息，比如播放链接，封面等
        elif('id' in query and query['type'] =='minfo'):
            music = platform_obj.get_music(query['id'])
            return resp.json(music)

        #获取一个平台推荐歌单
        elif ('rc' in query and query['type'] =='recom'):
            musics = platform_obj.get_recommendation()
            return resp.json(musics)
        
        #根据歌单id获取歌单信息
        elif('gd' in query and query['type'] =='playlist'):
            playlist =  platform_obj.get_playlist(query['gd'])
            return resp.json(playlist)
        
        #获取歌词
        elif('lrc' in query and query['type'] =='lyric'):
            lyric = platform_obj.get_lyric(query['lrc'])
            return resp.json(lyric)
        
        #获取用户列表
        elif('uid' in query and query['type'] =='userlist'):
            userlist = platform_obj.get_userlist(query['uid'])
            return resp.json(userlist)
        
        elif(query['type'] == 'vinfo' and 'songid' in query):
            videos = platform_obj.get_mv_info(query['songid'])
            return resp.json(videos)
        
        elif(query['type'] == 'vurl' and 'vid' in query):
            mvideo = platform_obj.get_mv_url(query['vid'])
            return resp.json(mvideo)

    #上述参数未被包含，返回错误响应
    else:
        return resp.error("type未标记")

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
            "headers": {'Content-Type': 'application/json','Access-Control-Allow-Origin':'*'},
            "body": json.dumps(jsonObj)
        }

