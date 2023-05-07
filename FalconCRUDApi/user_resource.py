import json
import falcon
from tinydb import Query
# from .utils import *
from .user_repository import *
from .models import User, UserType

class UserResource:
    def __init__(self, db):
        self.db = db

    @staticmethod    
    def validate_user_data_on_post(req, resp, resource, params):
        user_data = User(req.media["name"], req.media["type"])
        #check that the user's name does not have any numbers. If it does, return error resposne 400.
        if(any(character.isdigit() for character in user_data.name)):
            message = "Invalid data. User name must not include any numbers."
            raise falcon.HTTPBadRequest(title = 'Bad request', description = message)
        #check if the user type is either normal or admin. if not, return error response 400. 
        if user_data.type not in UserType.__members__:
            message = "Invalid data. User type must be either: normal or admin."
            raise falcon.HTTPBadRequest(title = 'Bad request', description = message)
        
        #create a user_query object to query the database and check if the user exists. If it exists, return 400, else continue.
        if check_if_user_exists(resource.db, user_data):
            message = "This user already exists."
            raise falcon.HTTPBadRequest(title = 'Bad request', description = message)
   
    @staticmethod    
    def validate_user_data_on_get(req, resp, resource, params):
        user_id = params.get('id')
        if user_id:
            try:
                user_data = get_user_by_id(resource.db, user_id)
                req.context["user_data"] = user_data
            except Exception as e:
                raise falcon.HTTP_INTERNAL_SERVER_ERROR(title = "An error has occured.", description = e)
            
            #return error if user does not exist
            if not user_data:
                message = f"User with ID: {user_id} does not exist."
                raise falcon.HTTPNotFound(title="Resource not found.", description=message)

    @falcon.before(validate_user_data_on_get)
    def on_get(self, req, resp, id = None):
        #check if there is a document/user ID provided with the request and try to retrieve their data.  
        if(id):
            user_data = req.context["user_data"]
        #     #add the user to the body of the response as a json/python string       
            resp.text = json.dumps(user_data, ensure_ascii=False)
        #     #Response status code 200 - OK
            resp.status = falcon.HTTP_OK
            return
        # #if there is no id, fetch all users from the database and return them in the response
        else:
            try:
                all_users = get_all_users(self.db)
            except Exception as e:
                 raise falcon.HTTP_INTERNAL_SERVER_ERROR(title = "An error has occured.", description = e)
            resp.text = json.dumps(all_users, ensure_ascii=False)
            resp.status = falcon.HTTP_200
            return
    
    @falcon.before(validate_user_data_on_post)
    def on_post(self, req, resp):
        #get user from the request body
        user_data = User(req.media["name"], req.media["type"])
        try:
            user_id = save_user(self.db, user_data, resp)
        except Exception as e:
            raise falcon.HTTP_INTERNAL_SERVER_ERROR(title = "An error has occured.", description = e)
        #Response status code 201 - Created
        message = "User created successfully."
        resp.status = falcon.HTTP_CREATED
        resp.text = json.dumps({"message": message, "id": user_id})
        # #set the route for this user using their id for future reference.
        resp.location = f'/users/{user_id}'

    def on_put(self, req, resp, id):
        new_user_data = req.media
        self.db.update(new_user_data, doc_ids=[int(id)])
        #Response status code 204 - No content
        resp.status = falcon.HTTP_204
       
    
    def on_delete(self, rep, resp, id):
        self.db.remove(doc_ids = [int(id)])
        #Response status code 204 - No content
        resp.status = falcon.HTTP_204
        

