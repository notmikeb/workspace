echo "start service: menu interpreter : menu view : menu start service"
echo "please replace 9999 below with sl4a's service port"
adb forward tcp:54311 tcp:48046
python -c "import android; a = android.Android(('localhost', 54321));a.makeToast('hello,world')" 

echo "example http://stackoverflow.com/questions/11770594/using-sl4a-python-and-bluetooth"
