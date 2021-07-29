from flask import Flask, render_template, request, redirect, url_for
from todo_app.flask_config import Config


from .data import session_items as session

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    return render_template('index.html', items = session.get_items())


@app.route('/addItem', methods=['GET'])
def add_item_page():
    return render_template('itemForm.html')

@app.route('/addItem', methods=['POST'])
def add_item():
    item = request.form.get('item') 
    session.add_item(item)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
