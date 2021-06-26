from flask import Flask, render_template, request, url_for, redirect, current_app
from .data.todoapi import TodoAPI
from .data.item import Item
from dateutil import parser
from .viewmodel import ViewModel
from .useradminviewmodel import UserAdminViewModel
from .app_config import Config
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from oauthlib.oauth2 import WebApplicationClient
import requests
from .data.user import User
from .data.userdb import UserDB

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config()) 
    
    todoapi = TodoAPI(app.config) 
    users_db = UserDB(app.config)

    login_manager = LoginManager()
    client = WebApplicationClient(app.config.get('GITHUB_CLIENT_ID', ''))

    @login_manager.unauthorized_handler
    def unauthenticated():
        uri = client.prepare_request_uri('https://github.com/login/oauth/authorize')
        return redirect(uri, code=302)

    
    @login_manager.user_loader
    def load_user(user_id):
         return get_user(user_id)
    
    login_manager.init_app(app)    
    # All the routes and setup code etc

    def is_permitted(role):
        return app.config.get('LOGIN_DISABLED', '') == 'True' or role in current_user.roles

    def logged_user():
        if app.config.get('LOGIN_DISABLED', '') == 'True':
            return User({'login':'unknown', 'roles':['writer'], 'avatar':'/favicon.ico'})
        
        return current_user

    def get_user(user_id):
        return users_db.get_user(user_id)
    

    def add_user(user_profile):
        default_roles = ['reader']
        if len(users_db.get_list_of_users()) == 0:
            default_roles = ['admin']
        
        users_db.add_user({**user_profile, 'roles': default_roles})
    
    def render_index_response():
        item_view_model = ViewModel(sorted(todoapi.get_list_of_items(), key=lambda item : (item.status, item.id)), logged_user())
        return render_template('index.html', view_model= item_view_model)

    def render_usersadmin_response():
        useradmin_view_model = UserAdminViewModel(users_db.get_list_of_users(), current_user)
        return render_template('useradmin.html', view_model= useradmin_view_model)

    @app.route('/login/callback', methods=['GET', 'POST'])
    def _callback():
        code = request.values['code']
        token_url, headers, body = client.prepare_token_request(token_url = 'https://github.com/login/oauth/access_token', code = code )
        token_response = requests.post(token_url, headers=headers, data=body, auth= (app.config.get('GITHUB_CLIENT_ID'), app.config.get('GITHUB_CLIENT_SECRET')),)
        client.parse_request_body_response(token_response.text)['access_token']
        
        userinfo_endpoint = 'https://api.github.com/user'
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)
        user_id = userinfo_response.json()['login']

        if get_user(user_id) is None:
            add_user(userinfo_response.json())
        
        user = get_user(user_id)
        login_user(user)
        
        return redirect('/', code=302)

    @app.route('/useradmin', methods=['GET'])
    @login_required
    def _useradmin():
        if not is_permitted('admin'):
            return redirect('/', code=302)
        
        return render_usersadmin_response()

    @app.route('/usersetrole/<user_id>/<role>/<add_remove>', methods=['POST'])
    @login_required
    def _usersetrole(user_id,role,add_remove):
        if not is_permitted('admin'):
            return redirect('/', code=302)
        
        user = users_db.get_user(user_id)
        roles = user.roles
        if role in roles and add_remove == 'remove':
            roles.remove(role)
        elif role not in roles and add_remove == 'add':
            roles.append(role)
        else:
            pass

        users_db.modify_roles(user_id,roles)
        return render_usersadmin_response()

    @app.route('/', methods=['GET'])
    @login_required
    def _index():
        return render_index_response()    

    @app.route('/add', methods=['POST'])
    @login_required
    def _add():
        if is_permitted('writer'):
            todoapi.add_item(request.form)
        return render_index_response()

    @app.route('/setstatus/<id>/<status>', methods=['POST'])
    @login_required
    def _setstatus(id,status):
        if is_permitted('writer'):
            todoapi.modify_item(id, {'status': status})
        return render_index_response()

    @app.route('/delete/<id>', methods=['POST'])
    @login_required
    def _delete(id):
        if is_permitted('writer'):
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