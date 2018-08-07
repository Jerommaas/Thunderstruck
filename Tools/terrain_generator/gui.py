

'''
Graphical User interface

provides a way of seeing what the generator does
draws components in 
'''
 
from scene import Scene
from generator import Generator


class GUI(object):
    def __init__(self, generator=None):
        if generator==None:
            generator=Generator()
        print("GUI hoihoi")




if __name__ == "__main__":
    # test gui
    gui = GUI()

