import tkinter as tk
from tkinter import messagebox
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('user_database.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS usernames (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL
    )
''')

conn.commit()

# Function to register a new user
def register_user():
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    
    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password without spaces")
        return
    
    try:
        # Insert into users table
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        # Insert into usernames table
        c.execute('INSERT INTO usernames (username) VALUES (?)', (username,))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
        registration_window.destroy()
        open_login_window()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists")

# Function to login the user
def login_user():
    username = login_entry_username.get().strip()
    password = login_entry_password.get().strip()
    
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    result = c.fetchone()
    
    if result:
        messagebox.showinfo("Success", "Login successful!")
        login_window.destroy()
        show_usernames_window()
    else:
        messagebox.showerror("Error", "Invalid username or password")

# Function to open the login window
def open_login_window():
    global login_window
    global login_entry_username
    global login_entry_password

    login_window = tk.Tk()
    login_window.title("Login")

    tk.Label(login_window, text="Username").pack()
    login_entry_username = tk.Entry(login_window)
    login_entry_username.pack()

    tk.Label(login_window, text="Password").pack()
    login_entry_password = tk.Entry(login_window, show='*')
    login_entry_password.pack()

    tk.Button(login_window, text="Sign In", command=login_user).pack()

    login_window.mainloop()

# Function to show all registered usernames
def show_usernames_window():
    usernames_window = tk.Tk()
    usernames_window.title("Registered Usernames")

    tk.Label(usernames_window, text="Registered Usernames:").pack()

    c.execute('SELECT username FROM usernames')
    users = c.fetchall()
    
    for user in users:
        tk.Label(usernames_window, text=user[0]).pack()

    usernames_window.mainloop()

# Registration window
registration_window = tk.Tk()
registration_window.title("Registration")

tk.Label(registration_window, text="Username").pack()
entry_username = tk.Entry(registration_window)
entry_username.pack()

tk.Label(registration_window, text="Password").pack()
entry_password = tk.Entry(registration_window, show='*')
entry_password.pack()

tk.Button(registration_window, text="Register", command=register_user).pack()

registration_window.mainloop()

conn.close()
