import os

class Config:

    def __init__(self):
        """Base configuration variables."""
        self.GITHUB_CLIENT_ID=os.environ.get('GITHUB_CLIENT_ID','')
        self.GITHUB_CLIENT_SECRET=os.environ.get('GITHUB_CLIENT_SECRET','')
        self.DB_CONNECTION_STRING = os.environ.get('DB_CONNECTION_STRING')
        self.DATA_COLLECTION = os.environ.get('DATA_COLLECTION','tasks')
        self.SECRET_KEY=os.environ.get('SECRET_KEY','')
        self.LOGIN_DISABLED = os.environ.get('LOGIN_DISABLED',None )
