from selenium import webdriver
from pyvirtualdisplay import Display
import time, random, json
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

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

	# display = Display(visible=0, size=(1920, 1080))
	# display.start()

	driver = webdriver.Chrome()
	driver.implicitly_wait(10)
	# while count<10000:
	driver.get(url)
	driver.refresh()
	# while True:
	# 	try:
	# 		element = WebDriverWait(driver, 10).until(
	# 			EC.visibility_of_element_located((By.CSS_SELECTOR, "."+tags["block"]))
	# 		)
	# 		time.sleep(3)
	# 		break
	# 	except:
	# 		print('hi')
	# 		continue
	WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
	time.sleep(3)
		

	aAList = driver.find_elements_by_css_selector("a")
	print(len(aAList))
	for Q in aAList[::-1]:

		if Q.text=="下一页" or Q.text=="下一页>" or len(aAList)>300:
			lastPage = 0
			page = 2
			while True:
					
				# aList = driver.find_elements_by_css_selector("a")
				# i = len(aList)-1
					
					
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
				# 	# content_list.append(tempDict)
					count += 1
				# # print(content_list)
				# # i = len(aList)-1
				print(count)
				if page == 1:
					break
				tempError = 0
				while True:
					try:
						islastPage = 0
						aList = driver.find_elements_by_css_selector("a")
						for i in aList[::-1]:
							# print(i.text)
							if islastPage == 0:
								try:
									int(i.text)
									lastPage = int(i.text)
									islastPage = 1
								except ValueError:
									continue
							print(i.text+">>"+str(page))
							if i.text == str(page):
								#i.click()
								ActionChains(driver).move_to_element(i).click(i).perform()
								# while True:
								# 	try:
								# 		element = WebDriverWait(driver, 10).until(
								# 			EC.visibility_of_element_located((By.CSS_SELECTOR, "."+tags["block"]))
								# 		)
								# 		time.sleep(3)
								# 		break
								# 	except:
								# 		continue
								# driver.refresh()
								WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
								time.sleep(5)
								page += 1
								break
						break
					except Exception as e:
						tempError+=1
						print(e)
						if tempError>=3:
							break
						else:
							continue
				if tempError>=3 or page%10 == 0:
					driver.quit()
					driver = webdriver.Chrome()
					driver.implicitly_wait(10)
					driver.get(url)
					driver.refresh()
					WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
					time.sleep(3)
					while True:
						maxPage = 0
						maxPageNum = 0
						islastPage = 0
						aList = driver.find_elements_by_css_selector("a")
						for i in aList[::-1]:
							print('>>>>>>>>'+i.text+'<')
							if islastPage == 0:
								try:
									int(i.text)
									lastPage = int(i.text)
									islastPage = 1
								except ValueError:
									continue
							else:
								if i.text == str(page):
									maxPageNum = int(i.text)
									maxPage = i
									ActionChains(driver).move_to_element(maxPage).click(maxPage).perform()
									WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
									time.sleep(5)
									break
								else:
									notdigit = 0
									if (i.text).isdigit():
										if int(i.text)>maxPageNum:
											if int(i.text)>page:
												continue
											else:
												maxPageNum = int(i.text)
												maxPage = i
												break
									# 	else:
									# 		continue
									# else:
									# 	if notdigit >=5:
									# 		break
									
						if maxPageNum == page:
							break
						else:
							ActionChains(driver).move_to_element(maxPage).click(maxPage).perform()
							WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
							time.sleep(5)
							

				count+=1
				# if count >= 10000:
				# 	break
				# print("page:"+aList[i].text)
				print("lastPage:"+str(lastPage))
				if page >= lastPage+1:
				# # if page == 100:
					page = 1
				
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
			else:
				countScroll = 0
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
	# f = open('HY_testDataWait.txt', 'w')
	# f.write(tempList)
	# f.close()
	print(count)
	# driver.close()
	# return count
	

tStart = time.time()
# channelNum = 0
# while channelNum<10000:
seleniumCrawler(URL_DY)

tEnd = time.time()
print (tEnd - tStart)


