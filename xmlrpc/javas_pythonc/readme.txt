https://gist.github.com/thomd/8106772

a java server and a python client



### client
javac -cp xmlrpc-helma-1.0.jar JavaClient.java
java -cp xmlrpc-helma-1.0.jar;xerces-2.4.0.jar;. JavaClient

> this will connect to a internet's xml-rpc server and get the result

### standalone server
javac -cp xmlrpc-helma-1.0.jar JavaServer.java
java -cp xmlrpc-helma-1.0.jar;xerces-2.4.0.jar;. JavaServer

> then run a python script as a xml-rpc client
> python -c "import xmlrpclib; print xmlrpclib.Server('http://localhost:8080/RPC2').sample.sumAndDifference(11,7)"


