# Importing necessary libraries for control and timing
import time  # For timer and control loop
import random  # For simulating sensor readings
from datetime import datetime, timedelta  # For managing time and scheduling

# Variable Definitions (Global Variables for State Tracking)
daily_par_accumulation = 0  # Keeps track of the accumulated PAR over the day
last_flush_date = datetime.now() - timedelta(weeks=2)  # Tracks the last water flushing date (start as 2 weeks ago)
target_ec = 1.8  # Target Electrical Conductivity level in mS/cm
target_ph = 5.5  # Target pH level
co2_min = 350  # Minimum acceptable CO2 concentration in ppm
co2_max = 1000  # Maximum acceptable CO2 concentration in ppm
temperature_min = 20  # Minimum temperature in Celsius
temperature_max = 26  # Maximum temperature in Celsius
humidity_min = 40  # Minimum humidity percentage
humidity_max = 70  # Maximum humidity percentage
irrigation_interval = 300  # Irrigation every 5 minutes in seconds
irrigation_duration = 30  # Irrigation lasts for 30 seconds
next_irrigation_time = time.time() + irrigation_interval  # Schedule next irrigation

# Additional control variables for state
is_peak_hour = False  # Flag to indicate if it's currently peak utility hour
current_time = time.time()  # Initialize current time

# -----------------------------------------------------------------
# Function: Lighting Control
# -----------------------------------------------------------------
def lighting_control():
    """
    Control logic for managing LED lighting to supplement sunlight.
    - Measures accumulated PAR over the day.
    - Turns on LED lights if the daily target is not met by sunset.
    """
    global daily_par_accumulation
    # Read current PAR level (µmol/m²/s)
    current_par = read_par_level()
    
    # Simulate sunlight during the day; accumulate light received
    if 6 <= datetime.now().hour <= 18:  # Daytime hours (6 AM - 6 PM)
        daily_par_accumulation += current_par * 0.5  # Accumulate light in µmol/m² over time step
    else:
        # Check if PAR accumulation is below target at sunset
        if daily_par_accumulation < 20000:  # Example target value for daily light intake
            control_led_lighting(True)  # Turn on LED lights
        else:
            control_led_lighting(False)  # Turn off LED lights

# -----------------------------------------------------------------
# Function: Nutrient Mixology Control
# -----------------------------------------------------------------
def nutrient_mixology_control():
    """
    Control logic for adjusting nutrient levels.
    - Uses pumps to add water and nutrients until target EC and pH are met.
    """
    current_ec = read_ec_level()  # Read current EC level
    current_ph = read_ph_level()  # Read current pH level

    # Iterate and adjust until target EC and pH are met (placeholder logic)
    while abs(current_ec - target_ec) > 0.1 or abs(current_ph - target_ph) > 0.1:
        if current_ec < target_ec:
            control_nutrient_pump_a(True)  # Add nutrient solution A
        elif current_ec > target_ec:
            control_valve_distilled(True)  # Add distilled water to reduce concentration

        if current_ph < target_ph:
            control_nutrient_pump_b(True)  # Add pH up solution
        elif current_ph > target_ph:
            control_nutrient_pump_c(True)  # Add pH down solution

        # Re-read levels
        current_ec = read_ec_level()
        current_ph = read_ph_level()
        
    # Stop all pumps and valves once target levels are achieved
    control_nutrient_pump_a(False)
    control_nutrient_pump_b(False)
    control_nutrient_pump_c(False)
    control_valve_distilled(False)

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
def co2_enrichment_control():
    """
    Control logic for CO2 enrichment.
    - Turns on CO2 valve when below a certain level and off when above.
    """
    current_co2 = read_co2_level()
    if current_co2 < co2_min:
        control_co2_valve(True)  # Open CO2 valve to enrich air
    elif current_co2 > co2_max:
        control_co2_valve(False)  # Close CO2 valve to prevent oversaturation

# -----------------------------------------------------------------
# Function: Temperature Control
# -----------------------------------------------------------------
def temperature_control():
    """
    Control logic for temperature using HVAC system.
    - Uses fuzzy logic to maintain temperature within the desired range.
    """
    current_temp = read_temperature()
    if current_temp < temperature_min:
        control_hvac(True)  # Turn on HVAC to increase temperature
    elif current_temp > temperature_max:
        control_hvac(True)  # Turn on HVAC to reduce temperature
    else:
        control_hvac(False)  # Turn off HVAC when within range

# -----------------------------------------------------------------
# Function: Humidity Control
# -----------------------------------------------------------------
def humidity_control():
    """
    Control logic for humidity.
    - Activates humidifier or irrigation based on humidity levels.
    """
    current_humidity = read_humidity()
    if current_humidity < humidity_min:
        global irrigation_interval
        irrigation_interval = 120  # Increase irrigation frequency (every 2 minutes)
    elif current_humidity > humidity_max:
        control_ventilation(True)  # Increase ventilation to reduce humidity

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
