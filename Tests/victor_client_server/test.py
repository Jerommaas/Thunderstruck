

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

from direct.task import Task 

class TestServer(Server):
    ''' Test sending a heartbeat to clients '''
    def __init__(self, host="localhost", port=5001 ):
        super().__init__(host=host, port=port )

    def heartbeat(self ):     
        myPyDatagram=Datagram()   
        print("server: sending heartbeat to {} clients".format(len(self.activeConnections) ) )
        self.BroadcastMessage( myPyDatagram )


class TestClient(Client):    
    def ProcessReaderData( self, data ):
        # TODO(vicdie): overwrite in derived classes
        print("{}: reading data!".format(self.name) )
        pass



if __name__ == "__main__":


    config = Config()

    port = 5001
    host = config["server"]["host"]

    # start server and clients
    server = TestServer( port=port, host=host )
    client1 = TestClient(port=port, host=host, name="Henk" )
    client2 = TestClient(port=port, host=host, name="Bert" )

    # run test
    tStart = time.time() 
    tLastHearbeat = tStart
    while time.time() < tStart + 10:
        Task.TaskManager().step() 
        if tLastHearbeat + 1 < time.time():
            server.heartbeat()
            tLastHearbeat = time.time()
    

    # close
    client1.Close()
    client2.Close() 
    server.Close()
