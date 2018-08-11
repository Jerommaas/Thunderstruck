from direct.showbase.ShowBase import ShowBase
import Entities.Terrain as Terrain
import Entities.skyDome as skyDome

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

        # Entities
        Terrain.Build()
        skyDome.Build()
            # Load terrain
                # Skybox
                # Weather
                # Lighting
            # Objects
            # Particles
                # Sparks, fire, LIGHTNING

        # User input
            # Controls- key bindings

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