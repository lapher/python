from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}                                            
path = "phantomjs-2.1.1-linux-x86_64/bin/phantomjs"
url = ('https://www.u-trust.com.tw/CaseBuy/House/')
web = webdriver.PhantomJS(path)

page_list=[]      
house={}          
house_list = []   



print("[網頁開啟 請稍候]")
web.get("http://rent.sinyi.com.tw/itemList.php/qnkyep")
print("[頁面擷取中]")
time.sleep(3)

leaf_first = [2,4,5,6]
for leaf in leaf_first:
    time.sleep(1)
    for i in web.find_elements_by_css_selector('#searchResult > ul >li'):
        x = i.find_element_by_css_selector("div.block > div.upper.clearfix > div > a").get_attribute('href')
        page_list.append(x)
    ll = '#searchResult > div.function > div > a:nth-child(%s)'%(leaf)
    web.find_element_by_css_selector(ll).click()
    print("Taipei Page first")

print(page_list)