# Database_handler.py

import sqlite3
from datetime import datetime
import os
import csv

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

    cursor.execute('''CREATE TABLE IF NOT EXISTS nutrient_mix
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           timestamp DATETIME,
                           plant_type TEXT,
                           number_of_plants INTEGER,
                           tank1_volume REAL,
                           tank2_volume REAL,
                           tank3_volume REAL,
                           main_tank_ec REAL)''')

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


def log_nutrient_mix(db_name, plant_type, number_of_plants, tank1_volume, tank2_volume, tank3_volume, main_tank_ec):
    if not table_exists(db_name, 'nutrient_mix'):
        setup_database(db_name)  # This will create the table if it doesn't exist

    conn = sqlite3.connect(f'Databases/{db_name}')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO nutrient_mix (timestamp, plant_type, number_of_plants, tank1_volume, tank2_volume, tank3_volume, main_tank_ec) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (datetime.now(), plant_type, number_of_plants, tank1_volume, tank2_volume, tank3_volume, main_tank_ec))
    conn.commit()
    conn.close()

def export_nutrient_mix_to_csv(db_name, output_file):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nutrient_mix")
    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([i[0] for i in cursor.description])  # write headers
        csv_writer.writerows(cursor)
    conn.close()

def table_exists(db_name, table_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    result = cursor.fetchone()
    conn.close()
    return result is not None