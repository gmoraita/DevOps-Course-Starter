import pytest
from todo_app.viewmodel import ViewModel
from todo_app.data.boardelements import *
from datetime import datetime

_TEST_BOARD_NAME = 'test_board_todotest'
_STATUS_TODO_ID = '1'
_STATUS_DOING_ID = '2'
_STATUS_DONE_ID = '3'


def create_test_item(id, title, due_date, description, status, last_updated_date = datetime.utcnow().strftime(r'%Y-%m-%dT%H:%M:%SZ')):
    return Item({Item.item_id: id, Item.item_title: title, Item.item_due_date: due_date, Item.item_description: description, Item.item_status: status, Item.item_last_updated: last_updated_date })

def create_test_board_statuses():
    return {
            _STATUS_TODO_ID: BoardStatus({BoardStatus.boardstatus_id: _STATUS_TODO_ID, BoardStatus.boardstatus_name: 'To Do'}),
            _STATUS_DOING_ID: BoardStatus({BoardStatus.boardstatus_id: _STATUS_DOING_ID, BoardStatus.boardstatus_name: 'Doing'}),
            _STATUS_DONE_ID: BoardStatus({BoardStatus.boardstatus_id: _STATUS_DONE_ID, BoardStatus.boardstatus_name: 'Done'})
        }

def create_test_items():
    test_items = []
    for x in range(0,16):
        status = ''
        if x < 3:
            status = _STATUS_TODO_ID
        elif x < 10:
            status = _STATUS_DOING_ID
        else:
            status = _STATUS_DONE_ID
        
        test_items.append(create_test_item(str(x), 'Test %d' % x, '02/02/2021', ' My Test %d is nice' % x, status))
    
    return test_items

def create_test_board(test_board_statuses):
    return Board({Board.board_id: '1', Board.board_name: _TEST_BOARD_NAME, Board.board_statuses: test_board_statuses})

@pytest.fixture()
def my_viewmodel():
    return ViewModel(create_test_items(), create_test_board(create_test_board_statuses()), Item)
    

def move_last_updated_to_the_past(items, num):
    if num > len(items):
        num = len(items) -1 
    for x in range(0,num):
        items[x].last_updated = '2020-01-01T00:00:00.000Z'
        
    
def test_get_todo_items(my_viewmodel):
    assert len(my_viewmodel.todo_items) == 3


def test_get_doing_items(my_viewmodel):
    assert len(my_viewmodel.doing_items) == 7

def test_get_done_items(my_viewmodel):
    assert len(my_viewmodel.done_items) == 6

def test_show_all_done_items(my_viewmodel):
    move_last_updated_to_the_past(my_viewmodel.done_items, 2)
    assert my_viewmodel.show_all_done_items == False
    
    # Remove last 2 items which are in Done to bring number of Done under 5.
    my_viewmodel._items = my_viewmodel.items[:-2]
    assert my_viewmodel.show_all_done_items == True

def test_recent_done_items(my_viewmodel):
    move_last_updated_to_the_past(my_viewmodel.done_items, 2)
    assert len(my_viewmodel.recent_done_items) == 4

def test_older_done_items(my_viewmodel):
    move_last_updated_to_the_past(my_viewmodel.done_items, 2)
    assert len(my_viewmodel.older_done_items) == 2