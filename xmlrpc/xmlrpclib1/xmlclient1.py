import xmlrpclib
server = xmlrpclib.ServerProxy('http://localhost:8888')
s = server.get_keyword_names()
print (s)
for i in s:
   print ("{} args:{}".format(i,server.get_keyword_arguments(i)))
   print ("{} docs:{}".format(i,server.get_keyword_documentation(i)))
   #run_keyword
   pass

if 'runcase' in s:
   print( server.run_keyword('runcase', ['0' , 'testcase1', 'param1', 'param2']) )
   print( server.run_keyword('runcase', ['0' , 'testcase1', 'param1', 'param2', 'param3']) )
if 'runaction' in s:
   print( server.run_keyword('runaction', ['1' , 'action1', 'param1', 'param2']) )
   print( server.run_keyword('runaction', ['1' , 'action2', 'param1', 'param2', 'param3']) )