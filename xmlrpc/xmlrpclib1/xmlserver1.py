import signal
import threading
from examplelibrary import ExampleLibrary
from robotremoteserver import RobotRemoteServer

server = RobotRemoteServer(ExampleLibrary(), port=8888)
signal.signal(signal.SIGINT, lambda signum, frame: server.stop())
server_thread = threading.Thread(target=server.serve)
server_thread.start()
while server_thread.is_alive():
    server_thread.join(0.1)