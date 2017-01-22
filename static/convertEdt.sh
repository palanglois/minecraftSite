#!/bin/bash

#Get the schedule from the ENS website
python /var/www/myServ/FlaskApp/static/saveEdt.py

#Convert it to csv (only way to make it happen so far...)
ssconvert /var/www/myServ/FlaskApp/static/edt.xls /var/www/myServ/FlaskApp/static/edt.csv
