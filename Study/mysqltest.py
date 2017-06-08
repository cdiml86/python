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
	conn = pymysql.connect(host='localhost',user= 'root',passwd='danailin',db='wechat',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
	cursor = conn.cursor()

	#sql = "INSERT INTO content_list VALUES ('2017-05-22', 'Mohan','123')"
	sql = "insert into wechat.content_list ( nick_name, date_d, content) values ( 你猜, 2017-05-26 22:11:28, 12534)"
	try:
   # 执行sql语句
		cursor.execute(sql)
   # 提交到数据库执行
		cursor.commit()
		rint ('插入成功')
		# cursor.close()
		# conn.close()
	except:
   # 如果发生错误则回滚
		# cursor.rollback()
		print ('插入失败')

# 关闭游标连接
	cursor.close()
# 关闭数据库连接
	conn.close()
if __name__ == '__main__':
	access_mysql()