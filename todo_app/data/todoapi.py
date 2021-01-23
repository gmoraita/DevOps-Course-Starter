from abc import ABC, abstractmethod
from .boardelements import *
from .trelloapicaller import TrelloAPICaller
import requests

class TrelloAPI():
   
    def __init__(self, config):
        self.init_todomapping() 
        self.config = config
        self.api = TrelloAPICaller(config)
        self._board = None
        
    def get_list_of_items(self):  
        return self.build_items_list(self.api.call_api('/boards/%s/cards' % self.board.id,'GET').json())
       
    def add_item(self, item_dict, status_index = 0):
        return self.api.call_api('/cards', 'POST', {**{'idList' : list(self.board.statuses.values())[status_index].id}, **item_dict}).json()
 
    def delete_item(self, id):
        return self.api.call_api('/cards/'+id, 'DELETE').json()
 
    def modify_item(self, id, atributes):
        return self.api.call_api('/cards/'+id, 'PUT', atributes).json()

    @property
    def board(self):
        if self._board == None:
            self._board = self.load_board() 

        return self._board

    def load_board(self):
        if  self.config.get('TRELLO_BOARD_ID', None) != None:
            return self.load_board_by_id(self.config['TRELLO_BOARD_ID'])    
        else:
            return self.load_board_by_name(self.config['TRELLO_BOARD_NAME'])

    def load_board_by_name(self, board_name) -> Board:
        boards = self.api.call_api('/members/%s/boards' % self.config['TRELLO_USER'], 'GET', {'lists':'all'}).json()

        for board_dict in boards:
            board = self.board_builder(board_dict)
            if board.name == board_name:
                return board
        
        return None

    def load_board_by_id(self, board_id) -> Board:
        return self.board_builder(self.api.call_api('/boards/%s' % board_id, 'GET', {'lists':'all'}).json())

    def build_items_list(self, item_dict_list: list) -> list :
        items_list =[]
        for item_dict in item_dict_list:
            items_list.append(Item( item_dict))

        return items_list
    

    def board_builder(self, board_dict) -> Board:
        board = Board(board_dict)
        board.statuses = self.boardstatuses_builder(board_dict.get(Board.board_statuses))
        return board

    def boardstatuses_builder(self, board_lists_dicts_list) -> dict:
        board_statuses_dict = {}
        for board_list_dict in board_lists_dicts_list:
            boardstatus = BoardStatus(board_list_dict)
            board_statuses_dict[boardstatus.id] = boardstatus
        return board_statuses_dict

    def init_todomapping(self):
        Item.item_id = 'id'
        Item.item_id_short = 'idShort'
        Item.item_title = 'name'
        Item.item_due_date = 'due'
        Item.item_description = 'desc'
        Item.item_status = 'idList'
        Item.item_last_updated = 'dateLastActivity'
        BoardStatus.boardstatus_id = 'id'
        BoardStatus.boardstatus_name = 'name'
        BoardStatus.boardstatus_pos = 'pos'
        Board.board_id = 'id'
        Board.board_name = 'name'
        Board.board_statuses = 'lists'

        