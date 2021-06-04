import pytest
from dotenv import find_dotenv , load_dotenv
from todo_app import app
import mongomock
import pymongo
from ..data.item import Item
from datetime import datetime
import os
from bson.objectid import ObjectId


initial_mock_tasks = [{
        Item.item_title: "Task 1",
        Item.item_due_date: "12/03/2021",
        Item.item_description: "My cool task 1",
        Item.item_status: Item.TODO, 
        Item.item_last_updated: datetime.utcnow()
    }, 
    {
        Item.item_title: "Task 2",
        Item.item_due_date: "14/03/2021",
        Item.item_description: "My cool task 2",
        Item.item_status: Item.TODO, 
        Item.item_last_updated: datetime.utcnow()
    }]
   


task_to_be_deleted = {
        Item.item_title: "Task 4",
        Item.item_due_date: "22/03/2021",
        Item.item_description: "My cool task 4",
        Item.item_status: Item.TODO
    }

task_to_be_moved = {
        Item.item_title: "Task 5",
        Item.item_due_date: "29/03/2021",
        Item.item_description: "My cool task 5",
        Item.item_status: Item.TODO
    }

def get_db_collection():
    db_conn = os.getenv('DB_CONNECTION_STRING')
    client = pymongo.MongoClient(db_conn)
    return client.todoapp['tasks']

@pytest.fixture
def app_client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    # Initialise mongomock here.
    with mongomock.patch(servers=(('fakemongo', 27017),)):
        # Create the new app.
        test_app = app.create_app()
        # Use the app to create a test_client that can be used in our tests.
        with test_app.test_client() as client:
            yield client


def test_show_tasks(app_client):
    tasks = get_db_collection() 
    tasks.insert_many(initial_mock_tasks)
    
    response = app_client.get('/')
    assert response.status_code == 200 
    assert tasks.find({Item.item_title: "Task 1"}) is not None

def test_add_task(app_client):
    new_task = {
        Item.item_title: "Task 3",
        Item.item_due_date: "17/03/2021",
        Item.item_description: "My cool task 3"
    }
    tasks = get_db_collection() 

    response = app_client.post('/add', data=dict(new_task))
    assert response.status_code == 200 

def test_delete_task(app_client):
    tasks = get_db_collection() 
    inserted_id = tasks.insert_one(task_to_be_deleted).inserted_id
    
    assert tasks.find_one({Item.item_id: inserted_id}) is not None
    response = app_client.post('/delete/%s' % ObjectId(inserted_id))
    assert response.status_code == 200 
    assert tasks.find_one({Item.item_id: inserted_id}) is None

def test_move_task(app_client):
    tasks = get_db_collection() 
    inserted_id = tasks.insert_one(task_to_be_moved).inserted_id
    
    assert tasks.find_one({Item.item_id: inserted_id, Item.item_status: Item.TODO}) is not None
    response = app_client.post('/setstatus/%s/%s' % (ObjectId(inserted_id), Item.DONE))
    assert response.status_code == 200 
    assert tasks.find_one({Item.item_id: inserted_id, Item.item_status: Item.DONE}) is not None
