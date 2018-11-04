


import sys
import inspect

# Panda 
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

# local
import main
from data_object import *
from camera import Camera


P3D_WIN_WIDTH = 720
P3D_WIN_HEIGHT = 560

#
# This class manages all objects in the scene, loads/saves, etc.
#

import json


def str_to_class(str):
    return reduce(getattr, str.split("."), sys.modules[__name__])

class PandaLoader(object):
    def __init__(self, world):
        self.world = world 
        self.objects = []
        self.events  = [] # list of user actions (add, move, edit object etc.)

    def load_scene(self, file):
        print( "PandaLoader.load_scene():\n\t{}".format( file  ) )
        self.world.loadInitialEnv() # TEMP
        world = self.world # shorthand
        with open(file) as f:
            data = json.load(f)
            self.json_data = data
            world.name = data.get('name', '<world name>') 
            world.version = data.get('version', 0) 
            json_objects = data["objects"]
            for obj in json_objects:
                # try to find this type
                try: 
                    subtype = globals()[obj["type"] ] 
                except:
                    print( "unknown type: {}".format(obj["type"]) )
                    continue

                # check if this class is a subclass of data_object
                if issubclass(subtype, data_object):
                    instance = subtype( obj["data"]  )
                    instance.name = obj["name"]  
                    self.objects.append(instance)
                else:
                    print("type is not a subclass of data_type!")
        
        # TODO(victor): super hacky, los dit goed op
        for obj in self.objects: 
            if hasattr( obj, "model"):
                obj_file = obj.model
                if obj_file:
                    print( "loading model: {}".format(obj_file) )
                    model = loader.loadModel(obj_file) 
                    model.reparentTo(self.world.render)


    def save_scene(self, file):
        print( "PandaLoader.save_scene():\n\t{}".format( file  ) ) 
        world = self.world
        data = self.json_data
        data["version"] = world.version+1
        data["name"] = world.name
        data["objects"] = []

        print( "saving objects")
        for obj in self.objects:
            json_data = dict()
            json_data["name"] = obj.name
            json_data["type"] = type(obj).__name__
            json_data["data"] = obj.save()
            data["objects"].append( json_data  )
            
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
        self.accept("escape", sys.exit)

        # add camera object
        self.cam = Camera(self)
        
        # fields from save file
        self.name = "<world name>"
        self.version = 0
        

    def loadInitialEnv(self):
        # Load the environment model.
        self.scene = loader.loadModel("environment")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        s = 0.02
        self.scene.setScale(s,s,s)
        # self.scene.setPos(-8, 42, 0)
        
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
    main.main()