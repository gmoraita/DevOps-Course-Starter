from abc import ABC, abstractmethod
from .boardelements import *
import pymongo
import requests
from bson.objectid import ObjectId
from datetime import datetime

class TodoAPI():
    def __init__(self, config):
        
        self.tasks = pymongo.MongoClient(config.get('DB_CONNECTION_STRING')).todoapp['tasks']
        
    def get_list_of_items(self): 
        return self.build_items_list(self.tasks.find())
        
    def add_item(self, item_dict, status_index = 0):
        return self.tasks.insert_one({**item_dict, Item.item_status : BoardStatus._TODO, Item.item_last_updated: datetime.utcnow()}).inserted_id

    def delete_item(self, id):
        return self.tasks.delete_one({Item.item_id : ObjectId(id)})
 
    def modify_item(self, id, attributes):
        return self.tasks.update_one({Item.item_id : ObjectId(id)}, {"$set": {**attributes, Item.item_last_updated: datetime.utcnow()}} )

    def build_items_list(self, item_dict_list: list) -> list :
        items_list =[]
        for item_dict in item_dict_list:
            items_list.append(Item( item_dict))

        return items_list
  