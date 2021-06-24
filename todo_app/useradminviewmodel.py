from datetime import datetime
from dateutil import parser
from .data.item import Item
from bson.objectid import ObjectId

class UserAdminViewModel:
    def __init__(self, users, user):
        self._users = users
        self._user = user

    @property
    def user(self):
        return self._user

    @property
    def users(self):
        return self._users
    