

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

from pandac.PandaModules import loadPrcFileData
loadPrcFileData("", "window-type none")
from direct.directbase import DirectStart
from direct.task import Task
 
from panda3d.core import NetDatagram

class Client(object):
    def __init__( self, host="localhost", port=5001, name="client"): 
        self.name = name
        
        self.cManager = QueuedConnectionManager()
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager,0)
        
        # how long until we give up trying to reach the server?
        timeout_in_miliseconds=3000  # 3 seconds
        
        self.myConnection=self.cManager.openTCPClientConnection(host,port,timeout_in_miliseconds)
        if not self.myConnection:
            print("client: Failed to connect to server!")
            return

        self.cReader.addConnection(self.myConnection)  # receive messages from server
        taskMgr.add(self.tskReaderPolling,"Poll the connection reader",-40)
        print("client: Successfully connected to server {} at {}!".format(port,host) )
 
        
    def tskReaderPolling(self,taskdata):
        # reader callback
        # print("client: tskListenerPolling() callback!")
        if self.cReader.dataAvailable():
            datagram=NetDatagram()  # catch the incoming data in this instance
            # Check the return value; if we were threaded, someone else could have
            # snagged this data before we did
            if self.cReader.getData(datagram): 
                self.ProcessReaderData( datagram )
        return Task.cont

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
