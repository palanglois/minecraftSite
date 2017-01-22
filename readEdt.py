# -*- coding: utf-8 -*-
import csv
import time
from cours import cours
from sortList import *

#Parse the obtained csv file and get relevant courses for the person 'name'
def getEdt(name):
  myEdt = []
  with open('/var/www/myServ/FlaskApp/static/edt.csv','r') as csvfile:
    reader = csv.reader(csvfile)
    data = []
    for row in reader:
      temp = list(row)
      data.append([s.decode('utf-8') for s in temp])
    print(len(data))
    semaineStr = ""
    dayLine = 0
    for i in range(len(data)):
      row = data[i]
      if row[0][0:7] == 'Semaine':
        semaineStr = row[0]
        #print('\n\n'+semaineStr+'\n\n')
        dayLine = i+1
      for j in range(len(row)):
        cell = row[j]
        for c in cours[name]:
          day = data[dayLine][j]
          if c.decode('utf-8') in cell.lower():
            if len(day) == 10:
              if int(day[5:7]) < int(time.strftime("%m")):
                break
              elif int(day[5:7]) == int(time.strftime("%m")) and int(day[8:10]) < int(time.strftime("%d")):
                break
            curTable = {'title' : cell,'hour' : data[i-1][j],'room' : data[i+2][j], 'day' : data[dayLine][j], 'week' : semaineStr}
            myEdt.append(curTable)
            break
  return sorted(myEdt,cmp=compare)

