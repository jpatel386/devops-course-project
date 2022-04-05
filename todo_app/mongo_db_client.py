import pymongo
from bson.objectid import ObjectId

class MongoDBClient: 

    def __init__(self, mongo_db_connection, mongo_db_name):
        self.client = pymongo.MongoClient(mongo_db_connection)
        self.db = self.client[mongo_db_name]
        self.items = self.db['items']
    
    def getItems(self):
        # items have 3 entities - id, title and status
        items = []
        for item in self.items.find():
            items.append(item)

        return items

    def addItem(self, item):
        # item is a string
        # default to 'to do' status
        item_to_add = {"name": item, "status": "to do"}
        self.items.insert_one(item_to_add)
    
    def updateItemStatus(self, id, status):
        print(id)
        self.items.update_one(
            {
                "_id": ObjectId(id)
            },
            {
                '$set': {"status": status}
            }
        )
        return

    def completeItem(self, id):
        self.updateItemStatus(id, "done")

    def markItemAsOpen(self, id):
        self.updateItemStatus(id, "to do")

    def markItemInProgress(self, id):
        self.updateItemStatus(id, "doing")
    