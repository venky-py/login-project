from flask import Flask, request, render_template_string
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)

# MySQL connection details
db_config = {
    'host': 'db',
    'user': 'root',
    'password': 'password',
    'database': 'user_db'
}

# Establish MySQL connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

@app.route('/')
def index():
    return render_template_string(open('index.html').read())

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    if conn is None:
        return 'Error connecting to the database.'
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        return 'Login successful!'
    else:
        return 'Invalid credentials.'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8881)
