'''
Server test class
'''
from sys import path
from os import getcwd
import time

path.append(getcwd() + "\\..\\..\\Tools\\game_config\\")  # TODO(victor): check if indeed windows
from config import Config

from panda3d.core import QueuedConnectionManager
from panda3d.core import QueuedConnectionListener
from panda3d.core import QueuedConnectionReader
from panda3d.core import ConnectionWriter

# 
from panda3d.core import PointerToConnection
from panda3d.core import NetAddress

from panda3d.core import loadPrcFileData
loadPrcFileData("", "window-type none")
# from direct.directbase import DirectStart
# from direct.showbase.ShowBase import ShowBase
from direct.task import Task 
 
from panda3d.core import NetDatagram
from panda3d.core import Datagram
 
class Server(object):
    
    # https://www.panda3d.org/manual/index.php/Client-Server_Connection
    
    def __init__( self, host="localhost", port=5001 ):
        taskMgr = Task.TaskManager()

        self.cManager = QueuedConnectionManager()
        self.cListener = QueuedConnectionListener(self.cManager, 0)
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager,0) 
        self.activeConnections = [] # We'll want to keep track of these later
        self.readerCallbacks = []

        backlog=1000 #If we ignore 1,000 connection attempts, something is wrong!
        self.tcpSocket = self.cManager.openTCPServerRendezvous(port,backlog)
        self.cListener.addConnection(self.tcpSocket)

        taskMgr.add(self.tskListenerPolling,"Poll the connection listener",-39)
        taskMgr.add(self.tskReaderPolling,"Poll the connection reader",-40)
        print("started server! ({} at {})".format(port,host) )

    def Start( self ):
        # derived servers can overwrite this function if needed
        pass

    def tskListenerPolling(self,taskdata):
        # listen for new connections
        # TODO(victor): what happens if a client shuts down?
        # print("server.tskListenerPolling()")
        if self.cListener.newConnectionAvailable(): 
            rendezvous = PointerToConnection()
            netAddress = NetAddress()
            newConnection = PointerToConnection()
            if self.cListener.getNewConnection(rendezvous,netAddress,newConnection):
                newConnection = newConnection.p()
                self.activeConnections.append(newConnection) # Remember connection
                self.cReader.addConnection(newConnection)     # Begin reading connection
                print("server: received new connection!")
        return Task.cont
        
    def tskReaderPolling(self,taskdata):
        # reader callback 
        if not self.cReader.dataAvailable():
            return Task.cont
             
        # catch the incoming data in this instance
        # Check the return value; if we were threaded, someone else could have
        # snagged this data before we did
        datagram=NetDatagram()  
        if not self.cReader.getData(datagram): 
            return Task.cont

        for callback in self.readerCallbacks:
            callback( datagram ) 
            
        return Task.cont
        
    def addReaderCallback( self, callbackFunction ):
        self.readerCallbacks.append( callbackFunction )

    def BroadcastMessage(self, datagram):
        # send the same message to all clients
        for client in self.activeConnections:
            self.cWriter.send(datagram,client)

    def Close( self ):
        # remove all clients
        for client in self.activeConnections:
            self.cReader.removeConnection(client)
            self.activeConnections=[]
 
        # close down our listener
        self.cManager.closeConnection(self.tcpSocket)



if __name__ == "__main__":

    print("=== Start ===")

    config = Config()

    server = Server( port=config["server"]["port"], host=config["server"]["host"] )
    server.Start()

    tStart = time.time()
    while time.time() < tStart + 10:
        pass

    # close
    server.Close()
    print("=== Done! ===")
