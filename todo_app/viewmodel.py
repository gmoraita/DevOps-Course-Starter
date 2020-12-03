class ViewModel:
    _TODO = 'To Do'
    _DOING = 'Doing'
    _DONE = 'Done'
    
    def __init__(self, items={}, statuses={}, item_params=None, board_name=''):
        self._items = items
        self._statuses = statuses 
        self._item_params = item_params
        self._board_name = board_name

    @property
    def items(self):
        return self._items
    
    @property
    def statuses(self):
        return self._statuses

    @property
    def item_params(self):
        return self._item_params

    @property
    def board_name(self):
        return self._board_name

    def get_items_with_status(self, status):
        items_list = []
        for item in self.items:
            if self.statuses[item.status].name == status:
                items_list.append(item)
        
        return items_list

    def todo_items(self):
        return self.get_items_with_status(ViewModel._TODO)

    def doing_items(self):
        return self.get_items_with_status(ViewModel._DOING)

    def done_items(self):
        return self.get_items_with_status(ViewModel._DONE)