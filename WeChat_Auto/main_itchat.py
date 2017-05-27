#!/usr/bin/python
# -*- coding: utf-8 -*-
# Created by Charles  www.chendan.wang
import itchat
import requests
from itchat.content import *
import time
import pymysql
L = []   #所有跟我说话的人名列表
KEY = 'e8aad2b9f3454d8a8fa4d16960d77004'
#-------------测试开始---------
# @itchat.msg_register(itchat.content.TEXT)
# def text_reply(msg):
#     return msg['Text']
#itchat.auto_login(hotReload=True)
#itchat.send('hell,world!',toUserName='filehelper')
#itchat.run()
#------------测试结束------
#---------------向api发送请求--------------
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
        #print(r)
        
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
#---------------向api发送请求结束--------------
#---------------------自动回复开始----------
# 这里是我们在“1. 实现微信消息的获取”中已经用到过的同样的注册方法
#@itchat.msg_register(itchat.content.TEXT) 图灵默认调用
# @itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING, PICTURE, RECORDING, ATTACHMENT, VIDEO])
def tuling_reply(msg):
    # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
    # config = {
    #     host: '211.149.239.36',
    #     port: 3306,
    #     user: 'wechat',
    #     passwd: 'wechatmima',
    #     charset:'utf8mb4',
    #     cursorclass:pymysql.cursors.DictCursor
    # }
    # conn = pymysql.connect(**config)
    # cursor = conn.cursor()
    defaultReply = '我在忙，稍后联系'
    # 如果图灵Key出现问题，那么reply将会是None
    aaa = '%s:%s（%s）' %(msg['User']['NickName'],msg['Content'],time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))  
    print (aaa)   #接收到的信息、发送者
    L.append(msg['User']['NickName']) #把每个跟我说话的人加到list L里
    #print (L)   #打印消息，都谁说话了

    fl=open('name_list.rtf','a')

    fl.write(msg['User']['NickName'])
    fl.write(',')
    fl.close()
    print ('%s发送消息次数：%s' %(msg['User']['NickName'],L.count(msg['User']['NickName'])))  #打印消息，这个人说了几次话
    if L.count(msg['User']['NickName']) > 5:  #做判断，这个人说了5次以上，就不回复了
        reply = None
        return reply
    else:
        if msg['Type'] == 'Text':
            reply = get_response(msg['Text'])
            if reply == '我不会说英语的啦，你还是说中文吧。':
                reply = None
            print('To%s：%s（%s）' %(msg['User']['NickName'],reply,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
            time.sleep(10)
            return reply
        else:
            reply = None
            return reply
#---------------------自动回复结束----------

#---------------------加好友开始----------
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.send_msg('你好!', msg['RecommendInfo']['UserName'])
#---------------------加好友结束----------
# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
#itchat.auto_login(hotReload=True)
itchat.auto_login(hotReload=True) #enableCmdQR=2
itchat.run()
