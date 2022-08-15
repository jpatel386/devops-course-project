from tkinter import Variable
import flask_login
import requests
import json
import os
import uuid
import oauthlib.oauth2 as auth
from todo_app.item import Item
from todo_app.mongo_db_client import MongoDBClient
from todo_app.view_model import ViewModel
from todo_app.user import User
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from todo_app.flask_config import Config
from flask_login import login_required, LoginManager
from loggly.handlers import HTTPSHandler
from logging import Formatter

def create_app():

    # App Setup
    config = Config()
    app = Flask(__name__)
    app.config.from_object(config)
    app.logger.setLevel(config.LOG_LEVEL)
    if app.config['LOGGLY_TOKEN'] is not None:
        handler = HTTPSHandler(f'https://logs-01.loggly.com/inputs/{app.config["LOGGLY_TOKEN"]}/tag/todo-app')
        handler.setFormatter(Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s"))
    app.logger.addHandler(handler)
    app.logger.info("Application starting...")
    mongo_db = MongoDBClient(config.mongo_db_connection, config.mongo_db_name)
    # Auth Setup
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.unauthorized_handler
    def unauthenticated():
        app.logger.warning("Unathenticated user - Attempting to authenticate...")
        state = str(uuid.uuid4())
        session['state'] = state
        url = "https://github.com/login/oauth/authorize"
        headers = {
            "Accept": "application/json"
        }
        params = {
            "client_id": config.git_client_id,
            "state" : state
        }
        response = requests.request("GET",url,headers=headers,params=params)
        return redirect(response.url)

    # Come to this route when no cookie present
    @app.route('/login/callback', methods=['GET'])
    def authenticate_user():
        app.logger.info('Got callback - Continuing attempt to authenticate...')
        if (not 'state' in session) or (session['state'] != request.args['state']):
            app.logger.error("Unauthorised user tried to gain entry")
            return render_template('unauthorised.html'), 401
        # Clear the session state now that we are authd so it can't be used again
        session['state'] = ""
        if "error" in request.args:
            app.logger.critical("Could not authenticate user")
            return render_template('unauthorised.html'), 401
        code = request.args['code']
        url = "https://github.com/login/oauth/access_token"
        headers = {
            "Accept": "application/json"
        }
        params = {
            "client_id": config.git_client_id,
            "client_secret": config.git_client_secret,
            "code": code
        }
        resp = requests.request("POST",url,headers=headers,params=params)
        if not resp.ok:
            app.logger.error("Unauthorised user tried to gain entry")
            return render_template('unauthorised.html'), 401
        access_token = resp.json()["access_token"]
        headers['Authorization'] = "token " + access_token
        url = "https://api.github.com/user"
        user_resp = requests.request("GET",url,headers=headers,params=params)
        if not user_resp.ok:
            app.logger.critical("Could not authenticate user")
            return render_template('unauthorised.html'), 401
        user_id = json.loads(user_resp.text)["id"]
        user = User(user_id)
        logged_in = flask_login.login_user(user)
        app.logger.info("Authorised user %s", user_id)
        return redirect(url_for('index'))


    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    def write_required(func):
        def wrapper_write_required(*args, **kwargs):
            allowed = False
            cur_user = flask_login.current_user
            app.logger.debug('Login disabled?: %s', config.LOGIN_DISABLED)
            app.logger.debug('Role is: %s', cur_user.role)
            # Check to see if we are in test mode or if we are a writer
            if config.LOGIN_DISABLED or cur_user.role == "writer":
                allowed = True            
            if allowed:
                return func(*args, **kwargs)
            else:
                app.logger.warn('Attempt to perform write action without writer role permission')
                return render_template('unauthorised.html'), 401
        return wrapper_write_required

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(directory=app.root_path, filename='favicon.ico', mimetype='image/vnd.microsoft.icon')

    @app.route('/')
    @login_required
    def index():
        items = []
        data = mongo_db.getItems()
        for item in data:
            items.append(Item(item['_id'], item['name'], item['status']))
        item_view_model = ViewModel(items)
        cur_user = flask_login.current_user
        # Could extend anon user mixin class with my def to include role - might be cleaner
        writer = config.LOGIN_DISABLED or cur_user.role == "writer"
        app.logger.debug('Current user getting data is a writer?: %s', writer)
        return render_template('index.html', view_model = item_view_model, writer = writer)

    @app.route('/addItem', endpoint='add_item_page', methods=['GET'])
    @login_required
    @write_required
    def add_item_page():
        return render_template('itemForm.html')

    @app.route('/addItem', endpoint='add_item', methods=['POST'])
    @login_required
    @write_required
    def add_item():
        item = request.form.get('item') 
        mongo_db.addItem(item)
        app.logger.info('New item added')
        return redirect(url_for('index'))

    @app.route('/complete_item/<id>', endpoint='complete_item', methods=['GET'])
    @login_required
    @write_required
    def complete_item(id):
        mongo_db.completeItem(id)
        app.logger.info('Item completed')
        return redirect(url_for('index'))

    @app.route('/reopen_item/<id>', endpoint='reopen_item', methods=['GET'])
    @login_required
    @write_required
    def reopen_item(id):
        mongo_db.markItemAsOpen(id)
        app.logger.info('Item reopened')
        return redirect(url_for('index'))

    @app.route('/doing_item/<id>', endpoint='in_progress_item', methods=['GET'])
    @login_required
    @write_required
    def in_progress_item(id):
        mongo_db.markItemInProgress(id)
        app.logger.info('Item in progresss')
        return redirect(url_for('index'))

    if __name__ == '__main__':
        app.run()
    
    return app