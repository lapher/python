import time
from math import radians, cos, sin, asin, sqrt  
import csv
from pyspark import SparkContext, SparkConf
import sys
school_dic  = {}
school_list = []
mrt_dic     = {}
mrt_list    = []
def haversine(lon1, lat1, lon2, lat2): 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])  
  
    dlon = lon2 - lon1   
    dlat = lat2 - lat1   
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2  
    c = 2 * asin(sqrt(a))   
    r = 6371 
    return c * r * 1000  

def chang_addr (data):
    count_s = 0
    count_m = 0
    lat = float(data.split(",")[1])
    lon = float(data.split(",")[2])
    for school in school_list:       
        meter = haversine(lon,lat,school['lon'],school['lat'])
        if meter < 700:
            count_s +=1
    for mrt in mrt_list: 
        meterm = haversine(lon,lat,mrt['lon'],mrt['lat'])
        if meterm < 700:
            count_m +=1
    house["mrt_count"] = count_m
    return [data.split(",")[0], count_s, count_m]

with open("house_school.csv", encoding='utf-8') as file:
    content = csv.reader(file, delimiter=' ', quotechar='|')
    for row in content:
        school_dic  = {}
        school_dic["id"] =  row[0].split(',')[0]
        school_dic["lat"] = float(row[0].split(',')[7])
        school_dic["lon"] = float(row[0].split(',')[8])
        school_list.append(school_dic) 

with open("MRT.csv", encoding='utf-8') as file:
    content2 = csv.reader(file, delimiter=' ', quotechar='|')
    for row2 in content2:
        mrt_dic  = {}
        mrt_dic["id"] =  row2[0].split(',')[0]
        mrt_dic["lat"] = float(row2[0].split(',')[3])
        mrt_dic["lon"] = float(row2[0].split(',')[4])
        mrt_list.append(mrt_dic) 

conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf=conf)


house_csv = sc.textFile('hdfs://localhost/user/cloudera/output').map(chang_addr).saveAsTextFile("s3n://s3-ap-northeast-1.amazonaws.com/ab106database")


