from flask import Flask, render_template, request, url_for
import random
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

@app.route('/api/query')
def get_query():
    import handler
    return handler.test()

if __name__ == '__main__':
  app.run(debug=True, port = 9000)