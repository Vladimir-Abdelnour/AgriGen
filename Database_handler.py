# Database_handler.py

import sqlite3
from datetime import datetime
import os

def setup_database(db_name):
    # Ensure the Databases folder exists
    if not os.path.exists('Databases'):
        os.makedirs('Databases')

    # Connect to the database in the Databases folder
    conn = sqlite3.connect(f'Databases/{db_name}')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS sensor_readings
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       timestamp DATETIME,
                       ec REAL,
                       ph REAL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS target_values
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       timestamp DATETIME,
                       target_ec REAL,
                       target_ph REAL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS action_log
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       timestamp DATETIME,
                       action TEXT)''')

    conn.commit()
    conn.close()

def get_latest_readings(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT ec, ph FROM sensor_readings ORDER BY timestamp DESC LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    return result if result else (None, None)

def get_target_values(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT target_ec, target_ph FROM target_values ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    return result if result else (None, None)

def log_action(db_name, action):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO action_log (timestamp, action) VALUES (?, ?)",
                   (datetime.now(), action))
    conn.commit()
    conn.close()