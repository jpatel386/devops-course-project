import requests
from flask import Flask, render_template, request, redirect, url_for

class TrelloClient:

    headers = {
        "Accept": "application/json"
    }

    def __init__(self, board_Id, trello_Key, trello_Token):
        self.trello_board_id = board_Id
        self.trello_key_params = {
            'key' : trello_Key,
            'token' : trello_Token
        }
        self.trello_todo_list_id = ""
        self.trello_doing_list_id = ""
        self.trello_done_list_id = ""

    def query_trello(self, method, url, query_params):
        return requests.request(method,url,headers=self.headers,params=query_params)

    def buildAddItemParams(self, item):
        add_item_query = self.trello_key_params.copy()
        add_item_query['idList'] = self.trello_todo_list_id
        add_item_query['name'] = item
        return add_item_query

    def buildNewTodoListParams(self):
        new_list_query_params = self.trello_key_params.copy()
        new_list_query_params['name'] = "To Do"
        new_list_query_params['idBoard'] = self.trello_board_id
        return new_list_query_params

    def addItem(self, item):
        #Add item to list to do
        add_item_url = "https://api.trello.com/1/cards"
        add_item_query = self.buildAddItemParams(item)
        add_item_resp = self.query_trello("POST", add_item_url, add_item_query)

    def getToDoItems(self):
        items=[]

        #Check if we have already retrieved the list id to speed up processing
        if not self.trello_todo_list_id:
            list_url = "https://api.trello.com/1/boards/"+self.trello_board_id+"/lists"
            list_resp = self.query_trello("GET", list_url, self.trello_key_params)
            if 200 != list_resp.status_code:
                return render_template('error.html')
            list_json = list_resp.json()
            #Check lists for list name matching To Do
            for list in list_json:
                if list['name'] == "To Do":
                    self.trello_todo_list_id = list['id']
                    break
        
        #If we don't have a list yet - ask the user to create one - can delete this and just auto create
        if not self.trello_todo_list_id:
            return render_template('createTodoList.html')
        
        cards_url = "https://api.trello.com/1/lists/"+self.trello_todo_list_id+"/cards"
        cards_resp = self.query_trello("GET", cards_url, self.trello_key_params)
        if 200 != cards_resp.status_code:
            return render_template('error.html')
        cards_json = cards_resp.json()
        return cards_resp.json()

    def create_todo_list(self):
        new_list_url = "https://api.trello.com/1/lists"
        new_list_query_params = self.buildNewTodoListParams()
        new_list_resp = self.query_trello("POST", new_list_url, new_list_query_params)
        if 200 != new_list_resp.status_code:
            return render_template('error.html')
        resp_dict = new_list_resp.json()
        self.trello_todo_list_id = resp_dict['id']
        
    def query_trello(self, method, url, query_params):
        return requests.request(method,url,headers=self.headers,params=query_params)

    def completeItemForId(self, id):
        if not self.trello_done_list_id:
            list_url = "https://api.trello.com/1/boards/"+self.trello_board_id+"/lists"
            list_resp = self.query_trello("GET", list_url, self.trello_key_params)
            if 200 != list_resp.status_code:
                return render_template('error.html')
            list_json = list_resp.json()
            for list in list_json:
                if list['name'] == "Done":
                    self.trello_done_list_id = list['id']
                    break
                
        if not self.trello_done_list_id:
            new_list_url = "https://api.trello.com/1/lists"
            new_list_query_params = self.trello_key_params.copy()
            new_list_query_params['name'] = "Done"
            new_list_query_params['idBoard'] = self.trello_board_id
            new_list_resp = self.query_trello("POST", new_list_url, new_list_query_params)
            if 200 != new_list_resp.status_code:
                return render_template('error.html')
            resp_dict = new_list_resp.json()
            self.trello_done_list_id = resp_dict['id']
        
        new_done_url = "https://api.trello.com/1/cards/"+id
        print(new_done_url)
        new_done_query_params = self.trello_key_params.copy()
        new_done_query_params['idList'] = self.trello_done_list_id
        new_done_query_resp = self.query_trello("PUT",new_done_url,new_done_query_params)

        if 200 != new_done_query_resp.status_code:
            return render_template('error.html')
