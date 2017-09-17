del sipwordcmodule.cpp
del sipwordWord.cpp
del sipAPIword.h
del *.o /s
del *.obj /s
del *.a /s
del *.sbf
python -c "import shutil;shutil.rmtree('build')"