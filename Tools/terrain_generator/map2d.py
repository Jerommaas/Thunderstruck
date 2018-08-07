
import numpy as np
import json




class map2d(object):
    '''
    Base class for 2d functions 
    '''
    map2d_id = 0
    def __init__(self, name='<some name>' ):
        self.name = name
        self.children = []
        self.class_name = self.__class__.__name__
        self.id = map2d.map2d_id
        map2d.map2d_id += 1

    def at(self, x, y ):
        # TODO(victor): implement (throw error)
        pass

    @staticmethod
    def classType(className):
        class_dict = { "FlatSurface" : FlatSurface, 
                "RoundHill" : RoundHill, 
                "Transform2d" : Transform2d } 
        return class_dict[className]

    def toJson(self):
        # NOTE: when saving as json, we only store the child ids, not the object itself
        # when reconstructing the objects, this means we have to look up the object belonging to this id
        dict_copy = dict( self.__dict__  )
        del dict_copy["children"]
        dict_copy["children_ids"] = [obj.id for obj in self.children]
        return dict_copy

    def fromJson(self, json_data ):
        self.__dict__.update(json_data)
        print( self.__dict__ )


    
class FlatSurface(map2d): 
    def __init__(self, name="Flat Surface"):
        super().__init__(name=name)  
    def at(self, x, y ):
        return np.zeros( x.shape )

class RoundHill(map2d):
    def __init__(self, name="Round Hill"):
        super().__init__(name=name)  
    def at(self, x, y ):
        return np.sin(x**2 + y**2) / (1 + x**2 + y**2)

class Transform2d(map2d):
    def __init__(self,childMap=None, x=1, y=2, rot=np.pi, name="Transform"):
        super().__init__(name=name)
        if not childMap == None:
            self.children = [childMap]
    def at(self, x, y ):
        #TODO(victor): apply transformation to x and y 
        return self.map.at(x,y)



if __name__ == "__main__":
    
    hill = RoundHill()
    jsonText = hill.toJson()
    print( jsonText )

    transform = Transform2d( hill,  x=1, y=2, rot=np.pi )
    jsonText = transform.toJson()
    print( jsonText )

    print( map2d.classType('FlatSurface') )