import pytest
import pymongo
from dotenv import find_dotenv , load_dotenv
from todo_app.data.item import Item
from todo_app import app
from datetime import datetime
import os
from threading import Thread 
from selenium import webdriver
from seleniumrequests import Firefox
from selenium.webdriver.support.ui import Select
from todo_app.app_config import Config

_TODO_URL = 'http://localhost:5000'


def create_temp_tasks_collection():
    temp_tasks_collection_name = 'temptasks_%s' % datetime.now().strftime(r"%Y%m%d%H%M%S%f")
    os.environ['DATA_COLLECTION'] = temp_tasks_collection_name
    return temp_tasks_collection_name

def delete_temp_tasks_collection(temp_tasks_collection_name):
    test_tasks = pymongo.MongoClient(Config().DB_CONNECTION_STRING).todoapp[temp_tasks_collection_name]
    test_tasks.drop()
    del os.environ['DATA_COLLECTION']


@pytest.fixture(scope='module')
def test_app():
    # Load the env file
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    
    # Create the new board & update the board id environment variable
    test_tasks = create_temp_tasks_collection()
    
    # construct the new application
    application = app.create_app()

    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app
    
    # Tear Down
    thread.join(1)
    delete_temp_tasks_collection(test_tasks)

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
    
    #get task id added
    taskid = driver.page_source[driver.page_source.find('status_select_')+len('status_select_'):driver.page_source.find('status_select_')+len('status_select_')+24]

    #check item status change to Doing
    select = Select(driver.find_element_by_id('status_select_%s' % taskid))
    select.select_by_index(1)
    driver.get(_TODO_URL)
    driver.refresh()
    assert ('/static/status_doing.png' in driver.page_source)
    

    #check item deleted
    driver.find_element_by_id("delete_%s" % taskid).click()
    driver.get(_TODO_URL)
    driver.refresh()
    assert ('a test description' not in driver.page_source)
    