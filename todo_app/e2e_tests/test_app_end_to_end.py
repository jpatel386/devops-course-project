import os
from threading import Thread
import pytest
from unittest.mock import patch, Mock
import dotenv
from todo_app.trello_client import TrelloClient
from todo_app import app
from todo_app.flask_config import Config
from selenium import webdriver
import requests
from flask import Flask, render_template, request, redirect, url_for

@pytest.fixture(scope='module')
def app_with_temp_board():
    # Create the new board & update the board id environment variable

    file_path = dotenv.find_dotenv('.env')
    dotenv.load_dotenv(file_path, override=True)

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
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome(options=opts) as driver:
        #driver.maximize_window()
        yield driver


def test_task_journey(driver, app_with_temp_board): 
    driver.get('http://127.0.0.1:5000/')
    assert driver.title == 'To-Do App'


def test_item_journey(driver, app_with_temp_board):
    driver.get('http://127.0.0.1:5000/')
    add_item_link = driver.find_element_by_link_text('Add a new item')
    add_item_link.click()
    driver.implicitly_wait(15)
    text_box = driver.find_element_by_id("item")
    text_box.send_keys("test item in e2e testing")
    add_button = driver.find_element_by_id('submit')
    add_button.click()
    # Check we were redirected back to home
    assert driver.current_url == 'http://127.0.0.1:5000/'
    todo_text = driver.find_element_by_xpath("//*[@id='Todo Table']/tbody/tr[1]/td[1]").text
    assert todo_text == "test item in e2e testing"
    # Mark as doing now
    mark_as_doing_link = driver.find_element_by_link_text('Doing')
    mark_as_doing_link.click()
    assert driver.current_url == 'http://127.0.0.1:5000/'
    doing_text = driver.find_element_by_xpath("//*[@id='Doing Table']/tbody/tr[1]/td[1]").text
    assert doing_text == "test item in e2e testing"
    # Mark as done now
    mark_as_done_link = driver.find_element_by_link_text('Done')
    mark_as_done_link.click()
    assert driver.current_url == 'http://127.0.0.1:5000/'
    done_text = driver.find_element_by_xpath("//*[@id='Done Table']/tbody/tr[1]/td[1]").text
    assert done_text == "test item in e2e testing"
    # Re-mark as todo
    mark_as_todo_link = driver.find_element_by_link_text('To Do')
    mark_as_todo_link.click()
    assert driver.current_url == 'http://127.0.0.1:5000/'
    todo_text = driver.find_element_by_xpath("//*[@id='Todo Table']/tbody/tr[1]/td[1]").text
    assert todo_text == "test item in e2e testing"
