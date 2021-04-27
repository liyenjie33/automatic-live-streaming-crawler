#coding:utf-8
from selenium import webdriver
from pyvirtualdisplay import Display
import time, json
from bs4 import BeautifulSoup

# display = Display(visible=0, size=(1280, 1080))
# display.start()
print('display success!')

driver = webdriver.Chrome()
driver.get("https://www.huomao.com/channel/all")
time.sleep(5)
#print(driver.page_source)

html = driver.page_source

# fp = open("douyuhtml2.txt", "w")
# fp.write(html)
# fp.close()
#driver.save_screenshot(driver.title+".png")

soup = BeautifulSoup(html, 'html.parser')
# print(soup.prettify())

fp = open('finalKey_HM.txt', "r")
line = fp.readline()
while line:
    LINE = line
    line = fp.readline()
fp.close()

LINE = json.loads(LINE)
for i in LINE:
	first = i
	break

channels = driver.find_elements_by_css_selector("."+first)



info1 = {}
info2 = {}
count = 0
for channel in channels:
	print(str(channel))
	count = count+1
	if count < 16 and count > 13:
		if count == 14:
			for tag in LINE:
				if tag == first:
					continue
				else:
					name = tag
					TAG = tag
					if tag.find(",") != -1:
						TAG = tag.replace(",", ".")
					temp = channel.find_elements_by_css_selector("."+TAG)
					for content in LINE[tag]:
						if content == 'text':
							TEXT = ''
							try:
								TEXT = temp[0].text
							except:
								continue
							info1[name+'_'+content] = TEXT
						else:
							attr = ''
							try:
								attr = temp[0].get_attribute(content)
							except:
								continue
							info1[name+'_'+content] = attr
		if count == 15:
			for tag in LINE:
				if tag == first:
					continue
				else:
					name = tag
					TAG = tag
					if tag.find(",") != -1:
						TAG = tag.replace(",", ".")
					temp = channel.find_elements_by_css_selector("."+TAG)
					for content in LINE[tag]:
						if content == 'text':
							TEXT = ''
							try:
								TEXT = temp[0].text
							except:
								continue
							info2[name+'_'+content] = TEXT
						else:
							attr = ''
							try:
								attr = temp[0].get_attribute(content)
							except:
								continue
							info2[name+'_'+content] = attr
	elif count <= 13:
		continue
	else:
		break


for i in list(info1):
	if info1[i] == info2[i]:
		del info1[i]
	elif info1[i].find('\n') != -1:
		del info1[i]
	else:
		continue

CT = []
for i in list(info1):
	if info1[i] not in CT:
		CT.append(info1[i])

	else:
		del info1[i]

print(info1)

config = {}
count = 0

for i in info1:
	# print(i)
	count = count+1
	if info1[i].find('http') != -1:
		if info1[i].find('jpg') != -1 or info1[i].find('png') != -1 or info1[i].find('JPG') != -1 or info1[i].find('PNG') != -1:
			# print('image:'+str(count))
			tag = i.split('_')
			config['image'] = str(tag)
		else:
			# print('url:'+str(count))
			tag = i.split('_')
			config['url'] = str(tag)

	elif info1[i].find('万') != -1 or info1[i].isdigit():
		# print('viewer:'+str(count))
		tag = i.split('_')
		config['viewer'] = str(tag)

	elif i.find('title') != -1 or i.find('TITLE') != -1 or i.find('Title') != -1 or i.find('intro') != -1 or i.find('room-name') != -1 or i.find('alt') != -1:
		# print('title:'+str(count))
		tag = i.split('_')
		config['title'] = str(tag)

	elif i.find('user') != -1 or i.find('username') != -1 or i.find('uname') != -1 or i.find('avatar') != -1:
		# print('host:'+str(count))
		tag = i.split('_')
		config['host'] = str(tag)

	elif i.find('zone') != -1 or i.find('type') != -1:
		# print('category:'+str(count))
		tag = i.split('_')
		config['category'] = str(tag)

	else:
		# print('else:'+str(count))
		tag = i.split('_')
		config[i] = str(tag)

	# print('1round:'+str(count))

print()
print(config)




driver.quit()




# link2_tag = soup.find_all(class_=first)
# print(link2_tag[0])
# print(link2_tag[1])

# print(soup.select())




