import pytest
from unittest.mock import patch, Mock
import dotenv
from todo_app import app
import re
import mongomock

@pytest.fixture 
def client():
# Use our test integration config instead of the 'real' version 
    file_path = dotenv.find_dotenv('.env.test')
    dotenv.load_dotenv(file_path, override=True)
    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client

@patch('requests.request')
def test_index_page(mock_get_requests, client):
    # Replace call to requests.get(url) with our own function
    mock_get_requests.side_effect = mock_get_lists
    response = client.get('/') 
    assert response.status_code == 200
    assert "Done" in response.data.decode()
    

def mock_get_lists(method,url,headers,params):
    # Based on the various URLs they can call - mock the responses
    # Call to create a list
    if re.search('https://api.trello.com/1/lists$', url):
        return Mock_List_Created()

    # Call to return lists
    if re.search('https://api.trello.com/1/boards/test_trello_board_id/lists', url):
        return Mock_Lists()

    # Call to return cards for a list
    if re.search('https://api.trello.com/1/lists/[^/]+/cards', url):
        return Mock_Cards()

    # Call to add a card
    if re.search('https://api.trello.com/1/cards$', url):
        return Mock_Add_Card()

    # Call to move a card to another list
    if re.search('https://api.trello.com/1/cards/[^/]+', url):
        return Mock_Move_Card()

    return None


def Mock_List_Created():
    response = Mock()
    response.status_code = 200
    response.json.return_value = {'id': '616894ef4467272bb801b125', 'name': 'Doing', 'closed': False, 'pos': 256, 'idBoard': '61042da018ae9930f24b1580', 'limits': {}}
    return response

def Mock_Lists():
    response = Mock()
    response.status_code = 200
    response.json.return_value = [{'id': '6120cca00361527e8d02aa39', 'name': 'To Do', 'closed': False, 'pos': 1024, 'softLimit': None, 'idBoard': '61042da018ae9930f24b1580', 'subscribed': False}, {'id': '6168956a1a982c1a6675ac15', 'name': 'Doing', 'closed': False, 'pos': 4608, 'softLimit': None, 'idBoard': '61042da018ae9930f24b1580', 'subscribed': False}, {'id': '6120ccaf2fad2c015b4ccdd9', 'name': 'Done', 'closed': False, 'pos': 8192, 'softLimit': None, 'idBoard': '61042da018ae9930f24b1580', 'subscribed': False}]
    return response

def Mock_Cards():
    response = Mock()
    response.status_code = 200
    response.json.return_value = [{'id': '6120ccaa9e04d28cdf8e1416', 'checkItemStates': None, 'closed': False, 'dateLastActivity': '2021-10-14T20:08:44.093Z', 'desc': '', 'descData': None, 'dueReminder': None, 'idBoard': '61042da018ae9930f24b1580', 'idList': '6120cca00361527e8d02aa39', 'idMembersVoted': [], 'idShort': 30, 'idAttachmentCover': None, 'idLabels': [], 'manualCoverAttachment': False, 'name': 'Done', 'pos': 16384, 'shortLink': 'dtM7IFdK', 'isTemplate': False, 'cardRole': None, 'badges': {'attachmentsByType': {'trello': {'board': 0, 'card': 0}}, 'location': False, 'votes': 0, 'viewingMemberVoted': False, 'subscribed': False, 'fogbugz': '', 'checkItems': 0, 'checkItemsChecked': 0, 'checkItemsEarliestDue': None, 'comments': 0, 'attachments': 0, 'description': False, 'due': None, 'dueComplete': False, 'start': None}, 'dueComplete': False, 'due': None, 'idChecklists': [], 'idMembers': [], 'labels': [], 'shortUrl': 'https://trello.com/c/dtM7IFdK', 'start': None, 'subscribed': False, 'url': 'https://trello.com/c/dtM7IFdK/30-done', 'cover': {'idAttachment': None, 'color': None, 'idUploadedBackground': None, 'size': 'normal', 'brightness': 'dark', 'idPlugin': None}}]
    return response

def Mock_Add_Card():
    return None

def Mock_Move_Card():
    return None

