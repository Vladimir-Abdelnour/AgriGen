# config_parser.py

import configparser
import ast

def get_config(config_file_path):
    config = configparser.ConfigParser()

    files_read = config.read(config_file_path)

    if not files_read:
        print("No configuration files were successfully read.")
        return None

    print(f"Successfully read configuration from: {files_read}")

    parsed_config = {
        'General': {
            'number_of_plants': config.getint('General', 'number_of_plants'),
            'floor_area': config.getfloat('General', 'floor_area'),
        },
        'Environment': {
            'co2_in': config.getfloat('Environment', 'co2_in'),
            'co2_out': config.getfloat('Environment', 'co2_out'),
            'water_vapor_density_in': config.getfloat('Environment', 'water_vapor_density_in'),
            'water_vapor_density_out': config.getfloat('Environment', 'water_vapor_density_out'),
            'num_air_exchanges': config.getfloat('Environment', 'num_air_exchanges'),
            'volume_room_air': config.getfloat('Environment', 'volume_room_air'),
            'temperature': config.getfloat('Environment', 'temperature'),
        },
        'Lighting': {
            'photosynthetic_radiation_lamps': config.getfloat('Lighting', 'photosynthetic_radiation_lamps'),
            'photosynthetic_radiation_surface': config.getfloat('Lighting', 'photosynthetic_radiation_surface'),
        },
        'Water': {
            'water_recycled': config.getfloat('Water', 'water_recycled'),
            'water_supply_rate': config.getfloat('Water', 'water_supply_rate'),
            'water_held_in_plants': config.getfloat('Water', 'water_held_in_plants'),
            'volume_nutrient_solution': config.getfloat('Water', 'volume_nutrient_solution'),
            'water_inflow_rate': config.getfloat('Water', 'water_inflow_rate'),
            'water_outflow_rate': config.getfloat('Water', 'water_outflow_rate'),
        },
        'Nutrients': {
            'ion_concentration_in': config.getfloat('Nutrients', 'ion_concentration_in'),
            'ion_concentration_out': config.getfloat('Nutrients', 'ion_concentration_out'),
            'lettuce_ratio': ast.literal_eval(config.get('Nutrients', 'lettuce_ratio')),
            'broccoli_ratio': ast.literal_eval(config.get('Nutrients', 'broccoli_ratio')),
            'lettuce_target_ec': config.getfloat('Nutrients', 'lettuce_target_ec'),
            'broccoli_target_ec': config.getfloat('Nutrients', 'broccoli_target_ec'),
            'tank1_concentration': config.getfloat('Nutrients', 'tank1_concentration'),
            'tank2_concentration': config.getfloat('Nutrients', 'tank2_concentration'),
            'tank3_concentration': config.getfloat('Nutrients', 'tank3_concentration'),
        },
        'Energy': {
            'elec_water_pumps': config.getfloat('Energy', 'elec_water_pumps'),
            'heat_energy_exchange': config.getfloat('Energy', 'heat_energy_exchange'),
            'elec_lamps': config.getfloat('Energy', 'elec_lamps'),
            'elec_air_conditioners': config.getfloat('Energy', 'elec_air_conditioners'),
        },
        'Plants': {
            'dry_mass_increase_rate': config.getfloat('Plants', 'dry_mass_increase_rate'),
            'current_plant_type': config.get('Plants', 'current_plant_type'),
            'plant_types': config.get('Plants', 'plant_types'),
        },
        'CO2': {
            'co2_human_respiration': config.getfloat('CO2', 'co2_human_respiration'),
            'co2_cylinder': config.getfloat('CO2', 'co2_cylinder'),
        },
        'Constants': {
            'conversion_factor_plant_mass': config.getfloat('Constants', 'conversion_factor_plant_mass'),
            'conversion_factor_elec_energy': config.getfloat('Constants', 'conversion_factor_elec_energy'),
            'conversion_factor_co2': config.getfloat('Constants', 'conversion_factor_co2'),
            'conversion_factor_water_vapor': config.getfloat('Constants', 'conversion_factor_water_vapor'),
            'conversion_factor_liquid_water': config.getfloat('Constants', 'conversion_factor_liquid_water'),
        },
        'Simulation': {
            'delta_t': config.getfloat('Simulation', 'delta_t'),
            't': config.getfloat('Simulation', 't'),
        },
    }

    return parsed_config