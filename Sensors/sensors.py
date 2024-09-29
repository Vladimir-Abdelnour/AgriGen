# Updated Sensor Reading Functions with Database Integration Comments for AgriGen
import sqlite3
# Nutrient Tank Water Levels
def read_water_level_nutrient_a():
    """
    Reads the current water level in Nutrient Tank A.
    Currently sourced from the 'sensory_data' database.
    Returns:
        float: Water level in liters (placeholder value).
    """
    # Placeholder for actual database reading
    # This will be replaced by actual sensor data integration in the future
    water_level_a = 150.0  # Example value in liters
    return water_level_a

def read_water_level_nutrient_b():
    """
    Reads the current water level in Nutrient Tank B.
    Currently sourced from the 'sensory_data' database.
    Returns:
        float: Water level in liters (placeholder value).
    """
    # Placeholder for actual database reading
    # This will be replaced by actual sensor data integration in the future
    water_level_b = 145.0  # Example value in liters
    return water_level_b

def read_water_level_nutrient_c():
    """
    Reads the current water level in Nutrient Tank C.
    Currently sourced from the 'sensory_data' database.
    Returns:
        float: Water level in liters (placeholder value).
    """
    # Placeholder for actual database reading
    # This will be replaced by actual sensor data integration in the future
    water_level_c = 155.0  # Example value in liters
    return water_level_c

def read_water_level_distilled():
    """
    Reads the current water level in the Distilled Water Tank.
    Currently sourced from the 'sensory_data' database.
    Returns:
        float: Water level in liters (placeholder value).
    """
    # Placeholder for actual database reading
    # This will be replaced by actual sensor data integration in the future
    water_level_distilled = 500.0  # Example value in liters
    return water_level_distilled

def read_water_level_nutrient_rich():
    """
    Reads the current water level in the Nutrient-Rich Tank.
    Currently sourced from the 'sensory_data' database.
    Returns:
        float: Water level in liters (placeholder value).
    """
    # Placeholder for actual database reading
    # This will be replaced by actual sensor data integration in the future
    water_level_nutrient_rich = 450.0  # Example value in liters
    return water_level_nutrient_rich

# Nutrient Mixology Sensor Functions
def read_ph_level():
    """
    Reads the pH level of the nutrient solution.
    Currently sourced from the 'sensory_data' database.
    Returns:
        float: pH level (placeholder value).
    """
    # Placeholder for actual database reading
    # This will be replaced by actual sensor data integration in the future
    ph_level = 5.8  # Example value for pH
    return ph_level

def read_ec_level():
    """
    Reads the Electrical Conductivity (EC) level of the nutrient solution.
    Currently sourced from the 'sensory_data' database.
    Returns:
        float: EC level in mS/cm (placeholder value).
    """
    # Placeholder for actual database reading
    # This will be replaced by actual sensor data integration in the future
    ec_level = 1.6  # Example value in mS/cm
    return ec_level

# Environment Control Sensor Functions
def read_co2_level():
    """
    Reads the CO2 concentration level in the greenhouse.
    Currently sourced from the 'sensory_data' database.
    Returns:
        float: CO2 concentration in ppm (placeholder value).
    """
    # Placeholder for actual database reading
    # This will be replaced by actual sensor data integration in the future
    co2_level = 400.0  # Example value in ppm
    return co2_level

def read_temperature():
    """
    Reads the temperature from various points in the greenhouse.
    Currently sourced from the 'sensory_data' database.
    Returns:
        float: Temperature in Celsius (placeholder value).
    """
    # Placeholder for actual database reading
    # This will be replaced by actual sensor data integration in the future
    temperature = 22.5  # Example value in °C
    return temperature

def read_humidity():
    """
    Reads the humidity level from various points in the greenhouse.
    Currently sourced from the 'sensory_data' database.
    Returns:
        float: Humidity level in percentage (placeholder value).
    """
    # Placeholder for actual database reading
    # This will be replaced by actual sensor data integration in the future
    humidity = 60.0  # Example value in %
    return humidity

def read_airflow():
    """
    Reads the airflow rate from the ventilation system.
    Currently sourced from the 'sensory_data' database.
    Returns:
        float: Airflow rate in cubic meters per second (placeholder value).
    """
    # Placeholder for actual database reading
    # This will be replaced by actual sensor data integration in the future
    airflow_rate = 1.2  # Example value in m³/s
    return airflow_rate

# Lighting Control Sensor Functions
def read_par_level():
    """
    Reads the Photosynthetically Active Radiation (PAR) levels.
    Currently sourced from the 'sensory_data' database.
    Returns:
        float: PAR level in µmol/m²/s (placeholder value).
    """
    # Placeholder for actual database reading
    # This will be replaced by actual sensor data integration in the future
    par_level = 800  # Example value in µmol/m²/s
    return par_level

# Energy Control Sensor Functions
def read_energy_usage():
    """
    Reads the real-time energy usage of the greenhouse system.
    Currently sourced from the 'sensory_data' database.
    Returns:
        float: Energy usage in kWh (placeholder value).
    """
    # Placeholder for actual database reading
    # This will be replaced by actual sensor data integration in the future
    energy_usage = 50.0  # Example value in kWh
    return energy_usage

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


