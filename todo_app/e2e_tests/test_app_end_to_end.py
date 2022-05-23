import os
from threading import Thread
import pytest
from unittest.mock import patch, Mock
import dotenv
from todo_app import app
from todo_app.flask_config import Config
from selenium import webdriver
import requests
from flask import Flask, render_template, request, redirect, url_for
from todo_app.mongo_db_client import MongoDBClient
from selenium.webdriver.firefox.options import Options #Firefox only

@pytest.fixture(scope='module')
def app_with_temp_board():
    
    # Disable login for tests
    os.environ['LOGIN_DISABLED'] = 'True'

    file_path = dotenv.find_dotenv('.env')
    dotenv.load_dotenv(file_path, override=True)
    # Set mongo_db_name to be test version 
    os.environ["mongo_db_name"] = "todo_app_test"
    config = Config()

    # construct the new application
    application = app.create_app() 
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True 
    thread.start()
    yield application

    # Tear Down
    thread.join(1) 

    # Drop the test DB
    test_mongo_db = MongoDBClient(config.mongo_db_connection, config.mongo_db_name)
    test_mongo_db.dropDbForName(config.mongo_db_name)

@pytest.fixture(scope="module")
def driver():
    # opts = Options() # Firefox only
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox') #Chrome only
    opts.add_argument('--disable-dev-shm-usage') #Chrome only
    # with webdriver.Firefox(options=opts) as driver:
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
