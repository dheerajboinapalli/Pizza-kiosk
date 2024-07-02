from flask import Flask, render_template, request, redirect, url_for, session, g
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Database configuration
db_config = {
    'user': 'root',         # your MySQL username
    'password': 'Mailp@ssw0rd',   # your MySQL password
    'host': 'localhost',    # your MySQL host, usually localhost
    'database': 'pizza_app_db'  # the name of your database
}

def get_db():
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(**db_config)
        except Error as e:
            print(f"Error: {e}")
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = get_db().cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        cursor.close()
        if user:
            session['user_id'] = user[0]
            return redirect(url_for('menu'))
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')
