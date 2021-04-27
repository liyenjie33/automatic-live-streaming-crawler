#!/usr/bin/env python
import time, datetime
import requests
import json

HuyaURL = "https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&tagAll=0&page="


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
				if len(data['data']['datas']):
					print("Page: ", page)
					liveData = data['data']['datas']
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
	info['category'] = data['gameFullName']
	info['vid'] = data['liveChannel']
	info['hostName'] = data['nick']
	info['title'] = data['introduction']
	info['thumbnailURL'] = data['avatar180']
	info['hot'] = ""
	info['timeStamp'] = str(datetime.datetime.now())[:-7]
	info['platform'] = "huya"
	info['videoURL'] = "https://www.huya.com/" + str(data['privateHost'])
	info['hostID'] = data['profileRoom']
	info['viewCount'] = data['totalCount']
	info['tag'] = data['recommendTagName']
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
			headers['Authorization'] = "Bearer " + token
			try:
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
	crawler(HuyaURL)
	time.sleep(300)
