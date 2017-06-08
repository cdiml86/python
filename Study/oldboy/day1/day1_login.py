#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Charles

user1 = 'charles'
password1 = '123456'
while 1:
	input_name = input('输入登录名：')
	if input_name != user1:                    	#如果判断输入用户名不存在
		print ('用户名不存在，请重新登录')			
	elif input_name == user1:						#如果判断输入用户名存在
		fl = open('disable_user.rtf','r')			#打开禁止登录名单
		#print ('打开禁止登录名单')
		lines = fl.readlines()						#读取名单内容
		#print ('关闭禁止登录名单')
		fl.close()
		for line in lines:							#循环读取内容存到line里
			if line == user1:						#如果禁止登录名单中有user1
				print ('您已被禁止登录，请退出！！')
				exit()
			else:
				for x in range(3):
					print ('for循环起始位置')
					input_pw = input('请输入密码：')
					if input_pw == password1:
						print ('恭喜您，登录成功！')
						exit()	
					else:
						if x < 2:
							print ('输入密码错误，请重新输入！')
							print (x)
						else:
							print ('密码输入3次错误，禁止登录！！')
							print (x)
							fl1 = open('disable_user.rtf','w')
							#print ('准备写禁止登录名单')
							fl1.write(user1)
							fl1.close()
							exit()
