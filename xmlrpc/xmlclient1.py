import xmlrpclib
server = xmlrpclib.ServerProxy('http://localhost:8888')
s = server.get_keyword_names()
print (s)
for i in s:
   print ("{} args:{}".format(i,server.get_keyword_arguments(i)))
   print ("{} docs:{}".format(i,server.get_keyword_documentation(i)))
   #run_keyword