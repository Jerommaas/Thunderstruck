from direct.showbase.ShowBase import ShowBase

# Als je nieuwe modules hebt voor bij *, voeg de verwijzing 
# toe in __init__.py van de module!
from Controls import *
from Entities import * 
from Entities.Objects import *

class Thunderstruck_server():
    def __init__(self):
        pass

        # Entities
            # Load terrain hgtmap
            # Load Objects 
        
        # Game Logic
            # Receive control input from client
            # Game Goals/Rules

        # Physics
            # Define truck behavior

        # Output
            # Send data to clients

class Thunderstruck_client(ShowBase):
    def __init__(self,server):
        ShowBase.__init__(self)

        # Init the Global Clock
        self.Clock = Clock.Clock(self)

        # ----- ENTITIES -----
        # World
        self.Terrain = Terrain.Terrain()
        self.SkyDome = skyDome.skyDome()
        #Light Sources?
        
        # Objects
        self.Truck1 = Trucks.Basic(self)
        
        # Particles
           # Sparks, fire, LIGHTNING

        self.Camera = Camera.Camera(self)
        # User input
        self.CM = Manager.ControlManager(self)

        # Server communication
            # Send User controls
            # Receive Trucks locations

        # Graphics
            # Renderer
            # Camera behavior
            # GUI frontend

        # Sound
            # Music Player
            # Sound effects

if __name__ == "__main__":
    server = Thunderstruck_server()
    #server.run()

    client  = Thunderstruck_client(server)
    client.run()