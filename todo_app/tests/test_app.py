import pytest
from todo_app.viewmodel import ViewModel
from todo_app.data.boardelements import *
from datetime import datetime

_TEST_BOARD_NAME = 'test_board_todotest'

def create_test_item(id, title, due_date, description, status, last_updated_date = datetime.utcnow().strftime(r'%Y-%m-%dT%H:%M:%SZ')):
    return Item({Item.item_id: id, Item.item_title: title, Item.item_due_date: due_date, Item.item_description: description, Item.item_status: status, Item.item_last_updated: last_updated_date })

def init_temp_board():
    
    _status_todo_id = '1'
    _status_doing_id = '2'
    _status_done_id = '3'

    test_board_statuses = {
        _status_todo_id: BoardStatus({BoardStatus.boardstatus_id: _status_todo_id, BoardStatus.boardstatus_name: 'To Do'}),
        _status_doing_id: BoardStatus({BoardStatus.boardstatus_id: _status_doing_id, BoardStatus.boardstatus_name: 'Doing'}),
        _status_done_id: BoardStatus({BoardStatus.boardstatus_id: _status_done_id, BoardStatus.boardstatus_name: 'Done'})
    }
    
    test_board = Board({Board.board_id: '1', Board.board_name: _TEST_BOARD_NAME, Board.board_statuses: test_board_statuses})

    test_items = []
    for x in range(0,16):
        status = ''
        if x < 3:
            status = _status_todo_id
        elif x < 10:
            status = _status_doing_id
        else:
            status = _status_done_id
        
        test_items.append(create_test_item(str(x), 'Test %d' % x, '02/02/2021', ' My Test %d is nice' % x, status))

    return test_board, test_items

@pytest.fixture()
def my_viewmodel():
    
    
    # populate board and do some prep
    test_board, test_items = init_temp_board()
    # generate the viewmodel
    viewmodel = ViewModel(
        test_items, 
        test_board.statuses, 
        Item, 
        _TEST_BOARD_NAME)

    # manipulate the done items for testing purposes
    amend_done_items_for_testing(viewmodel.done_items)

    return viewmodel
    

def amend_done_items_for_testing(done_items):
    if len(done_items)>2:
        done_items[0].last_updated = '2020-01-01T00:00:00.000Z'
        done_items[1].last_updated = '2020-01-01T00:00:00.000Z'   
    
def test_get_todo_items(my_viewmodel):
    assert len(my_viewmodel.todo_items) == 3


def test_get_doing_items(my_viewmodel):
    assert len(my_viewmodel.doing_items) == 7

def test_get_done_items(my_viewmodel):
    assert len(my_viewmodel.done_items) == 6

def test_show_all_done_items(my_viewmodel):
    assert my_viewmodel.show_all_done_items == False
    
    # Remove last 2 items which are in Done to bring number of Done under 5.
    my_viewmodel._items = my_viewmodel.items[:-2]
    assert my_viewmodel.show_all_done_items == True

def test_recent_done_items(my_viewmodel):
    assert len(my_viewmodel.recent_done_items) == 4

def test_older_done_items(my_viewmodel):
    assert len(my_viewmodel.older_done_items) == 2