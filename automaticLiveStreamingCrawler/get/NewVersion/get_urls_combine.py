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


content_list = []

def get_url(url):

	# tags = requests.get('http://localhost:3000/test?name=nodeDesired_ZQ&reget=no')
	# tags = json.loads(fp.readline())

	fp = open("nodeDesired_HY.txt", "r")
	tags = json.loads(fp.readline())
	fp.close()
	print(tags["block"])

	count = 0

	driver = webdriver.Chrome()
	driver.get(url)
	time.sleep(5)

	aList = driver.find_elements_by_css_selector("a")
	if len(aList)>300:
		lastPage = ""
		page = 2
		while True:
			aList = driver.find_elements_by_css_selector("a")
			# for i in aList:
			# 	print(i.text)
			
			
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
				# print(tempDict)
				content_list.append(tempDict)
				count += 1
			# print(content_list)
			# i = len(aList)-1
			for i in aList[::-1]:
				print(i.text)
				if lastPage == "":
					try:
						int(i.text)
						lastPage = int(i.text)
					except ValueError:
						continue
				print(i.text+str(page))
				if i.text == str(page):
					i.click()
					time.sleep(5)
					page += 1
					break
				

			count+=1
			# print("page:"+aList[i].text)
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


get_url(URL_HY)


