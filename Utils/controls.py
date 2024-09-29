# Actuator Control Functions for AgriGen Farming Operating System

# Irrigation Actuator Control Functions
def control_valve_nutrient_a(on: bool):
    """
    Controls the valve for Nutrient Tank A.
    Args:
        on (bool): True to open the valve, False to close it.
    """
    action = "Opening" if on else "Closing"
    print(f"{action} valve for Nutrient Tank A")  # Placeholder for actual valve control logic

def control_valve_nutrient_b(on: bool):
    """
    Controls the valve for Nutrient Tank B.
    Args:
        on (bool): True to open the valve, False to close it.
    """
    action = "Opening" if on else "Closing"
    print(f"{action} valve for Nutrient Tank B")  # Placeholder for actual valve control logic

def control_valve_nutrient_c(on: bool):
    """
    Controls the valve for Nutrient Tank C.
    Args:
        on (bool): True to open the valve, False to close it.
    """
    action = "Opening" if on else "Closing"
    print(f"{action} valve for Nutrient Tank C")  # Placeholder for actual valve control logic

def control_valve_distilled(on: bool):
    """
    Controls the valve for the Distilled Water Tank.
    Args:
        on (bool): True to open the valve, False to close it.
    """
    action = "Opening" if on else "Closing"
    print(f"{action} valve for Distilled Water Tank")  # Placeholder for actual valve control logic

def control_valve_nutrient_rich(on: bool):
    """
    Controls the valve for the Nutrient-Rich Tank.
    Args:
        on (bool): True to open the valve, False to close it.
    """
    action = "Opening" if on else "Closing"
    print(f"{action} valve for Nutrient-Rich Tank")  # Placeholder for actual valve control logic

def activate_pump(on: bool):
    """
    Activates or deactivates the main water pump.
    Args:
        on (bool): True to turn the pump on, False to turn it off.
    """
    action = "Activating" if on else "Deactivating"
    print(f"{action} main water pump")  # Placeholder for actual pump control logic

# Nutrient Mixology Actuator Control Functions
def control_nutrient_pump_a(on: bool):
    """
    Activates or deactivates the pump for Nutrient Solution A.
    Args:
        on (bool): True to activate the pump, False to deactivate it.
    """
    action = "Activating" if on else "Deactivating"
    print(f"{action} pump for Nutrient Solution A")  # Placeholder for actual pump control logic

def control_nutrient_pump_b(on: bool):
    """
    Activates or deactivates the pump for Nutrient Solution B.
    Args:
        on (bool): True to activate the pump, False to deactivate it.
    """
    action = "Activating" if on else "Deactivating"
    print(f"{action} pump for Nutrient Solution B")  # Placeholder for actual pump control logic

def control_nutrient_pump_c(on: bool):
    """
    Activates or deactivates the pump for Nutrient Solution C.
    Args:
        on (bool): True to activate the pump, False to deactivate it.
    """
    action = "Activating" if on else "Deactivating"
    print(f"{action} pump for Nutrient Solution C")  # Placeholder for actual pump control logic

# Environment Control Actuator Control Functions
def control_co2_valve(on: bool):
    """
    Opens or closes the CO2 valve.
    Args:
        on (bool): True to open the valve, False to close it.
    """
    action = "Opening" if on else "Closing"
    print(f"{action} CO2 valve")  # Placeholder for actual CO2 valve control logic

def control_hvac(on: bool):
    """
    Turns the HVAC system on or off.
    Args:
        on (bool): True to turn on, False to turn off.
    """
    action = "Turning on" if on else "Turning off"
    print(f"{action} HVAC system")  # Placeholder for actual HVAC control logic

def control_ventilation(on: bool):
    """
    Turns the ventilation system on or off.
    Args:
        on (bool): True to turn on, False to turn off.
    """
    action = "Turning on" if on else "Turning off"
    print(f"{action} ventilation system")  # Placeholder for actual ventilation control logic

# Lighting Control Actuator Control Functions
def control_led_lighting(on: bool):
    """
    Turns the LED lighting system on or off.
    Args:
        on (bool): True to turn on, False to turn off.
    """
    action = "Turning on" if on else "Turning off"
    print(f"{action} LED lighting system")  # Placeholder for actual lighting control logic

# Energy Management Actuator Control Function
def control_energy_selling(on: bool):
    """
    Enables or disables energy selling back to the grid.
    Args:
        on (bool): True to enable energy selling, False to disable.
    """
    action = "Enabling" if on else "Disabling"
    print(f"{action} energy selling to grid")  # Placeholder for actual energy management logic
