use vcvarsall.bat to setup the vc build env
E:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\vcvarsall.bat

cpp folder: generate the word_org.lib
py2 folder: use static lib, word_org.lib , to generate a word.pyd for import

py2
sip.exe -> from word.sip to sipwordmodule.cpp and sipwordWord.cpp
configure.py -> gen word.sbf and Makefile

