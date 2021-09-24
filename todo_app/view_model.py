class ViewModel:
    
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    def get_items_with_status(self, status):
        ret_items = []
        for item in self._items:
            if item.status == status:
                ret_items.append(item)
        return ret_items

    @property
    def todo_items(self):
        return self.get_items_with_status("to do")
        
    @property
    def doing_items(self):
        return self.get_items_with_status("doing")

    @property
    def done_items(self):
        return self.get_items_with_status("done")
