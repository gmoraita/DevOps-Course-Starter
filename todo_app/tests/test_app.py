import pytest
from todo_app.viewmodel import ViewModel
from todo_app.data.todoapi import TrelloAPI
from todo_app.data.boardelements import Item
from datetime import date, datetime

_TEST_BOARD_NAME = 'test_board_todotest'

def add_item(todoapi, title, due_date, description, status):
    return todoapi.add_item({Item.item_title: title, Item.item_due_date: '01/02/2021', Item.item_description: description}, status)

def delete_temp_board(todoapi, board_id):
    todoapi.call_api('/1/boards/%s' % board_id, 'DELETE').json()

def init_temp_board(todoapi):
    
    #To Do
    add_item(todoapi, 'Test 0', '02/02/2021', 'Test 0 is all right', 0)
    add_item(todoapi, 'Test 1', '02/02/2021', 'Test 1 is good', 0)
    add_item(todoapi, 'Test 2', '03/02/2021', 'Test 2 is cool', 0)
    # Doing
    add_item(todoapi, 'Test 3', '04/02/2021', 'Test 3 is great', 1)
    add_item(todoapi, 'Test 4', '05/02/2021', 'Test 4 is fantastic', 1)
    add_item(todoapi, 'Test 5', '06/02/2021', 'Test 5 is extraordinary', 1)
    add_item(todoapi, 'Test 6', '07/02/2021', 'Test 6 is gigantic', 1)
    add_item(todoapi, 'Test 7', '08/02/2021', 'Test 7 is exotic', 1)
    add_item(todoapi, 'Test 8', '09/02/2021', 'Test 8 is another league', 1)
    add_item(todoapi, 'Test 9', '10/02/2021', 'Test 9 is beyond this world', 1)
    add_item(todoapi, 'Test 10', '11/02/2021', 'Test 10 is infinitely amazing', 1)
    #Done
    add_item(todoapi, 'Test 11', '01/12/2020', 'Test 11 is peculiar', 2)
    add_item(todoapi, 'Test 12', '02/12/2020', 'Test 12 is weird', 2)
    add_item(todoapi, 'Test 13', '02/12/2020', 'Test 13 is bananas', 2)
    add_item(todoapi, 'Test 14', '02/12/2020', 'Test 14 is crazy', 2)
    add_item(todoapi, 'Test 17', '02/12/2020', 'Test 15 is mental', 2)
    add_item(todoapi, 'Test 16', '02/12/2020', 'Test 16 is insane', 2)

@pytest.fixture(scope="session")
def my_viewmodel():
    
    todoapi = TrelloAPI()
    # create board
    board = todoapi.call_api('/1/boards/', 'POST', {'name': _TEST_BOARD_NAME+'_'+date.today().strftime(r"%Y%m%d") + datetime.now().strftime(r"%H%M%S%f")}).json()
    # load board
    todoapi.board = todoapi.load_board(board['name'])
    # populate board and do some prep
    init_temp_board(todoapi)
    # generate the viewmodel
    viewmodel = ViewModel(
        todoapi.get_list_of_items(), 
        todoapi.board.statuses, 
        Item, 
        _TEST_BOARD_NAME)

    # manipulate the done items for testing purposes
    amend_done_items_for_testing(viewmodel.done_items)

    yield viewmodel
    delete_temp_board(todoapi, board['id'])

def amend_done_items_for_testing(done_items):
    if len(done_items)>2:
        done_items[0].last_updated = '2020-01-01T00:00:00.000Z'
        done_items[1].last_updated = '2020-01-01T00:00:00.000Z'   
    
def test_get_todo_items(my_viewmodel):
    assert len(my_viewmodel.todo_items) == 3


def test_get_doing_items(my_viewmodel):
    assert len(my_viewmodel.doing_items) == 8

def test_get_done_items(my_viewmodel):
    assert len(my_viewmodel.done_items) == 6

def test_show_all_done_items(my_viewmodel):
    assert my_viewmodel.show_all_done_items == False

def test_recent_done_items(my_viewmodel):
    assert len(my_viewmodel.recent_done_items) == 4

def test_older_done_items(my_viewmodel):
    assert len(my_viewmodel.older_done_items) == 2