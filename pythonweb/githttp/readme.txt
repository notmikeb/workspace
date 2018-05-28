http://stewartjpark.com/2015/01/02/implementing-a-git-http-server-in-python.html
use git tools and flask to support a git http server

server
git init --bare test
python3 app.py


client
git clone http://localhost:5000/test
