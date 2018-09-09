import sys
rootname = sys.path[0][:-24]
sys.path.insert(0,rootname)

from panda3d.core import *
from panda3d.core import Filename
getModelPath().appendDirectory(Filename.fromOsSpecific(rootname))

from direct.showbase.ShowBase import ShowBase
# Als je nieuwe modules hebt voor bij *, voeg de verwijzing 
# toe in __init__.py van de module!
from Controls import *
from Entities import * 
from Entities.Objects import *
import WVCamera
import WVControls


class WorldViewer(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        # ----- ENTITIES -----
        # World
        self.Terrain = Terrain.Terrain()
        self.SkyDome = skyDome.skyDome()

        self.Camera = WVCamera.Camera(self)
        # User input
        self.CM = WVControls.ControlManager(self)

if __name__ == "__main__":
    client  = WorldViewer()
    client.run()