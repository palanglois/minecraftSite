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
  images = []
  for root, dirs, files in os.walk('/var/www/myServ/FlaskApp/static/monsterApoPict/'):
    for filename in files:
      images.append({'src' : os.path.join("/static/monsterApoPict/",filename)})
  listPlayers = []
  with open('/var/www/myServ/FlaskApp/static/listPlayers.txt','r') as csvfile:
    reader = csv.reader(csvfile,delimiter = ' ')
    for row in reader:
      listPlayers.append({'name' : row[0]})
  return render_template('index.html', **{'images' : images, 'players' : listPlayers, 'nbPlayers' : len(listPlayers)})

if __name__ == "__main__":
  app.run()
