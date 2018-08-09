
'''
Main file for terrain generator.
Startup GUI, data object, and worker 
'''

import numpy as np
from gui import GUI
from scene import Scene
from generator import Generator


if __name__ == "__main__":
    
    scene = Scene()
    generator = Generator( scene=scene )

    
    gui = GUI(generator=generator)