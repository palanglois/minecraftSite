# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, render_template, send_from_directory, request
from flask_wtf import FlaskForm, widgets
from flask_wtf.csrf import CSRFProtect
from flask_appbuilder.widgets import ListWidget
from wtforms.fields import SelectMultipleField
from wtforms.widgets import CheckboxInput
import os
import csv
import sys
import json
from readEdt import *
from getEdt import downloadEdt
from coursList import coursList

app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = 's3cr3t'


class MultiCheckboxField(SelectMultipleField):
  widget = ListWidget(prefix_label=False)
  option_widget = CheckboxInput()

class SimpleForm(FlaskForm):
  all_courses = [(k.decode('utf-8'), v.decode('utf-8')) for k, v in coursList.items()]
  my_field = MultiCheckboxField('Cours choisis', choices=all_courses)

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

@app.route("/create_courses", methods=["GET"])
@csrf.exempt
def createCourses():
    my_form = SimpleForm()
    return(render_template('course_creator.html', form=my_form))

@app.route("/create_courses", methods=["POST"])
@csrf.exempt
def createCoursesPost():
  my_form = SimpleForm()
  if my_form.my_field.data is None: 
    return(render_template('tes_con.html'))
  data = None
  with open('course_combinations.json', 'r') as comb:
    data = json.load(comb)
  with open('course_combinations.json', 'w') as comb:
    data.append(my_form.my_field.data)
    json.dump(data, comb)
  comb_number = str(len(data)-1).zfill(6)
  print("comb_number : ", comb_number)
  url = 'http://lucienetleon.hopto.org/pa?id=' + comb_number
  return(render_template('page_url.html', url=url))

@app.route("/pa")
def paEdt():
  identifier = request.args.get('id')
  my_form = SimpleForm()
  downloadEdt()
  data = getEdt(int(identifier))
  return(render_template('edt.html', form=my_form, **{'listCours' : data}))

@app.route("/robots.txt")
def robots():
  robotsListString = open('/var/www/myServ/robots.txt','r').readlines()
  robotsString = "<br>".join(robotsListString)
  return(send_from_directory('/var/www/myServ','robots.txt'))

@app.route("/profile")
def profile():
  fakeProfile = dict()
  fakeProfile["pseudo"] = "Fake_Profile" 
  fakeProfile["date"] = "01.01.2001"
  fakeProfile["email"] = "fake_email@gmail.com"
  fakeProfile["profilePicture"] = "/static/steve.jpg"
  return render_template('profile.html',**fakeProfile)

@app.route("/onlineplayers")
def getPlayers():
  listPlayers = []
  with open('/var/www/myServ/FlaskApp/static/listPlayers.txt','r') as csvfile:
    reader = csv.reader(csvfile,delimiter = ' ')
    for row in reader:
      listPlayers.append({'name' : row[0]})
    data = {}
    data['nb'] = len(listPlayers)
    data['section'] = render_template('onlinePlayers.html', **{'players' : listPlayers, 'nbPlayers' : len(listPlayers) }).encode('utf-8')
    return json.dumps(data)

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
  #Rendering the page
  return render_template('index.html', **{'articles' : articlesData})

if __name__ == "__main__":
  app.run(debug=True)
