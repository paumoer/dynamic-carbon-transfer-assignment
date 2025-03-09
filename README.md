# A dynamic model for carbon transfers in Earth’s system - Assignment
Modeling carbon transfers in the Earth system using a six-pool carbon model.

This assignment focuses on modeling carbon transfers in the Earth system using a six-pool carbon model. Tasks include implementing carbon emission functions, solving differential equations to simulate carbon fluxes, integrating anthropogenic emissions, evaluating intervention scenarios, and analyzing required emission reductions for climate goals. Results are documented in a short report.
# List of Tasks
![six-pool-model](https://github.com/user-attachments/assets/d3af02a1-3a1c-4453-af26-9369d8377142)

## Part 1: Carbon Emission Functions 
Create a function to calculate land-use emissions (1750–2020).
Create a function to calculate fossil fuel emissions (1850–2020).
Plot and save a figure of land-use and fossil fuel emissions (Task_1.png).
## Part 2: Develop a Six-Pool Global Carbon Model 
Write a function to compute the rates of change for six carbon pools based on 11 fluxes.
Solve the differential equations using Scipy’s ODEINT with given parameters.
Simulate and plot carbon pool changes (1750–2020) without anthropogenic emissions (Task_2.png).
## Part 3: Integrating Emissions and Human Interventions 
Modify the carbon model to include emission functions from Part 1, toggleable with a Boolean variable.
Plot and save a figure of carbon pool changes including anthropogenic emissions (1750–2100) (Task_3_2.png).
Implement assigned human intervention scenarios, toggleable via a Boolean variable.
Calculate the required emissions reduction in 2025 to lower atmospheric carbon below 300 ppm by 2100.
Plot and save a figure of carbon pools with interventions (Task_3_4.png).
