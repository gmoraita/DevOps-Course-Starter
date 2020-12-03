import pytest
from todo_app.viewmodel import ViewModel
from todo_app.data.todoapi import TrelloAPI
from todo_app.data.boardelements import Item

_TEST_BOARD_NAME = 'test_board_todotest'

def delete_temp_board(todoapi, board_id):
    todoapi.call_api('/1/boards/%s' % board_id, 'DELETE').json()

def populate_temp_board(todoapi):
    #To Do
    todoapi.add_item({Item.item_title: 'Test 1', Item.item_due_date: '01/02/2021', Item.item_description: 'Test 1 is ok'}, 0)
    todoapi.add_item({Item.item_title: 'Test 2', Item.item_due_date: '02/02/2021', Item.item_description: 'Test 2 is good'}, 0)
    todoapi.add_item({Item.item_title: 'Test 3', Item.item_due_date: '03/02/2021', Item.item_description: 'Test 3 is cool'}, 0)
    # Doing
    todoapi.add_item({Item.item_title: 'Test 4', Item.item_due_date: '04/02/2021', Item.item_description: 'Test 4 is great'}, 1)
    todoapi.add_item({Item.item_title: 'Test 5', Item.item_due_date: '05/02/2021', Item.item_description: 'Test 5 is fantastic'},1)
    todoapi.add_item({Item.item_title: 'Test 6', Item.item_due_date: '06/02/2021', Item.item_description: 'Test 6 is extraordinary'},1)
    #Done
    todoapi.add_item({Item.item_title: 'Test 7', Item.item_due_date: '07/02/2021', Item.item_description: 'Test 7 is peculiar'},2)
    todoapi.add_item({Item.item_title: 'Test 8', Item.item_due_date: '08/02/2021', Item.item_description: 'Test 8 is weird'},2)


@pytest.fixture(scope="module")
def my_viewmodel():
    
    todoapi = TrelloAPI()
    #create board
    board = todoapi.call_api('/1/boards/', 'POST', {'name': _TEST_BOARD_NAME}).json()
    #load board
    todoapi.board = todoapi.load_board(board['name'])
    #populate board
    populate_temp_board(todoapi)

    viewmodel = ViewModel(
        todoapi.get_list_of_items(), 
        todoapi.board.statuses, 
        Item, 
        _TEST_BOARD_NAME)

    
    yield viewmodel
    delete_temp_board(todoapi, board['id'])

    
    
def test_get_todo_items(my_viewmodel):
    assert len(my_viewmodel.todo_items()) == 3


def test_get_doing(my_viewmodel):
    assert len(my_viewmodel.doing_items()) == 3


def test_get_done(my_viewmodel):
    assert len(my_viewmodel.done_items()) == 2