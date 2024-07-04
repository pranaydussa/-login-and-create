from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from mysql.connector import errorcode
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

def get_db_connection():
    try:
        print("Connecting to MySQL with the following parameters:")
        print(f"User: {Config.MYSQL_USER}")
        print(f"Password: {Config.MYSQL_PASSWORD}")
        print(f"Host: {Config.MYSQL_HOST}")
        print(f"Database: {Config.MYSQL_DB}")
        connection = mysql.connector.connect(
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            host=Config.MYSQL_HOST,
            database=Config.MYSQL_DB
        )
        return connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Database does not exist")
        else:
            print(f"Error: {err}")
    return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('You need to be logged in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        connection = get_db_connection()
        if connection is None:
            flash('Database connection failed!', 'error')
            return render_template('register.html')

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM UserDetails WHERE username=%s OR email=%s", (username, email))
        user_exists = cursor.fetchone()

        if user_exists:
            flash('Username or Email already exists!', 'error')
        else:
            cursor.execute("INSERT INTO UserDetails (username, email, password) VALUES (%s, %s, %s)", 
                           (username, email, hashed_password))
            cursor.execute("INSERT INTO RegisteredUsers (username, email) VALUES (%s, %s)", (username, email))
            connection.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))

        cursor.close()
        connection.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = get_db_connection()
        if connection is None:
            flash('Database connection failed!', 'error')
            return render_template('login.html')

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM UserDetails WHERE email=%s", (email,))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user and check_password_hash(user[3], password):
            session['username'] = user[1]
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password!', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
