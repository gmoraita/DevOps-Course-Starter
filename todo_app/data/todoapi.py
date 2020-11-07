from abc import ABC, abstractmethod
from configparser import ConfigParser
from .boardelements import *
import os
import requests

class TrelloAPI():
    TRELLO_ROOT_URL = 'https://api.trello.com'
    CREDS_CONFIG_FILE = 'trello.config'
   
    def __init__(self):
        #keep these calls in this sequence
        self.init_todomapper()    
        self.auth_query = self.get_trello_creds_section('trello_auth')
        self.user = self.get_trello_creds_section('trello_user').get('user')
        self.board = self.load_board(self.get_trello_creds_section('trello_board').get('name')) 

    def get_list_of_items(self):
        return self.build_items_list(self.call_api('/1/boards/%s/cards' % self.board.id,'GET').json())
       
    def add_item(self, item_dict):
        return self.call_api('/1/cards', 'POST', {**{'idList' : list(self.board.statuses.values())[0].id}, **item_dict}).json()
 
    def delete_item(self, id):
        return self.call_api('/1/cards/'+id, 'DELETE').json()
 
    def modify_item(self, id, atributes):
        return self.call_api('/1/cards/'+id, 'PUT', atributes).json()

    def load_board(self, board_name) -> Board:
        board = Board()
        boards = self.call_api('/1/members/%s/boards' % self.user, 'GET', {'lists':'all'}).json()

        for board_dict in boards:
            board = self.board_builder(board_dict)
            if board.name == board_name:
                break
        
        return board

    def call_api(self, api, method, params = {}) -> requests.Response:
        """
        Makes a call to the Trello API using key and token
        """
        
        url = self.TRELLO_ROOT_URL + api
        headers = {"Accept": "application/json"}
        query = {**self.auth_query, **params}
        
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

    def build_items_list(self, item_dict_list: list) -> list :
        items_list =[]
        for item_dict in item_dict_list:
            items_list.append(Item( item_dict, self.todomapper))

        return items_list
    

    def board_builder(self, board_dict) -> Board:
        board = Board(board_dict, self.todomapper)
        board.statuses = self.boardstatuses_builder(board_dict.get(self.todomapper.board_statuses))
        return board

    def boardstatuses_builder(self, board_lists_dicts_list) -> dict:
        board_statuses_dict = {}
        for board_list_dict in board_lists_dicts_list:
            boardstatus = BoardStatus(board_list_dict, self.todomapper)
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
        todomapper.boardstatus_id = 'id'
        todomapper.boardstatus_name = 'name'
        todomapper.boardstatus_pos = 'pos'
        todomapper.board_id = 'id'
        todomapper.board_name = 'name'
        todomapper.board_statuses = 'lists'
        
        self.todomapper = todomapper
        