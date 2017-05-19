#!/usr/bin/python
# -*- coding: utf-8 -*-
# Created by Charles  www.chendan.wang
import itchat
import requests
from itchat.content import *
import time

KEY = 'e8aad2b9f3454d8a8fa4d16960d77004'
#-------------测试开始---------
# @itchat.msg_register(itchat.content.TEXT)
# def text_reply(msg):
#     return msg['Text']
#itchat.auto_login(hotReload=True)
#itchat.send('hell,world!',toUserName='filehelper')
#itchat.run()
#------------测试结束------
def get_response(msg):
    # 这里我们就像在“3. 实现最简单的与图灵机器人的交互”中做的一样
    # 构造了要发送给服务器的数据
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'danxiaohao',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        print(r)
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        # ra = [r.get('text'),r.get('url')]
        # return ra
        # return [r.get('text'),r.get('url')]
        return r.get('text')
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return
#---------------------自动回复开始----------
# 这里是我们在“1. 实现微信消息的获取”中已经用到过的同样的注册方法
#@itchat.msg_register(itchat.content.TEXT) 图灵默认调用
# @itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING, PICTURE, RECORDING, ATTACHMENT, VIDEO])
def tuling_reply(msg):
    # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
    defaultReply = '我在忙，稍后联系'
    # 如果图灵Key出现问题，那么reply将会是None
    # if msg['Type'] not TEXT:
    #     print ('不是文字消息！')
    if msg['Type'] == 'Text':
        
        reply = get_response(msg['Text'])
        time.sleep(30)
        return reply
    else:
        reply = None
    # if reply == '我不会说英语的啦，你还是说中文吧。':
    #     reply = None
    #     print(reply)
    # a or b的意思是，如果a有内容，那么返回a，否则返回b
    # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
    # return reply 
#---------------------自动回复结束----------
#---------------------加好友开始----------
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.send_msg('你好!', msg['RecommendInfo']['UserName'])
#---------------------加好友结束----------
# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
#itchat.auto_login(hotReload=True)
itchat.auto_login(hotReload=True,enableCmdQR=2) 
itchat.run()
