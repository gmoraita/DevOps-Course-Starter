import pytest
from todo_app.viewmodel import ViewModel
from todo_app.data.boardelements import *
from datetime import datetime

_TEST_BOARD_NAME = 'test_board_todotest'

def create_test_item(id, title, due_date, description, status):
    return Item({Item.item_id: id, Item.item_title: title, Item.item_due_date: due_date, Item.item_description: description, Item.item_status: status, Item.item_last_updated: datetime.utcnow().strftime(r'%Y-%m-%dT%H:%M:%SZ') })

def init_temp_board():
    
    _status_todo_id = '123a'
    _status_doing_id = '345b'
    _status_done_id = '678c'

    test_board_statuses = {
        _status_todo_id: BoardStatus({BoardStatus.boardstatus_id: _status_todo_id, BoardStatus.boardstatus_name: 'To Do'}),
        _status_doing_id: BoardStatus({BoardStatus.boardstatus_id: _status_doing_id, BoardStatus.boardstatus_name: 'Doing'}),
        _status_done_id: BoardStatus({BoardStatus.boardstatus_id: _status_done_id, BoardStatus.boardstatus_name: 'Done'})
    }
    
    test_board = Board({Board.board_id: '123', Board.board_name: _TEST_BOARD_NAME, Board.board_statuses: test_board_statuses})

    test_items = [
        # To Do
        create_test_item('0', 'Test 0', '02/02/2021', 'Test 0 is all right', _status_todo_id), 
        create_test_item('0', 'Test 1', '02/02/2021', 'Test 1 is good', _status_todo_id),
        create_test_item('0', 'Test 2', '03/02/2021', 'Test 2 is cool', _status_todo_id),
        # Doing
        create_test_item('0', 'Test 3', '04/02/2021', 'Test 3 is great',_status_doing_id),
        create_test_item('0', 'Test 4', '05/02/2021', 'Test 4 is fantastic',_status_doing_id),
        create_test_item('0', 'Test 5', '06/02/2021', 'Test 5 is extraordinary',_status_doing_id),
        create_test_item('0', 'Test 6', '07/02/2021', 'Test 6 is gigantic',_status_doing_id),
        create_test_item('0', 'Test 7', '08/02/2021', 'Test 7 is exotic',_status_doing_id),
        create_test_item('0', 'Test 8', '09/02/2021', 'Test 8 is another league',_status_doing_id),
        create_test_item('0', 'Test 9', '10/02/2021', 'Test 9 is beyond this world',_status_doing_id),
        create_test_item('0', 'Test 10', '11/02/2021', 'Test 10 is infinitely amazing',_status_doing_id),
        #Done
        create_test_item('0', 'Test 11', '01/12/2020', 'Test 11 is peculiar',_status_done_id),
        create_test_item('0', 'Test 12', '02/12/2020', 'Test 12 is weird',_status_done_id),
        create_test_item('0', 'Test 13', '02/12/2020', 'Test 13 is bananas',_status_done_id),
        create_test_item('0', 'Test 14', '02/12/2020', 'Test 14 is crazy',_status_done_id),
        create_test_item('0', 'Test 17', '02/12/2020', 'Test 15 is mental',_status_done_id),
        create_test_item('0', 'Test 16', '02/12/2020', 'Test 16 is insane',_status_done_id),
    ]
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
    assert len(my_viewmodel.doing_items) == 8

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