
del /s/q/f dist >null
del null
echo %date% %time% > version.txt
c:\Python36\Scripts\pyinstaller.exe --onefile -y testapp.py
copy /y dist\testapp.exe d:\temp\testapp
copy /y version.txt d:\temp\testapp

dir \\localhost\d\temp\testapp
