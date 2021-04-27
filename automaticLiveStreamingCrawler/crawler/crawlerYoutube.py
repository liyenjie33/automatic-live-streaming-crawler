#!/usr/bin/env python
import requests
import time, datetime, random
import json
import re
import csv
import sys, os

# playlistID of live broadcast playlist
playlistID_youtube = [ 
"PLU12uITxBEPFJGVb2zSgCaWvMBe7vHonB", # 直播 
"PLiCvVJzBupKlQ50jZqLas7SAztTMEYv1f", # 遊戲 
"PL8fVUTBmJhHJrxHg_uNTMyRmsWbFltuQV", # 運動 
"PL57quI9usf_sQMlMeQrUr5O_pCncZilx3", # 科技 
"PLIFqWCuxNyoiKKthaTBqjIH6m6A9INomt", # 動物 
"PLU12uITxBEPFnoOrc_w0oJL6CEeKRhpcb", # 行動應用程式 
"PLU12uITxBEPHvBRHoUt-fzKr8Iz1HpfUC", # 網路攝影機直播 
]

# Youtube data API
STREAM_URL = "https://www.googleapis.com/youtube/v3/"
STREAM_MAX = "&maxResults=50"
STREAM_part = "&part=snippet,statistics,liveStreamingDetails"

# Get API key & Line token
def readConfig():
	with open ('/home/pi/youtube.json', 'rt') as f:
		data = f.read()
		f.close()
	return data

# Line notification
def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    
    payload = {'message': msg}
    while True:
        print("Line notify")
        try:
            r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload, timeout=2)
        except Exception as e:
            print("Error: ", e)
            time.sleep(60)
        else:
            break
    return r.status_code

# control API delay: used when API quota exceed
def delayControl():
	now = datetime.datetime.strptime(datetime.datetime.now().strftime('%H:%M'),'%H:%M')
	l = datetime.datetime.strptime('16:00','%H:%M')
	delay = l -now
	return delay

def modifyIP():
	#global IPflag
	with open ('/home/pi/ip.json', 'rt') as f:
		data = f.read()
		f.close()
	ipList = json.loads(data)['IP']

	ipNow = os.popen("cat /etc/dhcpcd.conf | grep -e \'^static ip_address=\' | cut -d= -f2")
	#print(ipNow)
	ipNow = ipNow.read().strip('\n')
	#ipNow = ipNow.read()
	print(ipNow)
	#print(len(ipNow))
	for i in range(1,5):
		if  ipList[str(i)] in ipNow:
			#print(i)
			if i < 4:
				IPflag = i + 1
			else:
				IPflag = 1
			print("IPflag:", IPflag)
			break


	#print(ipList)
	#print(type(ipList))
	"""
	if num == 0:
		with open ('/home/pi/ipStatus.txt', 'rt') as f:
			IPnow = f.read()
			print("Now IP is ", str(IPnow))
			f.close()
		for i in range(1,18):
			if ipList[str(i)] in str(IPnow):
				#print(i)
				IPflag = i
				num = IPflag
				print(num)
				break
	"""

	ip = ipList[str(IPflag)]
	_ip = str(ip) + "/24"
	print(_ip)
	ping = os.system('ping -c 1 -w 1 %s'%ip)
	if ping:
		print("IP modify...")
		try:
			#path = "sudo sed -i -e " + "\'s/static ip_address=" + ipNow + "/static ip_address=" + _ip + "/g\' /etc/dhcpcd.conf"
			#print(path)
			os.system("sudo sed -i -e \'s@static ip_address=%s@static ip_address=%s@g\' /etc/dhcpcd.conf" % (ipNow,_ip))
			time.sleep(3)
			#sys.exit()
		#except:
		#	sys.exit()
		#try:
			os.system("sudo ifconfig eth0 down")
			time.sleep(5)
			os.system("sudo ifconfig eth0 up")
			time.sleep(5)
		except Exception as e:
			print(e)
		"""	
		try:
			os.system('sudo ifconfig eth0 down')
			time.sleep(3)
			os.system('sudo ifconfig eth0 %s netmask 255.255.255.0 broadcast 140.115.154.255'%ip)
			time.sleep(3)
			os.system('sudo route add default gw 140.115.154.254')
			time.sleep(3)
			os.system('sudo ifconfig eth0 up')
			time.sleep(3)
		except Exception as e:
			print(e)
			os.system('sudo ifconfig eth0 up')
			time.sleep(3)
		"""
		for i in range(0,10):
			rs = os.system('ping -c 1 -w 1 8.8.8.8')
			if not rs:
				print("Finish IP modification: ", ip)
				break
			else:
				print("Failed: ", ip)
				time.sleep(10)
				if i == 10:
					ip = ""
	else:
		ip = ""
	return ip


# crawler: get API response data
def getVideos(playlistId):
	# apiFlag = 0 means that API quota haven't exceed
	apiFlag = 0
	while True:
		STREAM_KEY = random.choice(DEVELOPER_KEY)
		try:
			firstURL = STREAM_URL + "playlistItems?&playlistId=" + playlistId + "&key=" + STREAM_KEY + "&part=contentDetails"
			res = requests.get(firstURL)
		except:
			time.sleep(10)
			continue
		else:
			if (res.status_code) == 403:
				print("API Daily Limit Exceeded: ", STREAM_KEY)
				DEVELOPER_KEY.remove(STREAM_KEY)
				print(DEVELOPER_KEY)
				if not len(DEVELOPER_KEY):
					print("All API Key Exceed Daily Limit!!!")
					#delay = delayControl()
					#time.sleep(delay)
					apiFlag = 1
					break

			elif (res.status_code) == 200:
				res = res.json()
				nextPageToken = res.get('nextPageToken')
				while ('nextPageToken' in res):

					STREAM_KEY = random.choice(DEVELOPER_KEY)
					firstURL = STREAM_URL + "playlistItems?&playlistId=" + playlistId + "&key=" + STREAM_KEY + "&part=contentDetails"
					APIURL = firstURL + "&pageToken=" + nextPageToken

					nextPage = requests.get(APIURL)

					if (nextPage.status_code) == 403:
						print("API Daily Limit Exceeded: ", STREAM_KEY)
						try:
							DEVELOPER_KEY.remove(STREAM_KEY)
							print(DEVELOPER_KEY)
						except:
							pass

						if not len(DEVELOPER_KEY):
							res.pop('nextPageToken', None)
							apiFlag = 1

					elif (nextPage.status_code) == 200:
						nextPage = nextPage.json()
						try:
							res['items'] = res['items'] + nextPage['items']
						except:
							print(nextPage)
						else:
							if 'nextPageToken' not in nextPage:
								res.pop('nextPageToken', None)
							else:
								nextPageToken = nextPage['nextPageToken']
				break
	return res, apiFlag

# Parse API response data: get videoID and videoPublishedAt
def getVediosID(res):
	videoID_list = []
	count = 0
	for Key, Value in res.items():
		if Key == 'items':
			for data in Value:
				count+= 1
				videoID = data['contentDetails']
				if "videoPublishedAt" not in data['contentDetails']:
					data['contentDetails']['videoPublishedAt'] = ""
				print(videoID)
				#data['snippet']['resourceId']['videoId']
				videoID_list.append(videoID)
	print(count)
	return videoID_list

# ajax request header setting
def setHeaders():
	headers = {
	"Content-Type":"application/json; charset=UTF-8",
	"Host":"www.youtube.com",
	"User-Agent":"Mozilla/5.0 (X11; Linux armv7l; rv:60.0) Gecko/20100101 Firefox/60.0",
    #"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0"
	"Origin":"https://www.youtube.com"
	}
	return headers

# get video info by ajax request
def getVideoInfo(videoID, publishedAt, requestCount):
	info = {}
	subInfo = {}
	url = "https://www.youtube.com/watch?v=" + videoID + "/service_ajax?name=updatedMetadataEndpoint"
	while True:
		try:
			rs = requests.get(url, headers=setHeaders(), timeout=2)
		except Exception as e:
			print(e)
			time.sleep(10)
			continue
		else:
			break
	if (rs.status_code)== 429:
		exceedText = "YouTube 收到了大量由您的網路所發出的要求,因而中斷您的作業\nrequestCount: " + str(requestCount)
		print(exceedText)
		lineNotifyMessage(lineToken, exceedText)
		outputCSV(str(datetime.datetime.now())[:-7], str(requestNum), "BAN")
		return "BAN"

	elif (rs.status_code)== 200:
		print(url)
		try:
			data = re.search(r'{"responseContext".*', rs.text,flags=re.DOTALL | re.MULTILINE).group().split('\n')[0][0:-1]
			data = json.loads(data)
			data = data['contents']['twoColumnWatchNextResults']['results']['results']['contents']
			primaryInfo = data[0]['videoPrimaryInfoRenderer']
			secondaryInfo = data[1]['videoSecondaryInfoRenderer']
		except:
			info = {}
			return info
		else:
			try:
				#title
				info['title'] = primaryInfo['title']['runs'][0]['text']
				#viewCount
				viewCount = primaryInfo['viewCount']['videoViewCountRenderer']['viewCount']['runs'][0]['text'][0:-6]
				info['viewCount'] = ''.join(str(viewCount).split(','))
			except:
				info = {}
				return info
			else:
				#timeStamp
				info['timeStamp'] = str(datetime.datetime.now())[:-7]
				#videoURL
				info['videoURL'] = "https://www.youtube.com/watch?v=" + videoID
				#publishedAt
				info['publishedAt'] = publishedAt
				#tag & description
				tags = ""
				descriptions = ""
				try:
					for item in secondaryInfo['description']['runs']:
						try:
							tag = item['navigationEndpoint']['searchEndpoint']['query']
							tags += tag
						except:
							pass
						try:
							description = item['text']
							descriptions += description  
						except:
							pass
				except:
					pass
				#tag
				info['tag'] = tags
				#description
				info['description'] = descriptions
				#host
				info['hostName'] = secondaryInfo['owner']['videoOwnerRenderer']['title']['runs'][0]['text']
				#subscriberCount
				try:
					subInfo['subscriberCount'] = secondaryInfo['owner']['videoOwnerRenderer']['subscriberCountText']['runs'][0]['text'][0:-5]
				except:
					pass
				#category
				try:
					info['category'] = secondaryInfo['metadataRowContainer']['metadataRowContainerRenderer']['rows'][0]['metadataRowRenderer']['contents'][0]['runs'][0]['text']
				except:
					pass
				info['hostID'] = ""
				info['language'] = ""
				info['gameID'] = ""
				info['thumbnailURL'] = ""
				info['hot'] = ""
				info['platform'] = "Youtube"
				info['vid'] = videoID
				info['more'] = subInfo
	info = json.dumps(info, ensure_ascii=False).encode('utf-8')
	print(info)
	return(info)

# get post API token
def getPostToken(interface):
	macAddr = open('/sys/class/net/'+interface+'/address').readline()
	headers = {'Content-Type':'application/json'}
	data = {}
	data['CID'] = macAddr[0:17]
	while True:
		try:
			rs = requests.get("https://ps01.ooomg.live:8443/signin/crawler", headers=headers, data=json.dumps(data))
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

# post info to DB
def postAPI(data, token):
	headers = {'Content-Type':'application/json'}
	if bool(data):
		delay = 5
		while True:
			headers['Authorization'] = "Bearer " + token
			try:
				rs = requests.post("https://ps01.ooomg.live:8443/crawler/channel", data=data, headers=headers)
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


def outputCSV(time, requestNum, event):
	with open('/home/pi/youtube.csv','a') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerow([time, requestNum, event])



configData = readConfig()
DEVELOPER_KEY = json.loads(configData)['DEVELOPER_KEY']
lineToken = json.loads(configData)['LINETOKEN']
print(DEVELOPER_KEY,lineToken)
token = getPostToken('eth0')
requestNum = 0
#global IPflag
#IPflag = 0

#test = modifyIP()
#lineNotifyMessage(lineToken, "test")
#time.sleep(60)

while True:
	start = time.time()
	for playlistId in playlistID_youtube:
		videos, apiFlag = getVideos(playlistId)
		#print(apiFlag)
		if videos:
			result = getVediosID(videos)
			#print(result)
			count = 0
			for item in result:
				#print(item['videoId'])
				#print(item['videoPublishedAt'])
				count += 1
				print(count)
				requestNum += 1
				data = getVideoInfo(item['videoId'],item['videoPublishedAt'], requestNum)
				if data == "BAN":
					print(data)
					IPrs = modifyIP()
					modifyIPMsg = "Modify IP as " + str(IPrs)
					lineNotifyMessage(lineToken, modifyIPMsg)

				else:
					print("requestNum: ", requestNum, str(datetime.datetime.now())[:-7])
					token = postAPI(data, token)
					sleepTime = random.randint(10,15)
					time.sleep(sleepTime)
					print("sleepTime: ", sleepTime)
					if count%50 == 0:
						time.sleep(5)
					if requestNum%900 ==0:
						outputCSV(str(datetime.datetime.now())[:-7], str(requestNum), "")
		if apiFlag:
			delay = delayControl()
			time.sleep(delay)
			DEVELOPER_KEY = json.loads(configData)['DEVELOPER_KEY']

		time.sleep(30)
	print(time.time()-start)
