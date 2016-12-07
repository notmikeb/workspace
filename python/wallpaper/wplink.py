import requests
from BeautifulSoup import BeautifulSoup
page = requests.get("https://www.pexels.com/search/HD%20wallpaper/")
soup = BeautifulSoup(page.content)
links = soup.findAll("img")
import random

def genhtml(file):
   with open("output.html", 'w') as f:
     f.write("<body backgrond='{0}'><img src='{0}'></img></body>".format(file))


li = []
for l in links:
    if l.has_key('src'):
        li.append(l)
links = li
if len(links) > 0:
  r =int( random.random()*len(links) )
  print str(r) + "/" + str(len(links))
  l = links[ r ]
  print l['src']
  genhtml(l['src'])
else:
  print 'no data'

