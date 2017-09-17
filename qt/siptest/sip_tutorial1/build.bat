
rem generate  header structure
rem sip -c . word.sip

python setup.py build -c msvc

echo cd build\lib.win-am64-3.5
echo python
echo import word
echo w1 = word.Word(b'this is a sample')
echo w1.reverse()
echo w1 = 0

