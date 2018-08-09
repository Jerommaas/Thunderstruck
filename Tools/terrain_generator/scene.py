



'''
Scene object

performs all saving / loading of data objects
is used by the generator to perform actions on
'''

from map2d import *
import numpy as np
import json

class Scene(object):
    def __init__(self, sceneFile="scenes/test_scene.json"  ):
        self.sceneFile = sceneFile
        self.map2d_list = []
        self.map = None
        print("Scene.__init__()")
        self.load( sceneFile )

    def load(self, file):
        print("Scene.load()")
        with open( file, "r") as f:
            print("file: {} found!".format(file) )
            json_data = json.load( f )
            print( "\ndata:" )
            print( json_data )

            # first load all functions
            id_dict = dict()
            for obj_dict in json_data['map_functions']:
                print( obj_dict )

                class_name = obj_dict["class_name"]  
                class_type = globals()[class_name] #introspection
                class_instance = class_type()

                class_instance.fromJson( obj_dict )
                id_dict[class_instance.id] = class_instance
                self.map2d_list.append( class_instance )
                print( class_instance.__dict__ )

            # then set child objects based on ids
            for obj in self.map2d_list:
                obj.children = [ id_dict[i_id] for i_id in obj.children_ids ] 

            # the root function is the one named "<Main>" 
            main_node = list( filter(lambda x: x.name == "<Main>", self.map2d_list) )[0]
            self.map = main_node
            print( "main node: {}".format(main_node))

            print( "\n:" )

    def save(self, file=None):
        if file==None: 
            file=self.sceneFile
        print("Scene.save()")
        with open( file, "w") as f:
            print("file: {} found!".format(file) )
            
            map_list = [obj.toJson() for obj in self.map2d_list]
            print( map_list )

            all_data = {"map_functions": map_list, "name": "first map"}
            f.write( json.dumps( all_data, indent=4  ))
        return file

    def at(self, x, y):
        return self.map.at( x, y )

    def add( self, obj ):
        # TODO(victor): once other types of objects are allowed, add it to the correct list
        # TODO(victor): check if objects are unique
        self.map2d_list.append( obj )



if __name__ == "__main__":
    nx, ny = (21, 21)
    x = np.linspace(0, 1, nx)
    y = np.linspace(0, 1, ny)
    xv, yv = np.meshgrid(x, y)

    # test gui
    scene = Scene(sceneFile = "scenes/test_scene.json"  )

    if len(scene.map2d_list) ==0:
        hill = RoundHill() 
        transformedHill = Transform2d( hill, x=1, y=2, rot=np.pi ) 
        scene.add( hill )
        scene.add( transformedHill )
    

    print( "objects:" )
    for obj in scene.map2d_list:
        print( "- {}".format( obj.__dict__ ) )

    scene.at( xv, yv )

    saveFile = scene.save()

    # scene2 = Scene(sceneFile=saveFile)
    # verify that scene2 is equivalent to scene1

