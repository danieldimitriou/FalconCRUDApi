import json

import falcon


class User:
    def __init__(self, name, user_type):
        self.name = name
        self.user_type = user_type

class UserResource:
    def __init__(self, db):
        self.db = db

    def on_get(self, req, resp, id = None):
        if(id):
            user = self.db.get(doc_id=int(id))
            resp.text = json.dumps(user, ensure_ascii=False)
            resp.status = falcon.HTTP_200
        else:
        
            all_users = self.db.all()
            
            # Create a JSON representation of the resource
            resp.text = json.dumps(all_users, ensure_ascii=False)
            #Response status code 200 - OK
            resp.status = falcon.HTTP_200
    
    def on_post(self, req, resp):
        #get user from the body
        user = req.media
        #save to db
        user_id = self.db.insert(user)
        #Response status code 201 - Created
        resp.status = falcon.HTTP_201
        #set the route for this user using their id for future reference.
        resp.location = f'/users/{user_id}'
        resp.text = f"User created successfully."

    def on_put(self, req, resp, id):
        new_user_data = req.media
        self.db.update(new_user_data, doc_ids=[int(id)])
        #Response status code 204 - No content
        resp.status = falcon.HTTP_204
       
    
    def on_delete(self, rep, resp, id):
        self.db.remove(doc_ids = [int(id)])
        #Response status code 204 - No content
        resp.status = falcon.HTTP_204
        