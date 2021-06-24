from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_features):
        self._id = user_features['login']
        self._roles = user_features['roles']
        self._user_features = user_features
        
    @property
    def id(self):
        return self._id

    @property
    def roles(self):
        return self._roles

    @property
    def user_features(self):
        return self._user_features
