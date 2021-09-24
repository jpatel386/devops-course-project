from todo_app.item import Item
from todo_app.trello_client import TrelloClient
from todo_app.view_model import ViewModel
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
    data = trello_client.getItems()
    todo_data = data['to do']
    doing_data = data['doing']
    done_data = data['done']

    for card in todo_data:
        newItem = Item(card['id'], card['name'], "to do")
        items.append(newItem)
    
    for card in doing_data:
        newItem = Item(card['id'], card['name'], "doing")
        items.append(newItem)
    
    for card in done_data:
        newItem = Item(card['id'], card['name'], "done")
        items.append(newItem)
        
    

    item_view_model = ViewModel(items)

    print(item_view_model.todo_items)
    return render_template('index.html', view_model = item_view_model)

@app.route('/addItem', methods=['GET'])
def add_item_page():
    return render_template('itemForm.html')

@app.route('/addItem', methods=['POST'])
def add_item():
    item = request.form.get('item') 
    trello_client.addItem(item)
    return redirect(url_for('index'))

@app.route('/complete_item/<id>', methods=['GET'])
def complete_item(id):
    trello_client.completeItem(id)
    return redirect(url_for('index'))

@app.route('/reopen_item/<id>', methods=['GET'])
def reopen_item(id):
    trello_client.markItemAsOpen(id)
    return redirect(url_for('index'))

@app.route('/doing_item/<id>', methods=['GET'])
def in_progress_item(id):
    trello_client.markItemInProgress(id)
    return redirect(url_for('index'))

    
    

if __name__ == '__main__':
    app.run()
 