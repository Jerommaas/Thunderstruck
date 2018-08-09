

'''
Graphical User interface

provides a way of seeing what the generator does
draws components in 
'''
 
from scene import Scene
from generator import Generator 

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

import numpy as np

class view3d(object):
    ''' a window containing a 3d view of the generated world '''
    def __init__(self, scene ):
        self.scene = scene



class GUI(object):
    def __init__(self, generator=None):
        if generator==None:
            generator=Generator()
        print("GUI hoihoi")

        nx, ny = (201, 201)
        x = np.linspace(-100, 100, nx)
        y = np.linspace(-100, 100, ny)
        xv, yv = np.meshgrid(x, y)

        zv = generator.scene.at(xv,yv)

        fig = plt.figure()
        ax = fig.gca(projection='3d')   
        ax.set_zlim(-100, 100)

        surf = ax.plot_surface(xv,yv,zv, cmap=cm.coolwarm,
                            linewidth=0, antialiased=False)

        plt.show()      

if __name__ == "__main__":
    # test gui
    gui = GUI()



