import urllib2
import csv
import os

edtUrl = "http://www.math.ens-cachan.fr/servlet/com.univ.collaboratif.utils.LectureFichiergw?ID_FICHE=19520&OBJET=0017&ID_FICHIER=666921"

#Download and save the excel file to the static directory
def getAndParseEdt(url):
  content = urllib2.urlopen(url).read()
  f = open("/var/www/myServ/FlaskApp/static/edt.xls",'w')
  f.write(content)

getAndParseEdt(edtUrl)

