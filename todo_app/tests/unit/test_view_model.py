import pytest
from todo_app.view_model import ViewModel
from todo_app.item import Item

@pytest.fixture
def viewModel() -> ViewModel:
    items=[]
    items.append(Item(0, "First Item", "to do"))
    items.append(Item(0, "Random Item", "to do"))
    items.append(Item(0, "I'll be back", "to do"))
    items.append(Item(0, "Suckaaaa", "doing"))
    items.append(Item(0, "Testing is the worst part of coding - laugh when you see this in the PR @ Softwire peeps", "doing"))
    items.append(Item(0, "Parks and Rec", "doing"))
    items.append(Item(0, "Become a millionaire", "trying"))
    items.append(Item(0, "Do Chores", "done"))
    items.append(Item(0, "Devops Exercise 2", "done"))
    items.append(Item(0, "3 years at SCB", "done"))
    return ViewModel(items)

def test_return_todo_list_returned(viewModel: ViewModel):
    todo_items = viewModel.todo_items
    for item in todo_items:
        assert item.status == "to do"

def test_return_doing_list_returned(viewModel: ViewModel):
    doing_items = viewModel.doing_items
    for item in doing_items:
        assert item.status == "doing"
    
def test_return_done_list_returned(viewModel: ViewModel):
    done_items = viewModel.done_items
    for item in done_items:
        assert item.status == "done"

