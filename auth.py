import json
from functools import wraps
from flask import session, redirect, url_for

def load_users():
    with open('data/users.json', 'r') as file:
        return json.load(file)['users']

def check_credentials(username, password):
    users = load_users()
    for user in users:
        if user['username'] == username and user['password'] == password:
            return True
    return False

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session['user'] is None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function 