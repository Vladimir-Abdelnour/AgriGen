# Updated Sensor Reading Functions with Database Integration Comments for AgriGen
import sqlite3

# Helper function to query the database for specific sensor data
def get_sensor_data(parameter, timestamp):
    """
    Retrieves the value for a given column (parameter) and timestamp from the sensor_data table.

    Args:
        parameter (str): The column name in the sensor_data table (e.g., 'water_level_nutrient_a').
        timestamp (str): The timestamp value for the specific row (e.g., '2024-09-01 00:00:00').

    Returns:
        float: The sensor value for the specified parameter and timestamp, or None if not found.
    """
    conn = sqlite3.connect("Databases/static.db")  # Adjust path as necessary
    cursor = conn.cursor()
    sensor_value = None

    try:
        # Use the parameter as the column name and timestamp to filter the row
        query = f"SELECT {parameter} FROM sensor_data WHERE timestamp = ?"
        cursor.execute(query, (timestamp,))
        result = cursor.fetchone()
        
        # If result is found, extract and return the value
        if result:
            sensor_value = float(result[0])  # Convert the result to float
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
    
    return sensor_value

# Updated sensor functions with database integration

# Nutrient Tank Water Levels
def read_water_level_nutrient_a(timestamp):
    return get_sensor_data('water_level_nutrient_a', timestamp)

def read_water_level_nutrient_b(timestamp):
    return get_sensor_data('water_level_nutrient_b', timestamp)

def read_water_level_nutrient_c(timestamp):
    return get_sensor_data('water_level_nutrient_c', timestamp)

def read_water_level_distilled(timestamp):
    return get_sensor_data('water_level_distilled', timestamp)

def read_water_level_nutrient_rich(timestamp):
    return get_sensor_data('water_level_nutrient_rich', timestamp)

# Nutrient Mixology Sensor Functions
def read_ph_level(timestamp):
    return get_sensor_data('ph_level', timestamp)

def read_ec_level(timestamp):
    return get_sensor_data('ec_level', timestamp)

# Environment Control Sensor Functions
def read_co2_level(timestamp):
    return get_sensor_data('co2_level', timestamp)

def read_temperature(timestamp):
    return get_sensor_data('temperature', timestamp)

def read_humidity(timestamp):
    return get_sensor_data('humidity', timestamp)

def read_airflow(timestamp):
    return get_sensor_data('airflow_rate', timestamp)

# Lighting Control Sensor Functions
def read_par_level(timestamp):
    return get_sensor_data('par_level',timestamp)

# Energy Control Sensor Functions
def read_energy_usage(timestamp):
    return get_sensor_data('energy_usage', timestamp)


# Modified function with updated variable names and return statement
def read_plant_data(plant_type: str):
    """
    Reads plant-specific data from the database and sets control parameters.
    
    Args:
        plant_type (str): The type of plant (e.g., "Tomato", "Lettuce").
    
    This function connects to the 'sensory_data' database and retrieves values for:
    - ec_min, ec_max, ph_min, ph_max, co2_min, co2_max, temperature_min, temperature_max, humidity_min, humidity_max
    Returns:
        tuple: (ph_min, ph_max, ec_min, ec_max)
    """
    global co2_min, co2_max, temperature_min, temperature_max, humidity_min, humidity_max
    
    # Connect to the database (mock connection)
    conn = sqlite3.connect("Databases/static.db")  
    cursor = conn.cursor()


    try:
        # Define the plant type you're looking for
        plant_type = 'lettuce'  # Example plant type; change as needed

        # Retrieve data for the specific plant type from Nutrients table
        cursor.execute("""
            SELECT parameter, value
            FROM Nutrients
            WHERE parameter LIKE ?
        """, (f"{plant_type}_%",))
        nutrient_results = cursor.fetchall()

        # Retrieve general environmental data from Environment table
        cursor.execute("""
            SELECT parameter, value
            FROM Environment
        """)
        environment_results = cursor.fetchall()

        # Initialize variables for nutrient-specific parameters
        ec_min = ec_max = ph_min = ph_max = None

        # Parse nutrient results and assign to respective variables
        for parameter, value in nutrient_results:
            if parameter == f"{plant_type}_ec_min":
                ec_min = float(value)
            elif parameter == f"{plant_type}_ec_max":
                ec_max = float(value)
            elif parameter == f"{plant_type}_ph_min":
                ph_min = float(value)
            elif parameter == f"{plant_type}_ph_max":
                ph_max = float(value)

        # Initialize variables for general environmental parameters
        co2_min = co2_max = temperature_min = temperature_max = humidity_min = humidity_max = None

        # Parse environment results and assign to respective variables
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

        # Combine all results into a single result tuple
        result = (ec_min, ec_max, ph_min, ph_max, co2_min, co2_max, temperature_min, temperature_max, humidity_min, humidity_max)
        
        # Check if data was found for the specified plant type
        if result:

            # Output the result
            print("Result:", result)

            # Close the database connection
            conn.close()

            
            # Print the results to verify (can be logged or assigned as needed)
            print(f"Plant Type: {plant_type}")
            print(f"EC Range: {ec_min} - {ec_max} mS/cm")
            print(f"pH Range: {ph_min} - {ph_max}")
            print(f"CO2 Range: {co2_min} - {co2_max} ppm")
            print(f"Temperature Range: {temperature_min-273} - {temperature_max-273} °C")
            print(f"Humidity Range: {humidity_min} - {humidity_max} %")
            
            # Return the ph and ec ranges
            return ph_min, ph_max, ec_min, ec_max
        else:
            print(f"No data found for plant type: {plant_type}")
            return None, None, None, None  # Return None values if no data found
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None, None, None, None  # Return None values on database error
    
    finally:
        # Close the database connection
        conn.close()


