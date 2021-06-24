import pymongo
from datetime import datetime
from .user import User

class UserDB:
    def __init__(self, config):
        self.users = pymongo.MongoClient(config.get('DB_CONNECTION_STRING')).todoapp['users']

    def get_list_of_users(self): 
        return self.build_users_list(self.users.find())
    
    def get_user(self, user_id):
        user_features = self.users.find_one({'login': user_id})
        if user_features is None:
            return None
        
        return User(user_features)

    def add_user(self, user_dict):
        return self.users.insert_one({**user_dict, 'last_updated': datetime.utcnow()}).inserted_id

    def delete_user(self, id):
        return self.users.delete_one({ 'login': id})
 
    def modify_roles(self, id, roles):

        return self.users.update_one({'login' : id}, {"$set": {'roles': roles, 'last_updated': datetime.utcnow()}} )

    def build_users_list(self, user_dict_list: list) -> list :
        users_list =[]
        for user_dict in user_dict_list:
            users_list.append(User( user_dict))

        return users_list