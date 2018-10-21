


import sys

# Panda 
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

# local
import main
import data_object


P3D_WIN_WIDTH = 720
P3D_WIN_HEIGHT = 560

#
# This class manages all objects in the scene, loads/saves, etc.
#

import json
class PandaLoader(object):
    def __init__(self, world):
        self.world = world 
        self.objects = []

    def load_scene(self, file):
        print( "PandaLoader.load_scene():\n\t{}".format( file  ) )
        self.world.loadInitialEnv() # TEMP
        world = self.world # shorthand
        with open(file) as f:
            data = json.load(f)
            self.json_data = data
            world.name = data.get('name', '<world name>') 
            world.version = data.get('version', 0) 


    def save_scene(self, file):
        print( "PandaLoader.save_scene():\n\t{}".format( file  ) ) 
        world = self.world
        data = self.json_data
        data["version"] = world.version+1
        data["name"] = world.name
        with open(file, "w") as f:
            json.dump(data, f, indent=4)

    def load_object(self, file):
        obj = data_object.data_object()
        self.objects.append( obj )
        return obj

  
#
# this class constructs the panda frame, used for visualizing the current world
#  

class World(ShowBase):   
    def __init__(self):
        ShowBase.__init__(self) 
        self.loader = PandaLoader(self)
        # self.loadInitialEnv() # re-enable once gui is done
        self.accept("a", self.pressedA)
        self.accept("escape", sys.exit)
        
        # fields from save file
        self.name = "<world name>"
        self.version = 0
        
    
    def pressedA(self):
        print( "a pressed, keyboard focus ok")
        self.loadInitialEnv()


    def loadInitialEnv(self):
        # Load the environment model.
        self.scene = loader.loadModel("environment")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)
        
    def step(self):
        taskMgr.step()
    
    def bindToWindow(self, windowHandle):
        wp = WindowProperties().getDefault()
        wp.setOrigin(0,0)
        wp.setSize(P3D_WIN_WIDTH, P3D_WIN_HEIGHT)
        wp.setParentWindow(windowHandle)
        base.openDefaultWindow(props=wp )
        self.wp = wp


if __name__ == "__main__":
    main.start()