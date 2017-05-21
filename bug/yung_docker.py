# 設定
import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import pymongo
import time

tStart = time.time()
HOST = "https://buy.yungching.com.tw"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}   
url = "https://buy.yungching.com.tw/region/住宅_p/台北市-_c/?pg={}"
url2 = "https://buy.yungching.com.tw/region/住宅_p/新北市-_c/?pg={}"
res= requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'lxml')

page_list=[]     # 房子頁面
house={}         # 各間房子
house_list = []  # 全部房子
# 取個房子頁面
# range(1,全部頁面+1)
#限台北市
print("[頁面擷取中]")
for x in range(1,3):
    page = url.format(x)
    res= requests.get(page, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    a =soup.select("body > main > div.l-main-list > ul > li > a ")
    print("Taipei Page" + str(x))
    for c in a:
        full=[]
        hou =c['href']
        page_house = HOST+ hou
        full.append(page_house)
        pic = c.select("img")[0]['src']
        full.append(pic)
        page_list.append(full)
        time.sleep(10)


#計時        
print("[頁面擷取 完成]")
tEnd = time.time()
print ("It cost %f sec" % (tEnd - tStart))


# 取細項
print("[資料爬取中]")
tStart1 = time.time()
suma = 0
sume = 0
total = len(page_list)
for urls in page_list:
    res = requests.get(urls[0], headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    c = soup.select("body > main")
    for b in c:
        time.sleep(1)
        try:
            house['web'] = "yung"
            house['road'] = b.select("section.m-house-infomation > div.m-house-infos.right > div.m-info-house > div.left > div.house-info-addr")[0].text
            house["city"] = b.select("section.m-house-infomation > div.m-house-infos.right > div.m-info-house > div.left > div.house-info-addr")[0].text.split("區")[0].split("市")[1] + "區" 
            house["sec"] = b.select("section.m-house-infomation > div.m-house-infos.right > div.m-info-house > div.left > div.house-info-addr")[0].text.split("市")[0] + "市"       
            house['type'] = b.select("section.m-house-infomation > div.m-house-infos.right > div.m-house-info-wrap > div > div > span")[2].text
            if len(b.select("section.m-house-detail-block.detail-data > section.m-house-detail-list.bg-square > ul > li.right")[0].text.split('含車位')) != len(c):
                house['csize'] = b.select("section.m-house-detail-block.detail-data > section.m-house-detail-list.bg-square > ul > li.right")[0].text.split('含車位')[1].split('坪')[0]
            else:
                house['csize']= '0'
            house['lsize'] = b.select("section.m-house-detail-block.detail-data > section.m-house-detail-list.bg-square > ul > li.left")[0].text.split('土地坪數：')[1].split('坪')[0]                
            house['hsize'] = b.select("section.m-house-infomation > div.m-house-infos.right > div.m-house-info-wrap > div > div > span")[0].text.split()[1].split("坪")[0]        
            othersize = b.select("section.m-house-detail-block.detail-data > section.m-house-detail-list.bg-square > ul > li.right > ul > li")        
            dx=[]
            for i in othersize:
                x = i.text.split()[0]
                dx.append(x)
                st=''
                for j in dx:
                    st += (j+',')
            house['osize'] = st
            house['year' ]= b.select("section.m-house-infomation > div.m-house-infos.right > div.m-house-info-wrap > div > div > span")[1].text.split('年')[0]
            house['upfloor'] = b.select("section.m-house-infomation > div.m-house-infos.right > div.m-house-info-wrap > div > div > span")[3].text.split('/')[1].split('樓')[0] 
            house['floor'] = b.select("section.m-house-infomation > div.m-house-infos.right > div.m-house-info-wrap > div > div > span")[3].text.split('~')[0]
            #house['pattern'] = b.select("section.m-house-infomation > div.m-house-infos.right > div.m-house-info-wrap > div > div ")[1].text
            house['room'] = b.select("section.m-house-infomation > div.m-house-infos.right > div.m-house-info-wrap > div > div ")[1].text.split("房(室)")[0]    
            house['hall'] = b.select("section.m-house-infomation > div.m-house-infos.right > div.m-house-info-wrap > div > div ")[1].text.split("房(室)")[1].split("廳")[0]    
            house['bathroom'] = b.select("section.m-house-infomation > div.m-house-infos.right > div.m-house-info-wrap > div > div ")[1].text.split("廳")[1].split("衛")[0]
            house['price'] = b.select("section.m-house-infomation > div.m-house-infos.right > div.m-info-house > div.house-info-prices.right > em > span")[0].text              
            house['avgprice'] = ""
            other = b.select("section.m-house-detail-block.detail-data > section.m-house-detail-list.bg-other.last > div > ul > li")           
            dx2=[]
            for i2 in other:
                x2 = i2.text.split()[0]
                dx2.append(x2)
                st2=''
                for j2 in dx2:
                    st2 +=(j2+',')
            house['other'] = st2
            info = soup.select("body > main > section.m-house-detail-block.text-info > dir")[0].text.split()  
            stinfo=""
            for i3 in info:
                stinfo += i3
            house['intro'] = stinfo
            house['pic'] = urls[1]
            house_list.append(house)
            suma += 1
            print("[目前進度]  " + str(suma) +"/" + str(total) + "  錯誤: " +str(sume))
            
        except:
            sume += 1
            print("[BUG PAGE]" + urls[0])
#計時            
print("[資料完成]")
tEnd1 = time.time()
print ("It cost %f sec" % (tEnd1 - tStart1))

#匯入MongoDB
tStart2 = time.time()
print("[匯入資料庫]")
client = MongoClient('10.10.120.107', 27017)
db = client['admin']
collect = db['test3']

for hou in house_list:
    if '_id' in hou.keys():
        del hou['_id']
    collect.insert(hou)
#計時
print("[匯入資料庫 完成]")
tEnd2 = time.time()
print ("It cost %f sec" % (tEnd2 - tStart2))
        