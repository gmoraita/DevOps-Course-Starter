import pytest

from todo_app.data.todoapi import TrelloAPI
from todo_app.data.boardelements import Item
from todo_app import app
from datetime import date, datetime
import os
from threading import Thread 
from selenium import webdriver
from seleniumrequests import Firefox

_TEST_BOARD_NAME = 'test_board_todotest'
_TODO_URL = 'http://localhost:5000'

def create_temp_board():
    todoapi = TrelloAPI()
    board = todoapi.call_api('/1/boards/', 'POST', {'name': _TEST_BOARD_NAME+'_'+date.today().strftime(r"%Y%m%d") + datetime.now().strftime(r"%H%M%S%f")}).json()
    
    return board.get('id')

def delete_temp_board(board_id):
    todoapi = TrelloAPI()
    todoapi.call_api('/1/boards/%s' % board_id, 'DELETE').json()


@pytest.fixture(scope='module')
def test_app():
    # Create the new board & update the board id environment variable
    board_id = create_temp_board()
    os.environ['TRELLO_BOARD_ID'] = board_id
    # construct the new application
    application = app.create_app()

    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app
    
    # Tear Down
    thread.join(1)
    delete_temp_board(board_id)

@pytest.fixture(scope="module")
def driver():
    with Firefox() as driver:
        yield driver
 
    
def test_task_journey(driver: Firefox, test_app):
    #check board created
    driver.get(_TODO_URL)
    assert driver.title == 'To-Do App'

    #check item added
    add_response = driver.request('POST', _TODO_URL+ '/add', data = {Item.item_title: 'a test I do', Item.item_due_date: '01/02/2021', Item.item_description: 'a test description'})
    assert add_response.text.count('a test I do') == 1

    #check item status change to Doing
    new_task_id = add_response.text[add_response.text.find('setstatus/')+10:add_response.text.find('/',add_response.text.find('setstatus/')+10)]
    doing_status = add_response.text[add_response.text.find('<option value="')+15:add_response.text.find('">Doing</option>')]
    change_status_response = driver.request('POST', _TODO_URL+ '/setstatus/%s/%s' %(new_task_id, doing_status))
    assert change_status_response.text.count('"/> Doing</td>') == 1

    #check item deleted
    delete_response = driver.request('POST', _TODO_URL+'/delete/%s' % new_task_id)
    assert delete_response.text.count('a test I do') == 0