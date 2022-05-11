import requests
from bs4 import BeautifulSoup
import json
import collections as cl



diaDetail = cl.OrderedDict() 
keys = ['id','secKey','hour','min','trainType','trainFor']

seqNum = 0
# 時刻表URL
url = "https://transit.yahoo.co.jp/station/time/29191/?gid=4331&pref=27&done=time"

response = requests.get(url)
soup = BeautifulSoup(response.content,"html.parser")
timeTable =  soup.find("table",  attrs = {"class" : "tblDiaDetail"})
timeRows = timeTable.find_all("tr")

for timeRow in timeRows:
    hh_id = timeRow.get("id")
    hh = timeRow.find("td", attrs = {"class" : "hour"})
    if hh is not  None:
        hour = hh.text.zfill(2)
        if int ( hour ) >= 0 and int ( hour ) <= 4:
            hhsec = ( 25 + int ( hour ) ) * 3600
        else:
            hhsec = int( hour ) * 3600
    minutes = timeRow.find_all("li", attrs = {"class" : "timeNumb"})
    for minute in minutes:
        values = []
        mm = minute.find("dt").text.zfill(2).rstrip("◆")
        minsec = int( mm ) * 60
        sec = hhsec + minsec
        tt = minute.find(class_="trainType")
        if tt is None:
            trainType = " "
        else:
            trainType = tt.text
        tf = minute.find(class_="trainFor")
        if tf is None:
            trainFor = " "
        else:
            trainFor = tf.text
        
        seqNum += 1
        values = [seqNum,sec,hour,mm ,trainType,trainFor]
        DepartureTime = dict(zip(keys, values))
        diaDetail[str(seqNum).zfill(4)] = cl.OrderedDict( DepartureTime )

with open("diaDetail.json",'w') as wfp:
    json.dump( diaDetail, wfp, indent=4 )
