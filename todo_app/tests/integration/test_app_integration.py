import pytest
import dotenv
from todo_app import app
import re
import mongomock
import pymongo
import os

@pytest.fixture 
def client():
# Use our test integration config instead of the 'real' version 
    file_path = dotenv.find_dotenv('.env.test')
    dotenv.load_dotenv(file_path, override=True)
    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client

def test_add_item(client):
    #Check we can add an item
    #Check it is in the DB
    db = pymongo.MongoClient(os.environ.get('mongo_db_connection'))['test-db']
    collection = db['items']
    item_to_add = {"name": "Test-Item-Devops", "status": "to do"}
    collection.insert_one(item_to_add)
    response = client.get('/')
    print(response.data)
    assert response.status_code == 200
    assert "Test-Item-Devops" in response.data.decode()
    