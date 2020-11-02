from abc import ABC, abstractmethod
from configparser import ConfigParser
from .boardelements import *
import os
import requests

def todo_api_factory(api_name):
    if api_name == 'trello':
        return TrelloAPI()
    else:
        #TODO add more APIs in the future
        return None


class ToDoAPI(ABC):

    @abstractmethod
    def get_list_of_statuses(self):
        pass

    @abstractmethod
    def get_list_of_items(self):
        pass

    @abstractmethod
    def add_item(self, title):
        pass
    
    @abstractmethod
    def delete_item(self, id):
        pass

    @abstractmethod
    def modify_item(self, id, attributes):
        pass

    @property
    def todomapper(self) -> ToDoMapper:
        return self._todomapper

    @todomapper.setter
    def todomapper(self, mapper: ToDoMapper):
        self._todomapper = mapper

class TrelloAPI(ToDoAPI):
    TRELLO_ROOT_URL = 'https://api.trello.com'
    CREDS_CONFIG_FILE = 'creds.config'
   
    def __init__(self):
        self.init_todomapper()    

        #keep this call at the top as needed to get authorisation details for all subsequent calls
        self.auth_query = self.get_trello_creds_section('trello_auth')
        self.user = self.get_trello_creds_section('trello_user').get('user')

        self.boards = self.get_boards_of_user(self.user) 
        #Currently defaulting to the first board - in future we can have dropdown
        self.board_id = self.boards[0].id 
        self.statuses = self.boards[0].statuses

    def get_list_of_statuses(self):
        return self.statuses

    def get_list_of_items(self):
        items_list = []
        items_list.append(self.build_items_list_from_dict_list(self.call_api('/1/boards/%s/cards' % self.board_id,'GET').json()))
        return items_list
       
    def add_item(self, item_dict):
        return self.call_api('/1/cards', 'POST', {**{'idList' : list(self.statuses.values())[0].id}, **item_dict}).json()
 
    def delete_item(self, id):
        return self.call_api('/1/cards/'+id, 'DELETE').json()
 
    def modify_item(self, id, atributes):
        return self.call_api('/1/cards/'+id, 'PUT', atributes).json()



    def call_api(self, api, method, params = {}) -> requests.Response:
        """
        Makes a call to the Trello API using key and token
        """
        
        url = self.TRELLO_ROOT_URL + api
        headers = {"Accept": "application/json"}
        query = {**self.auth_query, **params}
        print ('url:%s headers:%s query:%s' % (url, headers, query))
        response = requests.request(
            method,
            url,
            headers=headers,
            params=query
        )

        return response


    def get_trello_creds_section(self, section) -> dict:
        creds_config = ConfigParser()
        creds_config.read(os.path.join(os.path.dirname(__file__), '', self.CREDS_CONFIG_FILE))
        return creds_config._sections[section]


    def get_boards_of_user(self, user) -> list:
        boards_list = []
        boards = self.call_api('/1/members/%s/boards' % user, 'GET', {'lists':'all'}).json()

        for board in boards:
            boards_list.append(self.board_builder(board))
        return boards_list

    

    def build_items_list_from_dict_list(self, item_dict_list: list):
        """
        Builds a list of Item from a list of dict containing each item's attributes

        Args:
            status: The status under which the items are
            item_dict_list: list of dict containing each item's attributes

        """
        items_list =[]
        for item_dict in item_dict_list:
            items_list.append(Item( item_dict, self.todomapper))

        return items_list
    

    def board_builder(self, board_dict) -> Board:
        board = Board()
        board.id = board_dict.get('id', '')
        board.name = board_dict.get('name', '')
        board.statuses = self.boardstatuses_builder(board_dict.get('lists'))
        return board

    def boardstatuses_builder(self, board_lists_dicts_list) -> dict:
        board_statuses_dict = {}
        for board_list_dict in board_lists_dicts_list:
            boardstatus = BoardStatus()
            boardstatus.id = board_list_dict.get('id','')
            boardstatus.name = board_list_dict.get('name','')
            boardstatus.pos = board_list_dict.get('pos','')
            board_statuses_dict[boardstatus.id] = boardstatus

        return board_statuses_dict

    def init_todomapper(self):
        todomapper = ToDoMapper()
        todomapper.item_id = 'id'
        todomapper.item_id_short = 'idShort'
        todomapper.item_title = 'name'
        todomapper.item_due_date = 'due'
        todomapper.item_description = 'desc'
        todomapper.item_status = 'idList'
        self.todomapper = todomapper
        