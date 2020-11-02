from flask import Flask, render_template, request
from .data.session_items import add_item, update_item, delete_item, get_items, get_statuses, get_todomapper, TODO_API
from dateutil import parser

app = Flask(__name__)

def render_index_response():
    return render_template('index.html', items_list = get_items(), statuses = get_statuses(), todomapper = get_todomapper(), todoapi_name= TODO_API)

@app.route('/', methods=['GET'])
def index():
    return render_index_response()    

@app.route('/add', methods=['POST'])
def add():
    add_item(request.form)
    return render_index_response()

@app.route('/setstatus/<id>/<status>', methods=['POST'])
def setstatus(id,status):
    update_item(id, {'idList': status})
    return render_index_response()

@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    delete_item(id)
    return render_index_response()

@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    date = parser.parse(date)
    native = date.replace(tzinfo=None)
    format='%d %b %Y'
    return native.strftime(format) 

if __name__ == '__main__':
    app.run()
