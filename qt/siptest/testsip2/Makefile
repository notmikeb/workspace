CODE_DIR = py2
.PHONY: all

all:
	cd cpp && cl /LD /LDd word.cpp
	cd cpp && lib /VERBOSE /OUT:word_org.lib word.obj
	cd py2 && cmdsip.bat
	cd py2 && python configure.py
	cd py2 && nmake -f Makefile
	cd py2 && python -c "import word; a = word.Word('mike') ; print(a.reverse())"

clean:
	del /q/f cpp\word.dll cpp\*.lib cpp\*.obj
	del /q/f py2\sip*.cpp py2\sip*.h py2\*.pyd* py2\*.sbf
	del /q/f py2\*.obj py2\*.exp py2\*.lib py2\Makefile