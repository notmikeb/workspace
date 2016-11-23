

all:
	gcc -c -fPIC testdata.c
	gcc -shared -o libtestdata.so testdata.o
	gcc testmain.c libtestdata.so
	
