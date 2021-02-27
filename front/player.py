# -*- encoding: utf-8 -*-
'''
@file_name    :player.py
@description  :
@time         :2021/02/25 01:15:48
@author       :Qifei
@version      :1.0
'''

import requests

def main_handler(event,context):
    baseUrl = "https://service-ife10uoc-1258461674.hk.apigw.tencentcs.com/release/music-api"
    #当返回html页面时，get一次后端api，激活云函数，这样前端html从api获取json时，api云函数会更快做出响应
    requests.get(baseUrl)
    with open('./index.html') as f:
        html = f.read()
    return {
    "isBase64Encoded": False,
    "statusCode": 200,
    "headers": {'Content-Type': 'text/html','Access-Control-Allow-Origin':'*'},
    "body": html
    }