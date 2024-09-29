# Importing necessary libraries for control and timing
import time  # For timer and control loop
import random  # For simulating sensor readings
from datetime import datetime, timedelta  # For managing time and scheduling

# Variable Definitions (Global Variables for State Tracking)
daily_par_accumulation = 0  # Keeps track of the accumulated PAR over the day
last_flush_date = datetime.now() - timedelta(weeks=2)  # Tracks the last water flushing date (start as 2 weeks ago)
irrigation_interval = 300  # Irrigation every 5 minutes in seconds
irrigation_duration = 30  # Irrigation lasts for 30 seconds
next_irrigation_time = time.time() + irrigation_interval  # Schedule next irrigation

# Additional control variables for state
is_peak_hour = False  # Flag to indicate if it's currently peak utility hour
current_time = time.time()  # Initialize current time

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
    forecast_data = {'cloudiness': random.randint(0, 100)}  # Simulating cloudiness with random values
    return forecast_data


# -----------------------------------------------------------------
# Function: Lighting Control
# -----------------------------------------------------------------

# Improved Lighting Control Function
def lighting_control():
    """
    Improved control logic for managing LED lighting to supplement sunlight.
    - Measures accumulated PAR over the day.
    - Turns on LED lights if the daily target is not met by sunset.
    - Uses weather forecast to adjust for cloudiness during the day.
    - Resets daily PAR accumulation at midnight.
    """
    global daily_par_accumulation
    current_hour = datetime.now().hour
    cloudiness = get_weather_forecast()  # Get cloudiness data from weather API

    # Start a new day: Reset the accumulated PAR at midnight
    if current_hour == 0:
        daily_par_accumulation = 0
    
    # Read current PAR level (µmol/m²/s)
    current_par = read_par_level()
    
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
def nutrient_mixology_control_v2(ph_min, ph_max, ec_min, ec_max):
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
            control_nutrient_pump_b(True)  # Use pump B to add pH up solution
            time.sleep(2)  # Allow time for mixing
            control_nutrient_pump_b(False)
        elif current_ph > ph_max:
            print("pH too high. Adding pH down solution.")
            control_nutrient_pump_c(True)  # Use pump C to add pH down solution
            time.sleep(2)  # Allow time for mixing
            control_nutrient_pump_c(False)
        
        # Re-read the pH value
        current_ph = read_ph_level()

    print(f"Final pH: {current_ph}")

    # Step 5: Adjust EC if it is outside the specified range
    while current_ec < ec_min or current_ec > ec_max:
        if current_ec < ec_min:
            print("EC too low. Adding more nutrient solution.")
            control_nutrient_pump_a(True)  # Add more nutrient solution A
            time.sleep(3)  # Allow time for mixing
            control_nutrient_pump_a(False)
        elif current_ec > ec_max:
            print("EC too high. Adding distilled water to dilute.")
            control_valve_distilled(True)  # Add distilled water to reduce EC
            time.sleep(3)  # Allow time for mixing
            control_valve_distilled(False)

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
        control_valve_nutrient_rich(True)  # Open nutrient-rich tank valve
        activate_pump(True)  # Activate pump to flush out the system
        time.sleep(60)  # Flush for 1 minute (placeholder value)
        control_valve_nutrient_rich(False)
        activate_pump(False)
        
        last_flush_date = datetime.now()  # Update last flush date

# -----------------------------------------------------------------
# Function: CO2 Enrichment Control
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# Function: CO2 Enrichment Control with Asymmetric Deadband on Upper Bound
# -----------------------------------------------------------------
def co2_enrichment_control(co2_min, co2_max, co2_upper_margin):
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
    current_co2 = read_co2_level()

    # Activate CO2 valve when CO2 drops below the lower bound (co2_min)
    if current_co2 < co2_min:
        control_co2_valve(True)  # Open CO2 valve to enrich the air
        print(f"CO2 level is {current_co2} ppm, below {co2_min} ppm. Activating CO2 enrichment.")
    
    # Deactivate CO2 valve when CO2 exceeds the upper bound + deadband margin
    elif current_co2 > co2_max + co2_upper_margin:
        control_co2_valve(False)  # Close CO2 valve to prevent oversaturation
        print(f"CO2 level is {current_co2} ppm, above {co2_max + co2_upper_margin} ppm. Deactivating CO2 enrichment.")


# -----------------------------------------------------------------
# Function: Temperature Control
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# Function: Temperature Control with Asymmetric Deadband for HVAC
# -----------------------------------------------------------------
def temperature_control(temperature_min, temperature_max, cooling_margin, heating_margin):
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
    current_temp = read_temperature()
    
    # Cooling Control: Turn on when above max, turn off only when below max - margin
    if current_temp > temperature_max:
        control_hvac(True)  # Turn on HVAC to cool
        print(f"Temperature is {current_temp}°C, above {temperature_max}°C. Activating cooling.")
    elif current_temp < temperature_max - cooling_margin:
        control_hvac(False)  # Turn off cooling
        print(f"Temperature is {current_temp}°C, below {temperature_max - cooling_margin}°C. Deactivating cooling.")
    
    # Heating Control: Turn on when below min, turn off only when above min + margin
    elif current_temp < temperature_min:
        control_hvac(True)  # Turn on HVAC to heat
        print(f"Temperature is {current_temp}°C, below {temperature_min}°C. Activating heating.")
    elif current_temp > temperature_min + heating_margin:
        control_hvac(False)  # Turn off heating
        print(f"Temperature is {current_temp}°C, above {temperature_min + heating_margin}°C. Deactivating heating.")


# -----------------------------------------------------------------
# Function: Humidity Control with Asymmetric Deadband and Error Handling
# -----------------------------------------------------------------
def humidity_control(humidity_min, humidity_max, upper_deadband):
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
    current_humidity = read_humidity()

    # Lower Bound Error Handling: Raise a log if humidity is below the minimum threshold
    if current_humidity < humidity_min:
        print(f"Error: Humidity level is {current_humidity}%, below the minimum of {humidity_min}%. Please check the system.")

    # Upper Bound Control: Turn on ventilation when above max, turn off only when below max - upper_deadband
    elif current_humidity > humidity_max:
        control_ventilation(True)  # Turn on ventilation to reduce humidity
        print(f"Humidity is {current_humidity}%, above {humidity_max}%. Activating ventilation.")
    elif current_humidity < humidity_max - upper_deadband:
        control_ventilation(False)  # Turn off ventilation
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

# -----------------------------------------------------------------
# Main Control Loop
# -----------------------------------------------------------------
def control_loop():
    """
    Main control loop for AgriGen.
    - Calls individual subsystem control functions continuously.
    """

    control_loop_with_plant_data("Tomato")


    while True:
        lighting_control()
        nutrient_mixology_control()
        irrigation_control()
        water_flushing_control()
        co2_enrichment_control()
        temperature_control()
        humidity_control()
        electricity_control()
        
        # Wait for a short interval before checking the status again
        time.sleep(1)

# Uncomment the following line to run the control loop (if real-time execution is intended)
# control_loop()
