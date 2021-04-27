import time, random
import requests
import json

def ajaxCrawler(url):
	url = json.loads(url)
	headers = {
	"User-Agent":"Mozilla/5.0 (X11; Linux armv7l; rv:60.0) Gecko/20100101 Firefox/60.0"
	}
	page = 1
	num = 0
	while True:
		if url['type'] == "page":
			try:
				rs = requests.get(url['url']+str(page), headers=headers, timeout=2)
			except Exception as e:
				print(e)
				time.sleep(5)
				continue
		elif url['type'] == "num":
			try:
				rs = requests.get(url['url'], headers=headers, timeout=2)
			except Exception as e:
				print(e)
				time.sleep(5)
				continue
		elif url['type'] == ".json":
			try:
				rs = requests.get(url['url']+str(page)+".json", headers=headers, timeout=2)
			except Exception as e:
				print(e)
				time.sleep(5)
				continue
		try:
			if (rs.status_code) == 200:
				data = rs.json()
				data = data['data']
				if len(url['parse']) != 0:
					for i in range(0, len(url['parse'])):
						tag = url['parse'][i]
						liveData = data[tag]
				else:
					liveData = data

				if len(liveData):
					for item in liveData:
						num += 1
						print(num)
						print(item)
					page += 1
				else:
					page = 1
					continue
			if num >= 10000:
				break
		except:
			continue
	return num



huya = {'parse': ['datas'], 'type': 'page', 'url': 'https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&tagAll=0&page='}
bili = {"url": "https://api.live.bilibili.com/room/v1/room/get_user_recommend?page=", "parse": [], "type": "page"}
zhanqi = {"type": ".json", "url": "https://www.zhanqi.tv/api/static/v2.1/live/list/20/", "parse": ["rooms"]}

start = time.time()
num = ajaxCrawler(json.dumps(zhanqi))
end = time.time()

print("Request num: ", num)
print("Excution time: ", str(end-start))