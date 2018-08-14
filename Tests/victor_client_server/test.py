

'''
Test using client and server

start up server, than 2 clients
let them both send and receive some stuff
'''

from sys import path
from os import getcwd
import time

path.append(getcwd() + "\\..\\..\\Tools\\game_config\\")  
from config import Config

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

    def ProcessReaderData(self, data): 
        # Todo: figure out who sent it
        print("Server: receiving data")


class TestClient(Client):   
    ''' Test receiving heartbeat from server ''' 
    def ProcessReaderData( self, data ):
        print("{}: reading data!".format(self.name) )
        pass

    def SendMessage(self): 
        print( "{}: sending message to server".format(self.name) )
        myPyDatagram=Datagram() 
        self.cWriter.send(myPyDatagram,self.myConnection)


if __name__ == "__main__":


    config = Config()

    port = config["server"]["port"]
    host = config["server"]["host"]

    # start server and clients
    server = TestServer( port=port, host=host )
    client1 = TestClient(port=port, host=host, name="Henk" )
    client2 = TestClient(port=port, host=host, name="Bert" )

    # run test
    # TODO(vicdie): run server and clients in separate threads, 
    # move Task.TaskManager().step() stuff 
    print("======= Server->Client =======")

    tStart = time.time() 
    tLastHearbeat = tStart
    while time.time() < tStart + 10:
        Task.TaskManager().step() # perform a step as often as possible
        if tLastHearbeat + 1 < time.time():
            server.heartbeat()
            tLastHearbeat = time.time()
    
    print("======= Client->Server =======")

    tStart = time.time() 
    tLastHearbeat = tStart
    while time.time() < tStart + 10:
        Task.TaskManager().step() # perform a step as often as possible
        if tLastHearbeat + 1 < time.time():
            client1.SendMessage()
            client2.SendMessage()
            tLastHearbeat = time.time()

    # close
    client1.Close()
    client2.Close() 
    server.Close()
