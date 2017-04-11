import sys

"""
andorid.py 
example: python -c "import android; a = android.Android(('localhost', 54321));a.makeToast('hello,world')"
api: http://www.mithril.com.au/android/doc/BluetoothFacade.html

atom
{'params': ('hello,world',), 'id': 0, 'method': 'makeToast'}

a.checkBluetoothState()
a._rpc('checkBluetoothState')
Result(id=0, result=True, error=None)
a.bluetoothMakeDiscoverable(2)
a._rpc( 'bluetoothMakeDiscoverable',2 )

MainThread	21:55:02:986	{'params': ('hello,world',), 'id': 0, 'method': 'makeToast'}	
MainThread	21:55:02:986	{u'error': None, u'id': 0, u'result': None}	
MainThread	21:55:26:114	{'params': (), 'id': 0, 'method': 'makeToast'}	
MainThread	21:55:26:114	{u'error': u'com.googlecode.android_scripting.rpc.RpcError: Argument 1 is not present', u'id': 0, u'result': None}	

MainThread	22:10:57:317	{'params': (), 'id': 0, 'method': 'checkBluetoothState'}	
MainThread	22:10:57:317	{u'error': None, u'id': 0, u'result': True}	
MainThread	22:12:23:572	{'params': (1,), 'id': 1, 'method': 'bluetoothMakeDiscoverable'}	
MainThread	22:12:23:572	{u'error': None, u'id': 1, u'result': None}	
MainThread	22:12:33:883	{'params': (1,), 'id': 2, 'method': 'bluetoothMakeDiscoverable'}	
MainThread	22:12:33:883	{u'error': None, u'id': 2, u'result': None}	
"""

import android

gDevs = []
gDevs.append( android.Android( ('localhost', 54320 )) )

def run1(*l,**d):
    print("run1 of run_sl4a")
    print("list:{}".format(repr(l)))
    print("dict:{}".format(repr(d)))
    l = l[0]
    print(type(l[0]))
    print(repr(l[0]))
    # l is id, method, all parameters
    try:
        import android
        index = int(l[0])
        if index > 54320:
           index = index - 54320 
        a = gDevs[index] # android.Android( ('localhost', int(l[0])) )
        k = l[2:]
        print ( k)
        a._rpc(l[1], *k)
    except:
        print(sys.exc_info())


"""
performance: first time 1.027 seconds, second time 0.007
MainThread	22:45:01:883	begin: 1.49192190188e+15	
MainThread	22:45:01:883	runCommand: sl4a_hello	
MainThread	22:45:01:883	self.name sl4a_hello	
MainThread	22:45:01:884	codetext is:import run_sl4a;run_sl4a.run1(['54320', 'makeToast', 'c-hello~'])	
MainThread	22:45:02:909	end: 1027000.0	
MainThread	22:45:09:428	runOneNode	
MainThread	22:45:09:429	begin: 1.49192190943e+15	
MainThread	22:45:09:429	runCommand: sl4a_hello	
MainThread	22:45:09:429	self.name sl4a_hello	
MainThread	22:45:09:430	codetext is:import run_sl4a;run_sl4a.run1(['54320', 'makeToast', 'c-hello~'])	
MainThread	22:45:09:436	end: 7000.0	
MainThread	22:45:12:947	runOneNode	
MainThread	22:45:12:947	begin: 1.49192191295e+15	
MainThread	22:45:12:947	runCommand: sl4a_hello	
MainThread	22:45:12:947	self.name sl4a_hello	
MainThread	22:45:12:947	codetext is:import run_sl4a;run_sl4a.run1(['54320', 'makeToast', 'c-hello~'])	
MainThread	22:45:12:952	end: 5000.0	
"""
    