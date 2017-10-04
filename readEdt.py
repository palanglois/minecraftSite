# -*- coding: utf-8 -*-
import csv
import time
import copy
from coursList import coursList
from sortList import *
import dateparser
from datetime import datetime
import json

#Parse the obtained csv file and get relevant courses for the person 'name'
def parseEdt(identifier):
  with open('/var/www/myServ/FlaskApp/static/course_combinations.json', 'r') as comb:
    cours = json.load(comb)[identifier]
  myEdt = []
  with open('/var/www/myServ/FlaskApp/static/edt.csv','r') as csvfile:
    reader = csv.reader(csvfile)
    data = []
    for row in reader:
      temp = list(row)
      data.append([s.decode('utf-8') for s in temp])
    semaineStr = ""
    dayLine = 0
    lineIterator = 0
    while lineIterator < len(data):
      row = data[lineIterator]
      if row[0][0:7].lower() == 'semaine':
        semaineStr = row[0]
        dayLine = lineIterator + 1
      else:
        lineIterator += 1
        continue
      innerIterator = lineIterator + 2
      while data[innerIterator][0][0:7].lower() != 'semaine':
        lineData = "".join(data[innerIterator])
        if not (lineData[0:2].isdigit() and lineData[2] == 'h'):
          innerIterator += 1
          if innerIterator >= len(data):
            break
          continue
        for dayColumn in range(5):
          courseDayDate = dateparser.parse(data[dayLine][dayColumn])
          if len(data[innerIterator][dayColumn]) >= 5:
            if data[innerIterator][dayColumn][0:2].isdigit():
              # Getting the course date
              curCourseDate = copy.deepcopy(courseDayDate)
              curCourseDate = curCourseDate.replace(hour=int(data[innerIterator][dayColumn][0:2]))
              curCourseDate = curCourseDate.replace(minute=int(data[innerIterator][dayColumn][3:5]))
              if curCourseDate < datetime.now().replace(hour=datetime.now().hour - 1):
                continue
              courseTitle = data[innerIterator + 1][dayColumn]
              for c in cours:
                if c.decode('utf-8') in courseTitle.lower():
                  courseHour = data[innerIterator][dayColumn]
                  courseRoom = data[innerIterator + 3][dayColumn]

                  # Fix for Laverne's mistakes
                  if len(courseRoom) == 0:
                    courseRoom = data[innerIterator + 4][dayColumn]
                  if len(data[innerIterator + 2][dayColumn]) == 0:
                    courseRoom = data[innerIterator + 4][dayColumn]

                  curTable = {'title' : courseTitle,
                              'hour'  : courseHour,
                              'room'  : courseRoom,
                              'day'   : data[dayLine][dayColumn],
                              'datetime' : curCourseDate}
                  myEdt.append(curTable)
                  break
        innerIterator += 1
        if innerIterator >= len(data):
          break
      lineIterator = innerIterator
  return sorted(myEdt, cmp=compare2)

