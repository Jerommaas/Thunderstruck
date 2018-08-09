

'''
Test using client and server

start up server, than 2 clients
let them both send and receive some stuff
'''

from sys import path
from os import getcwd
import time

path.append(getcwd() + "\\..\\..\\Tools\\game_config\\")  # TODO(victor): check if indeed windows
from config import Config

path.append(getcwd() + "\\..\\..\\Tools\\game_config\\")  # TODO(victor): check if indeed windows
from client import Client
from server import Server
from panda3d.core import NetDatagram 
from panda3d.core import Datagram

class TestServer(Server):
    ''' Test sending a heartbeat to clients every second '''
    def __init__(self, host="localhost", port=5001 ):
        super().__init__(host=host, port=port )

        # add heartbeat task

    def heartbeat(self ):     
        myPyDatagram=Datagram()   
        print("server: sending heartbeat to {} clients".format(len(self.activeConnections) ) )
        self.BroadcastMessage( myPyDatagram )


if __name__ == "__main__":


    config = Config()

    port = 5001

    server = TestServer( port=port, host=config["server"]["host"] )

    # NOTE: start server before trying to connect with the clients

    client1 = Client(port=port, host=config["client"]["host"] )
    client2 = Client(port=port, host=config["client"]["host"] )

    
    tStart = time.time() 
    tLastHearbeat = tStart
    while time.time() < tStart + 10:
        taskMgr.step()
        if tLastHearbeat +1 < time.time():
            server.heartbeat()
            tLastHearbeat = time.time()
    

    client1.Close()
    client2.Close()

    server.Close()

    # close