
'''
Class containing all functions for sharing an object state between client and server, in either direction

This class has no knowledge of weither it is client or server side, 
nor in which direction the info is flowing
'''

import json


class NetworkObject(object):
    
    MAX_NETWORK_OBJECTS_COUNT = 1000

    objectList = dict() # all objects, sending and receiving

    pendingObjectList = [] # newly created objects, will be removed by network manager 
    networkObjectId = 0 # hold the id of any new NetworkObject

    def __init__(self): 
        self.class_name = self.__class__.__name__  
        # NOTE: make sure derived objects can be default constructed! (no arguments in init except optional ones)
        NetworkObject.addObject(self)

    @staticmethod
    def addObject(obj):
        # TODO(victor): looping over all objects is not efficient, but will work for now 
        NetworkObject.pendingObjectList.append(obj)
        for i in range( NetworkObject.MAX_NETWORK_OBJECTS_COUNT ):
            if not ( i in NetworkObject.objectList ):
                # id is not yet used
                NetworkObject.objectList[i] = obj
                break
        else:
            print("NetworkObject.addObject(): no index available!")

    def toConstructMessage(self):
        # convert this object to some string representation
        return ""

    def fromConstructMessage(self, datastring):
        # convert a string representation into an object
        pass

    def toUpdate(self):
        # returns a string if an update was requried, 
        # this string contains the update data
        # otherwise, returns None
        return None

    def fromUpdate( self, datastring ):
        # overwrite in derived class, apply updates to variables
        # by default, simply apply the json data to the dict
        # objects which are sending lots of updates might need a more effcient method
        self.__dict__.update( json.loads(datastring) ) 


    def remove(self):
        # TODO(vicdie): alert the NetworkManager that this object needs to be removed
        raise NotImplementedError("NetworkObject.remove() not implemented!")


class NetworkEvent(object):
    def __init__(self, data=None): 
        self.class_name = self.__class__.__name__
        if data:
            self.fromMessage(data)
    def toMessage(self):
        return self.__dict__ 
    def fromMessage(self, data):
        self.__dict__.update( data )

'''
Testclasses for NetworkObject and NetworkEvent
'''
        
class NetworkPerson(NetworkObject):
    def __init__(self, name="<geen idee>", age=0, posx=0, posy=0 ):
        # NOTE: this object is default constructable, none of the arguments is required
        super().__init__()
        
        self.name = name 
        self.age = age
        self.posx = posx
        self.posy = posy
        
    def toConstructMessage(self):
        # convert this object to some dict representation 
        return self.__dict__  

    def fromConstructMessage(self, data):
        # convert a dict representation into an object
        self.__dict__.update(data) 

    def toUpdateMessage(self):
        # returns a dict containing the data if an update for this object was requried,  
        # otherwise, returns None
        return { "age": self.age}

    def fromUpdateMessage( self, data ):
        # overwrite in derived class, apply updates to variables
        self.__dict__.update( data )

    def __repr__(self):
        return "<networkPerson: name:{}, age:{}, x:{}, y:{}>".format(self.name, self.age, self.posx, self.posy)

class eventTextmessage(NetworkEvent):
    def __init__(self, message=None, data=None):
        super().__init__(data=data)
        if data==None:
            # only set variables if no message data was used
            self.message = message
    def __repr__(self):
        return "<eventTextMessage: {}>".format(self.message)
    def toMessage(self):
        return self.__dict__ 
    def fromMessage(self, data):
        self.__dict__.update( data )




if __name__ == "__main__":

    serverPerson = NetworkPerson( name="Henk", age=27, posx=3.14, posy=2.71 )
    message = serverPerson.toConstructMessage()
    clientPerson = NetworkPerson()
    clientPerson.fromConstructMessage( message )

    print( "\n=== construct ===" )
    print( serverPerson )
    print( message )
    print( clientPerson )

    serverPerson.age = 28
    updateMessage = serverPerson.toUpdateMessage() 
    clientPerson.fromUpdateMessage( updateMessage )

    print( "\n=== update ===" )
    print( serverPerson )
    print( updateMessage )
    print( clientPerson )