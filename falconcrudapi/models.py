from enum import Enum

class User():
    def __init__(self, name, type):
        #The names of a user is unique and can only contain letters.
        self.name = name
        #the type of a user can only be either normal or admin
        self.type = type

    #serialize the object to a dictionary, in order to be able to save the user to the database.
    def serialize(self):
            return vars(self)
    
#type of user, can be either admin or normal user
class UserType(Enum):
    normal = 1
    admin = 2
    