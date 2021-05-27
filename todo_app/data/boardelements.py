class BoardStatus():
    _TODO = 'To Do'
    _DOING = 'Doing'
    _DONE = 'Done'
    _statuses = [_TODO, _DOING, _DONE]
    boardstatus_id = 'id'
    boardstatus_name = 'name'
    boardstatus_pos = 'pos'
    def __init__(self, status_dict: dict = {}):
        self.id = status_dict.get(self.boardstatus_id,'')
        self.name = status_dict.get(self.boardstatus_name,'')
        self.pos = status_dict.get(self.boardstatus_pos,'')
    

class Item():
    item_id = '_id'
    item_id_short = 'idShort'
    item_title = 'name'
    item_due_date = 'due'
    item_description = 'desc'
    item_status = 'status'
    item_last_updated = 'dateLastActivity'
    def __init__(self, item_dict: dict = {}):
        self.id = str(item_dict.get(self.item_id, ''))
        self.id_short = item_dict.get(self.item_id_short, '')
        self.title = item_dict.get(self.item_title, '')
        self.due_date = item_dict.get(self.item_due_date, '')
        self.description = item_dict.get(self.item_description, '')
        self.status = item_dict.get(self.item_status, '')
        self.last_updated = item_dict.get(self.item_last_updated, '')