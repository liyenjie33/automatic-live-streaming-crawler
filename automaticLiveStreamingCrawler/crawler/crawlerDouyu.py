#!/usr/bin/env python
import time, datetime
import requests
import json

STREAM_URL = "https://www.douyu.com/directory/all"
#url ="https://www.douyu.com/japi/weblist/apinc/rec/list?uid=09a8d82ba493881e41a795af00051501&num=10"
douyuURL = "https://www.douyu.com/japi/weblist/apinc/rec/list?uid=3abfbd23dad7b827341b781100061501&num=20"

def crawler(URL):
	headers = {
	"User-Agent":"Mozilla/5.0 (X11; Linux armv7l; rv:60.0) Gecko/20100101 Firefox/60.0"
	}
	counter = 1
	while True:
		url = URL
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
				print(data)
			
				if len(data['data']):
					liveData = data['data']
					for item in liveData:
						print(counter)
						info = parse(item)
						counter += 1
						token = postAPI(info, token)
					time.sleep(2)
				elif not len(data['data']):
					break
			else:
				print(rs.text)
				continue

def parse(data):
	info = {}
	subInfo = {}
	info['category'] = data['cate2Name']
	info['vid'] = str(data['roomId'])
	info['hostName'] = data['nickname']
	info['title'] = data['roomName']
	info['thumbnailURL'] = data['avatar']
	info['hot'] = data['hot']
	info['timeStamp'] = str(datetime.datetime.now())[:-7]
	info['platform'] = "douyu"
	info['videoURL'] = "https://www.douyu.com/" + str(data['roomId'])
	info['hostID'] = ""
	info['viewCount'] = ""
	info['tag'] = ""
	info['description'] = ""
	info['language'] = ""
	info['gameID'] = ""
	info['publishedAt'] = ""
	#subInfo['rankType'] = data['rankType']
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
			rs = requests.get("https://ps01.ooomg.live:8443", headers=headers, data=json.dumps(data))
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
			headers['Authorization'] = "Bearer " + token
			try:
				rs = requests.post("https://ps01.ooomg.live:8443", data=data, headers=headers)
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
	crawler(douyuURL)
	time.sleep(300)
