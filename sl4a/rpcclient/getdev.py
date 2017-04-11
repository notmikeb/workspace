import subprocess

o = subprocess.check_output("adb devices", shell = True)
print (o)
o = o.split('\n')
lines = [ i.replace('\r', '') for i in o if i.replace('\r', '') != '']
devs = []
if len(lines) >= 2 and lines[1].find('\t') > 0:
   devs.append( lines[1].split('\t')[0] )

print (devs)


def getPort(devs, index):
    cmd = "adb -s {} shell netstat -a".format(devs[index])
    print cmd
    o = subprocess.check_output(cmd, shell=True)
    o = o.split('\n')
    lines = [ l for l in o if l.find('LISTEN') >= 0]  # remove all Not listen port
    lines = [ i.replace('\r', '') for i in o if i.find('localhost') > 0 or i.find('127.0.0.1') > 0]
    line = lines[0]
    line = [ l.replace(' ', '') for l in line.split(':') if len(l.replace(' ','')) >0 ]
    if len(line) > 0:
        print( line[1] )
        return line[1]
    return -1
 
ports = []
for i in range(len(devs)):
   p = getPort(devs,i)
   if p != -1:
       ports.append( (devs[i], p) )

print ("ports {}".format(ports))

# dev likes 'FOTGLMD5B1703350', p likes 48545
for index, pair in zip(range(len(ports)), ports):
   dev, p = pair
   print (index, dev, p)
   cmd = "adb -s {} forward tcp:5432{} tcp:{}".format(dev, index, p)
   print "cmd is {}".format(cmd)
   o = subprocess.check_output(cmd, shell = True)
   print o


if __name__ == "__main__":
   cmd = '''python -c "import android; a = android.Android(('localhost', 54320));a.makeToast('hello,world')"'''
   o = subprocess.check_output(cmd, shell = True)

   
   
