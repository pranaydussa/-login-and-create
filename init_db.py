import mysql.connector
from mysql.connector import errorcode
from config import Config

def create_database():
    connection = mysql.connector.connect(
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        host=Config.MYSQL_HOST
    )
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE {Config.MYSQL_DB}")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DB_CREATE_EXISTS:
            print("Database already exists.")
        else:
            print(err.msg)
    cursor.close()
    connection.close()

def create_tables():
    connection = mysql.connector.connect(
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        host=Config.MYSQL_HOST,
        database=Config.MYSQL_DB
    )
    cursor = connection.cursor()

    userdetails_table = """
    CREATE TABLE IF NOT EXISTS UserDetails (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(150) UNIQUE NOT NULL,
        email VARCHAR(150) UNIQUE NOT NULL,
        password VARCHAR(150) NOT NULL
    )
    """
    registeredusers_table = """
    CREATE TABLE IF NOT EXISTS RegisteredUsers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(150) UNIQUE NOT NULL,
        email VARCHAR(150) UNIQUE NOT NULL
    )
    """

    cursor.execute(userdetails_table)
    cursor.execute(registeredusers_table)

    cursor.close()
    connection.close()

if __name__ == '__main__':
    create_database()
    create_tables()
