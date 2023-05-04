import json

import falcon
from dataclasses import dataclass
from enum import Enum
from tinydb import Query


#type of user, can be admin or normal
class UserType(Enum):
    normal = 1
    admin = 2
    
    

class UserResource:
    def __init__(self, db):
        self.db = db

    def on_get(self, req, resp, id = None):
        #check if there is a document/user ID provided with the request and try to retrieve their data.  
        if(id):
            #get the user from the DB and handle the errors
            try:
                user = self.db.get(doc_id=int(id))
                if user is None:
                    raise ValueError(f"User with ID: {id} does not exist.")
            except ValueError as value_error:
                resp.status = falcon.HTTP_400
                resp.text = str(value_error)
                return
            except Exception as e:
                resp.status = falcon.HTTP_500
                resp.text = "An error occured while fetching the user from the database: {e}"
                return
            
            #add the user to the body of the response as a json/python string       
            resp.text = json.dumps(user, ensure_ascii=False)
            #Response status code 200 - OK
            resp.status = falcon.HTTP_200
            return
        #if there is no id, fetch all users from the database and return them in the response
        else:
            try:
                all_users = self.db.all()
            except Exception as e:
                resp.status = falcon.HTTP_500
                resp.text = "An error occured while fetching the users from the database: {e}"
            resp.text = json.dumps(all_users, ensure_ascii=False)
            resp.status = falcon.HTTP_200
    
    def on_post(self, req, resp):
        #get user from the request body
        user_data = req.media

        #check if the user type is either normal or admin. if not, return error response 400. 
        if(user_data["type"] not in UserType.__members__):
            resp.status = falcon.HTTP_400
            resp.text = f"Invalid data. User type must be either: normal or admin."
            return
        
        #check that the name of the user does not contain numbers.
        if(any(character.isdigit() for character in user_data["name"])):
            resp.status = falcon.HTTP_400
            resp.text = f"Invalid data. User name must not include any numbers."
            return

        #create a user_query object to query the database and check if the user exists. If it exists, return 400, else continue.
        user_query = Query()
        user_exists = self.db.contains((user_query.name == user_data["name"]) & (user_query.type == user_data["type"]))
        if user_exists:
           resp.status = falcon.HTTP_400
           resp.text = f"This user already exists."
           return
        #save the validated and unique use data to the db.
        try:
            user_id = self.db.insert(user_data)
            #Response status code 201 - Created
            resp.status = falcon.HTTP_201
            #set the route for this user using their id for future reference.
            resp.location = f'/users/{user_id}'
            resp.text = f"User created successfully."
        #in case there is an exception raised, catch it and return a response to the user
        except Exception:
            resp.status = falcon.HTTP_500
            resp.text = f"An internal error has occured. Please try again"
   
    def on_put(self, req, resp, id):
        new_user_data = req.media
        self.db.update(new_user_data, doc_ids=[int(id)])
        #Response status code 204 - No content
        resp.status = falcon.HTTP_204
       
    
    def on_delete(self, rep, resp, id):
        self.db.remove(doc_ids = [int(id)])
        #Response status code 204 - No content
        resp.status = falcon.HTTP_204
        