from flask import Flask, render_template, request, url_for
import random
import json
import traceback

import handler

app = Flask(__name__)

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

@app.route('/table')
def form_table():
    s_abc = [random.random() for _ in range(40)]
    return render_template('table.html', s_abc=s_abc)


@app.route('/api/related', methods=['GET', 'POST'])
def get_related():
    # post method, get the json data
    content = request.get_json()
    print("content is ", content)
    # {"ChipNames":"[\"MT6739\",\"MT7668\",\"MT6758\"]","Platforms":"[\"zion\",\"7668_mp2_1801\",\"gen35test\"]"}
    # sqlstring is 'ChipName' = 'MT6739' or 'ChipName' = 'MT7668' and Status != 'DONE'
    cnlist = content['ChipNames']
    pllist = content['Platforms']
    try:
        cnlist = json.loads(cnlist)
    except:
        traceback.print_exc()
        cnlist = []
    try:
        pllist = json.loads(pllist)
    except:
        traceback.print_exc()    
        pllist = []

    if len(cnlist) == 0  and len(pllist) == 0:
        return json.dumps({})  # a empty result
    
    print( cnlist , type(cnlist) )
    print (pllist, type(pllist) )
    cnstring = " or ".join(map( lambda x: " ChipName = '{}'".format(x), cnlist))
    plstring = " or ".join(map( lambda x: " Platform = '{}'".format(x), pllist))
    sqlstring = 'select top 50 * from dbo.Task where (' + cnstring + " or " + plstring + ") and Status != 'DONE' order by TaskID desc"
    print(sqlstring)
    try:
        return handler.query_sqlstring(sqlstring)
    except:
        return json.dumps( [{ 'TaskID': 0, 'Platform' : 'error', 'ChipName' : 'error'}])

@app.route('/api/query')
def get_query():
    
    max = 50
    try:
        max = int(request.args.get('max'))
    except:
        max = 50
    try:
        cl = request.args.get('cl')
    except:
        cl = None
    return handler.test(max, cl = cl)

if __name__ == '__main__':
  app.run(debug=True, port = 9000, host = "0.0.0.0")