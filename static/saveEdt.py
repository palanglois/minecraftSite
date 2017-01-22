import urllib2
import csv
import os
import re

#Url of the page where the edt is located
edtUrl = "http://www.math.ens-cachan.fr/planning--368972.kjsp?RH=1242415112528"
pageEdt = urllib2.urlopen(edtUrl).read()
a = [m.start() for m in re.finditer(r'xls',pageEdt)][0]
pageRest = pageEdt[a+14:-1]
b = [m.start() for m in re.finditer(r'onclick',pageRest)][0]
link = pageRest[0:b-2].replace("&amp;","&")

#Download and save the excel file to the static directory
def getAndParseEdt(url):
  content = urllib2.urlopen(url).read()
  f = open("/var/www/myServ/FlaskApp/static/edt.xls",'w')
  f.write(content)

getAndParseEdt(link)

