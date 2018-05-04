from flask import Flask, render_template, request, url_for
import random
import json
import traceback

from flask_appconfig import AppConfig
from flask_bootstrap import Bootstrap


import handler

app = Flask(__name__)

default_max = 100

@app.route('/api/data')
def get_data():
    s_abc = [random.random() for _ in range(40)]
    try:
      id = request.args.get('id')
    except:
      id = 0
    return render_template('abc.html', s_abc=s_abc, id = id)

@app.route('/')
def form():
    s_abc = [random.random() for _ in range(40)]
    return render_template('abc.html', s_abc=s_abc)


    
@app.route('/table.htm')
def form_tablehtm():
    s_abc = [random.random() for _ in range(40)]
    return render_template('table.html', s_abc=s_abc)

@app.route('/table')
def form_table():
    return form_tablehtm()
    
@app.route('/statistic15')
def form_statistic15():
    return render_template('statistic15.html')

@app.route('/statistic20')
def form_statistic20():
    return render_template('statistic20.html')
    
@app.route('/statistic')
def form_statistic():
    return form_statistic20()    

@app.route('/templates/<f1>')
def form_template_file(f1):
    #f1 = request.args.get('file')
    print(f1)
    return render_template(f1)
    
## RestAPI    



@app.route('/api/related', methods=['GET', 'POST'])
def get_related():
    # post method, get the json data
    content = request.get_json()
    print("content is ", content)
    # {"ChipNames":"[\"MT6739\",\"MT7668\",\"MT6758\"]","Platforms":"[\"zion\",\"7668_mp2_1801\",\"gen35test\"]"}
    # sqlstring is 'ChipName' = 'MT6739' or 'ChipName' = 'MT7668' and Status != 'DONE'
    
    
    try:
        cnlist = content['ChipNames']
        cnlist = json.loads(cnlist)
    except:
        traceback.print_exc()
        cnlist = []
    try:
        pllist = content['Platforms']
        pllist = json.loads(pllist)
    except:
        traceback.print_exc()    
        pllist = []
    try:
        maxtaskid = content['maxtaskid']
        maxtaskid = int(maxtaskid)
    except:
        maxtaskid = 99999999

    if len(cnlist) == 0  and len(pllist) == 0:
        return json.dumps({})  # a empty result
    
    print( cnlist , type(cnlist) )
    print (pllist, type(pllist) )
    cnpllist = []
    try:
        for i in cnlist:
            for j in pllist:
                cnpl = i + "_" + j
                cnpllist.append(cnpl)
    except:
        traceback.print_exc()
    #cnstring = " or ".join(map( lambda x: " ChipName = '{}'".format(x), cnlist))
    #plstring = " or ".join(map( lambda x: " Platform = '{}'".format(x), pllist))
    cnplstring = " or ".join(map( lambda x: "concat(ChipName, concat('_', Platform)) = '{}'".format(x), cnpllist))
    
    sqlstring = 'select top 50 * from dbo.Task where (' + cnplstring + ") and Status != 'DONE' and TaskID <= " + str(maxtaskid) + " order by TaskID desc"
    print(sqlstring)
    try:
        return handler.query_sqlstring(sqlstring)
    except:
        return json.dumps( [{ 'TaskID': 0, 'Platform' : 'error', 'ChipName' : 'error'}])

@app.route('/api/query')
def get_query():
    print("get_query")
    max = default_max
    try:
        max = int(request.args.get('max'))
    except:
        max = default_max
    try:
        cl = request.args.get('cl')
    except:
        cl = None
    return handler.test(max, cl = cl)
    
@app.route('/api/waiting')
def get_waiting():
    max = default_max
    try:
        max = int(request.args.get('max'))
    except:
        max = default_max
    try:
        mode =  request.args.get('mode')
    except:
        mode = 'BT'
    if mode == 'BT':
        where1 = "Mode like '%BT%'"
    elif mode == 'AP':
        #where1 = "Mode like '%AP%' or Mode like '%ST%'"
        where1 = "Mode not like '%BT%'"
    else:
        where1 = "Mode like '%BT%'"
        
    sqlstring = "select top {max} * from dbo.Task where {where1} and Status != 'DONE' order by TaskID desc ".format(max = max, where1 = where1)
    print(sqlstring)
    try:
        return handler.query_sqlstring(sqlstring)
    except:
        return json.dumps( [{ 'TaskID': 0, 'Platform' : 'error', 'ChipName' : 'error'}]) 

from flask_nav import Nav
from flask_nav.elements import *

nav = Nav()
nav.register_element('frontend_top', Navbar(
  View('Home', '.form'),
  View('Pre-test', '.form_statistic20'),
  View('Post-test', '.form_statistic15'),
  View('Table', '.form_tablehtm'),
  Text('HelloWorld')))

if __name__ == '__main__':
  AppConfig(app)
  Bootstrap(app)
  nav.init_app(app)
  app.run(debug=True, port = 9000, host = "0.0.0.0")
