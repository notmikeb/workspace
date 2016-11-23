TARGET = word.pyd
OFILES = sipwordcmodule.obj sipwordWord.obj
HFILES = sipAPIword.h 

CC = cl
CXX = cl
LINK = link
CPPFLAGS = -DNDEBUG -DUNICODE -DWIN32 -DQT_LARGEFILE_SUPPORT -I. -Ic:\python27\include
CFLAGS = -nologo -Zm200 -Zc:wchar_t- -O2 -MD -W3
CXXFLAGS = -nologo -Zm200 -Zc:wchar_t- -O2 -MD -W3 -w34100 -w34189
LFLAGS = /NOLOGO /DYNAMICBASE /NXCOMPAT /DLL /MANIFEST /MANIFESTFILE:$(TARGET).manifest /SUBSYSTEM:WINDOWS /INCREMENTAL:NO
LIBS = /LIBPATH:c:\python27\libs ..\cpp\word_org.lib python27.lib
.SUFFIXES: .c .cpp .cc .cxx .C


{.}.cpp{}.obj::
	$(CXX) -c $(CXXFLAGS) $(CPPFLAGS) -Fo @<<
	$<
<<

{.}.cc{}.obj::
	$(CXX) -c $(CXXFLAGS) $(CPPFLAGS) -Fo @<<
	$<
<<

{.}.cxx{}.obj::
	$(CXX) -c $(CXXFLAGS) $(CPPFLAGS) -Fo @<<
	$<
<<

{.}.C{}.obj::
	$(CXX) -c $(CXXFLAGS) $(CPPFLAGS) -Fo @<<
	$<
<<

{.}.c{}.obj::
	$(CC) -c $(CFLAGS) $(CPPFLAGS) -Fo @<<
	$<
<<

all: $(TARGET)

$(OFILES): $(HFILES)

$(TARGET): $(OFILES)
	$(LINK) $(LFLAGS) /OUT:$(TARGET) @<<
	  $(OFILES) $(LIBS)
<<
	mt -nologo -manifest $(TARGET).manifest -outputresource:$(TARGET);2

install: $(TARGET)
	@if not exist c:\python27\Lib\site-packages mkdir c:\python27\Lib\site-packages
	copy /y $(TARGET) c:\python27\Lib\site-packages\$(TARGET)

clean:
	-del $(TARGET)
	-del sipwordcmodule.obj
	-del sipwordWord.obj
	-del $(TARGET).manifest
