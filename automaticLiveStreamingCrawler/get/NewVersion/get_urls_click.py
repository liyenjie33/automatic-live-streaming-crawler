from selenium import webdriver
from pyvirtualdisplay import Display
import time, random


#SCROLL_PAUSE_TIME = 3

# display = Display(visible=0, size=(1920, 1080))
# display.start()


URL_ZQ = "https://www.zhanqi.tv/lives"
URL_BL = "https://live.bilibili.com/all"
URL_DY = "https://www.douyu.com/directory/all"
URL_HY = "https://www.huya.com/l"


titleList = []

def get_url(url):

	ct = 0

	driver = webdriver.Chrome()
	driver.get(url)
	time.sleep(5)
	
	# count = 2
	lastPage = ""
	page = 2
	while True:
		aList = driver.find_elements_by_css_selector("a")
		i = len(aList)-1
		
		result = []
		result = driver.find_elements_by_css_selector(".DyListCover-intro")
		# ct += 1
		for target in result:
			titleList.append(target.text)
		# if ct == 2:
		# 	break

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

		# count = count+1
		print("page:"+aList[i].text)
		print(len(aList)-1)
		print(i)
		if page == lastPage+1:
			break
		
	# print(titleList)
	# print(len(titleList))
	# print(lastPage)

	# driver.close()

get_url(URL_DY)
while True:
	continue