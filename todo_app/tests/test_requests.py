import pytest
from dotenv import find_dotenv , load_dotenv
from todo_app import app
from .mock_responses import MockResponses
from mongomock import patch, MongoClient
from ..data.boardelements import BoardStatus, Item
from datetime import datetime
import os

mockresponses = MockResponses()

def mock_db_records():
    
    mock_tasks = [  {
                    Item.item_title: "Task 1",
                    Item.item_due_date: "12/03/2021",
                    Item.item_description: "My cool task 1",
                    Item.item_status: BoardStatus._TODO, 
                    Item.item_last_updated: datetime.utcnow()
                }, 
                {
                    Item.item_title: "Task 2",
                    Item.item_due_date: "14/03/2021",
                    Item.item_description: "My cool task 2",
                    Item.item_status: BoardStatus._TODO, 
                    Item.item_last_updated: datetime.utcnow()
                }]
   
    return mock_tasks

@pytest.fixture
def app_client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = app.create_app()
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as app_client:
        yield app_client  


@patch(servers=(('fakemongo', 27017),))
def test_add_record(app_client):
    db_conn = os.getenv('DB_CONNECTION_STRING')
    client = MongoClient(db_conn)
    tasks = client.get_default_database().todoapp['tasks']
    tasks.insert_many(mock_db_records())
    

    response = app_client.post('/add', data=dict(mock_db_records()[0]))
    assert response.status_code == 200 

    #html_string = str(response.data)
    #assert 'Task 1' in html_string
    #assert html_string.count('status_0') == 4 # 4 in todo
    #assert html_string.count('status_1') == 3 # 3 doing
    #assert html_string.count('status_2') == 5 # 5 done


