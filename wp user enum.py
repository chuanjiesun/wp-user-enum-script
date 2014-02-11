#Usage: python xx.py http://xxx.xxx numID  #http://www.freebuf.com/?author=12211
# http://www.hzx521.com  http://www.freebuf.com http://www.kaifazhe.me/
#例如python wp.py http://www.kaifazhe.me/ 2000
import re, sys, threading, os
from urllib import parse, request
#from http import client
from time import sleep, time, ctime
from bs4 import BeautifulSoup as beautifulsoup

def meiju(k):
	global flag, count#这个也要再次声明为global,不然就会当成局部变量
	try:
		data = url + '/?author=' + str(k)
		req = request.urlopen(data, timeout = 20)#网络太烂设置的超时时间长一些
		#print('starting to read...')
		resp = req.read(2000)
		#print(resp)
		data_decode = resp.decode(encoding = 'utf-8')
		#sleep(4)
		#print('\n\n\nafter decode : {}'.format(data_decode))
		data_soup = beautifulsoup(data_decode, from_encoding='utf-8')
		#print(data_soup)
		for a in data_soup.find_all('title'):
			#print(a)#<title>kelz - FreeBuf.COM</title>
			b = a.get_text().strip()#由于freebuf的格式为
				#<title>
				#  sn0rt - FreeBuf.COM</title>需要去除空格   变为#sn0rt - FreeBuf.COM
			b = b.split(' ')  #以-分割 [sn0rt, FreeBuf.COM] #具体分隔符还要看具体的站配置,一般用户名后面都有空格
			#print(b[0]) #就打印出sn0rt了
			b = b[0].strip()#进一步去除空格 不然在用户名后存在空格
			print('用户{0}：{1}'.format(k, b))#a.get_text()))#kelz - FreeBuf.COM
			f_w.write('用户'+str(k)+': '+b+'\n')#k是int型， 写入的是字符型
	except Exception as e:
		excepts.append(k)
		length = len(excepts)
		if length > 3:#试了相邻两个相减差值为1，判断用户结束  也可以
			excepts.sort()#类似冒泡排序，这个自带的函数
			for i in range(1,length):
				if i+1 < length:
					if (excepts[i]-excepts[i-1] == 1) and (excepts[i+1] - excepts[i] == 1): 
						#print(excepts[i-1], excepts[i], excepts[i+1])
						#实际由于多线程不一定相邻相减，有任意两个相减为1
						#print('{0}和{1}差值接近'.format(excepts[length-1],excepts[j]))
						#print('貌似结束了 ： {}'.format(excepts[i-1]))
						count.append(excepts[i-1])
						flag = False

			if len(count)>3:
				count = list(set(count))
				print('count is : {}'.format(count))
		else:			
			print('{0} error is : {1}'.format(k, e))


def main():
	global f_w, count, flag #声明个全局变量，用于meiju函数的文件写入
	count = []
	f_w = open('freebuf.txt', 'w+')#, encoding = 'utf-8')
	if num >= 50: #用于判断输入用户ID数是否大于线程数50,小于就开num个线程
		xiancheng_num = 50
	else:
		xiancheng_num = num
	#xiancheng_num = (50 if t else num)
	flag = True
	for i in range(1,num+1,xiancheng_num):#相当于开50个线程


		for j in range(xiancheng_num):
			j = i+j
			t = threading.Thread(target = meiju, args=(j, ))
			t.daemon = True
			threads.append(t)
			t.start()
		for j in range(len(threads)):
			#print(len(threads),j)
			threads[j].join()
		threads.clear()

		if flag:
			print(flag)
			pass
		else:
			print('Flag is : {}  ##########################'.format(flag))
			break#出现了连续的找不到页面就是不存在了

	f_w.close()
	print('\n\n结束循环了\n\n')
	length_count = len(count)
	print(count)#'\n\n错误列表:{}'.format(count))
	count.sort()
	count_set = list(set(count))
	print('\n\n\nwp user enum Fuck IS OVER ！！ 从{}开始就木有了。。。'.format(count_set[0]))


if __name__ =='__main__':
	if len(sys.argv) ==3 or len(sys.argv) ==5:
		t1 = time()
		print('start at : {}'.format(ctime()))
		print('len of params is : {}'.format(len(sys.argv)))
		url = sys.argv[1]
		url = url.rstrip('/')#防止用户输入例如http://xxx.xx/去除最后的/
		print('url is : {}'.format(url))
		num = sys.argv[2]
		print('num is : {}'.format(num))#<class 'str'>
		num = int(num)#这里num是字符串类型，需要转换一下
		print(type(num))  #<class 'int'>
		patt_host = '(?<=://)\w+-?\w+\.\w+[\.\w+]{0,}'
		host = re.search(patt_host, url).group()
		print('host is : {}'.format(host))
		threads = []
		excepts = [] #用于记录所有连接异常，判断是否用户遍历结束

		main()
		t2 = time()
		print('stop at : {}'.format(ctime()))
		print('time elasped : {0:.2f} s'.format(t2-t1))

	else:
		print('Uasge:python xxx.py http://cxxx.xxx.com/xxx.com  numID')
		sys.exit(0)
