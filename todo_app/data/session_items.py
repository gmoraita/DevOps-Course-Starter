import json
from flask import session
from .todoapi import todo_api_factory, _TRELLO

TODO_API = _TRELLO
todoapi = todo_api_factory(TODO_API)

def get_todomapper():
    """
    Fetches the ToDoMapper with all the field mappings .

    Returns:
        ToDoMapper: The ToDoMapper with all the field mappings.
    """ 
    return todoapi.todomapper

def get_statuses():
    """
    Fetches all statuses .

    Returns:
        list: The list of statuses.
    """ 
    return todoapi.get_list_of_statuses()

def get_items():
    """
    Fetches all items from the apo.

    Returns:
        list: The list of items sorted by status and then by ID.
    """ 

    return sorted(todoapi.get_list_of_items(), key=lambda item : (item[0].status))

def add_item(item_dict):
    """
    Adds a new item with the specified title to the todo list.

    Args:
        title: The title of the item.

    """

    return todoapi.add_item(item_dict)


def update_item(id, item_params:dict):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        id: The id of the item to update.
        item_params: a dictionary of the item params to update (Trello params)
    """

    return todoapi.modify_item(id, item_params)
    

def delete_item(id):
    """
    Deletes a specific item from the session.

    Args:
        id: The id of the item to delete.

    """
    return todoapi.delete_item(id)
    