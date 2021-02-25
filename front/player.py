# -*- encoding: utf-8 -*-
'''
@file_name    :player.py
@description  :
@time         :2021/02/25 01:15:48
@author       :Qifei
@version      :1.0
'''


def main_handler(event,context):
    with open('./index.html') as f:
        html = f.read()
    return {
    "isBase64Encoded": False,
    "statusCode": 200,
    "headers": {'Content-Type': 'text/html','Access-Control-Allow-Origin':'*'},
    "body": html
    }