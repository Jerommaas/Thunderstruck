

'''
Client test class
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

class Client(object):
    def __init__( self, host="localhost", port=5001, name="client"): 
        self.name = name
        
        self.cManager = QueuedConnectionManager()
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager,0)
        
        self.readerCallbacks = []

        taskMgr = Task.TaskManager()
        
        # how long until we give up trying to reach the server?
        timeout_in_miliseconds=3000  # 3 seconds
        
        self.myConnection = self.cManager.openTCPClientConnection(host,port,timeout_in_miliseconds)
        if not self.myConnection:
            print("{}: Failed to connect to server!".format(self.name) )
            return

        self.cReader.addConnection(self.myConnection)  # receive messages from server
        taskMgr.add(self.tskReaderPolling,"Poll the connection reader",-40)
        print("{}: Successfully connected to server {} at {}!".format(self.name,port,host) )
 
        
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

    def ProcessReaderData( self, data ):
        # TODO(vicdie): overwrite in derived classes 
        pass

    def Close( self ):
        # close connection if it exists
        if self.myConnection:
            self.cManager.closeConnection(self.myConnection)





if __name__ == "__main__":

    print("=== Start ===")

    config = Config()

    client = Client( port=config["server"]["port"], host=config["server"]["host"] )

    tStart = time.time()
    while time.time() < tStart + 10:
        pass

    # close
    client.Close()
    print("=== Done! ===")
