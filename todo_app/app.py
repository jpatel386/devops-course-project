from todo_app.item import Item
from todo_app.trello_client import TrelloClient
from flask import Flask, render_template, request, redirect, url_for
from todo_app.flask_config import Config
import requests
import json
import os

app = Flask(__name__)
app.config.from_object(Config)

trello_client = TrelloClient(Config.trello_board_id, Config.trello_key, Config.trello_token)

@app.route('/')
def index():
    items = []
    cards = trello_client.getToDoItems()
    for card in cards:
            newItem = Item(card["id"], card['name'], False)
            items.append(newItem)
    return render_template('index.html', items = items)

@app.route('/addItem', methods=['GET'])
def add_item_page():
    return render_template('itemForm.html')

@app.route('/addItem', methods=['POST'])
def add_item():
    item = request.form.get('item') 
    trello_client.addItem(item)
    return redirect(url_for('index'))

@app.route('/createTodoList', methods=['GET'])
def createTodoList():
    trello_client.create_todo_list()
    return redirect(url_for('index'))

@app.route('/complete_item/<id>', methods=['GET'])
def complete_item(id):
    trello_client.completeItemForId(id)
    return redirect(url_for('index'))
    
    

if __name__ == '__main__':
    app.run()
 