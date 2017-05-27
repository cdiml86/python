#!/usr/bin/python
# -*- coding: utf-8 -*-
# Created by Charles  www.chendan.wang

import pymysql
import pymysql.cursors
def access_mysql():
	# config = {
 #        host='211.149.239.36',
 #        user= 'wechat',
 #        passwd='wechatmima',
 #        db='wechatdb',
 #        charset='utf8mb4',
 #        cursorclass=pymysql.cursors.DictCursor
 #    }
	conn = pymysql.connect(host='211.149.239.36',user= 'wechat',passwd='wechatmima',db='wechatdb',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
	cursor = conn.cursor()

	sql = "INSERT INTO list_name(date_d,nickname)VALUES ('2017-05-22', 'Mohan')"
	try:
   # 执行sql语句
		cursor.execute(sql)
   # 提交到数据库执行
		cursor.commit()
	except:
   # 如果发生错误则回滚
		cursor.rollback()

# 关闭游标连接
	cursor.close()
# 关闭数据库连接
	conn.close()
if __name__ == '__main__':
	access_mysql()