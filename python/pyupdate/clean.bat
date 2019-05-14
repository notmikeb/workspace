del /s/q/f build
rmdir /s/q build
del /s/q/f dist
rmdir /s/q dist
del /s/q/f __pycache__
rmdir /s/q __pycache__
del *.spec /s/q/f
del testapp.exe version.txt
cd testapp && call clean.bat
