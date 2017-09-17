echo "url is https://www.codeproject.com/Articles/84461/MinGW-Static-and-Dynamic-Libraries"


g++ -c ../word.cpp -o word.o
ar rcs libword.a word.o

copy libword.a ..

echo "*.a is a static library"
echo "*.so is a dynamic library"

g++ -c wordclient.cpp
g++ -o wordclient.exe wordclient.o -L. -lword

echo -lword is to link 'lib'word'.a'

cl word.obj wordclient.cpp -I.. 
cl -c ../word.cpp -o word.o 
