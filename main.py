# Importing libraries
import time
import os
from Database_handler import setup_database, get_latest_readings, get_target_values, log_action
from Config.config_parser import get_config


def mix_nutrients(db_name):
    target_ec, target_ph = get_target_values(db_name)
    if target_ec is None or target_ph is None:
        log_action(db_name, "Error: No target values found in database")
        return

    log_action(db_name, "Nutrient mixing started")

    while True:
        current_ec, current_ph = get_latest_readings(db_name)
        if current_ec is None or current_ph is None:
            log_action(db_name, "Error: No sensor readings found in database")
            break

        if current_ec < target_ec:
            log_action(db_name, "Adding nutrient A")
            time.sleep(0.5)  # Simulate pump action
            log_action(db_name, "Adding nutrient B")
            time.sleep(0.5)  # Simulate pump action
        elif current_ph > target_ph:
            log_action(db_name, "Adding pH down solution")
            time.sleep(0.2)  # Simulate pump action
        elif current_ph < target_ph:
            log_action(db_name, "Adding pH up solution")
            time.sleep(0.2)  # Simulate pump action
        else:
            log_action(db_name, "Nutrient levels and pH in target range")
            break

        time.sleep(60)  # Wait for mixing

    log_action(db_name, "Nutrient mixing finished")


def main():
    # Specify the path to the config file
    config_file_path = os.path.join('Config', 'config.ini')

    # Get the parsed configuration
    config = get_config(config_file_path)

    # Read input values from config
    number_of_plants = config['General']['number_of_plants']
    floor_area = config['General']['floor_area']

    co2_in = config['Environment']['co2_in']
    co2_out = config['Environment']['co2_out']
    water_vapor_density_in = config['Environment']['water_vapor_density_in']
    water_vapor_density_out = config['Environment']['water_vapor_density_out']
    temperature = config['Environment']['temperature']
    num_air_exchanges = config['Environment']['num_air_exchanges']
    volume_room_air = config['Environment']['volume_room_air']

    photosynthetic_radiation_lamps = config['Lighting']['photosynthetic_radiation_lamps']
    photosynthetic_radiation_surface = config['Lighting']['photosynthetic_radiation_surface']

    water_recycled = config['Water']['water_recycled']
    water_supply_rate = config['Water']['water_supply_rate']
    water_held_in_plants = config['Water']['water_held_in_plants']
    water_inflow_rate = config['Water']['water_inflow_rate']
    water_outflow_rate = config['Water']['water_outflow_rate']

    ion_concentration_in = config['Nutrients']['ion_concentration_in']
    ion_concentration_out = config['Nutrients']['ion_concentration_out']

    elec_water_pumps = config['Energy']['elec_water_pumps']
    heat_energy_exchange = config['Energy']['heat_energy_exchange']

    dry_mass_increase_rate = config['Plants']['dry_mass_increase_rate']

    co2_human_respiration = config['CO2']['co2_human_respiration']
    co2_cylinder = config['CO2']['co2_cylinder']

    conversion_factor_plant_mass = config['Constants']['conversion_factor_plant_mass']
    conversion_factor_elec_energy = config['Constants']['conversion_factor_elec_energy']
    conversion_factor_co2 = config['Constants']['conversion_factor_co2']
    conversion_factor_water_vapor = config['Constants']['conversion_factor_water_vapor']
    conversion_factor_liquid_water = config['Constants']['conversion_factor_liquid_water']

    elec_air_conditioners = config['Energy']['elec_air_conditioners']

    delta_t = config['Simulation']['delta_t']
    t = config['Simulation']['t']

    # Calculations
    water_use_efficiency = (water_recycled + water_held_in_plants) / water_supply_rate

    water_vapor_loss = (volume_room_air * num_air_exchanges * (
                water_vapor_density_in - water_vapor_density_out)) / floor_area

    co2_loss = conversion_factor_co2 * num_air_exchanges * volume_room_air * (co2_in - co2_out) / floor_area

    co2_use_efficiency = (co2_cylinder - co2_loss) / (co2_cylinder + co2_human_respiration)

    light_energy_efficiency_parl = (
                                               conversion_factor_plant_mass * dry_mass_increase_rate) / photosynthetic_radiation_lamps

    light_energy_efficiency_parp = (
                                               conversion_factor_plant_mass * dry_mass_increase_rate) / photosynthetic_radiation_surface

    electric_energy_efficiency = conversion_factor_elec_energy * light_energy_efficiency_parl

    elec_lamps = photosynthetic_radiation_lamps / conversion_factor_elec_energy

    ions_absorbed = ion_concentration_in * water_inflow_rate - ion_concentration_out * water_outflow_rate

    # Note: Some calculations are commented out due to missing variables or circular dependencies
    cop_heat_pumps = heat_energy_exchange / elec_air_conditioners
    #elec_air_conditioners = (elec_lamps + elec_water_pumps + heat_energy_exchange) / cop_heat_pumps
    elec_total = elec_lamps + elec_air_conditioners + elec_water_pumps
    # This is a simplified example and would need to be adjusted based on your specific system
    ion_concentration = config['Nutrients']['ion_concentration_in']  # mol/mol
    nutrient_solution_supply_rate = config['Water']['water_inflow_rate']  # kg/(m²·s)
    density_of_solution = 1000  # kg/m³ (assuming it's close to water density)

    # Convert water inflow rate to volume
    volume_inflow_rate = nutrient_solution_supply_rate / density_of_solution  # m³/(m²·s)

    # Calculate ions_supplied
    ions_supplied = ion_concentration * volume_inflow_rate  # mol/(m²·s)
    fertilizer_use_efficiency = ions_absorbed / ions_supplied

    # Print some results
    print(f"Number of plants: {number_of_plants}")
    print(f"Water Use Efficiency: {water_use_efficiency}")
    print(f"CO2 Use Efficiency: {co2_use_efficiency}")
    print(f"Light Energy Efficiency (PAR_L): {light_energy_efficiency_parl}")
    print(f"Electric Energy Efficiency: {electric_energy_efficiency}")

    # Database operations
    db_name = 'hydroponics.db'
    setup_database(db_name)

    # Example of running the nutrient mixing process
    mix_nutrients(db_name)


if __name__ == "__main__":
    main()