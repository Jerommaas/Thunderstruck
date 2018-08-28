# python packages
from sys import path
from os import getcwd
import time
import json 

# client / server
from panda3d.core import QueuedConnectionManager
from panda3d.core import QueuedConnectionListener
from panda3d.core import QueuedConnectionReader
from panda3d.core import ConnectionWriter

# other panda stuff
from panda3d.core import *
from panda3d.direct import *
from panda3d.core import NetDatagram
from panda3d.core import Datagram
from panda3d.core import PointerToConnection
from panda3d.core import NetAddress
from panda3d.core import loadPrcFileData
loadPrcFileData("", "window-type none")
from direct.task import Task 
 
# self made packages
from NetworkObject import NetworkObject, NetworkEvent, NetworkPerson, eventTextmessage
path.append(getcwd() + "\\..\\..\\Tools\\game_config\\")
# from config import Config


class ClientServerBase(object):
    '''
    Baseclass for client and server, 
    these two have almost all functionality similar, except for who is responsible for opening / closing connections
    and the fact that server can have multiple connections
    '''
    def __init__(self, host="localhost", port=5001, name="client or server" ):
        self.name = name
        self.port = port
        self.host = host
        
        self.cManager = QueuedConnectionManager()
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager,0)
        
        self.connections = []       # list of connections, contains 1 item for client, multiple for server
        
        self.readerCallback = None # will be called when a new message arrives
        self.writerCallback = None # will be called when a message needs to be constructed

        self.taskMgr = Task.TaskManager()
        self.taskMgr.add(self.tskReaderPolling,"Poll the connection reader",-40)
        self.taskMgr.add(self.tskWriterPolling,"Send data package",-39)


    def setReaderCallback( self, callbackFunction ):
        self.readerCallback = callbackFunction 

    def setWriterCallback( self, callbackFunction ):
        self.writerCallback = callbackFunction 
        
    def tskReaderPolling(self,taskdata):

        # reader callback 
        if not self.cReader.dataAvailable():
            # print( "tskReaderPolling(): no data available!" )
            return Task.cont

        datagram=NetDatagram()  
        if not self.cReader.getData(datagram): 
            print( "tskReaderPolling(): cannot claim data!" )
            return Task.cont

        if self.readerCallback:
            print( "tskReaderPolling():readerCallback()" )
            self.readerCallback( datagram ) 
            
        return Task.cont

    def tskWriterPolling( self , data ): 
        
        if not self.writerCallback:
            return Task.cont

        data = self.writerCallback()
        if data == None:
            return Task.cont
            

        assert(isinstance(data,Datagram))

        print( "tskWriterPolling() sending to : {}".format(len(self.connections) ))

        for con in self.connections:
            if con:
                print( "tskWriterPolling() sending" )
                self.cWriter.send(data,con)

        return Task.cont
 

    def Close( self ):
        # close each of the connections
        for c in self.connections:
            self.cManager.closeConnection(c) 

    def ProcessReaderData( self, data ): 
        raise NotImplementedError("overwrite ProcessReaderData() in client/server implementation")


class Client(ClientServerBase):
    def __init__( self, host="localhost", port=5001, name="client"): 
        super().__init__( host=host, port=port, name=name)
        # self.setReaderCallback( sel.ProcessReaderData )

        timeout_in_miliseconds=3000  # 3 seconds
        self.connections.append( self.cManager.openTCPClientConnection(self.host,self.port,timeout_in_miliseconds) )
        if not self.connections:
            print("{}: Failed to connect to server!".format(self.name) )
            return
            
        for con in self.connections:
            if con:
                self.cReader.addConnection(con) 
            else:
                print( "failed to add connection!" )

        self.taskMgr.add(self.tskReaderPolling,"Poll the connection reader",-40)


class Server(ClientServerBase): 
    def __init__( self, host="localhost", port=5001 , name="server" ):
        super().__init__( host=host, port=port, name=name)
        # self.setReaderCallback( sel.ProcessReaderData )

        backlog=1000 
        self.tcpSocket = self.cManager.openTCPServerRendezvous(port,backlog)
        self.cListener = QueuedConnectionListener(self.cManager, 0)
        self.cListener.addConnection(self.tcpSocket)

        self.taskMgr.add(self.tskListenerPolling,"Poll the connection listener",-39) 
 
    def tskListenerPolling(self,taskdata): 
        if self.cListener.newConnectionAvailable(): 
            rendezvous = PointerToConnection()
            netAddress = NetAddress()
            newConnection = PointerToConnection()
            if self.cListener.getNewConnection(rendezvous,netAddress,newConnection):
                newConnection = newConnection.p()
                self.connections.append(newConnection) # Remember connection
                self.cReader.addConnection(newConnection)     # Begin reading connection
                print("server: received new connection!")
        return Task.cont

    # TODO(victor): what happens when a connection drops away?

    def BroadcastMessage(self, datagram):
        # send the same message to all clients
        for con in self.connections:
            self.cWriter.send(datagram,con)
            
    # def ProcessReaderData( self, data ):
    #     # TODO(vicdie): overwrite in derived classes 
    #     pass

    def Close( self ):
        # remove all clients
        for con in self.connections:
            self.cReader.removeConnection(con)
        self.connections=[]
        self.cManager.closeConnection(self.tcpSocket)


'''
NOTE: base network manager
contains functions for packing all managed objects in a string
and extracting objects from this string

The functions for sending and receiving new objects are almost identical on server and client side
'''

class NetworkManager(object):
    ''' 
    Network manager baseclass, 
    Defines the interface of derived objects, takes care of all generic stuff
    '''

    class MessageEnum:
        EVENT = 1
        CONSTRUCT = 2
        UPDATE = 3
        DESTRUCT = 4

    def __init__(self, client_or_server):
        self.client_or_server = client_or_server

        self.eventQueue = []    # events which will need to be sent in the next event update
        self.newObjectQueue = [] # objects for which a construction message needs to be sent
        self.destructObjectQueue = [] # objects for which a destruction message needs to be sent
        
        self.client_or_server.setReaderCallback( self.readerCallback )
        self.client_or_server.setWriterCallback( self.writerCallback )
        
        self.managedNetworkObjects = [] # objects owned by this NetworkManager
        self.sharedNetworkObjects = dict() # self.clientNetworkObjects[connection] = dict(id, object)
        self.receivedNetworkEvents = dict() 

    def readerCallback( self, data ):
        print("reader callback!" )
        # data contains two fields: 1 containing the message type (EVENT, CONSTRUCT, UPDATE, DESTRUCT)
        # the other is a string, containing the actual data (in json format for now)
        sender = data.getConnection()
        iterator = DatagramIterator(data)
        messageEnum = iterator.getUint8()

        if not sender in self.receivedNetworkEvents:
            self.receivedNetworkEvents[sender] = []

        if messageEnum == NetworkManager.MessageEnum.EVENT:
            # received an event message
            messageString = iterator.getString()
            messageJsonData = json.loads( messageString )
            for obj in messageJsonData: 
                # class_type = globals()[ obj["class_name"]  ] #introspection
                # class_instance = class_type( data=obj ) 
                class_instance = globals()[obj["class_name"]]( data=obj ) 
                print( "received event: {}".format(class_instance) )
                # Add new event to list, keep track of who sent it (sender)
                self.receivedNetworkEvents[sender].append( class_instance )


    def writerCallback( self ):

        # if there are no events queued, return None
        if not self.eventQueue:
            return None

        # collect data
        data = []
        for event in self.eventQueue: 
            data.append( event.toMessage() )
        self.eventQueue = []

        # make a message for the events
        myPyDatagram=Datagram() 
        myPyDatagram.add_uint8( NetworkManager.MessageEnum.EVENT )
        datastring = json.dumps(data) 
        print( datastring )
        myPyDatagram.add_string(datastring)

        print("server: writer callback")
        return myPyDatagram

    def add(self, newObject ):
        self.managedNetworkObjects.append( newObject )
        self.newObjectQueue.append( newObject)
        # self.sendNewObject(newObject)
        print("NetworkManager: added object! {}".format(newObject) ) 

    def remove( self, removeObject ):
        self.managedNetworkObjects.remove( removeObject )
        self.destructObjectQueue.append( removeObject )
        print("NetworkManager: removed object! {}".format(removeObject) ) 

    def addEvent( self, event ):
        assert(isinstance(event,NetworkEvent)) # check correct type
        self.eventQueue.append(event) 
        print("NetworkManager: sending new event! {}".format(event) ) 
    

'''
NOTE: client and server network manager are almost identical. 
The client implementation also gets a dictionary with connections, even though there is only one (server)
This is to keep the underlying code exactly the same, so that as much of the code as possible is shared between client and server
'''

class ClientNetworkManager(NetworkManager):
    def __init__(self, client):
        super().__init__(client)

    def addEvent( self, event ):
        super().addEvent( event )
        # TODO(victor): Do client specific stuff when a new event is sent

    def readerCallback( self, data ):
        super().readerCallback( data )
        print("ClientNetworkManager: reader callback" ) 
        # TODO(victor): Do client specific stuff when new data arrives

class ServerNetworkManager(NetworkManager):
    def __init__(self, server):
        super().__init__(server)

    def addEvent( self, event ):
        super().addEvent( event )
        # TODO(victor): Do server specific stuff when a new event is sent

    def readerCallback( self, data ):
        super().readerCallback( data )
        print("ServerNetworkManager: reader callback" ) 
        # TODO(victor): Do server specific stuff when new data arrive




'''
'''



if __name__ == "__main__":
    
    server = Server()
    serverManager = ServerNetworkManager(server)

    client = Client()
    clientManager = ClientNetworkManager(client)

    # TODO(victor): maybe we want to provide the networkobject with the sendingNetworkManager that it belongs to
    # This way, when the object is destructed, we don't need to tell the network manager about it
    person1 = NetworkPerson() 

    # TODO(vicdie): this is needed for as long as client and server are not separately running 
    # a static field can be added to the NetworkObject, which points to the NetworkManager where new ones need to register
    serverManager.add( person1 )
    # make some changes to person1
    serverManager.remove( person1 )

    # make sure the receiving side obtains a new NetworkPerson and a text message

    b_send = True

    tStart = time.time()  
    while time.time() < tStart + 2:

        if time.time() > tStart + 1 and b_send:
            b_send = False 
            textMessage = eventTextmessage( "server says hoi" )
            serverManager.addEvent( textMessage ) 
            textMessage2 = eventTextmessage( "server says dag" )
            serverManager.addEvent( textMessage2 )

        Task.TaskManager().step() # perform a step as often as possible

    print("bla")