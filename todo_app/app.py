from flask import Flask, render_template, request, url_for, redirect
from .data.todoapi import TrelloAPI
from .data.boardelements import Item
from dateutil import parser
from .viewmodel import ViewModel

app = Flask(__name__)
todoapi = TrelloAPI()

def render_index_response():
    item_view_model = ViewModel(
        sorted(todoapi.get_list_of_items(), key=lambda item : (item.status, item.id)), 
        todoapi.board.statuses, 
        Item, 
        todoapi.board.name)
    return render_template('index.html', view_model= item_view_model)

@app.route('/', methods=['GET'])
def index():
    return render_index_response()    

@app.route('/add', methods=['POST'])
def add():
    todoapi.add_item(request.form)
    return render_index_response()

@app.route('/setstatus/<id>/<status>', methods=['POST'])
def setstatus(id,status):
    todoapi.modify_item(id, {'idList': status})
    return render_index_response()

@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    todoapi.delete_item(id)
    return render_index_response()

@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    ''' Used for the conversion of dates from the API '''
    date = parser.parse(date)
    native = date.replace(tzinfo=None)
    format='%d %b %Y'
    return native.strftime(format) 

if __name__ == '__main__':
    app.run()
