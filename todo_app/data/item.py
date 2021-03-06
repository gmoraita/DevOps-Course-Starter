class Item():
    TODO = 'To Do'
    DOING = 'Doing'
    DONE = 'Done'
    statuses = [TODO, DOING, DONE]
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