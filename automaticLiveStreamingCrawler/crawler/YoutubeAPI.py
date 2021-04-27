#https://stackoverflow.com/questions/18804904/retrieve-all-videos-from-youtube-playlist-using-youtube-v3-api
# pip3 install google-api-python-client
import requests
import json
import time, random, datetime


DEVELOPER_KEY = []

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

playlistID_youtube = [ 
"PLU12uITxBEPFJGVb2zSgCaWvMBe7vHonB", # 直播 
"PLiCvVJzBupKlQ50jZqLas7SAztTMEYv1f", # 遊戲 
"PL8fVUTBmJhHJrxHg_uNTMyRmsWbFltuQV", # 運動 
"PL57quI9usf_sQMlMeQrUr5O_pCncZilx3", # 科技 
"PLIFqWCuxNyoiKKthaTBqjIH6m6A9INomt", # 動物 
"PLU12uITxBEPFnoOrc_w0oJL6CEeKRhpcb", # 行動應用程式 
"PLU12uITxBEPHvBRHoUt-fzKr8Iz1HpfUC", # 網路攝影機直播 
]

STREAM_URL = "https://www.googleapis.com/youtube/v3/"
#videos?id=
STREAM_MAX = "&maxResults=50"
STREAM_part = "&part=snippet,liveStreamingDetails"
STREAM_KEY = "&key=" + random.choice(DEVELOPER_KEY)


def fetch_all_youtube_videos(playlistId):
	firstURL = STREAM_URL + "playlistItems?&playlistId=" + playlistId + "&key=" + random.choice(DEVELOPER_KEY) + "&part=snippet"
	while True:
		res = requests.get(firstURL, timeout=2)
		if res.status_code == 200:
			res = res.json()
			break
		else:
			firstURL = STREAM_URL + "playlistItems?&playlistId=" + playlistId + "&key=" + random.choice(DEVELOPER_KEY) + "&part=snippet"
			print(firstURL)

	nextPageToken = res.get('nextPageToken')

	while ('nextPageToken' in res):
		APIURL = firstURL + "&pageToken=" + nextPageToken
		nextPage = requests.get(APIURL).json()
		#print(nextPage)
		if 'items' in nextPage:
			#print("hi")
			#print(nextPage['items'])
			res['items'] = res['items'] + nextPage['items']
		else:
			continue

		if 'nextPageToken' not in nextPage:
			res.pop('nextPageToken', None)
		else:
			nextPageToken = nextPage['nextPageToken']
	return res

def fetch_all_vediosID(res):
	videoID_list = []
	#count = 0
	for Key, Value in res.items():
		if Key == 'items':
			for data in Value:
				#count+= 1
				videoID = data['snippet']['resourceId']['videoId']
				videoID_list.append(videoID)
	#print(count)
	return videoID_list

#url = "https://www.googleapis.com/youtube/v3/videos?id=RaIJ767Bj_M&part=snippet,statistics&key=AIzaSyCIHZWjStQyFZsA9UaPPEC1HR72gy1_5M0"
def fetch_all_vediosInfo(videoID):
	url = STREAM_URL + "videos?id=" +videoID + STREAM_part + "&key=" + random.choice(DEVELOPER_KEY)
	while True:
		r = requests.get(url, timeout=2)
		if r.status_code == 200:
			break
		else:
			url = STREAM_URL + "videos?id=" +videoID + STREAM_part + "&key=" + random.choice(DEVELOPER_KEY)
			time.sleep(5)
	return (json.loads(r.text))
	
def generateInfo(data):
	info = {}
	try:
		info['Title'] = data['items'][0]['snippet']['title']
	except:
		info['Title'] = ""
	try:
		info['Description'] = data['items'][0]['snippet']['description']
	except:
		info['Description'] = ""
	info['Platform'] = "Youtube"
	try:
		info['VideoID'] = data['items'][0]['id']
	except:
		info['VideoID'] = ""
	try:
		info['Host'] = data['items'][0]['snippet']['channelTitle']
	except:
		info['Host'] = ""
	#info['Status'] = ""
	try:
		info['Thumbnails'] = data['items'][0]['snippet']['thumbnails']['default']['url']
	except:
		info['Thumbnails'] = ""
	try:
		info['Published'] = data['items'][0]['snippet']['publishedAt']
	except:
		info['Published'] = ""
	#if 'tags' in (data['items'][0]['snippet']).keys():
	try:
		tags = data['items'][0]['snippet']['tags']
		info['Tags'] = str(','.join(tags))
	except:
		info['Tags'] = ""
	info['Timestamp'] = str(datetime.datetime.now())[:-7]
	#info['ViewCount'] = data['items'][0]['statistics']['viewCount']
	try:
		info['Viewers'] = data['items'][0]['liveStreamingDetails']['concurrentViewers']
		info['ActualStartTime'] = data['items'][0]['liveStreamingDetails']['actualStartTime']
	except:
		pass
	info['VideoURL'] = "https://www.youtube.com/watch?v=" + info['VideoID']
	info['Channel'] = info['Host']
	#info['LikeCount'] = data['items'][0]['statistics']['likeCount']
	#info['DislikeCount'] = data['items'][0]['statistics']['dislikeCount']
	#info['CommentCount'] = data['items'][0]['statistics']['commentCount']
	info = json.dumps(info)
	return info
"""
def store_videoInfo(info):
	info = json.loads(info)
	#print(type(info))
	temp = [info['Platform'], info['VideoURL'], info['Title'], info['Host'], info['Timestamp']]
	key = str('_'.join(temp))

	r = redis.Redis(host = 'localhost', password='mwnlmwnl', port = 5487, decode_responses = True, db = 4)
	r.hmset(key, info)
	print("save!")	
"""

count = 0
start = time.time()
while True:
	#start = time.time()
	for playlistId in playlistID_youtube:
		videos = fetch_all_youtube_videos(playlistId)
		result = fetch_all_vediosID(videos)
		print(result)
		#count = 0
		for item in result:
			data = fetch_all_vediosInfo(item)
			data = generateInfo(data)
			if json.loads(data)['Title'] != "":
				count += 1
				print(count)
				print(json.loads(data))
			#store_videoInfo(data)
			if count%50 == 0:
				time.sleep(5)
			if count >= 10000:
				break
		time.sleep(10)
	#print(time.time()-start)
end = time.time()
print("Request num: ", count)
print("Excution time: ", (end-start))