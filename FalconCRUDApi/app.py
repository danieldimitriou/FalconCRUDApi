import falcon
from tinydb import TinyDB, Query
from .users import UserResource


#create the Falcon app instance
app = application = falcon.App()

#create a DB instance
db = TinyDB('userDB.json')

#create the users resource
users = UserResource(db)
#add the users resource as a route
app.add_route('/users', users)
app.add_route('/users/{id}', users)
