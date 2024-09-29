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


def create_static_db(csv_folder, db_name='static.db'):
    # Ensure the Databases folder exists
    if not os.path.exists('Databases'):
        os.makedirs('Databases')

    # Connect to the database in the Databases folder
    db_path = os.path.join('Databases', 'static.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # List of CSV files to process (excluding sensors.csv)
    csv_files = ['general.csv', 'environment.csv', 'lighting.csv', 'water.csv', 'nutrients.csv',
                 'energy.csv', 'plants.csv', 'co2.csv', 'constants.csv', 'simulation.csv']

    for csv_file in csv_files:
        table_name = os.path.splitext(csv_file)[0]
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name}
                          (parameter TEXT PRIMARY KEY, value REAL)''')

        with open(os.path.join(csv_folder, csv_file), 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header
            for row in csv_reader:
                cursor.execute(f"INSERT OR REPLACE INTO {table_name} (parameter, value) VALUES (?, ?)", row)

    # Create and populate sensor_data table
    cursor.execute('''CREATE TABLE IF NOT EXISTS sensor_data
                      (timestamp TEXT, 
                       ec REAL, 
                       ph REAL, 
                       co2_in REAL, 
                       co2_out REAL, 
                       water_vapor_density_in REAL, 
                       water_vapor_density_out REAL, 
                       temperature REAL, 
                       photosynthetic_radiation_lamps REAL, 
                       photosynthetic_radiation_surface REAL, 
                       water_recycled REAL, 
                       water_supply_rate REAL, 
                       ion_concentration_in REAL, 
                       ion_concentration_out REAL, 
                       elec_lamps REAL, 
                       elec_air_conditioners REAL, 
                       elec_water_pumps REAL, 
                       co2_human_respiration REAL, 
                       co2_cylinder REAL)''')

    with open(os.path.join(csv_folder, 'sensors.csv'), 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header
        for row in csv_reader:
            cursor.execute('''INSERT INTO sensor_data VALUES 
                              (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', row)

    conn.commit()
    conn.close()


def get_config_from_static_db():
    db_path = os.path.join('Databases', 'static.db')
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"The database file {db_path} does not exist.")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    config = {}
    tables = ['general', 'environment', 'lighting', 'water', 'nutrients', 'energy', 'plants', 'co2', 'constants',
              'simulation']

    # First, let's check which tables actually exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    existing_tables = [row[0] for row in cursor.fetchall()]
    print(f"Existing tables in the database: {existing_tables}")

    for table in tables:
        if table in existing_tables:
            try:
                cursor.execute(f"SELECT parameter, value FROM {table}")
                config[table] = {row[0]: row[1] for row in cursor.fetchall()}
            except sqlite3.OperationalError as e:
                print(f"Error reading from table {table}: {e}")
        else:
            print(f"Table {table} does not exist in the database.")

    conn.close()
    return config


def get_sensor_data(start_time, end_time, db_name='static.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sensor_data WHERE timestamp BETWEEN ? AND ?", (start_time, end_time))
    sensor_data = cursor.fetchall()
    conn.close()
    return sensor_data



# Function to read plant-specific data and set control parameters
# Define the function to read plant data
# Define the function to read plant data and return the values
def read_plant_data(plant_type: str):
    """
    Reads plant-specific data from the database and sets control parameters.
    
    Args:
        plant_type (str): The type of plant (e.g., "Tomato", "Lettuce").
    
    Returns:
        tuple: Contains (ph_min, ph_max, ec_min, ec_max, co2_min, co2_max, temperature_min, temperature_max, humidity_min, humidity_max)
    """
    # Initialize variables to None
    ph_min = ph_max = ec_min = ec_max = None
    co2_min = co2_max = temperature_min = temperature_max = humidity_min = humidity_max = None

    # Connect to the database (replace with actual database path)
    conn = sqlite3.connect("Databases/static.db")
    cursor = conn.cursor()

    try:
        # Query to retrieve EC and pH parameters for the specified plant type from the Nutrients table
        cursor.execute("""
            SELECT parameter, value
            FROM Nutrients
            WHERE parameter LIKE ?
        """, (f"{plant_type}_%",))
        
        nutrient_results = cursor.fetchall()
        
        # Assign nutrient-specific values to respective variables
        for parameter, value in nutrient_results:
            if parameter == f"{plant_type}_ec_min":
                ec_min = float(value)
            elif parameter == f"{plant_type}_ec_max":
                ec_max = float(value)
            elif parameter == f"{plant_type}_ph_min":
                ph_min = float(value)
            elif parameter == f"{plant_type}_ph_max":
                ph_max = float(value)

        # Query to retrieve general environmental parameters from the Environment table
        cursor.execute("""
            SELECT parameter, value
            FROM Environment
        """)
        environment_results = cursor.fetchall()
        
        # Assign environmental parameters to respective variables
        for parameter, value in environment_results:
            if parameter == "co2_min":
                co2_min = float(value)
            elif parameter == "co2_max":
                co2_max = float(value)
            elif parameter == "temperature_min":
                temperature_min = float(value)
            elif parameter == "temperature_max":
                temperature_max = float(value)
            elif parameter == "humidity_min":
                humidity_min = float(value)
            elif parameter == "humidity_max":
                humidity_max = float(value)

        result = (ph_min, ph_max, ec_min, ec_max, co2_min, co2_max, temperature_min, temperature_max, humidity_min, humidity_max)

        # Print to verify the values
        print(f"pH Range: {ph_min} - {ph_max}")
        print(f"EC Range: {ec_min} - {ec_max}")
        print(f"CO2 Range: {co2_min} - {co2_max}")
        print(f"Temperature Range: {temperature_min} - {temperature_max} °C")
        print(f"Humidity Range: {humidity_min} - {humidity_max} %")
        # Example usage of the function with a mock plant type (replace with real plant types)
        # Uncomment the line below to use the function in your environment:
        # read_plant_data("Tomato")

        # Return the variables as a tuple
        return result
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None  # Return None in case of a database error

    finally:
        # Close the database connection
        conn.close()

    


def push_data_to_database(current_par, current_ec, current_ph, current_co2, current_temp, current_humidity, daily_par_accumulation, is_peak_hour):
    """
    Creates an 'output.db' database in the 'Databases' folder and pushes the given values into a table named 'control_data'.
    
    Args:
        current_par (float): Current PAR value.
        current_ec (float): Current EC value.
        current_ph (float): Current pH value.
        current_co2 (float): Current CO2 value.
        current_temp (float): Current temperature value.
        current_humidity (float): Current humidity value.
        daily_par_accumulation (float): Daily PAR accumulation value.
        is_peak_hour (bool): Indicates whether it is currently a peak utility hour.
    """

    print("Here")
    # Define the path to the output database
    db_path = os.path.join("Databases", "output.db")
    
    # Create or connect to the output database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create the table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS control_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            current_par REAL,
            current_ec REAL,
            current_ph REAL,
            current_co2 REAL,
            current_temp REAL,
            current_humidity REAL,
            daily_par_accumulation REAL,
            is_peak_hour INTEGER
        )
    """)
    print("Over Here")
    # Insert the current values into the table
    cursor.execute("""
        INSERT INTO control_data (current_par, current_ec, current_ph, current_co2, current_temp, current_humidity, daily_par_accumulation, is_peak_hour)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (current_par, current_ec, current_ph, current_co2, current_temp, current_humidity, daily_par_accumulation, int(is_peak_hour)))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print("Data pushed to output.db successfully.")