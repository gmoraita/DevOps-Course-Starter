import os

class Config:

    def __init__(self):
        """Base configuration variables."""
        self.DB_CONNECTION_STRING = os.environ.get('DB_CONNECTION_STRING')
        