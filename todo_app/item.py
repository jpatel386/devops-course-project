class Item:

    def __init__(self, id, title, status):
        self.id = id
        self.title = title
        #status passed in must match 'to do', 'doing', 'done'
        self.status = status
        
