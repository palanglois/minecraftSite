import urllib2
import csv
import os
import BeautifulSoup as bs

#Url of the page where the edt is located
edtUrl = "http://www.math.ens-cachan.fr/planning--368972.kjsp?RH=1242415112528"
pageEdt = urllib2.urlopen(edtUrl).read()
soup = bs.BeautifulSoup(pageEdt)
#Finding the "<li class="xls">" tag
linkLocation = soup.findAll('li',{ "class" : "xls"})[0]
#Extracting the first hypertext link inside of it
links = bs.BeautifulSoup(str(linkLocation),parseOnlyThese=bs.SoupStrainer('a'))
linkTab = [link for link in links]
link=str(linkTab[0]['href'])

#Download and save the excel file to the static directory
def getAndParseEdt(url):
  content = urllib2.urlopen(url).read()
  f = open("/var/www/myServ/FlaskApp/static/edt.xls",'w')
  f.write(content)

getAndParseEdt(link)

