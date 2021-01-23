import os

class Config:

    def __init__(self):
        """Base configuration variables."""
        self.TRELLO_BASE_URL = 'https://api.trello.com/1'
        self.TRELLO_API_KEY = os.environ.get('TRELLO_API_KEY')
        self.TRELLO_API_SECRET = os.environ.get('TRELLO_API_SECRET')
        self.TRELLO_BOARD_ID = os.environ.get('TRELLO_BOARD_ID')
        self.TRELLO_USER = os.environ.get('TRELLO_USER')
        self.TRELLO_BOARD_NAME = os.environ.get('TRELLO_BOARD_NAME')
    
    def asDict(self):
        return {
            'TRELLO_BASE_URL': self.TRELLO_BASE_URL,
            'TRELLO_API_KEY' : self.TRELLO_API_KEY ,
            'TRELLO_API_SECRET': self.TRELLO_API_SECRET ,
            'TRELLO_BOARD_ID': self.TRELLO_BOARD_ID,
            'TRELLO_USER': self.TRELLO_USER ,
            'TRELLO_BOARD_NAME':self.TRELLO_BOARD_NAME
        }
        