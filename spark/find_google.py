import time
from pyspark import SparkConf, SparkContext
import urllib  
from urllib.request import urlopen  
import json
from pymongo import MongoClient
import pymongo 


conf = SparkConf().setMaster("local").setAppName("My_Google")
sc = SparkContext (conf = conf)

def getGeoFromAddress(data):
    try:
        time.sleep(1)
        ID = data["_id"]
        address = data["road"]
        addressUrl = "http://maps.googleapis.com/maps/api/geocode/json?address=" + address  

        addressUrlQuote = urllib.parse.quote(addressUrl, ':?=/')  
        response = urlopen(addressUrlQuote).read().decode('utf-8')  
        responseJson = json.loads(response)  

        lat = responseJson.get('results')[0]['geometry']['location']['lat']  
        lon = responseJson.get('results')[0]['geometry']['location']['lng']  
    except:
        print("error")
 
    return[ID,lat,lon]

house={}
house_list = []

client = MongoClient('10.10.120.107', 27017)
db = client.admin
collection = db.yung
cur = collection.find()
for x in cur:
    house={}
    house["_id"] = x['_id']
    house["road"] = x['road']
    house_list.append(house)

input = sc.parallelize(house_list).map(getGeoFromAddress).saveAsTextFile("hdfs://localhost/user/cloudera/output")