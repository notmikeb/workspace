

oldpwd=`pwd`

all:
	cd c++ && qmake
	$(MAKE) -C c++
	cd py && python runsip.py
	cd py && python configure.py
	$(MAKE) -C py 
	cd py && echo "export LD_LIBRARY_PATH=../c++" > run.sh
	cd py && echo "echo use python to import hello" >> run.sh
	cd py && echo "python -c 'import hello; print hello.Hello()'" >> run.sh
	chmod +x py/run.sh
	cd py && ./run.sh
clean:
	rm -f c++/*.so c++/*.o c++/*.so.*.* c++/*.so.* c++/Makefile
	rm -f py/*.so py/*.h py/*.exp py/*.cpp py/Makefile py/*.o py/*.sbf
