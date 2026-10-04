import pymysql
import configparser
import os
from tkinter import messagebox

# Global variables
mycursor = None
conn = None

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')

# Only these are ever interpolated into a SQL column name (never raw user input)
ALLOWED_SEARCH_COLUMNS = {'Id', 'Name', 'Phone', 'Role', 'Gender', 'Salary'}


def load_db_config():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_PATH):
        # Fall back to defaults and create the file so it's easy to edit later
        config['database'] = {'host': 'localhost', 'user': 'root', 'password': ''}
        with open(CONFIG_PATH, 'w') as f:
            config.write(f)
    config.read(CONFIG_PATH)
    return config['database']


def connect_database():
    global mycursor, conn
    try:
        db_config = load_db_config()
        conn = pymysql.connect(
            host=db_config.get('host', 'localhost'),
            user=db_config.get('user', 'root'),
            password=db_config.get('password', '')
        )
        mycursor = conn.cursor()
    except Exception:
        messagebox.showerror(
            'Error',
            'Could not connect to MySQL.\n\n'
            'Please check that:\n'
            '1. MySQL server is running\n'
            '2. config.ini has the correct host/user/password'
        )
        return

    mycursor.execute('CREATE DATABASE IF NOT EXISTS employee_data')
    mycursor.execute('USE employee_data')
    mycursor.execute(
        '''CREATE TABLE IF NOT EXISTS data(
            Id VARCHAR(20),
            Name VARCHAR(50),
            Phone VARCHAR(15),
            Role VARCHAR(50),
            Gender VARCHAR(20),
            Salary DECIMAL(10,2),
            Image_Path VARCHAR(255)
        )'''
    )
    try:
        mycursor.execute('ALTER TABLE data ADD COLUMN Image_Path VARCHAR(255)')
    except Exception:
        pass


def insert(id, name, phone, role, gender, salary, image_path):
    if mycursor is None:
        return
    mycursor.execute(
        'INSERT INTO data VALUES (%s,%s,%s,%s,%s,%s,%s)',
        (id, name, phone, role, gender, salary, image_path)
    )
    conn.commit()


def id_exists(id):
    if mycursor is None:
        return False
    mycursor.execute(
        'SELECT COUNT(*) FROM data WHERE Id=%s',
        (id,)
    )
    result = mycursor.fetchone()
    return result[0] > 0


def fetch_employees():
    if mycursor is None:
        return []
    mycursor.execute('SELECT * FROM data')
    return mycursor.fetchall()


def update(id, new_name, new_phone, new_role, new_gender, new_salary, new_image_path):
    if mycursor is None:
        return
    mycursor.execute(
        'UPDATE data SET name=%s,phone=%s,role=%s,gender=%s,salary=%s,Image_Path=%s WHERE id=%s',
        (new_name, new_phone, new_role, new_gender, new_salary, new_image_path, id)
    )
    conn.commit()


def delete(emp_id):
    if mycursor is None:
        return
    mycursor.execute(
        'DELETE FROM data WHERE Id = %s',
        (emp_id,)
    )
    conn.commit()


def search(option, value):
    if mycursor is None:
        return []
    # option must come from our own dropdown, never typed by the user directly;
    # this check stops it ever being used to inject arbitrary SQL
    if option not in ALLOWED_SEARCH_COLUMNS:
        return []
    query = f"SELECT * FROM data WHERE {option} LIKE %s"
    mycursor.execute(query, ('%' + value + '%',))
    return mycursor.fetchall()


def search_by_exact_id(id):
    if mycursor is None:
        return []
    mycursor.execute('SELECT * FROM data WHERE Id=%s', (id,))
    return mycursor.fetchall()


def deleteall_records():
    if mycursor is None:
        return
    mycursor.execute('TRUNCATE TABLE data')
    conn.commit()


connect_database()
