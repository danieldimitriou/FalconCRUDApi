import falcon
from tinydb import TinyDB
from FalconCRUDApi.user_resource import UserResource
from FalconCRUDApi.user_repository import user_repository

#create the Falcon app instance
app = application = falcon.App()

#create a DB instance & users table
db = TinyDB('userDB.json')
users_table = db.table('users')

#create the repository and pass the users_table as a parameter for the queries
repository = user_repository(users_table)

#create the users resource and inject the repository
users = UserResource(repository)

#add the users resource as a route
app.add_route('/users', users)
app.add_route('/users/{id}', users)