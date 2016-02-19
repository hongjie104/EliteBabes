#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
爬elitebabes的图片
'''

__author__ = "32968210@qq.com"

import os, re, requests
from pyquery import PyQuery as pq
import printColor
# import urllib

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}

def mkDir(path):
	if not os.path.exists(path):
		os.makedirs(path)
	return path	

# 开始下载图片
def downloadImg(url, imgPath):
	if os.path.exists(imgPath):
		printColor.printDarkWhite(u"跳过已存在图片:%s" % imgPath)
	else:
		printColor.printBlue(u"开始下载图片:%s" % url)
		try:
			r = requests.get(url, stream = True)
		except Exception, e:
			printColor.printRed(e)
			return
		with open(imgPath, 'wb') as f:
			for chunk in r.iter_content(chunk_size = 1024): 
				if chunk:
					f.write(chunk)
					f.flush()
		# data = urllib.urlopen(url).read()
		# f = file(imgPath, "wb")
		# f.write(data)
		# f.close()

# 抓取相册
def fetchAlbum(url):
	# 相册的地址：演员名字加上相册名
	# http://www.elitebabes.com/ai-sayama-topless-together/
	printColor.printDarkSkyBlue(u"开始访问相册%s" % url)
	global headers
	response = requests.get(url, headers = headers, cookies = {})
	if response.status_code == 200:
		d = pq(response.text)
		# 获取相册的类别、主角名和相册名
		liList = d('#breadcrumbs ol li')
		a = liList[0].find('a')
		# 相册集的名字
		category = a.text
		# 相册集url
		categoryUrl = a.attrib['href']
		a = liList[1].find('a')
		# 演员名
		actress = a.text
		# 演员url
		actressUrl = a.attrib['href']
		# 相册名
		name = liList[2].text
		
		# 建立相册的目录
		albumDir = "images/%s/%s" % (category, name)
		mkDir(albumDir)
		# 将相册数据保存起来
		json = "{\n\t\"name\":\"%s\",\n\t\"actress\":\"%s\",\n\t\"category\":\"%s\",\n\t\"actressUrl\":\"%s\",\n\t\"categoryUrl\":\"%s\",\n\t\"url\":\"%s\"\n}" % (name, actress, category, actressUrl, categoryUrl, url)
		f = open(albumDir + "/data.json", "wb")
		f.write(json)
		f.close()

		for a in d('.gallery-b li a'):
			imgUrl = a.attrib['href']
			downloadImg(imgUrl, "%s/%s" % (albumDir, imgUrl.split('/')[-1]))
			
	else:
		printColor.printRed(u"访问相册出错 %s" % url)

def fetch(category):
	url = "http://www.elitebabes.com/%s/" % category
	printColor.printDarkSkyBlue(u"开始访问相册集%s" % url)
	global headers
	response = requests.get(url, headers = headers, cookies = {})
	if response.status_code == 200:
		d = pq(response.text)
		for a in d('.gallery-a li a'):
			fetchAlbum(a.attrib['href'])
	else:
		printColor.printRed(u"访问出错 %s" % url)

if __name__ == '__main__':
	# 所有类别
	categoryList = ["all-gravure", "als-scan", "digital-desire", "errotica-archives", 
					"femjoy", "hegre-art", "holly-randall", "met-art", "mpl-studios", 
					"photodromm", "playboy", "rylsky-art", "watch-4-beauty", "zemani", "x-art"]

	for category in categoryList:
		fetch(category)
		break

	printColor.printDarkPink(u"结束")