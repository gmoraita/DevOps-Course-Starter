from .todomapper import ToDoMapper

class Board():
    def __init__(self):
        self.id = '' 
        self.name = '' 
        self.statuses = {} 

class BoardStatus():
    def __init__(self):
        self.id = ''
        self.name = ''
        self.pos = ''

class Item():
    def __init__(self, item_dict: dict = {}, todomapper : ToDoMapper = ToDoMapper()):
        self.id = item_dict.get(todomapper.item_id, '')
        self.id_short = item_dict.get(todomapper.item_id_short, '')
        self.title = item_dict.get(todomapper.item_title, '')
        self.due_date = item_dict.get(todomapper.item_due_date, '')
        self.description = item_dict.get(todomapper.item_description, '')
        self.status = item_dict.get(todomapper.item_status, '')