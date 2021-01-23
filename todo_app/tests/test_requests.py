import pytest
from dotenv import find_dotenv , load_dotenv
from todo_app import app
from mock import patch, Mock
from .mock_responses import MockResponses
import os

mockresponses = MockResponses()


def mock_responses(method, url, **kwargs):
    response = Mock()
    if url.startswith('https://api.trello.com/1/boards/%s/cards' % mockresponses.board_id):
        response.json.return_value = mockresponses.cards
        return response
        
    elif url.startswith('https://api.trello.com/1/members/%s/boards' % os.getenv('TRELLO_USER')):
        response.json.return_value = mockresponses.boards
        return response


    return None


@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = app.create_app()
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client  


@patch('requests.request')
def test_index_page(mock_get_requests, client):
    mock_get_requests.side_effect = mock_responses

    response = client.get('/')
    assert response.status_code == 200 
    
    html_string = str(response.data)
    assert 'Tempting to say' in html_string
    assert html_string.count('status_0') == 4 # 4 in todo
    assert html_string.count('status_1') == 3 # 3 doing
    assert html_string.count('status_2') == 5 # 5 done