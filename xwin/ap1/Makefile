

all: testx.o
	g++ $< -lX11 -o testx
clean:
	rm *.o testx
.c.o:
	g++ $@ -lX11
