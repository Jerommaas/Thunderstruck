


import main


#
# Base class for objects which need to be saved and loaded from map files
#

class data_object(object):
    def __init__(self, json_data):
        # check data
        self.first_field = 5
        self.second_field = 6
        self.load( json_data ) 

    def load( self , json_data ):
        # TODO(victor): construct correct type of object
        # pass arguments to this objects constructor
        # let it figure it out from there
        self.__dict__.update(json_data)

    def save( self ):
        # returns a json object of all relevant fields within this object
        json_data = { "first_field": self.first_field, "second_field": self.second_field}
        return json_data

        
        

class terrain_object(data_object):
    def __init__(self, json_data):
        print( "terrain_object(): {}".format(json_data)  )
        return super().__init__(json_data)

    def load( self, json_data ):
        self.__dict__.update(json_data)
        
    def save( self ):       
        json_data = { "first_field": self.first_field, 
                    "second_field": self.second_field
                    }
        return json_data


class panda_object(data_object):
    def __init__(self, json_data):
        return super().__init__(json_data)

    def load( self, json_data ):
        self.__dict__.update(json_data)
        
    def save( self ):        
        json_data = { "first_field": self.first_field, 
                      "second_field": self.second_field}
        return json_data





if __name__ == "__main__":
    main.main()