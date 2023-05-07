#This module is responsible for the database operations.
from tinydb import Query 
import falcon

def get_user_by_id(db, user_id):
    return db.get(doc_id=int(user_id))

def get_all_users(db):
    # all_users =  db.all()
    # print(all_users)
    return db.all()

def save_user(db, user, resp):
    return db.insert(user.serialize())


#return True if user exists, false & http error code if user doesn't exist.
def check_if_user_exists(db, user):
    user_query = Query()
    if db.contains((user_query.name == user.name) & (user_query.type == user.type)):
        return True
    return False
