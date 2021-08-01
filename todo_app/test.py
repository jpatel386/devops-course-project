from dotenv import load_dotenv
load_dotenv()

import requests
import json
import os

trello_key = os.environ.get('trello_key')
trello_token = os.environ.get('trello_token')
trello_board_id = os.environ.get('trello_board_id')

trello_key_params = {
    'key' : trello_key,
    'token' : trello_token
}

headers = {
   "Accept": "application/json"
}

def query_trello(method, url, query_params):
    response = requests.request(method,url,params=query_params)
    return json.loads(response.text)


url = "https://api.trello.com/1/lists/61042da018ae9930f24b1582/cards"
list_resp = query_trello("GET", url, trello_key_params)
print(list_resp)