from .todomapper import ToDoMapper

class Board():
    def __init__(self, board_dict: dict = {}, todomapper : ToDoMapper = ToDoMapper()):
        self.id = board_dict.get(todomapper.board_id,'') 
        self.name = board_dict.get(todomapper.board_id,'') 
        self.statuses = {} 

class BoardStatus():
    def __init__(self, status_dict: dict = {}, todomapper : ToDoMapper = ToDoMapper()):
        self.id = status_dict.get(todomapper.boardstatus_id,'')
        self.name = status_dict.get(todomapper.boardstatus_name,'')
        self.pos = status_dict.get(todomapper.boardstatus_pos,'')

class Item():
    def __init__(self, item_dict: dict = {}, todomapper : ToDoMapper = ToDoMapper()):
        self.id = item_dict.get(todomapper.item_id, '')
        self.id_short = item_dict.get(todomapper.item_id_short, '')
        self.title = item_dict.get(todomapper.item_title, '')
        self.due_date = item_dict.get(todomapper.item_due_date, '')
        self.description = item_dict.get(todomapper.item_description, '')
        self.status = item_dict.get(todomapper.item_status, '')