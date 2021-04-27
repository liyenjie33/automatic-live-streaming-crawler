from selenium import webdriver
from pyvirtualdisplay import Display
import time, random, json
# import requests


#SCROLL_PAUSE_TIME = 3

# display = Display(visible=0, size=(1920, 1080))
# display.start()

URL_ZQ = "https://www.zhanqi.tv/lives"
URL_BL = "https://live.bilibili.com/all"
URL_DY = "https://www.douyu.com/directory/all"
URL_HY = "https://www.huya.com/l"
URL_HJ = "https://www.huajiao.com/category/1000"
URL_EG = "https://egame.qq.com/livelist"
URL_IK = "http://www.inke.cn/hotlive_list.html"
URL_MX = "https://mixer.com/browse/all"


content_list = []

def seleniumCrawler(url):

	# tags = requests.get('http://localhost:3000/test?name=nodeDesired_ZQ&reget=no')
	# tags = json.loads(fp.readline())

	fp = open("nodeDesired_DY.txt", "r")
	tags = json.loads(fp.readline())
	fp.close()
	print(tags["block"])

	count = 0

	driver = webdriver.Chrome()
	driver.get(url)
	time.sleep(3)

	aAList = driver.find_elements_by_css_selector("a")
	print(len(aAList))
	for Q in aAList[::-1]:

		if Q.text=="下一页" or Q.text=="下一页>" or len(aAList)>300:
			lastPage = 0
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
							try:
								goalBlock = target.find_element_by_css_selector("."+goal)
							except:
								goalBlock = ""
							if tag[len(tag)-1] == 'text':
								try:
									content = goalBlock.text
								except:
									content = ""
							else:
								try:
									content = goalBlock.get_attribute(tag[len(tag)-1])
								except:
									content = ""

							tempDict[category] = content
					print(tempDict)
					content_list.append(tempDict)
					count += 1
				# print(content_list)
				# i = len(aList)-1
				if page == lastPage+1 :
				# if page == 100:
					break
				print(aList[::-1])
				for i in aList[::-1]:
					print(i.text)
					if lastPage == 0:
						try:
							int(i.text)
							lastPage = int(i.text)
						except ValueError:
							continue
					print(i.text+str(page))
					if i.text == str(page):
						i.click()
						time.sleep(3)
						page += 1
						break
					

				count+=1
				# print("page:"+aList[i].text)
				print("lastPage:"+str(lastPage))
				# if page == lastPage+1:
				# # if page == 100:
				# 	break
			break

	if Q==aAList[0]:

		countScroll = 0
		
		driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
		last_height = driver.execute_script("return document.body.scrollHeight")
		# WWW = 4
		# while WWW>0:
		while True:
			# Scroll down to bottom
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			# Wait to load page
			time.sleep(random.randint(1,3))
			# Calculate new scroll height and compare with last scroll height
			new_height = driver.execute_script("return document.body.scrollHeight")
			if new_height == last_height:
				countScroll+=1
				if countScroll == 3:
					break
				else:
					continue
			last_height = new_height
			# WWW-=1
		
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
					if goal[-1:]==".":
						goal = goal[:-1]

					try:
						goalBlock = target.find_element_by_css_selector("."+goal)
					except:
						goalBlock = ""
					if tag[len(tag)-1] == 'text':
						try:
							content = goalBlock.text
						except:
							content = ""
					else:
						try:
							content = goalBlock.get_attribute(tag[len(tag)-1])
						except:
							content = ""

					tempDict[category] = content
			print(tempDict)
			content_list.append(tempDict)
			count += 1

	# print(content_list)
	tempList = []
	tempList = json.dumps(content_list)
	# print(tempList)
	f = open('DY_testData.txt', 'w')
	f.write(tempList)
	f.close()
	print(count)
	# driver.close()


seleniumCrawler(URL_DY)


