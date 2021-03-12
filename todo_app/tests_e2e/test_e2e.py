import pytest
from dotenv import find_dotenv , load_dotenv
from todo_app.data.trelloapicaller import TrelloAPICaller
from todo_app.data.boardelements import Item
from todo_app import app
from datetime import datetime
import os
from threading import Thread 
from selenium import webdriver
from seleniumrequests import Firefox
from selenium.webdriver.support.ui import Select
from todo_app.app_config import Config


_TEST_BOARD_NAME = 'test_board_todotest'
_TODO_URL = 'http://localhost:5000'


def create_temp_board():
    api = TrelloAPICaller(Config().asDict())
    board = api.call_api('/boards/', 'POST', {'name': _TEST_BOARD_NAME+'_'+datetime.now().strftime(r"%Y%m%d%H%M%S%f")}).json()
    
    return board.get('id')

def delete_temp_board(board_id):
    api = TrelloAPICaller(Config().asDict())
    api.call_api('/boards/%s' % board_id, 'DELETE').json()


@pytest.fixture(scope='module')
def test_app():
    # Load the env file
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    
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
    os.environ['MOZ_HEADLESS'] = '1'
    with Firefox() as driver:
        yield driver
 
    
def test_task_journey(driver: Firefox, test_app):
    #check board created
    driver.get(_TODO_URL)
    assert driver.title == 'To-Do App'

    #check item added
    elem_form_task_title = driver.find_element_by_name("name")
    elem_form_task_title.send_keys('my very own task')
    elem_form_task_due = driver.find_element_by_name("due")
    elem_form_task_due.send_keys('07/07/2022')
    elem_form_task_desc = driver.find_element_by_name("desc")
    elem_form_task_desc.send_keys('a test description')
    
    driver.find_element_by_id("todoform").submit()
    driver.get(_TODO_URL)
    driver.refresh()
    assert ('a test description' in driver.page_source)
    
    #check item status change to Doing
    select = Select(driver.find_element_by_id('status_select_1'))
    select.select_by_index(1)
    driver.get(_TODO_URL)
    driver.refresh()
    assert ('/static/status_1.png' in driver.page_source)
    

    #check item deleted
    driver.find_element_by_id("delete_1").click()
    driver.get(_TODO_URL)
    driver.refresh()
    assert ('a test description' not in driver.page_source)
    