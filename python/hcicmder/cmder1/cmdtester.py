


#python test 2 


import threading
import time
import sys

def gettid():
    return "["+ str(threading.get_ident())+"] "

class User(threading.Thread):
    def __init__(self, name, opcode = None, device = None):
        threading.Thread.__init__(self)
        self._name = name + " user"
        self._opcode = opcode
        self._device = device
        self.start()
        
    def run(self):
        # send a command and wait its' complete
        time.sleep(3)
        print(gettid() + self._name + "befoe sendCmd")
        r = self._device.sendCmd(self._opcode)
        print(gettid() +self._name + "after sendCmd")
        r.wait_status()
        print(gettid() +self._name + "after status-ed")
        r.wait_complete()
        print(gettid() +self._name + "after complete-ed")

        
class HciCmdSession():
    def __init__(self, cmder = None, opcode = 0):
        self.cmder = cmder
        self.event = threading.Condition()
        self._status = threading.Event()
        self._complete = threading.Event()
        self._state = 0 # 0 -> 1 -> 2
        self._opcode = opcode
        
    def wait_status(self):
        cv = self._status
        cv.wait()
        print(gettid() +self._opcode + "end of wait_status()")
        
    def wait_complete(self, check_func = None, timeout = 0):
        # Consume one item
        cv = self._complete
        cv.wait()
        print(gettid() +self._opcode + "end of wait_complete()")

    def state(self):
        return self._state
        
    def handle_status(self):
        # Produce one item
        cv = self.event
        cv.acquire()
        self._status.set()
        self._state = 1
        print(gettid() + "{} is status-ed!".format(self._opcode))
        cv.release()
        
    def handle_complete(self):
        cv = self.event
        cv.acquire()
        self._complete.set()
        self._state = 2
        print(gettid() + "{} is completed!".format(self._opcode))
        cv.release()
"""
Hci commands cannot send multiple times without wait-for status back (allow-command)
A session is about 
"""
class HciCmder(threading.Thread):
    def __init__(self, device, fakeRx = None):
        threading.Thread.__init__(self)
        self.device = device
        # only allow 1 cmd sent ! wait until release
        self.cmdLock = threading.Condition()
        self.runEvent = threading.Event()
        self._lock = threading.Condition()
        self.state = 0
        self.count = 0
        self.fakeRx = fakeRx
        self.sessions = []
        
    def sendCmd(self, data):
        self.cmdLock.acquire()
        r = HciCmdSession(cmder = self, opcode = data)
        self.sessions.insert(0, r)
        self.cmdLock.release()
        return r
    def dumpSessions(self):
        print(gettid() +"-" * 10)
        self.cmdLock.acquire()
        for i in range(len(self.sessions)):
            s1 = self.sessions[i]
            print(gettid() +"{}: opcode:{} state:{}".format(i, s1._opcode, s1.state()))
        self.cmdLock.release()
        print(gettid() +"-" * 10)
    def open(self):
        if self.state != 0:
            raise Exception("has open !")
        self.device.open()
        self.start()
        self._lock.acquire()
        self.state = 1
        self._lock.release()
        
    def close(self):
        #todo: break the run loop
        self.stop()
        print(gettid() +"before join")
        self.join()
        print(gettid() +"after join")
        self.device.close()
    def stop(self):
        self.runEvent.set()
        self._lock.acquire()
        self.state = 0
        self._lock.release()
        
    def run(self):
        # read data from bus 
        print(gettid() +"HciCmder: run " + self.device.name )
        while not self.runEvent.is_set():
            # read data from bus until is is fail
            data = self.device.rx()
            if data == None:
                self.runEvent.wait(3)
            else:
                print(gettid() +"trigger a previous hci-session")
                self.cmdLock.acquire()
                for i in range(len(self.sessions)-1, -1, -1):
                    if self.sessions[i].state() == 0:
                        print( gettid() +"{} to handle_status({})".format(self.sessions[i]._opcode, data))
                        self.sessions[i].handle_status()
                        break
                    elif self.sessions[i].state() == 1:
                        print( gettid() +"{} to handle_complete({})".format(self.sessions[i]._opcode, data))
                        self.sessions[i].handle_complete()
                        break
                self.cmdLock.release()
                print(gettid() +"trigger a previous hci-session - done")
                
            print(gettid() +"HciCmder: runEvent is not set yet. do recive " + str(self.count) )
            self.count += 1
            #if self.fakeRx != None and random.Random().random() > 0.3: # 1/3 chance to fake a data
            #    self.device._fakeData("fake-" + str(self.count))
        print(gettid() +"HciCmder: run finished " + self.device.name )
        
class Device():
    def __init__(self, name = "unkown", config = None, bus = None):
        self.name = name
        self.config = config
        self.bus = bus
        self.readLock = threading.Lock()
        self.dataset = []
        
    def rx(self):
        # // keep a loop to receive data form 
        self.readLock.acquire()
        if len(self.dataset) > 0:
            data = self.dataset.pop()
        else:
            data = None
        self.readLock.release()
        return data
    def tx(self, data):
        time.sleep(1 + 1 * len(data))
        return None
    def _fakeData(self, data):
        self.readLock.acquire()
        self.dataset.insert(0, data)
        self.readLock.release()
    def open(self):
        return True
    def close(self):
        return False
    
d1 = Device("d1")
d2 = Device("d2")
cmder1 = HciCmder(d1, fakeRx = True)
#cmder2 = HciCmder(d2)
cmder1.open()
#cmder2.oopen()
cmder2 = HciCmder(d2)
print("open done")
#a = cmder1.sendCmd(data)
#print("send done")
#a.wait_complete()
print("complete done")

u1 = User('mike', 'm1', cmder1)

print (gettid() +"a1 to fake response")
print (gettid() +"b1 to send a command")
print (gettid() +"d to dump sessions")
threading.get_ident()

if True:
  try:
    print("print 'q' to exit ! ")
    i = input()
    while (i != "q"):
        if i[0] == 'a':
            d1._fakeData(i)
        if i[0] == 'b':
            cmder1.sendCmd(i)
        if i[0] == 'd':
            cmder1.dumpSessions()
        print(gettid() +"print 'q' to exit ! ")
        print(gettid() +"input is:" + i)
        time.sleep(1)
        i = input()
    print(gettid() +"exit interactive")
    cmder1.stop()
  except:
    e = sys.exc_info()
    print(e[0], e[1], e[2])
cmder1.close()