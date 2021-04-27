#!/usr/bin/env python
import time, datetime
import requests
import json
import re
from myLog import MyLog

STREAM_URL  = "https://api.twitch.tv/kraken/streams/"
Initialurl  = "https://api.twitch.tv/helix/streams?first=100" #For TwitchAPI function
Twitch_Url  = "https://www.twitch.tv/" 

myLog = MyLog("Twitch")

def readConfig():
    with open ('/home/pi/twitch.json', 'rt') as f:
        data = f.read()
        f.close()
    return data

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

def getOAtoken():
    #myHeaders = {'Client-ID':ClientID, 'client_secret': "fynlkfq6myoufsdygdjq5ptbcig1ed", 'grant_type': "client_credentials"}
    OA_URL = "https://id.twitch.tv/oauth2/token?client_id=" + ClientID + "&client_secret=" + secret + "&grant_type=client_credentials"
    while True:
        try:
            rs = requests.post(OA_URL)
        except Exception as e:
            print(e)
            lineNotifyMessage(lineToken, "Twitch getOAtoken failed")
            time.sleep(10)
            continue
        else:
            #lineNotifyMessage(lineToken, "Twitch getOAtoken succeed")
            print(rs.json())
            token = rs.json()['access_token']
            print(token)
            break
    return token

def RequestAPI(url, OAtoken):
    token = "Bearer " + OAtoken
    myHeaders = {'Client-ID' : ClientID, 'Authorization':token}
    while True:
        try:
            r = requests.get(url,headers = myHeaders, timeout=2)
        except Exception as e:
            print(e)
            myLog.error("RequestAPI failed: " + e)
            time.sleep(5)
            continue
        else:
            if r.status_code == 200:
                res = r.json()
                break
            else:
                token = "Bearer " + getOAtoken()
                myHeaders = {'Client-ID' : ClientID, 'Authorization':token}
    return res, token

def generateURL_Ccursor(data):
    urlByStream = []
    cursor = ''
    for Key, Value in data.items(): 
        if Key == 'data':
            for key in Value:
                info = {}
                data = {}
                for dataKey, dataValue in key.items():
                    if dataKey == 'language':
                        info[dataKey] = dataValue
                    elif dataKey == 'id':
                        info['vid'] = dataValue
                    elif dataKey == 'viewer_count':
                        info['viewCount'] = dataValue
                    elif dataKey == 'thumbnail_url':
                        info['thumbnailURL'] = dataValue
                    elif dataKey == 'tag_ids':
                        try:
                            info['tag'] = str(','.join(dataValue))
                        except:
                            pass
                    elif dataKey == 'user_id':
                        info['hostID'] = dataValue
                    elif dataKey == 'title':
                        info['title'] = dataValue
                    elif dataKey == 'user_name':
                        videoURL = Twitch_Url + dataValue
                        info['videoURL'] = videoURL
                        info['hostName'] = dataValue
                    elif dataKey == 'started_at':
                        info['publishedAt'] = dataValue
                    elif dataKey == 'game_id':
                        info['gameID'] = dataValue
                    else:
                        dataValue = str(dataValue).replace('\"','\\\"')
                        data[dataKey] = dataValue
                info['description'] = ""
                info['category'] = ""
                info['hot'] = ""
                info['timeStamp'] = str(datetime.datetime.now())[:-7]
                info['platform'] = "Twitch"
                info['more'] = data
                info = json.dumps(info, ensure_ascii=False).encode('utf-8')
                #print(data)
                urlByStream.append(info)
        elif Key == 'pagination':
            try:
                cursor = Value['cursor']
            except:
                cursor = ""
    return urlByStream, cursor

def crawlerTwitch():
	start = time.time()
	counter = 0
	token = getPostToken('eth0')
	OAtoken = getOAtoken()

	data, OAtoken = RequestAPI(Initialurl, OAtoken)
	info_list, cursor = generateURL_Ccursor(data)
	APIURL = Initialurl + "&after=" + cursor
	while True:
		counter = counter + 1
		try:
			data, OAtoken = RequestAPI(APIURL, OAtoken)
		except:
			break
		else:
			info_list, cursor = generateURL_Ccursor(data)
			APIURL = Initialurl + "&after=" + cursor
			for item in info_list:
				print(json.loads(item))
				myLog.info(json.loads(item)['videoURL'])
				token = postAPI(item, token)
			if counter == 25:
			#	print("Finish Twitch!")
				time.sleep(60)
	print(time.time()-start)
	print(counter)

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
                #print(rs)
                if (rs.status_code) == 200:
                    myLog.info("Post to DB: " + str(rs.status_code))
                    print(rs.status_code)
                    break
                elif (rs.status_code) == 401:
                    myLog.warning("Post to DB: " + str(rs.status_code) + "token error")
                    token = getPostToken('eth0')
                    continue
            except:
                time.sleep(delay)
                if delay<60:
                    delay += 5
                continue
    return token


configData = readConfig()
ClientID = json.loads(configData)['ClientID']
secret = json.loads(configData)['ClientSecret']
lineToken = json.loads(configData)['LINETOKEN']
while True:
	crawlerTwitch()
	time.sleep(300)


"""
# Twitch data format
{'language': 'en', 
'id': '35991336352', 
'viewer_count': 1317, 
'type': 'live', 
'game_id': '68000', 
'thumbnail_url': 'https://static-cdn.jtvnw.net/previews-ttv/live_user_dizzykitten-{width}x{height}.jpg', 
'tag_ids': ['6ea6bca4-4712-4ab9-a906-e3336a9d8039'], 
'user_id': '47474524', 
'title': 'Spooky games! ASMR later!', 
'VideoURL': 'https://www.twitch.tv/DizzyKitten', 
'started_at': '2019-10-17T01:33:29Z', 
'user_name': 'DizzyKitten'}
"""
