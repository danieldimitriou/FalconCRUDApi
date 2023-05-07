#This module is responsible for the database operations.
from tinydb import Query 

class user_repository:
    def __init__(self, table):
        self.table = table

    def get_user_by_id(self, user_id):
        return self.table.get(doc_id=int(user_id))

    def get_all_users(self):
        return self.table.all()

    def save_user(self, user):
        return self.table.insert(user)

    def update_user(self, user_id, updated_user_data):
        user_query = Query()
        return self.table.update(updated_user_data, doc_ids=[user_id])

    def delete_user(self, user_id):
        return self.table.remove(doc_ids = [user_id])
    
    # return True if user exists, false if user doesn't exist.
    # Supposes that the users have unique names.
    def check_if_user_exists_by_name(self, user):
        user_query = Query()
        if self.table.contains(user_query.name == user["name"]):
            return True
        return False
