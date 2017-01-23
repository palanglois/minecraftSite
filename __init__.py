# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, render_template, send_from_directory
import os
import csv
import sys
from readEdt import *

app = Flask(__name__)

@app.route("/chaimaa")
def chaimaaEdt():
  os.system("/var/www/myServ/FlaskApp/static/convertEdt.sh")
  data = getEdt("Chaimaa")
  return(render_template('edt.html',**{'studentName' : u"Chaïmaa", 'listCours' : data}))

@app.route("/othman")
def othmanEdt():
  os.system("/var/www/myServ/FlaskApp/static/convertEdt.sh")
  data = getEdt("Othman")
  return(render_template('edt.html',**{'studentName' : "Othman", 'listCours' : data}))

@app.route("/pa")
def paEdt():
  os.system("/var/www/myServ/FlaskApp/static/convertEdt.sh")
  data = getEdt("PA")
  return(render_template('edt.html',**{'studentName' : "PA", 'listCours' : data}))

@app.route("/robots.txt")
def robots():
  robotsListString = open('/var/www/myServ/robots.txt','r').readlines()
  robotsString = "<br>".join(robotsListString)
  return(send_from_directory('/var/www/myServ','robots.txt'))

@app.route("/onlineplayers")
def getPlayers():
  listPlayers = []
  with open('/var/www/myServ/FlaskApp/static/listPlayers.txt','r') as csvfile:
    reader = csv.reader(csvfile,delimiter = ' ')
    for row in reader:
      listPlayers.append({'name' : row[0]})
    return render_template('onlinePlayers.html', **{'players' : listPlayers, 'nbPlayers' : len(listPlayers) })

@app.route("/")
def hello():
  #Listing all articles directory
  artDir = '/var/www/myServ/FlaskApp/static/articles'
  artList = [[os.path.join(artDir,o),o] for o in os.listdir(artDir) if os.path.isdir(os.path.join(artDir,o))]
  
  #Filling the data for each article
  articlesData = []
  for article in artList:
    artData = dict()
    csvFile = open(os.path.join(article[0],"article.csv"))
    reader = csv.reader(csvFile,delimiter='\\')
    csvList = [row for row in reader]
    artData['title'] = unicode(csvList[0][0],'utf-8')
    artData['link'] = csvList[1][0]
    artData['description'] = unicode(csvList[2][0],'utf-8')
    #Filling the images path
    imgPath = os.path.join(article[0],"images")
    imgList = []
    for root, dirs, files in os.walk(imgPath):
      for img in files:
        imgList.append({'src' : os.path.join('/static/articles',article[1],'images',img)})
    artData['images'] = imgList
    articlesData.append(artData)

  listPlayers = []
  with open('/var/www/myServ/FlaskApp/static/listPlayers.txt','r') as csvfile:
    reader = csv.reader(csvfile,delimiter = ' ')
    for row in reader:
      listPlayers.append({'name' : row[0]})
  return render_template('index.html', **{'articles' : articlesData, 'players' : listPlayers, 'nbPlayers' : len(listPlayers)})

if __name__ == "__main__":
  app.run()
