from flask import Flask, render_template, request, url_for, redirect, current_app
from .data.todoapi import TodoAPI
from .data.item import Item
from dateutil import parser
from .viewmodel import ViewModel
from .app_config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config()) 
    
    todoapi = TodoAPI(app.config) 
    
    # All the routes and setup code etc
    
    def render_index_response():
        item_view_model = ViewModel(sorted(todoapi.get_list_of_items(), key=lambda item : (item.status, item.id)))
        return render_template('index.html', view_model= item_view_model)

    @app.route('/', methods=['GET'])
    def _index():
        return render_index_response()    

    @app.route('/add', methods=['POST'])
    def _add():
        todoapi.add_item(request.form)
        return render_index_response()

    @app.route('/setstatus/<id>/<status>', methods=['POST'])
    def _setstatus(id,status):
        todoapi.modify_item(id, {'status': status})
        return render_index_response()

    @app.route('/delete/<id>', methods=['POST'])
    def _delete(id):
        todoapi.delete_item(id)
        return render_index_response()

    @app.template_filter('strftime')
    def _jinja2_filter_datetime(date, fmt=None):
        ''' Used for the conversion of dates from the API '''
        date = parser.parse(date)
        native = date.replace(tzinfo=None)
        format='%d %b %Y'
        return native.strftime(format) 


    return app

if __name__ == '__main__':
    create_app().run()