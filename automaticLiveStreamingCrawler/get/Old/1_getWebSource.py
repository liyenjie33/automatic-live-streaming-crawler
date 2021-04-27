from selenium import webdriver
from pyvirtualdisplay import Display
import time, json
from bs4 import BeautifulSoup

# display = Display(visible=0, size=(1280, 1080))
# display.start()
print('display success!')
#platform = input('enter url:')

driver = webdriver.Chrome()
driver.get('https://www.huomao.com/channel/all')
time.sleep(10)
#print(driver.page_source)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

htmlFile = 'html_example.txt'
fp = open(htmlFile, "w")
fp.write(str(soup))
fp.close()

driver.quit()