# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 14:27:56 2023

@author: Paula Mörstedt

Group 4: Number 22
"""
#%% all librarie
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.integrate as spi

#%%
""""USER INPUT NEEDED: PLEASE DECIDE: 
        if antropogenic emissions (land-use and fossil-fuel emission) are to be included:
            turn anthrop = True
        if human interventions are to be included: 
            turn human_interventions = True
        if you want to calulate a certain atmospheric carbon goal:
            turn get_carbon_goal = True
        PLEASE NOTICE: if human_interventions = True, then anthrop needs to be True as well
                        if get_carbon_goal == True, then anthrop and human_interventions needs to be True"""
            
anthrop = False #False means assuming no anthropogenic emissions from 1750-2020

human_interventions = False #False means assuming no human interventions 

get_carbon_goal = False

"""Human intervention scenarios: Choose a scenario by changing mynumber"""
mynumber = 3

scenarionumbers = [19,20,21,22,23,24]
landuse_slopes = [-0.0033, -0.0033, -0.01, -0.01, 0, 0] #PgC/yr/yr
fossil_slopes = [-0.01483, -0.1217, -0.01483, -0.1217, 0, 0] #PgC/yr/yr
action_years = [2035, 2065, 2035, 2065, 2035, 2065]

scenarionumber = scenarionumbers[mynumber]
landuse_slope = landuse_slopes[mynumber]
fossil_slope = fossil_slopes[mynumber]
action_year = action_years[mynumber]

"""USER INPUT: Change the values below, if you want to calculate which slope 
                the fossil fuel emission functions needs to have
                in order to reach in the goal_year the goal_carbon_emissions."""

goal_year = 2100
year_of_change = 2025 #year when the change begins
goal_carbon_emissions_ppmv = 300 #ppmv
goal_carbon_emissions = goal_carbon_emissions_ppmv * 2.13 #PgC
goal_slope = 0 #starting point for the while loop 
stepwidth = 0.001 #stepwidth for the numerical solution of calculating the goal slope 

#%% preventing bugs
if anthrop == False and human_interventions == True:
    anthrop = True
    print("Your user input is wrong. If you want to include human interventions 'anthrop' needs to be 'True'.\n The code has been therefore modified.")
elif get_carbon_goal and not anthrop and not human_interventions:    
    anthrop == True
    human_interventions == True
    print("Your user input is wrong. If you want to get the slope for your carbon goal, turn anthrop and human_interventions == True. I did that for you. You are welcome.")

#%%
""""Functions that calculate the land-use and fossil-fuel emissions."""
def land_use_emissions(year):
    #function that calculates the land-use emissions for a given year (assuming land-use emissions started in 1750)
       # depending on including human interventions or not
    #input: year, human_interventions - a boolean that tells to include 
    #output: emissions for given year in PgC/yr
    if year < 1750: 
        landuse_emissions= 0 
    elif year <= 1900: 
        landuse_emissions= (year - 1750)*0.0033
    elif year > 1900 and year <= 1950: 
        landuse_emissions = ((1900 - 1750)*0.0033) + ((year - 1900)*0.01)
    elif year > 1950: 
        landuse_emissions = ((1900 - 1750)*0.0033) + ((1950 - 1900)*0.01)
 
    return landuse_emissions
    
def land_use_emissions_humanint(year):
    landuse_emissions = ((1900 - 1750)*0.0033) + ((1950 - 1900)*0.01) + ((year - (action_year-1))*landuse_slope)
    return landuse_emissions

def fossil_fuel_emissions(year):
    #function that calculates the fossil-fuel emissions for a given year
    #input: year
    #output: emissions for given year in PgC/yr
    if not get_carbon_goal:
        if year < 1850:
            ff_emissions= 0 
        elif year >= 1850 and year <= 1950: 
            ff_emissions= (year-1850 + 1)*0.01483 
        elif year > 1950: 
            ff_emissions= ((1950-1850 + 1)*0.01483) + ((year-1950)*0.1217)
            
    else: #if get_carbon_goal == True  
        if year < 1850:
            ff_emissions= 0 
        elif year >= 1850 and year <= 1950: 
            ff_emissions= (year-1850 + 1)*0.01483 
        elif year > 1950 and year < year_of_change: 
            ff_emissions= ((1950-1850 + 1)*0.01483) + ((year-1950)*0.1217)
        elif year >= year_of_change:
            ff_emissions = ((1950-1850 + 1)*0.01483) + (((year_of_change-1)-1950)*0.1217) + ((year - (year_of_change-1))*goal_slope)

    return ff_emissions
    

def fossil_fuel_emissions_humanint(year):
    ff_emissions = ((1950-1850 + 1)*0.01483) + (((action_year-1)-1950)*0.1217) + ((year - (action_year-1))*fossil_slope)
    return ff_emissions

#%%
"""Six-pool global carbon model"""

#initial source pool values
atm0 = 600 #PgC
bio0 = 730 #PgC
soil0 = 1250 #PgC
ocshallow0 = 1000 #PgC
ocdeep0 = 40000 #PgC
geo0 = 90000000 #PgC
S0 = [atm0, bio0, soil0, ocshallow0, ocdeep0, geo0] 

#variables that need definition
    #from the atm_bio_flow
f_0  = 62 #PgC/yr
beta = 0.4
    #from the ocshallow_atm_flow
kpsi = 0.07 #1/yr


def dSdt(S,t):
    #state change function which calculates the rates of change for 6 carbon pools
    #input: system state array or list in the following order atm, bio, soil, ocshallow, ocdeep, geo
    #output:system change ergo an array of system change functions
    
    if not anthrop:
        delta = 0
        gamma = 0
    elif anthrop and not human_interventions:
        delta = land_use_emissions(t)
        gamma = fossil_fuel_emissions(t)
    elif anthrop and human_interventions and not get_carbon_goal:
        if t < action_year:
            delta = land_use_emissions(t)
            gamma = fossil_fuel_emissions(t)
        else:
            delta = land_use_emissions_humanint(t)
            gamma = fossil_fuel_emissions_humanint(t)
    elif get_carbon_goal:
        gamma = fossil_fuel_emissions(t)
        if t < action_year:
            delta = land_use_emissions(t)
        else:
            delta = land_use_emissions_humanint(t)
            
    #initial source pool values
    atm0 = 600 #PgC
    bio0 = 730 #PgC
    soil0 = 1250 #PgC
    ocshallow0 = 1000 #PgC
    ocdeep0 = 40000 #PgC
    geo0 = 90000000 #PgC
    
    #define the current state variables for the different pools depending on the input array
    atm_current = S[0]
    bio_current = S[1]
    soil_current = S[2]
    ocshallow_current = S[3]
    ocdeep_current = S[4]
    geo_current = S[5]
    
    atm_current_ppmv = atm_current / 2.13 #with 1ppmv = 2.13PgC    
    
    #define all the flows between the pools
    atm_bio_flow = f_0*(1 + beta * math.log(atm_current/atm0)) #function f #math.log calculates the natural logarithm
    atm_ocshallow_flow = (70/atm0)*atm_current
    soil_atm_flow = (62/soil0)*soil_current
    bio_atm_flow = delta #emissions from land use taks 1
    epsilon = 3.69 + (1.86e-2 * atm_current_ppmv) - (1.8e-6*atm_current_ppmv**2)
    ocshallow_atm_flow = kpsi * (ocshallow0 + epsilon * (ocshallow_current - ocshallow0)) #psi function
    geo_atm_flow1 = (0.2/geo0)*geo_current
    geo_atm_flow2 = gamma #emissions from fossil fuels task 1
    bio_soil_flow1 = (62/bio0)*bio_current
    bio_soil_flow2 = delta
    ocshallow_ocdeep_flow = (60/ocshallow0)*ocshallow_current
    ocdeep_ocshallow_flow = (60/ocdeep0)*ocdeep_current
    ocdeep_geo_flow = (0.2/ocdeep0)*ocdeep_current
    
    #define the rates of change
    datm_dt = soil_atm_flow + bio_atm_flow + ocshallow_atm_flow + geo_atm_flow1 + geo_atm_flow2 - atm_bio_flow - atm_ocshallow_flow
    dbio_dt = atm_bio_flow - bio_atm_flow - bio_soil_flow1 - bio_soil_flow2
    dsoil_dt = bio_soil_flow1 + bio_soil_flow2 - soil_atm_flow
    docshallow_dt = atm_ocshallow_flow + ocdeep_ocshallow_flow - ocshallow_atm_flow - ocshallow_ocdeep_flow
    docdeep_dt = ocshallow_ocdeep_flow - ocdeep_geo_flow - ocdeep_ocshallow_flow
    dgeo_dt = ocdeep_geo_flow - geo_atm_flow1 - geo_atm_flow2
    
    return [datm_dt, dbio_dt, dsoil_dt, docshallow_dt, docdeep_dt, dgeo_dt]

#%%
"""Calculating the solution"""
if not anthrop: 
    t_range = np.arange(1750,2021,1)
    solution = spi.odeint(dSdt, S0, t_range)      
    
elif anthrop and not get_carbon_goal:
    t_range = np.arange(1750,2101,1)
    solution = spi.odeint(dSdt, S0, t_range)
    
elif get_carbon_goal:
    """ Required fossil fuel emissions rate that 
    brings atmospheric carbon concentrations to 300 ppmv by 2100"""

    t_range = np.arange(1750,2101,1)
   # solution = spi.odeint(dSdt, S0, t_range)
    
    #get the index of the goal year, in case we change the t_range or want another goal year
    goal_year_index = 0
    for element in t_range:
        if element == 2100:
            break
        else:
            goal_year_index += 1
    
    solution_3_5 = spi.odeint(dSdt, S0, t_range)
    
    while solution_3_5[goal_year_index][0] > goal_carbon_emissions:
        goal_slope -= stepwidth
        solution_3_5 = spi.odeint(dSdt, S0, t_range)

#The required fossil fuel emissions rate equals the variable goal_slope 


#%%
"""Plotting the results Task 1"""

x_values = np.linspace(1750,2020,270)

y_values_landuse = []
y_values_fossilfuels = []

for x_value in x_values:
    y_values_landuse.append(land_use_emissions(x_value))
    y_values_fossilfuels.append(fossil_fuel_emissions(x_value))

    
plt.plot(x_values, y_values_landuse, markersize = 3, label = "land-use emissions")
plt.plot(x_values, y_values_fossilfuels, markersize = 3, label = "fossil-fuel emissions")

# Add labels, title, legend, and grid
plt.xlim(1750, 2020)
plt.xlabel("Time in years")
plt.ylabel("CO2 emissions in PgC/yr")
plt.legend()
plt.savefig("Task 1.png", dpi = 300)
plt.show()


#%%
"""Plotting the solution of the carbon pool calculation"""  
if not get_carbon_goal:  
    #resize the solutions values for a better plot
    solution_copy = solution.copy()
    solution_copy[:, 4] = solution_copy[:, 4] * 10**(-2)  # resize the numbers for Deep Ocean
    solution_copy[:, 5] = solution_copy[:, 5] *10**(-5)  # resize the numbers for Geosphere  
    
    # Adding labels
    S_names = ["Atmosphere", "Biosphere", "Soils", "Shallow Ocean", "Deep Ocean 10E-2", "Geosphere 10E-5"]
    
    #plot that depicts changes in the carbon pools
    for i in range(len(S0)):
        plt.plot(t_range, solution_copy[:, i], label = S_names[i])
    
    # names and labels
    plt.xlabel('time / years')
    plt.ylabel('Carbon concentration / PgC')
    plt.legend(loc='upper left') #bbox_to_anchor=(0.5, -0.15))

    if not anthrop:
        plt.savefig("Task_2.png", dpi = 300) #Task 2
    elif anthrop and not human_interventions:
        plt.savefig("Task_3_2.png", dpi = 300) #Task 3_2
    elif anthrop and human_interventions and not get_carbon_goal: 
        plt.savefig("Task_3_4.png", dpi = 300)
        
else:
    print("No carbon pool plot generated in the case of calculating the goal_slope.")