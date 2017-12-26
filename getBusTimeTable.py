# coding: utf-8

import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime, date, timezone, timedelta

def getNiigataBusTime(holyday):
    #URLの指定
    html = urlopen("https://transfer.navitime.biz/niigatabrt-newsystem/pc/diagram/BusDiagram?orvCode=00060437&course=0001400058&stopNo=11")
    bsObj = BeautifulSoup(html, "html.parser")

    #テーブルを指定
    tablenum = 0
    if holyday :
        tablenum = 1
        
    table = bsObj.findAll("table",{"class":"diagram-table parallel"})[tablenum]
    rows = table.findAll("tr")
    busStop = bsObj.find(id='diagram-result-subject')
    if busStop : busStop = busStop.string.replace('\t','').replace('\n','')
    destination = bsObj.find(class_='td-destination').string
    if destination : destination = destination.string

    r = re.compile('[0-9]+')
    timelist = [[] for i in range(24)]
    for row in rows:
        hour = row.find('th',class_='hour')
        if hour :
            h = timelist[int(r.search(hour.string).group(0))%24]
            for min in row.findAll(['a']):
                h.append(int("{0}".format(r.search(min.string).group(0))))
    return timelist,busStop,destination

def getXBusTime(holyday,h,min,num,table):
    ret = []
    for i in range( h, 23 ):
        for j in table[i]:
            if i > h or j > min:
                ret.append("{0:02d}:{1:02d}".format(i,j))
                if len(ret) >= num:
                    return ret
    return ret

def getBusTimeTextTable(holyday,table):
    ret=""
    for i in range( 0, 23 ):
        if len(table[i])>0:
            for j in table[i]:
                ret +=("{0:02d}:{1:02d} ".format(i,j))
            ret += '\n'
    return ret

def isHolyday():
    html = urlopen("http://s-proj.com/utils/checkHoliday.php")
    bsObj = BeautifulSoup(html, "html.parser")
    return "holiday" in bsObj

def getNextXBusTime(num):
    time = datetime.now(timezone(timedelta(hours=+9))).time()
    wkd = isHolyday()
    table, busStop, destination = getNiigataBusTime(wkd)
    return [','.join(getXBusTime(wkd,time.hour,time.minute,num,table)),getBusTimeTextTable(wkd,table), busStop, destination]

