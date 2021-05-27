from datetime import datetime
from dateutil import parser
from .data.boardelements import BoardStatus
from bson.objectid import ObjectId

class ViewModel:
    def __init__(self, items, item_params=None):
        self._items = items
        self._item_params = item_params
        self._statuses = BoardStatus._statuses

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
    def todo_items(self):
        return self.get_items_with_status(BoardStatus._TODO)
    @property
    def doing_items(self):
        return self.get_items_with_status(BoardStatus._DOING)
    @property
    def done_items(self):
        return self.get_items_with_status(BoardStatus._DONE)

    @property
    def recent_done_items(self):
        return self.get_filtered_done_items(self.get_items_with_status(BoardStatus._DONE), False)

    @property
    def older_done_items(self):
        return self.get_filtered_done_items(self.get_items_with_status(BoardStatus._DONE), True)

    @property
    def show_all_done_items(self):
        if len(self.get_items_with_status(BoardStatus._DONE)) < 5:
            return True
        else:
            return False

    def get_items_with_status(self, status):
        items_list = []
        for item in self.items:
            if item.status == status:
                items_list.append(item)
        
        return items_list

    def get_filtered_done_items(self, done_items, show_older = False):
        '''
            Returns a filtered list of items based on the last updated dated.
            
            If showing only older then will return all tasks with last updated date < today
            
            Else if keep recent then will return all tasks with last updated date = today
        '''
        filtered_done_items = []        
        for item in done_items:
            item_last_updated =  item.last_updated.date()
            today = datetime.utcnow().date()
            if (show_older and item_last_updated < today) or (not show_older and item_last_updated == today) :
                filtered_done_items.append(item)
        
        return filtered_done_items