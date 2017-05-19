#!/usr/bin/python
# -*- coding: utf-8 -*-
# Created by Charles  www.chendan.wang
import requests
import time
from wxpy import *
bot = Bot(cache_path=True,console_qr=2)

#-------------测试开始---------
# 机器人账号自身
# myself = bot.self

# 向文件传输助手发送消息
# bot.file_helper.send('Hello from wxpy!')
#------------测试结束------

# my_friend = ensure_one(bot.search('陈丹'))
tuling = Tuling(api_key='e8aad2b9f3454d8a8fa4d16960d77004')

# 使用图灵机器人自动与指定好友聊天
@bot.register()
def reply_my_friend(msg):
    tuling.do_reply(msg)
    print (msg)
embed()