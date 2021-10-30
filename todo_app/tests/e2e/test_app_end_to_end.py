import os
from threading import Thread
import pytest
from unittest.mock import patch, Mock
import dotenv
from todo_app.trello_client import app, TrelloClient
from todo_app.flask_config import Config
from selenium import webdriver
import requests
from flask import Flask, render_template, request, redirect, url_for

@pytest.fixture(scope='module')
def app_with_temp_board():
    # Create the new board & update the board id environment variable

    config = Config()
    # CHANGE TRELLO CLIENT TO NOT TAKE BOARD ID ON INIT AND INSTEAD USE ENV BOARD ID IN THE CLIENT ITSELF

    # Then i don't need to pass it in here or in app and it uses the default environment one whenever it needs to reference it in the class
    test_trello=TrelloClient(config.trello_board_id, config.trello_key, config.trello_token)
    
    
    
    board_id = test_trello.create_trello_board("END-TO-END TEST")
    os.environ['trello_board_id'] = board_id 
    # construct the new application
    application = app.create_app() 
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True 
    thread.start()
    yield application

    # Tear Down
    thread.join(1) 
    test_trello.delete_trello_board(board_id)

@pytest.fixture(scope="module")
def driver():
    with webdriver.Safari() as driver:
        yield driver


def test_task_journey(driver, app_with_temp_board): 
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'


#Use selenium to add to the to_do list and use trello api to see if it's been added to the board 

