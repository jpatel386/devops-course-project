from todo_app.item import Item
from todo_app.mongo_db_client import MongoDBClient
from todo_app.view_model import ViewModel
from flask import Flask, render_template, request, redirect, url_for
from todo_app.flask_config import Config
import requests
import json
import os

def create_app():

    config = Config()
    app = Flask(__name__)
    app.config.from_object(config)
    mongo_db = MongoDBClient(config.mongo_db_connection, config.mongo_db_name)

    @app.route('/')
    def index():
        items = []
        data = mongo_db.getItems()
        for item in data:
            items.append(Item(item['_id'], item['name'], item['status']))
        item_view_model = ViewModel(items)
        # print(item_view_model.todo_items)
        return render_template('index.html', view_model = item_view_model)

    @app.route('/addItem', methods=['GET'])
    def add_item_page():
        return render_template('itemForm.html')

    @app.route('/addItem', methods=['POST'])
    def add_item():
        item = request.form.get('item') 
        mongo_db.addItem(item)
        return redirect(url_for('index'))

    @app.route('/complete_item/<id>', methods=['GET'])
    def complete_item(id):
        mongo_db.completeItem(id)
        return redirect(url_for('index'))

    @app.route('/reopen_item/<id>', methods=['GET'])
    def reopen_item(id):
        mongo_db.markItemAsOpen(id)
        return redirect(url_for('index'))

    @app.route('/doing_item/<id>', methods=['GET'])
    def in_progress_item(id):
        mongo_db.markItemInProgress(id)
        return redirect(url_for('index'))

        
        

    if __name__ == '__main__':
        app.run()
    
    return app