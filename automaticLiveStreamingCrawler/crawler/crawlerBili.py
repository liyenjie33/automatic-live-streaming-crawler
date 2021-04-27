#!/usr/bin/env python
import time, datetime
import requests
import json

biliURL = "https://api.live.bilibili.com/room/v1/room/get_user_recommend?page="

def crawler(URL):
	headers = {
	"User-Agent":"Mozilla/5.0 (X11; Linux armv7l; rv:60.0) Gecko/20100101 Firefox/60.0"
	}
	page = 1
	counter = 1
	while True:
		url = URL + str(page)
		print(url)
		try:
			rs = requests.get(url, headers=headers, timeout=2)
		except Exception as e:
			print(e)
			time.sleep(5)
			continue
		else:
			if counter == 1:
				token = getPostToken('eth0')
			if (rs.status_code) == 200:
				data = rs.json()
				if len(data['data']):
					print("Page: ", page)
					liveData = data['data']
					for item in liveData:
						print(counter)
						info = parse(item)
						counter += 1
						token = postAPI(info, token)
					page += 1
					time.sleep(2)
				else:
					break
			else:
				print(rs.text)
				continue

def parse(data):
	info = {}
	subInfo = {}
	info['category'] = ""
	info['vid'] = str(data['roomid'])
	info['hostName'] = data['uname']
	info['title'] = data['title']
	info['thumbnailURL'] = data['face']
	info['hot'] = ""
	info['timeStamp'] = str(datetime.datetime.now())[:-7]
	info['platform'] = "bilibili"
	info['videoURL'] = "https://live.bilibili.com" + str(data['link'])
	info['hostID'] = data['uid']
	info['viewCount'] = data['online']
	info['tag'] = ""
	info['description'] = ""
	info['language'] = ""
	info['gameID'] = ""
	info['publishedAt'] = ""
	#subInfo['test'] = "test"
	info['more'] = subInfo

	print(info)
	return json.dumps(info)


def getPostToken(interface):
	macAddr = open('/sys/class/net/'+interface+'/address').readline()
	headers = {'Content-Type':'application/json'}
	data = {}
	data['CID'] = macAddr[0:17]
	while True:
		try:
			rs = requests.get("http://10.33.7.63:3000/signin/crawler", headers=headers, data=json.dumps(data))
		except:
			time.sleep(5)
			continue
		else:
			if (rs.status_code) == 200:
				token = rs.json()['token']
				print(token)
			else:
				token = ""
			break
	return token

def postAPI(data, token):
	headers = {'Content-Type':'application/json'}
	if bool(data):
		delay = 5
		while True:
			try:
				headers['Authorization'] = "Bearer " + token
				rs = requests.post("http://10.33.7.63:3000/crawler/channel", data=data, headers=headers)
				print(rs)
				if (rs.status_code) == 200:
					break
				elif (rs.status_code) == 401:
					token = getPostToken('eth0')
					continue
			except:
				time.sleep(delay)
				if delay<60:
					delay += 5
				continue
	return token

while True:
	crawler(biliURL)
	time.sleep(300)
