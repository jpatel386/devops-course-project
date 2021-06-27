from flask import Flask, render_template, request, redirect, url_for
from todo_app.flask_config import Config


from .data import session_items as session

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    #return 'Hello World!'
    print(session.get_items())
    return render_template('index.html', items = session.get_items())


@app.route('/addItem', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        item = request.form.get('item') 
        print(item)
        return item_added(item)
    else:
        return show_add_item_form()

def show_add_item_form():
        return render_template('itemForm.html')

def item_added(item):
    session.add_item(item)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
