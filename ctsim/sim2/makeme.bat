g++ -c -o sim2.o sim2.c
g++ -shared -o sim2.dll sim2.o -Wl,--out-implib
g++ -c -o simmain.o simmain.c
g++ -o simmain.exe simmain.o -L. -lsim2
