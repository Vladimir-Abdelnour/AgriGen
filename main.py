#Importing libraries 


# Variable Definitions for AgriGen

elec_air_conditioners = None  # Electricity consumption of air conditioners (heat pumps) in MJ m−2 h−1
elec_lamps = None             # Electricity consumption of lamps in MJ m−2 h−1
elec_water_pumps = None       # Electricity consumption of water pumps, air fans, etc. in MJ m−2 h−1
elec_total = None             # Total electricity consumption in MJ m−2 h−1
co2_use_efficiency = None     # CO2 use efficiency
cop_heat_pumps = None         # Coefficient of performance of heat pumps for cooling
co2_in = None                 # CO2 concentration of room air in µmol mol−1
co2_out = None                # CO2 concentration of outside air in µmol mol−1
co2_loss = None               # CO2 loss to the outside in µmol m−2 h−1
co2_fixed_by_plants = None    # CO2 fixed by plants in µmol m−2 h−1
co2_human_respiration = None  # CO2 released in room air by human respiration in µmol m−2 h−1
co2_cylinder = None           # CO2 supplied to room air from CO2 cylinder in µmol m−2 h−1
delta_t=None                  # Time step used for change of flow
t=None                        # Time at a certain point
dry_mass_increase_rate = None # Dry mass increase rate of plants in µmol m−2 h−1
electric_energy_efficiency = None # Electric energy use efficiency
floor_area = None             # Floor area of culture room in m²
conversion_factor_plant_mass = None # Conversion factor from plant dry mass to chemical energy, 20 MJ kg−1
fertilizer_use_efficiency = None # Inorganic fertilizer use efficiency
conversion_factor_elec_energy = None # Conversion factor from electric energy to PAR_L in MJ m−2 h−1
heat_energy_removed = None    # Heat energy removed from culture room by heat pumps in MJ m−2 h−1
heat_energy_exchange = None   # Heat energy exchange by air infiltration and penetration through walls in MJ m−2 h−1
ion_concentration_in = None   # Ion concentration of "I" in nutrient solution at the inlet of culture beds in mol mol−1
ion_concentration_out = None  # Ion concentration of "I" in nutrient solution at the outlet of culture beds in mol mol−1
ions_supplied = None          # Supply rate of inorganic fertilizer ion element "I" supplied to the PFAL in mol m−2 h−1
ions_absorbed = None          # Absorption rate of inorganic fertilizer ion element "I" by plants in mol m−2 h−1
conversion_factor_co2 = None  # Conversion factor from volume to mass of CO2 (1.80 kg m−3 at 25°C and 101.3 kPa)
conversion_factor_water_vapor = None # Conversion factor from volume to mass of water (0.736 kg m−3 at 25°C and 101.3 kPa)
conversion_factor_liquid_water = None # Conversion factor from volume to mass of liquid water (997 kg m−3 at 25°C and 101.3 kPa)
light_energy_efficiency_parl = None # Light energy use efficiency with respect to PAR_L
light_energy_efficiency_parp = None # Light energy use efficiency with respect to PAR_p
num_air_exchanges = None          # Number of air exchanges in h−1
photosynthetic_radiation_lamps = None # Photosynthetically active radiation emitted from lamps in MJ m−2 h−1
photosynthetic_radiation_surface = None # Photosynthetically active radiation received at plant community surface in MJ m−2 h−1
volume_room_air = None        # Volume of room air in m³
volume_nutrient_solution = None # Volume of nutrient solution in culture beds in m³
water_vapor_density_in = None # Water vapor density of room air in kg m−3
water_vapor_density_out = None # Water vapor density of outside air in kg m−3
water_recycled = None         # Liquid water collected for recycling use in the PFAL in kg m−2 h−1
water_vapor_loss = None       # Water vapor loss rate from the PFAL to the outside in kg m−2 h−1
water_held_in_plants = None   # Water held in plants in the PFAL in kg m−2 h−1
water_supply_rate = None      # Water supply rate into the PFAL in kg m−2 h−1
transpiration_rate = None     # Transpiration rate of plants in the PFAL in kg m−2 h−1
water_uptake_rate = None      # Water uptake rate of plants in culture beds in kg m−2 h−1
water_inflow_rate = None      # Water inflow rate to hydroponic culture beds in the PFAL in kg m−2 h−1
water_outflow_rate = None     # Water outflow rate from hydroponic culture beds in the PFAL in kg m−2 h−1
water_use_efficiency = None   # Water use efficiency


# Equation for Water Use Efficiency (WUE)
# WUE = (water_recycled + water_held_in_plants) / water_supply_rate
water_use_efficiency = (water_recycled + water_held_in_plants) / water_supply_rate

# Equation for Water Vapor Loss (WL)
# water_vapor_loss = volume_room_air * num_air_exchanges * (water_vapor_density_in - water_vapor_density_out) / floor_area
water_vapor_loss = (volume_room_air * num_air_exchanges * (water_vapor_density_in - water_vapor_density_out)) / floor_area

# Equation for CO2 Use Efficiency (CUE)
# CUE = co2_fixed_by_plants / (co2_cylinder + co2_human_respiration) = (co2_cylinder - co2_loss) / (co2_human_respiration + co2_cylinder)
co2_use_efficiency = (co2_cylinder - co2_loss)  / (co2_cylinder + co2_human_respiration)

# Equation for CO2 Loss (CL)
# co2_loss = conversion_factor_co2 * num_air_exchanges * volume_room_air * (co2_in - co2_out) / floor_area
co2_loss = conversion_factor_co2 * num_air_exchanges * volume_room_air * (co2_in - co2_out) / floor_area

# Equation for Light Energy Use Efficiency of Lamps (LUE_L)
# light_energy_efficiency_parl = (conversion_factor_plant_mass * dry_mass_increase_rate) / photosynthetic_radiation_lamps
light_energy_efficiency_parl = (conversion_factor_plant_mass * dry_mass_increase_rate) / photosynthetic_radiation_lamps

# Equation for Light Energy Use Efficiency of Plant Community (LUE_p)
# light_energy_efficiency_parp = (conversion_factor_plant_mass * dry_mass_increase_rate) / photosynthetic_radiation_surface
light_energy_efficiency_parp = (conversion_factor_plant_mass * dry_mass_increase_rate) / photosynthetic_radiation_surface

# Equation for Electric Energy Use Efficiency of Lighting (EUE_L)
# electric_energy_efficiency = conversion_factor_elec_energy * light_energy_efficiency_parl
electric_energy_efficiency = conversion_factor_elec_energy * light_energy_efficiency_parl

# Equation for Electricity Consumed by Lamps (elec_lamps)
# elec_lamps = photosynthetic_radiation_lamps / conversion_factor_elec_energy
elec_lamps = photosynthetic_radiation_lamps / conversion_factor_elec_energy

# Equation for Coefficient of Performance of Heat Pumps (COP)
# cop_heat_pumps = heat_energy_removed / elec_air_conditioners
cop_heat_pumps = heat_energy_removed / elec_air_conditioners

# Equation for Inorganic Fertilizer Use Efficiency (FUE_I)
# fertilizer_use_efficiency = ions_absorbed / ions_supplied
fertilizer_use_efficiency = ions_absorbed / ions_supplied

# Equation for Total Electricity Consumption (elec_total)
# elec_total = elec_lamps + elec_air_conditioners + elec_water_pumps
elec_total = elec_lamps + elec_air_conditioners + elec_water_pumps

# Equation for Electricity Consumption for Air Conditioning (elec_air_conditioners)
# elec_air_conditioners = (elec_lamps + elec_water_pumps + heat_energy_exchange) / cop_heat_pumps
elec_air_conditioners = (elec_lamps + elec_water_pumps + heat_energy_exchange) / cop_heat_pumps

# Equation for Net Photosynthetic Rate (co2_fixed_by_plants)
# co2_fixed_by_plants = co2_cylinder + co2_human_respiration - ((conversion_factor_co2 * num_air_exchanges * volume_room_air * (co2_in - co2_out)) / floor_area) * (co2_in - co2_out)
# Intermediate term for change in CO2 concentration over time
delta_co2_in = (co2_in(t + delta_t/2) - co2_in(t - delta_t/2)) / delta_t

co2_fixed_by_plants = co2_cylinder + co2_human_respiration - ((conversion_factor_co2 * num_air_exchanges * volume_room_air * (co2_in - co2_out)) / floor_area) + delta_co2_in

# Equation for Transpiration Rate (transpiration_rate)
# transpiration_rate = water_recycled + (num_air_exchanges * (volume_room_air * (water_vapor_density_in - water_vapor_density_out)) / floor_area)
# Intermediate term for change in water vapor density over time
delta_water_vapor_density_in = (water_vapor_density_in(t + delta_t/2) - water_vapor_density_in(t - delta_t/2)) / delta_t
transpiration_rate = water_recycled + (num_air_exchanges * (volume_room_air * (water_vapor_density_in - water_vapor_density_out)) / floor_area)+delta_water_vapor_density_in

# Equation for Water Uptake Rate by Plants (water_uptake_rate)
# water_uptake_rate = water_held_in_plants + transpiration_rate
water_uptake_rate = water_held_in_plants + transpiration_rate

# Equation for Ion Uptake Rate by Plants (ions_absorbed)
# ions_absorbed = ion_concentration_in * water_inflow_rate - ion_concentration_out * water_outflow_rate
ions_absorbed = ion_concentration_in * water_inflow_rate - ion_concentration_out * water_outflow_rate