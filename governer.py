# Importing necessary libraries for control and timing
import time  # For timer and control loop
import random  # For simulating sensor readings
from datetime import datetime, timedelta  # For managing time and scheduling
from Sensors.sensors import*
from Database_handler import *
from Utils.controls import *
from PIL import Image, ImageTk
import os
from enum import Enum
import requests
import json
import creds

class Color(Enum):
    Red = "#C90303"
    Yellow = "#CDB908"
    Green = "#27BC1A"

#UI Controls
temp_text = ""
hum_text = ""
ph_text = ""
ec_text = ""
temp_color = Color.Green
hum_color = Color.Green
ph_color = Color.Green
ec_color = Color.Green
alert_messages = []
alert_message_colors = []
image_index = 0

API_ENDPOINT = 'https://plant.id/api/v3/identification'

# Define the coordinates for Tempe, Arizona
latitude = 33.4255
longitude = -111.9400

# Define the URL to get the weather forecast
url = f"https://api.weather.gov/points/{latitude},{longitude}"

# Get the forecast grid data (which contains temperature, humidity, sky cover, rain probability, etc.)
response = requests.get(url)
response.raise_for_status()  # Raise an error for bad responses
forecast_url = response.json()['properties']['forecastGridData']

# Fetch the forecast grid data
forecast_response = requests.get(forecast_url)
forecast_response.raise_for_status()  # Raise an error for bad responses
forecast_data = forecast_response.json()

# Extract the relevant weather properties
properties_data = forecast_data['properties']

# Extract the current date
current_date = datetime.now().date()

# Function to find today's weather data
def get_weather_for_today(data, key):
    if key in data:
        for item in data[key]['values']:
            forecast_date = datetime.fromisoformat(item['validTime'][:10]).date()
            if forecast_date == current_date:
                return item['value']
    return None

# Variable Definitions (Global Variables for State Tracking)
daily_par_accumulation = 0  # Keeps track of the accumulated PAR over the day
last_flush_date = datetime.now() - timedelta(weeks=2)  # Tracks the last water flushing date (start as 2 weeks ago)
irrigation_interval = 10  # Irrigation every 5 minutes in seconds
irrigation_duration = 3  # Irrigation lasts for 30 seconds
next_irrigation_time = time.time() + irrigation_interval  # Schedule next irrigation

# Additional control variables for state
is_peak_hour = False  # Flag to indicate if it's currently peak utility hour
current_time = time.time()  # Initialize current time

def identify_plant_health(image_path):
    # Open the image file in binary mode
    with open(image_path, 'rb') as image_file:
        #Prepare the headers with the API key for authentication
        headers = {
            'Api-Key': creds.API_KEY
        }

        #Prepare the data for the request
        files = {
            'images': image_file  # The image file for plant identification
        }

        #Adjust the data parameters based on available modifiers
        data = {
            'health': 'all',  # Get both plant species classification and health assessment
            #'classification_level': 'species',  # Restrict classification to species level
            #'similar_images': 'true'  # Get similar images for the suggestions
        }

        #Make the POST request to the API
        response = requests.post(API_ENDPOINT, headers=headers, files=files, data=data)

        #Check the response
        if response.status_code == 200 or response.status_code == 201:
            #Parse the JSON responses
            result = response.json()
            return result
        else:
            #Handle the error
            return f"Error: {response.status_code}, {response.text}"

#TO BE BUILD BY GEETH
def read_from_api(location: str):
    """
    Reads weather forecast data from an API for a specified location.
    Args:
        location (str): The location for which the forecast is needed (e.g., "New York").
    Returns:
        dict: A dictionary with forecast information such as cloudiness.
    """
    # Placeholder for API call - Replace with real API logic
    # Example response format: {'cloudiness': 60} means 60% cloud cover
    forecast_data = random.randint(0, 100)  # Simulating cloudiness with random values
    return forecast_data


# -----------------------------------------------------------------
# Function: Lighting Control
# -----------------------------------------------------------------

# Improved Lighting Control Function
def lighting_control(timestamp):
    """
    Improved control logic for managing LED lighting to supplement sunlight.
    - Measures accumulated PAR over the day.
    - Turns on LED lights if the daily target is not met by sunset.
    - Uses weather forecast to adjust for cloudiness during the day.
    - Resets daily PAR accumulation at midnight.
    """
    global daily_par_accumulation
    current_hour = datetime.now().hour
    cloudiness = read_from_api("Arizona")  # Get cloudiness data from weather API

    # Start a new day: Reset the accumulated PAR at midnight
    if current_hour == 0:
        daily_par_accumulation = 0
    
    # Read current PAR level (µmol/m²/s)
    current_par = read_par_level(timestamp)
    
    # Daytime (6 AM - 6 PM): Accumulate light and consider weather conditions
    if 6 <= current_hour <= 18:
        # Accumulate light received over time step (µmol/m²)
        daily_par_accumulation += current_par * 0.5  # Assuming this function runs every 0.5 seconds

        # Turn on LED lights if cloudiness is above 50% to compensate for lack of sunlight
        if cloudiness > 50:
            control_led_lighting(True)
        else:
            control_led_lighting(False)
    
    # Sunset check: Ensure the target daily PAR is met
    if current_hour == 18:  # Sunset hour
        if daily_par_accumulation < 20000:  # Example target value for daily light intake in µmol/m²
            control_led_lighting(True)  # Turn on LED lights to compensate
        else:
            control_led_lighting(False)  # Turn off LED lights as target is met
    
    # Ensure LED lights are turned off during night hours (post-sunset)
    if current_hour > 18:
        control_led_lighting(False)

# -----------------------------------------------------------------
# Function: Nutrient Mixology Control with Proper Mixing Order and EC/pH Adjustment
# -----------------------------------------------------------------
def nutrient_mixology_control(ph_min, ph_max, ec_min, ec_max):
    """
    Control logic for mixing nutrient solutions in hydroponic systems.
    - Ensures proper mixing order: Nutrient A -> Nutrient B -> Nutrient C.
    - Adjusts pH to stay within the specified range (ph_min, ph_max).
    - Adjusts EC (Electrical Conductivity) to stay within the specified range (ec_min, ec_max).

    Args:
        ph_min (float): Minimum acceptable pH level.
        ph_max (float): Maximum acceptable pH level.
        ec_min (float): Minimum acceptable EC level in mS/cm.
        ec_max (float): Maximum acceptable EC level in mS/cm.
    """

    global ph_text, ec_text
    # Step 1: Start by adding Nutrient A
    print("Adding Nutrient A to the reservoir.")
    control_nutrient_pump_a(True)  # Activate pump for Nutrient A
    time.sleep(5)  # Allow time for the nutrient to mix (Placeholder, adjust as needed)
    control_nutrient_pump_a(False)  # Stop pump for Nutrient A

    # Read EC and pH after adding Nutrient A
    current_ec = read_ec_level()
    current_ph = read_ph_level()

    # Step 2: Add Nutrient B after ensuring Nutrient A is fully mixed and stable
    print("Adding Nutrient B to the reservoir.")
    control_nutrient_pump_b(True)  # Activate pump for Nutrient B
    time.sleep(5)  # Allow time for the nutrient to mix
    control_nutrient_pump_b(False)  # Stop pump for Nutrient B

    # Read EC and pH after adding Nutrient B
    current_ec = read_ec_level()
    current_ph = read_ph_level()

    # Step 3: Add Nutrient C after the first two are blended properly
    print("Adding Nutrient C to the reservoir.")
    control_nutrient_pump_c(True)  # Activate pump for Nutrient C
    time.sleep(5)  # Allow time for the nutrient to mix
    control_nutrient_pump_c(False)  # Stop pump for Nutrient C

    # Read EC and pH after adding Nutrient C
    current_ec = read_ec_level()
    current_ph = read_ph_level()

    # Step 4: Adjust pH if it is outside the specified range
    while current_ph < ph_min or current_ph > ph_max:
        if current_ph < ph_min:
            print("pH too low. Adding pH up solution.")
            ph_color = Color.Red
            control_nutrient_pump_b(True)  # Use pump B to add pH up solution
            time.sleep(2)  # Allow time for mixing
            control_nutrient_pump_b(False)
        elif current_ph > ph_max:
            print("pH too high. Adding pH down solution.")
            ph_color = Color.Red
            control_nutrient_pump_c(True)  # Use pump C to add pH down solution
            time.sleep(2)  # Allow time for mixing
            control_nutrient_pump_c(False)
        
        # Re-read the pH value
        current_ph = read_ph_level()

    ph_color = Color.Green

    print(f"Final pH: {current_ph}")

    # Step 5: Adjust EC if it is outside the specified range
    while current_ec < ec_min or current_ec > ec_max:
        if current_ec < ec_min:
            print("EC too low. Adding more nutrient solution.")
            ec_color = Color.Red
            control_nutrient_pump_a(True)  # Add more nutrient solution A
            time.sleep(3)  # Allow time for mixing
            control_nutrient_pump_a(False)
        elif current_ec > ec_max:
            print("EC too high. Adding distilled water to dilute.")
            ec_color = Color.Red
            control_valve_distilled(True)  # Add distilled water to reduce EC
            time.sleep(3)  # Allow time for mixing

            control_valve_distilled(False)

        ec_color = Color.Green

        # Re-read the EC value
        current_ec = read_ec_level()

    print(f"Final EC: {current_ec}")

    # Final state after mixing and adjustment
    print("Nutrient solution is now stable and within desired pH and EC ranges.")
    
# -----------------------------------------------------------------
# Function: Irrigation Control
# -----------------------------------------------------------------
def irrigation_control():
    """
    Control logic for irrigation.
    - Turns on the pump every 5 minutes for 30 seconds.
    """
    global next_irrigation_time
    if time.time() >= next_irrigation_time:
        activate_pump(True)  # Turn on the water pump
        time.sleep(irrigation_duration)  # Pump for the specified duration
        activate_pump(False)  # Turn off the water pump
        next_irrigation_time = time.time() + irrigation_interval  # Schedule next irrigation

# -----------------------------------------------------------------
# Function: Water Flushing Control
# -----------------------------------------------------------------
def water_flushing_control():
    """
    Control logic for water flushing.
    - Performs a complete flush every two weeks.
    """
    global last_flush_date
    if datetime.now() >= last_flush_date + timedelta(weeks=2):
        # Activate valves and pumps to flush the entire system
        global alert_messages
        alert_messages.append("Flushing the Entire System and Restarting")
        alert_message_colors.append(Color.Red)
        control_valve_nutrient_rich(True)  # Open nutrient-rich tank valve
        activate_pump(True)  # Activate pump to flush out the system
        time.sleep(6)  # Flush for 1 minute (placeholder value)
        control_valve_nutrient_rich(False)
        activate_pump(False)
        
        last_flush_date = datetime.now()  # Update last flush date

# -----------------------------------------------------------------
# Function: CO2 Enrichment Control with Asymmetric Deadband on Upper Bound
# -----------------------------------------------------------------
def co2_enrichment_control(timestamp, co2_min, co2_max, co2_upper_margin):
    """
    Control logic for CO2 enrichment with asymmetric deadband.
    - Turns on CO2 valve when below a certain level.
    - Turns off CO2 valve using an upper bound with deadband to avoid frequent toggling.

    Args:
        co2_min (float): Minimum acceptable CO2 concentration in ppm.
        co2_max (float): Maximum acceptable CO2 concentration in ppm (main threshold).
        co2_upper_margin (float): Deadband margin for the upper bound to prevent frequent toggling.
    """
    # Read the current CO2 level from the sensor (placeholder function call)
    current_co2 = read_co2_level(timestamp)
    print(current_co2)
    print(co2_min)

    # Activate CO2 valve when CO2 drops below the lower bound (co2_min)
    if current_co2 < co2_min:
        control_co2_valve(True)  # Open CO2 valve to enrich the air
        print(f"CO2 level is {current_co2} ppm, below {co2_min} ppm. Activating CO2 enrichment.")
    
    # Deactivate CO2 valve when CO2 exceeds the upper bound + deadband margin
    elif current_co2 > co2_max + co2_upper_margin:
        control_co2_valve(False)  # Close CO2 valve to prevent oversaturation
        print(f"CO2 level is {current_co2} ppm, above {co2_max + co2_upper_margin} ppm. Deactivating CO2 enrichment.")

# -----------------------------------------------------------------
# Function: Temperature Control with Asymmetric Deadband for HVAC
# -----------------------------------------------------------------
def temperature_control(time,temperature_min, temperature_max, cooling_margin, heating_margin):
    """
    Control logic for temperature using HVAC system with asymmetric deadband control.
    - Uses deadband margins to avoid frequent toggling of HVAC system for cooling and heating.

    Args:
        temperature_min (float): Minimum acceptable temperature in Celsius.
        temperature_max (float): Maximum acceptable temperature in Celsius.
        cooling_margin (float): Deadband margin for cooling to prevent frequent toggling.
        heating_margin (float): Deadband margin for heating to prevent frequent toggling.
    """
    # Read the current temperature from the sensor (placeholder function call)
    current_temp = read_temperature(time)

    global temp_color
    # Cooling Control: Turn on when above max, turn off only when below max - margin
    if current_temp > temperature_max:
        control_hvac(True)  # Turn on HVAC to cool
        temp_color = Color.Red
        print(f"Temperature is {current_temp}°C, which is above {temperature_max}°C. Activating cooling.")
    elif current_temp < temperature_max - cooling_margin:
        control_hvac(False)  # Turn off cooling
        temp_color = Color.Green
        print(f"Temperature is {current_temp}°C, which is below {temperature_max - cooling_margin}°C. Deactivating cooling.")
    
    # Heating Control: Turn on when below min, turn off only when above min + margin
    elif current_temp < temperature_min:
        control_hvac(True)  # Turn on HVAC to heat
        temp_color = Color.Red
        print(f"Temperature is {current_temp}°C, which is below {temperature_min}°C. Activating heating.")
    elif current_temp > temperature_min + heating_margin:
        control_hvac(False)  # Turn off heating
        temp_color = Color.Green
        print(f"Temperature is {current_temp}°C, which is above {temperature_min + heating_margin}°C. Deactivating heating.")


# -----------------------------------------------------------------
# Function: Humidity Control with Asymmetric Deadband and Error Handling
# -----------------------------------------------------------------
def humidity_control(time,humidity_min, humidity_max, upper_deadband):
    """
    Control logic for humidity with asymmetric deadband and error handling.
    - Activates dehumidifier or ventilation based on humidity levels.
    - Raises an error log if humidity falls below the minimum threshold.

    Args:
        humidity_min (float): Minimum acceptable humidity percentage.
        humidity_max (float): Maximum acceptable humidity percentage.
        upper_deadband (float): Deadband margin for the upper bound to prevent frequent toggling.
    """
    # Read the current humidity from the sensor (placeholder function call)
    current_humidity = read_humidity(time)

    global hum_color
    # Lower Bound Error Handling: Raise a log if humidity is below the minimum threshold
    if current_humidity < humidity_min:
        global alert_messages
        alert_messages.append(f"Humidity level is very low at {current_humidity}%.")
        alert_message_colors.append(Color.Red)
        print(f"Error: Humidity level is {current_humidity}%, below the minimum of {humidity_min}%. Please check the system.")
        hum_color = Color.Red

    # Upper Bound Control: Turn on ventilation when above max, turn off only when below max - upper_deadband
    elif current_humidity > humidity_max:
        control_ventilation(True)  # Turn on ventilation to reduce humidity
        hum_color = Color.Red
        print(f"Humidity is {current_humidity}%, above {humidity_max}%. Activating ventilation.")
    elif current_humidity < humidity_max - upper_deadband:
        control_ventilation(False)  # Turn off ventilation
        hum_color = Color.Green
        print(f"Humidity is {current_humidity}%, below {humidity_max - upper_deadband}%. Deactivating ventilation.")

# -----------------------------------------------------------------
# Function: Electricity Control
# -----------------------------------------------------------------
def electricity_control():
    """
    Control logic for managing electricity use.
    - Adjusts HVAC setpoints and responds to utility signals.
    """
    global temperature_max
    if is_peak_hour:
        temperature_max -= 4  # Reduce cooling setpoint during peak hours
        control_energy_selling(True)  # Sell excess energy back to the grid
    else:
        control_energy_selling(False)  # Disable energy selling

# Main Control Loop with Plant-Specific Data Integration

def update_info(temperature, humidity, ph, ec):
    global temp_text, hum_text, ph_text, ec_text
    temp_text = str(temperature)
    hum_text = str(humidity)
    ph_text = str(ph)
    ec_text = str(ec)

def get_alerts():
    return alert_messages

def get_alert_colors():
    return alert_message_colors

def get_textinfo():
    return temp_text, hum_text, ph_text, ec_text

def get_colorinfo():
    return temp_color, hum_color, ph_color, ec_color

def control_loop_with_plant_data(plant_type: str, i: int):

    if i == 0:
        # Specify the path to the CSV files
        csv_folder = os.path.join('StaticFiles')

        # Create static.db from CSV files
        create_static_db(csv_folder)

        # Get configuration from static.db
        try:
            # Get configuration from static.db
            config = get_config_from_static_db()
        except Exception as e:
            print(f"Error reading configuration: {e}")
            return

            # Check if we got all the expected configuration
        expected_tables = ['general', 'environment', 'lighting', 'water', 'nutrients', 'energy', 'plants', 'co2',
                           'constants', 'simulation']
        missing_tables = [table for table in expected_tables if table not in config]
        if missing_tables:
            print(f"Warning: The following tables are missing from the configuration: {missing_tables}")

        # Read input values from config
        # General
        number_of_plants = int(config['general']['number_of_plants'])
        floor_area = float(config['general']['floor_area'])

        # Environment
        co2_min = float(config['environment']['co2_min'])
        co2_max = float(config['environment']['co2_max'])
        water_vapor_density_in = float(config['environment']['water_vapor_density_in'])
        water_vapor_density_out = float(config['environment']['water_vapor_density_out'])
        temperature = float(config['environment']['temperature'])
        num_air_exchanges = float(config['environment']['num_air_exchanges'])
        volume_room_air = float(config['environment']['volume_room_air'])

        # Lighting
        photosynthetic_radiation_lamps = float(config['lighting']['photosynthetic_radiation_lamps'])
        photosynthetic_radiation_surface = float(config['lighting']['photosynthetic_radiation_surface'])

        # Water
        water_recycled = float(config['water']['water_recycled'])
        water_supply_rate = float(config['water']['water_supply_rate'])
        water_held_in_plants = float(config['water']['water_held_in_plants'])
        water_inflow_rate = float(config['water']['water_inflow_rate'])
        water_outflow_rate = float(config['water']['water_outflow_rate'])

        # Nutrients
        ion_concentration_in = float(config['nutrients']['ion_concentration_in'])
        ion_concentration_out = float(config['nutrients']['ion_concentration_out'])

        # Energy
        elec_water_pumps = float(config['energy']['elec_water_pumps'])
        heat_energy_exchange = float(config['energy']['heat_energy_exchange'])
        elec_air_conditioners = float(config['energy']['elec_air_conditioners'])

        # Plants
        dry_mass_increase_rate = float(config['plants']['dry_mass_increase_rate'])

        # CO2
        co2_human_respiration = float(config['co2']['co2_human_respiration'])
        co2_cylinder = float(config['co2']['co2_cylinder'])

        # Constants
        conversion_factor_plant_mass = float(config['constants']['conversion_factor_plant_mass'])
        conversion_factor_elec_energy = float(config['constants']['conversion_factor_elec_energy'])
        conversion_factor_co2 = float(config['constants']['conversion_factor_co2'])
        conversion_factor_water_vapor = float(config['constants']['conversion_factor_water_vapor'])
        conversion_factor_liquid_water = float(config['constants']['conversion_factor_liquid_water'])

        # Simulation
        delta_t = float(config['simulation']['delta_t'])
        t = float(config['simulation']['t'])

        # Calculations
        water_use_efficiency = (water_recycled + water_held_in_plants) / water_supply_rate

        water_vapor_loss = (volume_room_air * num_air_exchanges * (
                water_vapor_density_in - water_vapor_density_out)) / floor_area

        # co2_loss = conversion_factor_co2 * num_air_exchanges * volume_room_air * (co2_in - co2_out) / floor_area

        # co2_use_efficiency = (co2_cylinder - co2_loss) / (co2_cylinder + co2_human_respiration)

        light_energy_efficiency_parl = (
                                               conversion_factor_plant_mass * dry_mass_increase_rate) / photosynthetic_radiation_lamps

        light_energy_efficiency_parp = (
                                               conversion_factor_plant_mass * dry_mass_increase_rate) / photosynthetic_radiation_surface

        electric_energy_efficiency = conversion_factor_elec_energy * light_energy_efficiency_parl

        elec_lamps = photosynthetic_radiation_lamps / conversion_factor_elec_energy

        ions_absorbed = ion_concentration_in * water_inflow_rate - ion_concentration_out * water_outflow_rate

        # Note: Some calculations are commented out due to missing variables or circular dependencies
        cop_heat_pumps = heat_energy_exchange / elec_air_conditioners
        # elec_air_conditioners = (elec_lamps + elec_water_pumps + heat_energy_exchange) / cop_heat_pumps
        elec_total = elec_lamps + elec_air_conditioners + elec_water_pumps
        # This is a simplified example and would need to be adjusted based on your specific system
        ion_concentration = config['nutrients']['ion_concentration_in']  # mol/mol
        nutrient_solution_supply_rate = config['water']['water_inflow_rate']  # kg/(m²·s)
        density_of_solution = 1000  # kg/m³ (assuming it's close to water density)

        # Convert water inflow rate to volume
        volume_inflow_rate = nutrient_solution_supply_rate / density_of_solution  # m³/(m²·s)

        # Calculate ions_supplied
        ions_supplied = ion_concentration * volume_inflow_rate  # mol/(m²·s)
        fertilizer_use_efficiency = ions_absorbed / ions_supplied

        # Print some results
        # print(f"Number of plants: {number_of_plants}")
        # print(f"Water Use Efficiency: {water_use_efficiency}")
        # print(f"CO2 Use Efficiency: {co2_use_efficiency}")
        # print(f"Light Energy Efficiency (PAR_L): {light_energy_efficiency_parl}")
        # print(f"Electric Energy Efficiency: {electric_energy_efficiency}")

        # # Database operations
        # db_name = 'hydroponics.db'
        # setup_database(db_name)
        #
        # # Example of running the nutrient mixing process
        # mix_nutrients(db_name, config)

        """
        Main control loop for AgriGen with plant-specific data integration.
        - Reads plant-specific data from the database based on the plant type.
        - Calls individual subsystem control functions continuously.

        Args:
            plant_type (str): The type of plant being cultivated (e.g., "Tomato").
        """

    # Read plant-specific control parameters from the database
    ec_min, ec_max, ph_min, ph_max, co2_min, co2_max, temperature_min, temperature_max, humidity_min, humidity_max = read_plant_data(
        plant_type)

    # Main control loop to manage all subsystems
    conn = sqlite3.connect("Databases/static.db")
    cursor = conn.cursor()

    # Query to get the first timestamp
    cursor.execute("SELECT timestamp FROM sensor_data")
    timestamp = cursor.fetchall()

    # Check if a result was returned
    if timestamp:
        print(len(timestamp))
    else:
        print("No data found in the sensor_data table.")

    # Close the database connection
    conn.close()

    current_time = timestamp[i][0]

    # Simulated sensor readings for demonstration purposes
    current_par = read_par_level(current_time)         # Simulate a PAR sensor reading
    current_ec = read_ec_level(current_time)           # Simulate an EC sensor reading
    current_ph = read_ph_level(current_time)           # Simulate a pH sensor reading
    current_co2 = read_co2_level(current_time)         # Simulate a CO2 sensor reading
    current_temp = read_temperature(current_time)      # Simulate a temperature sensor reading
    current_humidity = read_humidity(current_time)     # Simulate a humidity sensor reading

    #Execute control functions
    lighting_control(current_time)
    print("Nutrients Mixing")
    #commented out for temporary reasons
    #nutrient_mixology_control(ph_min, ph_max, ec_min, ec_max)
    print("Irigation")
    irrigation_control()
    print('Flushing')
    water_flushing_control()
    print('CO2 Enrichment')
    co2_enrichment_control(current_time, co2_min, co2_max,co2_upper_margin=0.02) # Assuming a 0.02 margin for CO2 control
    print('Temperature')
    temperature_control(current_time, temperature_min, temperature_max, cooling_margin=2, heating_margin=2) # Example margins
    print('Humidity')
    humidity_control(current_time,humidity_min, humidity_max, upper_deadband=5) # Example deadband margin for humidity
    print('Electricity')
    electricity_control()

    #Monitor Plant Health Constantly and Report any issues

    #Select an image from the images folder
    images_folder = "images"
    image_files = [f for f in os.listdir(images_folder)]
    global image_index
    image_path = os.path.join(images_folder, image_files[image_index])
    image_index = (image_index + 1) % len(image_files)

    plant_health_result = identify_plant_health(image_path)
    fin_result = json.dumps(plant_health_result)
    fin_result = json.loads(fin_result)
    probability = float(fin_result['result']['is_healthy']['probability'])
    global alert_messages
    if (probability > 0.4):
        alert_messages.append(f"The plant has a {probability*100:.2f}% chance of being unhealthy.")
        alert_message_colors.append(Color.Red)

    # Fetch the required weather data
    temperature_celsius = get_weather_for_today(properties_data, 'temperature')  # Temperature in Celsius
    humidity = get_weather_for_today(properties_data, 'relativeHumidity')  # Relative Humidity in %
    sky_cover = get_weather_for_today(properties_data, 'skyCover')  # Sky Cover in %
    rain_probability = get_weather_for_today(properties_data, 'probabilityOfPrecipitation')  # Rain probability in %

    if sky_cover is not None:
        alert_messages.append(f"Sky Cover for Tempe: {sky_cover}%")
        alert_message_colors.append(Color.Yellow)

    if rain_probability is not None:
        alert_messages.append(f"Rain Probability: {rain_probability}%")
        alert_message_colors.append(Color.Yellow)

    update_info(int(current_temp), int(current_humidity), round(current_ph, 1), round(current_ec, 2))

     # Push the current sensor readings and control states to the output database
    push_data_to_database(
        current_par=current_par,
        current_ec=current_ec,
        current_ph=current_ph,
        current_co2=current_co2,
        current_temp=current_temp,
        current_humidity=current_humidity,
        daily_par_accumulation=daily_par_accumulation,
        is_peak_hour=is_peak_hour
    )
    print('over here')
