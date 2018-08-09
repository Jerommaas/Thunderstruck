

'''
Read config file, provide an interface for easily reading the data

usage:
config = Config("some_file.json")
client_port = config["client"]["port"]
'''
import os
import json


class Config(object):
    def __init__( self, file ):
        # Read file
        here = os.path.dirname(os.path.abspath(__file__))
        with open( here+file, 'r') as f:
            self.json_config = json.load(f)

    def __getitem__(self, key):
        # get key
        try:
            return self.json_config[key]
        except:
            print( "ERROR: attempting to obtain config[{}]".format(key) )
            raise # propagate error


if __name__ == "__main__":

    config_file = "./config_file.json"
    config = Config( config_file )

    client_port = config["client"]["port"]
    client_host = config["client"]["host"]

    print( "port: {}; host: {};".format(client_port,client_host) )
