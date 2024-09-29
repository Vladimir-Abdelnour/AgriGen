# Importing libraries
import time
import os
import csv
import ast
from Database_handler import *


# def mix_nutrients(db_name, config):
#     plant_type = config['Plants']['current_plant_type']
#     number_of_plants = config['General']['number_of_plants']
#
#     tank1_volume, tank2_volume, tank3_volume, target_ec = calculate_nutrient_mix(plant_type, number_of_plants, config)
#
#     # Simulate mixing process
#     main_tank_ec = (tank1_volume * config['Nutrients']['tank1_concentration'] +
#                     tank2_volume * config['Nutrients']['tank2_concentration'] +
#                     tank3_volume * config['Nutrients']['tank3_concentration']) / (
#                                tank1_volume + tank2_volume + tank3_volume)
#
#     # Log the nutrient mix
#     log_nutrient_mix(db_name, plant_type, number_of_plants, tank1_volume, tank2_volume, tank3_volume, main_tank_ec)
#
#     print(f"Mixed nutrients for {number_of_plants} {plant_type} plants.")
#     print(f"Tank 1: {tank1_volume:.2f}L, Tank 2: {tank2_volume:.2f}L, Tank 3: {tank3_volume:.2f}L")
#     print(f"Main tank EC: {main_tank_ec:.2f} mS/cm (Target: {target_ec} mS/cm)")


# def calculate_nutrient_mix(plant_type, plant_types, number_of_plants, config):
#     if plant_type in plant_types:
#         ratio = config['nutrients'][plant_type+'_ratio']
#         target_ec = config['nutrients'][plant_type+'_target_ec']
#     else:
#         print(plant_type)
#         print("lettuce")
#         print(type("lettuce"))
#         print(type(plant_type))
#         raise ValueError("Unknown plant type")
#
#     # Convert ratio to a list of floats
#     ratio = ast.literal_eval(ratio)
#     ratio = [float(r) for r in ratio]
#
#     total_ratio = sum(ratio)
#     total_volume = number_of_plants * 0.1  # Assume 0.1L per plant
#
#     tank1_volume = (ratio[0] / total_ratio) * total_volume
#     tank2_volume = (ratio[1] / total_ratio) * total_volume
#     tank3_volume = (ratio[2] / total_ratio) * total_volume
#
#     return tank1_volume, tank2_volume, tank3_volume, target_ec


# def mix_nutrients(db_name, config):
#     plant_type = config['plants']['current_plant_type']
#     plant_types = config['plants']['plant_types']
#     number_of_plants = config['general']['number_of_plants']
#
#     tank1_volume, tank2_volume, tank3_volume, target_ec = calculate_nutrient_mix(plant_type, plant_types, number_of_plants, config)
#
#     # Simulate mixing process
#     main_tank_ec = (tank1_volume * config['nutrients']['tank1_concentration'] +
#                     tank2_volume * config['nutrients']['tank2_concentration'] +
#                     tank3_volume * config['nutrients']['tank3_concentration']) / (
#                                tank1_volume + tank2_volume + tank3_volume)
#
#     # Log the nutrient mix
#     log_nutrient_mix(db_name, plant_type, number_of_plants, tank1_volume, tank2_volume, tank3_volume, main_tank_ec)
#
#     print(f"Mixed nutrients for {number_of_plants} {plant_type} plants.")
#     print(f"Tank 1: {tank1_volume:.2f}L, Tank 2: {tank2_volume:.2f}L, Tank 3: {tank3_volume:.2f}L")
#     print(f"Main tank EC: {main_tank_ec:.2f} mS/cm (Target: {target_ec} mS/cm)")

def main():
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
    co2_in = float(config['environment']['co2_in'])
    co2_out = float(config['environment']['co2_out'])
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
    ion_concentration = config['nutrients']['ion_concentration_in']  # mol/mol
    nutrient_solution_supply_rate = config['water']['water_inflow_rate']  # kg/(m²·s)
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

    # # Database operations
    # db_name = 'hydroponics.db'
    # setup_database(db_name)
    #
    # # Example of running the nutrient mixing process
    # mix_nutrients(db_name, config)


if __name__ == "__main__":
    main()