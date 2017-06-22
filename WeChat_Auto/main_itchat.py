#!/usr/bin/python
# -*- coding: utf-8 -*-
# Created by Charles  www.chendan.wang
import itchat
import requests
from itchat.content import *
import time
import pymysql
import pymysql.cursors
# L = []   #所有跟我说话的人名列表
#--------------连接数据库开始--------
def connDB(): #连接数据库函数
    conn=pymysql.connect(host='211.149.239.36',user='wechat',passwd='wechatmima',db='wechatdb',charset='utf8mb4')
    cur=conn.cursor()
    return (conn,cur)
def exeUpdate(cur,sql):#更新语句，可执行update,insert语句
    sta=cur.execute(sql)
    return(sta)

def exeDelete(cur,IDs): #删除语句，可批量删除
    for eachID in IDs.split(' '):
        sta=cur.execute('delete from relationTriple where tID =%d'% int(eachID))
    return (sta)

def exeQuery(cur,sql):#查询语句
    cur.execute(sql)
    return (cur)

def connClose(conn,cur):#关闭所有连接
    cur.close()
    conn.close()
#--------------连接数据库结束--------

KEY = 'e8aad2b9f3454d8a8fa4d16960d77004'  #图灵KEY

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

    defaultReply = '我在忙，稍后联系'
    # 如果图灵Key出现问题，那么reply将会是None
    mnname = msg['User']['NickName']
    mcontent = msg['Content']
    ttime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    ttime2 = time.strftime('%H:%M:%S',time.localtime(time.time()))
    aaa = '%s:%s（%s-%s）' %(mnname,mcontent,ttime,ttime2)  
    print (aaa)   #接收到的信息、发送者
    #调用连接数据库的函数        
    # conn=connDB();
    # cur=connDB();
    conn=pymysql.connect(host='211.149.239.36',user='wechat',passwd='wechatmima',db='wechatdb',charset='utf8mb4')
    cur=conn.cursor()
    sta=exeUpdate(cur, 'INSERT INTO content_list(date_y,date_h,nick_name,contentd) VALUES("%s","%s","%s","%s");'%(ttime,ttime2,mnname,mcontent) )
    # sql = 'insert into content_list values(%s,%s,%s)' %(ttime,mnname,mcontent)
    # sta = cur.execute(sql)
    if(sta==1):
        print('内容插入数据库成功')
    else:
        print('内容插入数据库失败')
    conn.commit()
    
    #L.append(msg['User']['NickName']) #把每个跟我说话的人加到list L里
    exeQuery(cur,'SELECT nick_name FROM content_list where date_y = "%s"' %(time.strftime('%Y-%m-%d',time.localtime(time.time()))))
    A = cur.fetchall()
    #print (A)   #打印消息，都谁说话了

    # fl=open('name_list.rtf','a')

    # fl.write(msg['User']['NickName'])
    # fl.write(',')
    # fl.close()

    # print ('%s发送消息次数：%s' %(msg['User']['NickName'],L.count(msg['User']['NickName'])))  #打印消息，这个人说了几次话
    AB = (msg['User']['NickName'],)
    print ('%s发送消息次数：%s' %(msg['User']['NickName'],A.count(AB)))  #打印消息，这个人说了几次话
    # if L.count(msg['User']['NickName']) > 5:  #做判断，这个人说了5次以上，就不回复了
    if A.count(AB) > 5:  #做判断，这个人说了5次以上，就不回复了
        reply = None
        return reply
    else:
        if msg['Type'] == 'Text':
            reply = get_response(msg['Text'])
            if reply == '我不会说英语的啦，你还是说中文吧。':
                reply = None
            time.sleep(10)
            print('To%s：%s（%s）' %(msg['User']['NickName'],reply,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
            sta=exeUpdate(cur, 'INSERT INTO content_list(date_y,date_h,nick_name,contentd) VALUES("%s","%s","To:%s","%s");'%(time.strftime('%Y-%m-%d',time.localtime(time.time())),time.strftime('%H:%M:%S',time.localtime(time.time())),msg['User']['NickName'],reply) )
            if(sta==1):
                print('内容插入数据库成功')
            else:
                print('内容插入数据库失败')
            conn.commit()
            connClose(conn, cur)
            return reply
        else:
            reply = None
            connClose(conn, cur)
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