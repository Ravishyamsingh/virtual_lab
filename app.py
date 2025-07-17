from flask import Flask, render_template, redirect, url_for, session, request
from auth import check_credentials, login_required, load_users
from routes.mono_alphabetic import mono_alphabetic
from routes.shift_cipher import shift_cipher
from routes.one_time_pad import one_time_pad
from routes.hash_function import hash_function
from routes.des_algorithm import des_algorithm
from routes.aes_algorithm import aes_algorithm
from routes.message_auth import message_auth
from routes.dsa_algorithm import dsa_algorithm
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Register blueprints
app.register_blueprint(mono_alphabetic)
app.register_blueprint(shift_cipher)
app.register_blueprint(one_time_pad)
app.register_blueprint(hash_function)
app.register_blueprint(des_algorithm)
app.register_blueprint(aes_algorithm)
app.register_blueprint(message_auth)
app.register_blueprint(dsa_algorithm)

# Routes
@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Clear any existing session
    if 'user' in session:
        session.pop('user', None)
    
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            
            print(f"Login attempt for username: {username}")  # Debug log
            
            if not username or not password:
                return render_template('login.html', error='Please enter both username and password')
            
            # Check if the username exists in users.json
            users = load_users()
            print(f"Loaded users: {users}")  # Debug log
            
            if not users:
                print("No users loaded from file")  # Debug log
                return render_template('login.html', error='Unable to verify credentials. Please try again.')
                
            username_exists = any(user['username'].lower() == username.lower() for user in users)
            print(f"Checking username '{username}' against available usernames: {[user['username'] for user in users]}")  # Debug log
            
            if not username_exists:
                print(f"Username not found: {username}")  # Debug log
                return render_template('login.html', error='Username not found')
            
            if check_credentials(username, password):
                print(f"Successful login for username: {username}")  # Debug log
                session['user'] = {
                    'username': username,
                    'email': f'{username}@example.com'
                }
                return redirect(url_for('index'))
            else:
                print(f"Invalid password for username: {username}")  # Debug log
                return render_template('login.html', error='Incorrect password')
                
        except Exception as e:
            app.logger.error(f"Login error: {str(e)}")
            import traceback
            print(f"Login error details: {traceback.format_exc()}")  # Debug log
            return render_template('login.html', error='An error occurred. Please try again.')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
