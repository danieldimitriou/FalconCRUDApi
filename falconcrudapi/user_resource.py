import json
import falcon
from falconcrudapi.models import User, UserType
from falconcrudapi.utils import validate_json_fields

class UserResource:
    def __init__(self, user_repository):
        self.user_repository = user_repository
        
    @staticmethod    
    def on_post_validation(req, resp, resource, params):
        #check that the request's body includes only the fields name and type
        user_data = validate_json_fields(req.media)
        #check that the user's name does not have any numbers or characters. If it does, return error resposne 400.
        if not user_data.name.isalpha():
            message = "Invalid data. User name must not include any numbers."
            raise falcon.HTTPBadRequest(title = 'Bad request', description = message)
        #check if the user type is either normal or admin. if not, return error response 400. 
        if user_data.type not in UserType.__members__:
            message = "Invalid data. User type must be either: normal or admin."
            raise falcon.HTTPBadRequest(title = 'Bad request', description = message)
        
        #create a user_query object to query the database and check if the user exists. If it exists, return 400, else continue.
        if resource.user_repository.check_if_user_exists_by_name(user_data.serialize()):
            message = "This user already exists."
            raise falcon.HTTPBadRequest(title = 'Bad request', description = message)
   
    @staticmethod    
    def on_get_validation(req, resp, resource, params):
        user_id = params.get('id')
        if user_id:
            try:
                user_data = resource.user_repository.get_user_by_id(user_id)
                req.context["user_data"] = user_data
            except Exception as e:
                raise falcon.HTTP_INTERNAL_SERVER_ERROR(title = "An error has occured.", description = e)
            
            #return error if user does not exist
            if not user_data:
                message = f"User with ID: {user_id} does not exist."
                raise falcon.HTTPNotFound(title="Resource not found.", description=message)
   
    @staticmethod    
    def on_put_validation(req, resp, resource, params):
        #check that the request's body includes only the fields name and type
        updated_user_data = validate_json_fields(req.media)
        #check if a user id is provided in the uri
        user_id = params.get('id')
        if not user_id:
            message = "User ID is missing in the URI."
            raise falcon.HTTPBadRequest(title='Bad request', description=message)
                
        #check that the user's name does not have any numbers or characters. If it does, return error resposne 400.
        if not updated_user_data.name.isalpha():
            message = "Invalid data. User name must not include any numbers."
            raise falcon.HTTPBadRequest(title = 'Bad request', description = message)
        
        #check if the user type is either normal or admin. if not, return error response 400. 
        if updated_user_data.type not in UserType.__members__:
            message = "Invalid data. User type must be either: normal or admin."
            raise falcon.HTTPBadRequest(title = 'Bad request', description = message)
        
        #check that the user with the provided id exists
        if not resource.user_repository.get_user_by_id(user_id):
            message = f"User with ID: {user_id} does not exist."
            raise falcon.HTTPNotFound(title="Resource not found.", description=message)  
        
    @staticmethod    
    def on_delete_validation(req, resp, resource, params):
        user_id = params.get('id')
        if not user_id:
            message = "User ID is missing in the URI."
            raise falcon.HTTPBadRequest(title='Bad request', description=message)
        if not resource.user_repository.get_user_by_id(user_id):
            message = f"User with ID: {user_id} does not exist."
            raise falcon.HTTPNotFound(title="Resource not found.", description=message)  
        
    @falcon.before(on_post_validation)
    def on_post(self, req, resp):
        #get user from the request body
        user_data = User(name= req.media["name"], type= req.media["type"])
        try:
            user_id = self.user_repository.save_user(user_data.serialize())
        except Exception as e:
            raise falcon.HTTP_INTERNAL_SERVER_ERROR(title = "An error has occured.", description = e)
        #Response status code 201 - Created
        message = "User created successfully."
        resp.status = falcon.HTTP_CREATED
        resp.text = json.dumps({"message": message, "User ID": user_id})
        #set the route for this user using their id for future reference.
        resp.location = f'/users/{user_id}'          
    
    @falcon.before(on_get_validation)
    def on_get(self, req, resp, id = None):
        #check if there is a document/user ID provided with the request and try to retrieve their data.  
        if(id):
            user_data = req.context["user_data"]
            #add the user to the body of the response as a json/python string       
            resp.text = json.dumps(user_data, ensure_ascii=False)
            #Response status code 200 - OK
            resp.status = falcon.HTTP_OK
            return
        #if there is no id, fetch all users from the database and return them in the response
        else:
            try:
                all_users = self.user_repository.get_all_users()
            except Exception as e:
                 raise falcon.HTTP_INTERNAL_SERVER_ERROR(title = "An error has occured.", description = e)
            resp.text = json.dumps(all_users, ensure_ascii=False)
            resp.status = falcon.HTTP_200
            return
        
    @falcon.before(on_put_validation)
    def on_put(self, req, resp, id):
        updated_user_data = User(name= req.media["name"], type= req.media["type"])
        try:
            self.user_repository.update_user(int(id), updated_user_data.serialize())
        except Exception as e:
            raise falcon.HTTP_INTERNAL_SERVER_ERROR(title = "An error has occured.", description = e)

        #Response status code 200 - OK
        resp.status = falcon.HTTP_OK
        message = f"User with ID: {id} has been updated successfully."
        resp.text = json.dumps({"message": message})       

    @falcon.before(on_delete_validation)
    def on_delete(self, rep, resp, id):
        try:
            self.user_repository.delete_user(int(id))
        except Exception as e:
            raise falcon.HTTP_INTERNAL_SERVER_ERROR(title = "An error has occured.", description = e)
        #Response status code 200 - OK
        resp.status = falcon.HTTP_200
        message = f"User with ID:{id} has been deleted successfully."
        resp.text = json.dumps({"message":message})