


import main
import json


class data_object(object):
    def __init__(self, json_data):
        # check data
        self.first_field = 5
        self.second_field = 6
        self.load(json_data) 

    def load( self , json_data ):
        self.__dict__.update(json_data) # by default, add all fields to dict

    def save( self ):
        # returns a json object of all relevant fields within this object
        json_data = { }
        return json_data


class terrain_object(data_object):
    """
    Class for describing a terrain
    """
    def __init__(self, json_data):
        self.textures = ["<some texture file>", "<some other texture file>"] # TODO(victor) multiple textures
        self.height = "<some height map>"
        self.blend = "<some blend map>"
        self.xyz = [0,0,0]
        self.rot = [0,0,0]
        return super().__init__(json_data)

    def save( self ):
        json_data = { "textures": self.textures, 
                      "height": self.height, 
                      "blend": self.blend, 
                      "xyz": self.xyz, 
                      "rot": self.rot}
        return json_data


class panda_object(data_object):
    """
    Default object
    """
    def __init__(self, json_data):
        # set default values
        self.model = "<some .egg file>"
        self.xyz = [0,0,0]
        self.rot = [0,0,0]
        # override with data in json
        return super().__init__(json_data)
        
    def save( self ):        
        json_data = { "model": self.model, 
                      "xyz": self.xyz, 
                      "rot": self.rot}
        return json_data


if __name__ == "__main__":
    main.main()