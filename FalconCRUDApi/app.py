import falcon
from tinydb import TinyDB
from falconcrudapi.user_resource import UserResource
from falconcrudapi.user_repository import user_repository
import os

#create the Falcon app instance
app = application = falcon.App()

#create a DB instance & users table
db = TinyDB(os.environ.get("DB_NAME"))
users_table = db.table(os.environ.get("TABLE_NAME"))

#create the repository and pass the users_table as a parameter for the queries
repository = user_repository(users_table)

#create the users resource and inject the repository
users = UserResource(repository)

#add the users resource as a route
app.add_route('/users', users)
app.add_route('/users/{id}', users)