class ViewModel:
    def __init__(self, items, statuses, item_params, board_name):
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