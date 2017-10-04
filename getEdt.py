import urllib

def downloadEdt():
    urllib.urlretrieve("https://docs.google.com/spreadsheets/d/1yS1SKXenOvwjYRHxeAFPPsW9xgGPuBMjh0O4XBIyWHA/gviz/tq?tqx=out:csv", "/var/www/myServ/FlaskApp/static/edt.csv")


