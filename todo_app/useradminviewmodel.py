from datetime import datetime
from dateutil import parser
from .data.item import Item
from bson.objectid import ObjectId

class UserAdminViewModel:
    def __init__(self, users, logged_user):
        self._users = users
        self._logged_user = logged_user

    @property
    def logged_user(self):
        return self._logged_user

    @property
    def users(self):
        return self._users

    @property
    def is_sole_admin(self):
        admins = 0
        for user in self._users:
            if 'admin' in user.roles:
                admins += 1
        
        if admins > 1:
            return False
        else:
            return True

    