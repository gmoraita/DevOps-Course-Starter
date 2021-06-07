import os

class Config:

    def __init__(self):
        """Base configuration variables."""
        DB_USERNAME=os.environ.get('DB_USERNAME','')
        DB_PASSWORD=os.environ.get('DB_PASSWORD','')
        DB_CLUSTER=os.environ.get('DB_CLUSTER','')
        if DB_CLUSTER == 'test':
            self.DB_CONNECTION_STRING = os.environ.get('DB_CONNECTION_STRING')
        else:
            self.DB_CONNECTION_STRING = 'mongodb+srv://%s:%s@%s/todoapp?retryWrites=true&w=majority' % (DB_USERNAME,DB_PASSWORD,DB_CLUSTER)        
        
        self.DATA_COLLECTION = os.environ.get('DATA_COLLECTION','tasks')
