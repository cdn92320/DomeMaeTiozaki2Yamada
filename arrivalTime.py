import requests
from bs4 import BeautifulSoup
import json
import re

def transferSt(soup):
    keys = ['stationName','arrivalTime']
    routeDatail = soup.find( class_="routeDetail")
    stationTime = routeDatail.find_all( class_="station")
    arrival = []
    for el in stationTime:
        if "着" in el.text:
            transStation = {}
            hhmm = el.text.split("着")[0]
            stationName = el.find( "dt" ).text

            values = [stationName, hhmm ]
            transfer= dict(zip(keys, values))
            arrival.append(transfer)

    return arrival
            
            
url1 = "https://transit.yahoo.co.jp/search/result?from="
fromstation = "ドーム前千代崎"
url2 = "&to="
tostation = "山田(大阪府・阪急線)"
url3 = "&fromgid=ZH90Fy8HeOc&togid=QzcaJHNXik-&flatlon=%2C%2C29191&tlatlon=%2C%2C26229"
url4 = "&via=天神橋筋六丁目&via=淡路&viacode=26061&viacode=25816"
prmYear = "&y=2022"
prmDay = "&m=05&d=11"
prmHour = "&hh="
prmMin1 = "&m1="
prmMin2 = "&m2="
url5 = "&type=1&ticket=ic&expkind=1&userpass=1&ws=1&s=0&al=1&shin=1&ex=1&hb=1&lb=1&sr=1#route03"

with open("diaDetail.json", 'r') as rfp:
    diaDetail = json.load(rfp)

for key in diaDetail.keys():
    line = diaDetail[key]
    # print ( key + " " + line["id"] + " " + line["hour"] + ":" + line["min"] + line["trainType"] + line["trainFor"] )

    m1,m2 = line["min"][:1], line["min"][1:]
    url = url1 + fromstation + url2 + tostation + url3 + url4 + prmYear + prmDay
    url = url + prmHour + line["hour"]
    url = url + prmMin1 + m1
    url = url + prmMin2 + m2
    url = url + url5

    response = requests.get(url)
    soup = BeautifulSoup(response.content,"html.parser")
#    routeList = soup.find( class_="routeList" ) # 到着時間の記載部分を抽出
    routeList = soup.find( class_="summary" ) # 到着時間の記載部分を抽出
    ftime = routeList.find( class_="time" ).text.split("→")[0]
    arrivalTimeValue = routeList.find( class_="time" ).text.split("→")[1].split("（")[0]
    transferText = routeList.find( class_="transfer" ).text
    transfer = int(re.sub(r"[^0-9]","",transferText))
    transferArrival = transferSt(soup)

    addItem = { "arrivalTime" : arrivalTimeValue, "transferNum" : transfer, "transferArrival" : transferArrival }
    line |= addItem
    diaDetail[key] = line

with open ("diaDetail2.json",'w') as wfp:
    json.dump( diaDetail, wfp, indent=4 )

    






