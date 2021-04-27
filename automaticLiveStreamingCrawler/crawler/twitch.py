import time, datetime
import requests
import json
import re


STREAM_URL  = "https://api.twitch.tv/kraken/streams/"
Initialurl  = "https://api.twitch.tv/helix/streams?first=100" #For TwitchAPI function
Twitch_Url  = "https://www.twitch.tv/"
OA_URL = "https://id.twitch.tv/oauth2/token?client_id=o130mjub1zdhudq4brd8n5eeh0y99f&client_secret=fynlkfq6myoufsdygdjq5ptbcig1ed&grant_type=client_credentials"
ClientID = "o130mjub1zdhudq4brd8n5eeh0y99f"

def getOAtoken():
	#myHeaders = {'Client-ID':ClientID, 'client_secret': "fynlkfq6myoufsdygdjq5ptbcig1ed", 'grant_type': "client_credentials"}
	rs = requests.post(OA_URL)
	print(rs.json())
	token = rs.json()['access_token']
	print(token)
	return token

def RequestAPI(url,token):
    token = "Bearer " + token
    myHeaders = {'Client-ID' : ClientID, 'Authorization':token}
    while True:
        try:
            r = requests.get(url,headers = myHeaders, timeout=2)
        except Exception as e:
            print(e)
            time.sleep(5)
            continue
        else:
            if r.status_code == 200:
                res = r.json()
                break
            else:
                token = "Bearer " + getOAtoken()
                myHeaders = {'Client-ID' : ClientID, 'Authorization':token}
    return res

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
	token = getOAtoken()
	print("OAtoken: ", token)
	data = RequestAPI(Initialurl,token)
	info_list, cursor = generateURL_Ccursor(data)
	APIURL = Initialurl + "&after=" + cursor
	while True:
		#print("while")
		try:
			data = RequestAPI(APIURL,token)
		except:
			break
		else:
			#print(data)
			info_list, cursor = generateURL_Ccursor(data)
			APIURL = Initialurl + "&after=" + cursor
			#print(info_list)
			for item in info_list:
				counter = counter + 1
				#print("hi")
				print(counter)
				print(json.loads(item.decode('utf-8')))
			if counter == 100:
			#	print("Finish Twitch!")
				time.sleep(5)
			if counter >= 10000:
				break
	print("request num: ", counter)
	print("Excution time: ", (time.time()-start))
	

crawlerTwitch()
#getOAtoken()