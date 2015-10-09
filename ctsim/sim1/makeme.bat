g++ -c -o sim1.o sim1.c
g++ -shared -o sim1.dll sim1.o -Wl,--out-implib
g++ -c -o simmain.o simmain.c
g++ -o simmain.exe simmain.o -L. -lsim1