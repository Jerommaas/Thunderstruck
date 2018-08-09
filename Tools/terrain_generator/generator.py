'''
Generator

performs all actions on the scene object
the GUI provides methods to perform these actions in a user interface and draw result
'''
 
from scene import Scene 


class Generator(object):
    def __init__(self, scene=None):
        if scene==None:
            scene=Scene()
        self.scene = scene
        print("Generator.__init__()")




if __name__ == "__main__":
    # test gui
    generator = Generator()



