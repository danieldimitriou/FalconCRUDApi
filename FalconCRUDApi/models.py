from enum import Enum
import json

class User():
    def __init__(self, name, type):
        self.name = name
        self.type = type

    #serialize the object to a dictionary, in order to be able to save the user to the database.
    def serialize(self):
            return vars(self)
    
#type of user, can be either admin or normal
class UserType(Enum):
    normal = 1
    admin = 2
    