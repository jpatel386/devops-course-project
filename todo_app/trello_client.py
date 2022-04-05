# This is no longer used as our main backend to store lists - We have switched to mongoDb as our main backend for data storage now

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

    def buildNewListParams(self, listName):
        new_list_query_params = self.trello_key_params.copy()
        new_list_query_params['name'] = listName
        new_list_query_params['idBoard'] = self.trello_board_id
        return new_list_query_params

    def create_list(self, listName):
        new_list_url = "https://api.trello.com/1/lists"
        new_list_query_params = self.buildNewListParams(listName)
        new_list_resp = self.query_trello("POST", new_list_url, new_list_query_params)
        if not new_list_resp.ok:
            return render_template('error.html')
        resp_dict = new_list_resp.json()
        if listName == 'To Do':
            self.trello_todo_list_id = resp_dict['id']
        elif listName == 'Doing':
            self.trello_doing_list_id = resp_dict['id']
        elif listName == 'Done':
            self.trello_done_list_id = resp_dict['id']

    def setListIds(self):
        list_url = "https://api.trello.com/1/boards/"+self.trello_board_id+"/lists"
        list_resp = self.query_trello("GET", list_url, self.trello_key_params)
        print(list_resp)
        if not list_resp.ok:
            return render_template('error.html')
        list_json = list_resp.json()
        #Check lists for list name matching 'To Do', 'Doing' or 'Done'. After we go through one list name, we will check if we have a list id for all of them 
        for list in list_json:
            if list['name'] == "To Do":
                self.trello_todo_list_id = list['id']
            elif list['name'] == "Doing":
                self.trello_doing_list_id = list['id']
            elif list['name'] == "Done":
                self.trello_done_list_id = list['id']
            
    def get_cards_for_list(self, listId):
        cards_url = "https://api.trello.com/1/lists/"+listId+"/cards"
        cards_resp = self.query_trello("GET", cards_url, self.trello_key_params)
        if not cards_resp.ok:
            return render_template('error.html')
        return cards_resp.json()

    def getItems(self):
        #Check if we have already retrieved the list ids we need to speed up processing
        if not self.trello_todo_list_id:
            self.setListIds()
         
        #Once we have called this - technically all list id's should exist. If they don't, then we can attempt to create the lists
        if not self.trello_doing_list_id:
            self.create_list("To Do")
            if not self.trello_todo_list_id:
                raise ValueError("No trello_todo_list_id found even after attempt to create")
        
        if not self.trello_doing_list_id:
            self.create_list("Doing")
            if not self.trello_doing_list_id:
                raise ValueError("No trello_doing_list_id found even after attempt to create")

        if not self.trello_done_list_id:
            self.create_list("Done")
            if not self.trello_done_list_id:
                raise ValueError("No trello_done_list_id found even after attempt to create")
        
        to_do = self.get_cards_for_list(self.trello_todo_list_id)
        doing = self.get_cards_for_list(self.trello_doing_list_id)
        done = self.get_cards_for_list(self.trello_done_list_id)

        return {"to do" : to_do, "doing" : doing, "done" : done}

    def addItem(self, item):
        #Add item to list to do
        add_item_url = "https://api.trello.com/1/cards"
        add_item_query = self.buildAddItemParams(item)
        add_item_resp = self.query_trello("POST", add_item_url, add_item_query)


    def markItemAsOpen(self, id):
        if not self.trello_todo_list_id:
            self.setListIds()
        
        if not self.trello_todo_list_id:
            self.create_list("To Do")
            if not self.trello_done_list_id:
                return render_template('error.html')

        reopen_url = "https://api.trello.com/1/cards/"+id
        reopen_query_params = self.trello_key_params.copy()
        reopen_query_params['idList'] = self.trello_todo_list_id
        reopen_query_resp = self.query_trello("PUT",reopen_url,reopen_query_params)

        if not reopen_query_resp.ok:
            return render_template('error.html')

    def markItemInProgress(self, id):
        if not self.trello_doing_list_id:
            self.setListIds()
        
        if not self.trello_doing_list_id:
            self.create_list("Doing")
            if not self.trello_doing_list_id:
                return render_template('error.html')
        
        doing_url = "https://api.trello.com/1/cards/"+id
        doing_query_params = self.trello_key_params.copy()
        doing_query_params['idList'] = self.trello_doing_list_id
        doing_query_resp = self.query_trello("PUT",doing_url,doing_query_params)

        if not doing_query_resp.ok:
            return render_template('error.html')

    def completeItem(self, id):
        if not self.trello_done_list_id:
            self.setListIds()
                
        if not self.trello_done_list_id:
            self.create_list("Done")
            if not self.trello_done_list_id:
                return render_template('error.html')
        
        done_url = "https://api.trello.com/1/cards/"+id
        done_query_params = self.trello_key_params.copy()
        done_query_params['idList'] = self.trello_done_list_id
        done_query_resp = self.query_trello("PUT",done_url,done_query_params)

        if not done_query_resp.ok:
            return render_template('error.html')

    def create_trello_board(self, name):
        new_board_url = "https://api.trello.com/1/boards"
        new_board_query_params = self.trello_key_params.copy()
        new_board_query_params['name'] = name
        new_board_resp = self.query_trello("POST", new_board_url, new_board_query_params)
        if not new_board_resp.ok:
            return render_template('error.html')
        resp_dict = new_board_resp.json()
        return resp_dict['id']

    def delete_trello_board(self, id):
        delete_board_url = "https://api.trello.com/1/boards/"+str(id)
        delete_board_params = self.trello_key_params.copy()
        delete_board_resp = self.query_trello("DELETE",delete_board_url, delete_board_params)
        if not delete_board_resp.ok:
            return render_template('error.html')
        resp_dict = delete_board_resp.json()

    
