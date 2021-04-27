from selenium import webdriver
from pyvirtualdisplay import Display
import time, random, json
import threading
from seleniumwire import webdriver as Webdriver
from urllib.parse import unquote
from urllib.parse import urlparse


#SCROLL_PAUSE_TIME = 3

# display = Display(visible=0, size=(1920, 1080))
# display.start()

keyHtml = {
	"https://www.douyu.com/directory/all":"nodeDesired_DY", 
	"https://live.bilibili.com/all":"nodeDesired_BL",
	"https://www.huya.com/l":"nodeDesired_HY",
	"https://www.zhanqi.tv/lives":"nodeDesired_ZQ",
	"https://www.huajiao.com/category/1000":"nodeDesired_HJ",
	"https://egame.qq.com/livelist":"nodeDesired_EG",
	"http://www.inke.cn/hotlive_list.html":"nodeDesired_IK"
}

URL_ZQ = "https://www.zhanqi.tv/lives"
URL_BL = "https://live.bilibili.com/all"
URL_DY = "https://www.douyu.com/directory/all"
URL_HY = "https://www.huya.com/l"
URL_HJ = "https://www.huajiao.com/category/1000"
URL_EG = "https://egame.qq.com/livelist"


content_list = []

seleniumList = ["https://www.huya.com/l"]
ajaxList = []

class seleniumDriver:
	def __init__(self):
		self.driver = Webdriver.Chrome()

	def request(self, url):
		#self.driver.implicitly_wait(2)
		self.driver.get(url)
		self.driver.refresh()
		time.sleep(1)

	def actionScroll(self, num):
		for i in range(1, num):
			try:
				self.driver.execute_script('window.scrollTo(0,document.documentElement.scrollHeight);')
			except:
				continue
			else:
				time.sleep(random.randint(1, 3))

	def actionNextPage(self, page):
		location = self.driver.find_elements_by_tag_name("a")
		for tag in range(len(location)-3, -1, -1):
			try:
				#print(location[tag].text)
				int(location[tag].text)
			except:
				continue
			else:
				#print(location[tag].text)
				if int(location[tag].text) == page:
					location[tag].click()
					time.sleep(3)
					break
	def _close(self):
		self.driver.close()

	def getURL(self):
		result = []
		for request in self.driver.requests:
			if request.response:
				try:
					resHeader = request.response.headers['Content-Type']
				except:
					continue
				else:
					#result.append(unquote(request.path, 'utf-8'))
					
					if "text/html" in request.response.headers['Content-Type']:
						#print(
						#		unquote(request.path, 'utf-8'),
						#		request.response.status_code,
						#		request.response.headers['Content-Type']
						#		)
						result.append(unquote(request.path, 'utf-8'))
					elif "application/json" in request.response.headers['Content-Type']:
						#print(
						#	unquote(request.path, 'utf-8'),
						#	request.response.status_code,
						#	request.response.headers['Content-Type']
						#	)
						result.append(unquote(request.path, 'utf-8'))
					
		return result


def cmpBA(contentB, contentA):
	result = []
	for diff in set(contentA).symmetric_difference(set(contentB)):
		#print(diff)
		result.append(diff)
	return result

def cmpRe(content):
	resultDic = {}
	result = []
	for url in content:
		resultDic.setdefault(urlparse(url).path,[]).append(url)
	for path in resultDic:
		if len(resultDic[path]) > 1:
			if len(resultDic[path]) < 5:
				#print(resultDic[path])
				result.append(resultDic[path])
	#print(result)
	if len(result) == 1:
		result = result[0]
		return result
	else:
		return []

def check(content):
	result = []
	for url in content:
		#print(url)
		try:
			rs = requests.get(url)
		except:
			continue
		else:
			try:
				data = rs.json()
				data = data['data']
			except:
				pass
			else:
				if isinstance(data, list):
					if len(data) >= 10:
						#print(url)
						result.append(url)
						#return result
				else:
					for key in data:
						if isinstance(data[key], list):
							if len(data[key]) >= 10:
								#print(url)
								result.append(url)
								#return result
	return result

def generateURL(ajaxs):
	URL = {}
	# check URL type
	if 'page' in ajaxs:
		try:
			url = re.search(r'\S+page=',ajaxs, flags=re.DOTALL | re.MULTILINE).group()
			print(url)
		except:
			pass
		else:
			URL['url'] = url
			URL['type'] = "page"

	elif 'num' in ajaxs:
		URL['url'] = ajaxs
		URL['type'] = "num"

	elif '.json' in ajaxs:
		try:
			URL['url'] = re.search(r'\S+/',ajaxs, flags=re.DOTALL | re.MULTILINE).group()
			URL['type'] = ".json"
		except:
			pass

	# handle parse rule
	try:
		rs = requests.get(ajaxs)
	except:
		pass
	else:
		if (rs.status_code) == 200:
			try:
				data = rs.json()
				data = data['data']
			except:
				pass
			else:
				if isinstance(data, list):
					URL['parse'] = []
				else:
					for key in data:
						if isinstance(data[key], list):
							URL.setdefault('parse',[]).append(key)
	print(URL)
	return json.dumps(URL)

def searchAjax(url):
	browser = seleniumDriver()
	browser.request(url)
	before = browser.getURL()
	print(len(before))
	try:
		browser.actionScroll(3)
	except:
		pass
	try:
		browser.actionNextPage(2)
		browser.actionNextPage(3)
	except:
		pass
	after = browser.getURL()
	browser._close()
	print(len(after))

	result = cmpBA(before, after)
	print("前後比對：\n", result)
	ajaxURLs = cmpRe(result)
	print("path\n", ajaxURLs)
	#ajaxURL = generateURL(ajaxURLs)
	if ajaxURLs:
		#print("Yes", ajaxURLs[0])
		ajaxURL = generateURL(ajaxURLs[0])
		if ("type" in json.loads(ajaxURL).keys()) & ("parse" in json.loads(ajaxURL).keys()):
			print("Yes", ajaxURL)
			#ajaxCrawler(ajaxURL)
			ajaxList.append(ajaxURL)
		else:
			print("No", url)
			seleniumList.append(url)

	else:
		ajaxURLs = check(result)
		print("內容\n", ajaxURLs)
		if ajaxURLs:
			#print("Yes", ajaxURLs)
			for item in ajaxURLs:
				ajaxURL = generateURL(item)
				if ("type" in json.loads(ajaxURL).keys()) & ("parse" in json.loads(ajaxURL).keys()):
					print("Yes", ajaxURL)
					#ajaxCrawler(ajaxURL)
					ajaxList.append(ajaxURL)
				else:
					print("No", url)
					seleniumList.append(url)
		else:
			print("No", url)
			seleniumList.append(url)

def ajaxCrawler():
	while True:
		if ajaxList != []:
			for url in ajaxList:
				url = json.loads(url)
				headers = {
				"User-Agent":"Mozilla/5.0 (X11; Linux armv7l; rv:60.0) Gecko/20100101 Firefox/60.0"
				}
				page = 1
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
									print(item)
								page += 1
							else:
								break
					except:
						continue

def mainAjax():
	platformList = []
	while True:
		with open('platform.json', 'rt') as f:
			platform = f.read()
			f.close()
		platform = json.loads(platform)['platform']
		platform = list(set(platform).difference(set(platformList)))
		print(platform)
		if platform:
			for url in platform:
				searchAjax(url)
				platformList.append(url)

		else:
			time.sleep(300)


def seleniumCrawler():
	global seleniumList
	
	while True:
		if seleniumList != []:
			driver = webdriver.Chrome()
			for url in seleniumList:
				# tags = requests.get('http://localhost:3000/test?name=nodeDesired_ZQ&reget=no')
				# tags = json.loads(fp.readline())
				global keyHtml
				fp = open(keyHtml[url]+".txt", "r")
				tags = json.loads(fp.readline())
				fp.close()
				# print(tags["block"])

				count = 0

				
				driver.get(url)
				time.sleep(random.randint(1,3))
				aList = []
				aList = driver.find_elements_by_css_selector("a")
				print(len(aList)-1)
				if len(aList)>300:
					lastPage = ""
					page = 2
					while True:
						aList = driver.find_elements_by_css_selector("a")
						i = len(aList)-1
						
						results = driver.find_elements_by_css_selector("."+tags["block"])
				    
						for target in results:
							tempDict = {}
							for category in tags:
								if category =="block":
									continue
								else:
									tag = tags[category]
									if len(tag)>2:
										goal = "_".join(tag[0:len(tag)-1])
									else:
										goal = tag[0]

									goal = goal.replace(",", ".")
									if goal[-1:]==".":
										goal = goal[:-1]
									goalBlock = target.find_element_by_css_selector("."+goal)
									if tag[len(tag)-1] == 'text':
										content = goalBlock.text
									else:
										content = goalBlock.get_attribute(tag[len(tag)-1])

									tempDict[category] = content
							content_list.append(tempDict)
							count += 1

						while(i>=0):
							print(aList[i].text)
							if lastPage == "":
								try:
									int(aList[i].text)
									lastPage = int(aList[i].text)
								except ValueError:
									continue
							if aList[i].text == str(page):
								aList[i].click()
								time.sleep(5)
								page += 1
								break
							i -= 1

						count+=1
						print("page:"+aList[i].text)
						print(len(aList)-1)
						print(i)
						if page == 5:
							break
				else:


				
					driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
					last_height = driver.execute_script("return document.body.scrollHeight")
					while True:
						# Scroll down to bottom
						driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
						# Wait to load page
						time.sleep(random.randint(1,3))
						# Calculate new scroll height and compare with last scroll height
						new_height = driver.execute_script("return document.body.scrollHeight")
						if new_height == last_height:
							break
						last_height = new_height
					
					# r = requests.get('https://www.google.com.tw/')
					results = driver.find_elements_by_css_selector("."+tags["block"])
				    
					for target in results:
						tempDict = {}
						for category in tags:
							if category =="block":
								continue
							else:
								tag = tags[category]
								if len(tag)>2:
									goal = "_".join(tag[0:len(tag)-1])
								else:
									goal = tag[0]

								goal = goal.replace(",", ".")
								goalBlock = target.find_element_by_css_selector("."+goal)
								if tag[len(tag)-1] == 'text':
									content = goalBlock.text
								else:
									content = goalBlock.get_attribute(tag[len(tag)-1])

								tempDict[category] = content
						content_list.append(tempDict)
						count += 1

				print(content_list)
				print(count)
				# driver.close()
		else:
			continue


ts = threading.Thread(target = seleniumCrawler)
ta = threading.Thread(target = ajaxCrawler)

ts.start()
ta.start()

mainAjax()
