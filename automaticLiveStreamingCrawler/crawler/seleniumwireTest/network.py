# https://github.com/wkeeling/selenium-wire
# module path: ~/.local/lib/python3.5/site-packages
from seleniumwire import webdriver
import time
import random
from urllib.parse import unquote
from urllib.parse import urlparse
import requests
import difflib
import json
import re


class seleniumDriver:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def request(self, url):
        # self.driver.implicitly_wait(2)
        self.driver.get(url)
        self.driver.refresh()
        time.sleep(1)

    def actionScroll(self, num):
        for i in range(1, num):
            try:
                self.driver.execute_script(
                    'window.scrollTo(0,document.documentElement.scrollHeight);')
            except:
                continue
            else:
                time.sleep(random.randint(1, 3))

    def actionNextPage(self, page):
        location = self.driver.find_elements_by_tag_name("a")
        for tag in range(len(location)-3, -1, -1):
            try:
                print(location[tag].text)
                int(location[tag].text)
            except:
                continue
            else:
                print(location[tag].text)
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
                    # result.append(unquote(request.path, 'utf-8'))

                    if "text/html" in request.response.headers['Content-Type']:
                        # print(
                        #		unquote(request.path, 'utf-8'),
                        #		request.response.status_code,
                        #		request.response.headers['Content-Type']
                        #		)
                        # print(request.url)
                        #result.append(unquote(request.path, 'utf-8'))
                        result.append(unquote(request.url, 'utf-8'))
                    elif "application/json" in request.response.headers['Content-Type']:
                        # print(
                        #	unquote(request.path, 'utf-8'),
                        #	request.response.status_code,
                        #	request.response.headers['Content-Type']
                        #	)
                        print(request.url)
                        #result.append(unquote(request.path, 'utf-8'))
                        result.append(unquote(request.url, 'utf-8'))

        return result


def cmpBA(contentB, contentA):
    result = []
    for diff in set(contentA).symmetric_difference(set(contentB)):
        # print(diff)
        result.append(diff)
    return result


def cmpRe(content):
    resultDic = {}
    result = []
    for url in content:
        resultDic.setdefault(urlparse(url).path, []).append(url)
    for path in resultDic:
        if len(resultDic[path]) > 1:
            if len(resultDic[path]) < 5:
                # print(resultDic[path])
                result.append(resultDic[path])
    # print(result)
    if len(result) == 1:
        result = result[0]
        return result
    else:
        return []


def check(content):
    result = []
    for url in content:
        # print(url)
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
                        # print(url)
                        result.append(url)
                        # return result
                else:
                    for key in data:
                        if isinstance(data[key], list):
                            if len(data[key]) >= 10:
                                # print(url)
                                result.append(url)
                                # return result
    return result


def generateURL(ajaxs):
    URL = {}
    # check URL type
    if 'page' in ajaxs:
        try:
            url = re.search(r'\S+page=', ajaxs,
                            flags=re.DOTALL | re.MULTILINE).group()
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
            URL['url'] = re.search(
                r'\S+/', ajaxs, flags=re.DOTALL | re.MULTILINE).group()
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
                            URL.setdefault('parse', []).append(key)
    print(URL)
    return json.dumps(URL)
    """
  url1 = urlparse(ajaxs[0])
  url2 = urlparse(ajaxs[1])
  if url1.params != url2.params:
    for i in range(0, len(url1.params)):
      if url1.params[i] != url2.params[i]:
        try:
          int(url1.params[i])
        except:
          pass
        else:
          URL.setdefault('int',[]).append(i)
  """


def ajaxCrawler(url):
    url = json.loads(url)
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux armv7l; rv:60.0) Gecko/20100101 Firefox/60.0"
    }
    page = 1
    while True:
        if url['type'] == "page":
            try:
                rs = requests.get(url['url']+str(page),
                                  headers=headers, timeout=2)
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
                rs = requests.get(url['url']+str(page) +
                                  ".json", headers=headers, timeout=2)
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
    print(after)

    result = cmpBA(before, after)
    print("前後比對：\n", result)
    ajaxURLs = cmpRe(result)
    print("path\n", ajaxURLs)
    # ajaxURL = generateURL(ajaxURLs)
    if ajaxURLs:
        # print("Yes", ajaxURLs[0])
        ajaxURL = generateURL(ajaxURLs[0])
        if ("type" in json.loads(ajaxURL).keys()) & ("parse" in json.loads(ajaxURL).keys()):
            print("Yes", ajaxURL)
            ajaxCrawler(ajaxURL)
        else:
            print("No", url)

    else:
        ajaxURLs = check(result)
        print("內容\n", ajaxURLs)
        if ajaxURLs:
            # print("Yes", ajaxURLs)
            for item in ajaxURLs:
                ajaxURL = generateURL(item)
                if ("type" in json.loads(ajaxURL).keys()) & ("parse" in json.loads(ajaxURL).keys()):
                    print("Yes", ajaxURL)
                    ajaxCrawler(ajaxURL)
                else:
                    print("No", url)
        else:
            print("No", url)


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
            time.sleep(10)


searchAjax("https://www.huya.com/l")

# url = generateURL(['https://api.live.bilibili.com/room/v1/room/get_user_recommend?page=2', 'https://api.live.bilibili.com/room/v1/room/get_user_recommend?page=3'])
# ajaxCrawler(json.loads(url))
