from flask import Flask, render_template, request, redirect, url_for
from todo_app.flask_config import Config
import requests
import json
import os

app = Flask(__name__)
app.config.from_object(Config)

todo_list = []
trello_todo_list_id = ""
trello_done_list_id = ""

trello_board_id = Config.trello_board_id

trello_key_params = {
    'key' : Config.trello_key,
    'token' : Config.trello_token
}

headers = {
   "Accept": "application/json"
}

def query_trello(method, url, query_params):
    return requests.request(method,url,headers=headers,params=query_params)

@app.route('/')
def index():

    global trello_todo_list_id
    global todo_list
    
    todo_list = []

    #Check if we have already retrieved the list id to speed up processing
    if not trello_todo_list_id:
        list_url = "https://api.trello.com/1/boards/"+trello_board_id+"/lists"
        list_resp = query_trello("GET", list_url, trello_key_params)
        if 200 != list_resp.status_code:
            return render_template('error.html')
        list_json = json.loads(list_resp.text)
        #Check lists for list name matching To Do
        for list in list_json:
            if list['name'] == "To Do":
                trello_todo_list_id = list['id']
                break
    
    #If we don't have a list yet - ask the user to create one - can delete this and just auto create
    if not trello_todo_list_id:
        return render_template('createTodoList.html')
    
    cards_url = "https://api.trello.com/1/lists/"+trello_todo_list_id+"/cards"
    cards_resp = query_trello("GET", cards_url, trello_key_params)
    if 200 != cards_resp.status_code:
        return render_template('error.html')
    cards_json = json.loads(cards_resp.text)
    for card in cards_json:
        id = card["id"]
        status = "NOT STARTED"
        title = card["name"]
        todo_list.append({'id' : id, 'status' : status, 'title' : title})
    return render_template('index.html', items = todo_list)

@app.route('/addItem', methods=['GET'])
def add_item_page():
    return render_template('itemForm.html')

@app.route('/addItem', methods=['POST'])
def add_item():
    item = request.form.get('item') 
    #Add item to list to do
    add_item_url = "https://api.trello.com/1/cards"
    add_item_query = trello_key_params
    add_item_query['idList'] = trello_todo_list_id
    add_item_query['name'] = item
    add_item_resp = query_trello("POST", add_item_url, trello_key_params)
    return redirect(url_for('index'))

@app.route('/createTodoList', methods=['GET'])
def createTodoList():
    new_list_url = "https://api.trello.com/1/lists"
    new_list_query_params = trello_key_params
    new_list_query_params['name'] = "To Do"
    new_list_query_params['idBoard'] = trello_board_id
    new_list_resp = query_trello("POST", new_list_url, new_list_query_params)
    if 200 != new_list_resp.status_code:
        return render_template('error.html')
    global trello_todo_list_id
    resp_dict = json.loads(new_list_resp.text)
    trello_todo_list_id = resp_dict['id']
    return redirect(url_for('index'))

@app.route('/complete_item/<id>', methods=['GET'])
def complete_item(id):
    #print(id)
    #We have the ID of the card
    #Now we want to add it to the completed list and remove it from the To Do list

    global trello_done_list_id

    if not trello_done_list_id:
        list_url = "https://api.trello.com/1/boards/"+trello_board_id+"/lists"
        list_resp = query_trello("GET", list_url, trello_key_params)
        if 200 != list_resp.status_code:
            return render_template('error.html')
        list_json = json.loads(list_resp.text)
        for list in list_json:
            if list['name'] == "Done":
                trello_done_list_id = list['id']
                break
            
    if not trello_done_list_id:
        new_list_url = "https://api.trello.com/1/lists"
        new_list_query_params = trello_key_params
        new_list_query_params['name'] = "Done"
        new_list_query_params['idBoard'] = trello_board_id
        new_list_resp = query_trello("POST", new_list_url, new_list_query_params)
        if 200 != new_list_resp.status_code:
            return render_template('error.html')
        resp_dict = json.loads(new_list_resp.text)
        trello_done_list_id = resp_dict['id']
    
    new_done_url = "https://api.trello.com/1/cards/"+id
    print(new_done_url)
    new_done_query_params = trello_key_params
    new_done_query_params['idList'] = trello_done_list_id
    new_done_query_resp = query_trello("PUT",new_done_url,new_done_query_params)

    if 200 != new_done_query_resp.status_code:
        return render_template('error.html')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()