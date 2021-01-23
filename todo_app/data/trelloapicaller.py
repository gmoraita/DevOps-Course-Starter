import requests

class TrelloAPICaller():

    def __init__(self, config):
        self.config = config

    def call_api(self, api, method, params = {}) -> requests.Response:
        """
        Makes a call to the Trello API using key and token
        """
        auth_query =  { 'key': self.config['TRELLO_API_KEY'], 'token': self.config['TRELLO_API_SECRET'] }
        url = self.config['TRELLO_BASE_URL'] + api
        headers = {"Accept": "application/json"}
        query = {**auth_query, **params}

        response = requests.request(
            method,
            url,
            headers=headers,
            params=query
        )
        
        return response
        