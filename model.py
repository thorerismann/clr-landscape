#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 00:45:17 2022

@author: tge
"""

from nlmpy import nlmpy
import pandas as pd
from dataclasses import dataclass
import random
import numpy as np
datadir = "/home/tge/dev/rust-model/clr-landscape/data" 



    # First make the landscape using the neutral landscape model standard in landscape ecology
    # This is chosen as coffee is often planted in a patchwork of forest farms
    # quantititeis chosen follow The Paper
    
    ############################################
    # define parameters
    #######################################
    
# grid parameters
size = 40 #x,y size of the grid
cluster = 0.4 # cluster value ranging from 0-1 for neutral landscape model
proportions = [0.4,0.6] # proportion of values in each category (0,1 coffee not coffee)
plants_per_cell = 8 # number of plants in each cell

# plant values
max_production = 4000 # typical production of coffee beans per plant
resistance = 1 # base resistance of plant (none)
production = 1 # percentage of max production of berries

# weather parameters (if weather is good for infection)
weather_within_cell_dry = 0.2
weather_within_cell_wet = 0.7
weather_adj = 0.6
weather_cluster = 0.05

# virus values
days = 1/365 # base progression time of virus
progression_cutoff = [20,40,60,120] # days after infection when infection grows more rapidly
progression_scaling = [1,4,8,16] # scaling factor of infection rate (eg 20 < x < 40 virus grows at 4* days)


# infection parameters

#######################################
# make landscape
#######################################

def make_landscape(size,cluster):
    landscape = nlmpy.randomClusterNN(size, size, cluster, "8-neighbourhood")
    landscape = pd.DataFrame(nlmpy.classifyArray(landscape, proportions))
    landscape = landscape.astype(bool)
    return landscape

# create the plants in each grid cell with coffee
########################################
# define coffe plant class
#########################################

@dataclass
class Plant:
    grid: tuple = (0,0) # location of plant in grid cell
    plant: int = 0 # id of plant in grid cell
    infection: float = 0 # level of infection 0 < infection < 1
    infectivity: int = 0 # level of infectivity is 10*infection except during latency period (0)
    production: float = 1 # 0< production < 1 modifies the output relative to max berry output based on infection level
    resistance: float = 1 # resistance to clr slows spread of the virus
    cost: int = 100
    
    def progression(self):
        # remove first if
        if (self.infection > 0) and ( self.infection <1):
            if self.infection < progression_cutoff[0]*days:
                self.infection = self.infection + progression_scaling[0]*days*self.resistance
            elif (self.infection < progression_cutoff[1]*days) and (self.infection<1):
                self.infection  = self.infection + progression_scaling[1]*days*self.resistance
            elif (self.infection < progression_cutoff[2]*days) and (self.infection<1):
                self.infection = self.infection + progression_scaling[2]*days*self.resistance
            elif (self.infection < progression_cutoff[3]*days) and (self.infection<1):
                self.infection = self.infection + progression_scaling[3]*days*self.resistance
            else:
                self.infection = self.infection + 20*days*self.resistance
        if self.infection >1:
            self.infection = 1
            
    def get_production(self):
        self.production = (1-0.5*self.infection)*max_production
    
    def define_infectivity(self):
        # defines infectivity based on cutoff of days
        if self.infection < 20*days:
            self.infectivity = int(0)
        else:
            self.infectivity = self.infection
        return self.infectivity


def get_harvest():
    total_berries = 0
    for i in myplants:
        total_berries = total_berries + max_production*i.production
    return total_berries

def weather_effects(day):
    """
    Define whether or not weather effects are good for spreading each day (1) within grid cells (2) between adj grid cells (3) across clusters
    """
    if day < 180:
        cell = random.uniform(0,1) < weather_within_cell_dry
    else:
        cell = random.uniform(0,1)< weather_within_cell_wet
    cluster = False
    grid = False

    # if it is, is weather ok to spread further to neighboring grids (small wind, normalish conditions)
    if cell:
        cluster = random.uniform(0,1)<weather_adj
    # if it is, is weather ok to spread to other clusters (e.g. wind and rain)
        if cluster & cell:
            grid = random.uniform(0,1) < weather_cluster
            return [cell,cluster,grid]
        else:
            return [cell,cluster,grid]
    else:
        return [cell,cluster,grid]

def get_neighbors(grid):
    possible =  [(grid[0]+1,grid[1]+1),(grid[0],grid[1]+1),(grid[0]-1,grid[1]+1),(grid[0]-1,grid[1]),(grid[0]-1,grid[1]-1),(grid[0],grid[1]-1),(grid[0]+1,grid[1]-1),(grid[0]+1,grid[1])]
    return possible
 
def get_gridscore(gridsquare):
    return sum([x.infectivity for x in myplants if x.grid == gridsquare])    

def within_cell_infection(gridsquare):
    """
    Within cell infection depends on the infection score of the grid. The infection score is a linear function of the infectivity of each plant in the cell
    - For simplicity, there are 3 conditions: low infection score = low probability of infection, medium infection score = medium probability of infection, high infection score = guaranteed infection
    - 
    Only one new pl
    
    """
    infection_score = get_gridscore(gridsquare)
    plants_in_cell_healthy = [x for x in myplants if (x.infection < 0.001) &  (x.grid == gridsquare)]
    if  len(plants_in_cell_healthy) > 0:
        if infection_score < 0.4:
            pass
        else:
            plants_in_cell_healthy[0].infection = days
            pass
    return (gridsquare,infection_score)


def neighbor_cell_infection(gridscore):
    """
    The likelihood of infecting one additional plant in any given adjascent grid. If the infection score is too low, then there is no adjascent grid infection.
    For simplicity an infection score above 1 gives a fixed chance of infecting one plant in an adjascent grid cell.
    """
    neighbors  = get_neighbors(gridscore[0])
    healthy_neighbors = [x for x in myplants if (x.grid in neighbors) and (x.infection < 0.0001)]
    a = max(1,random.randint(0, len(healthy_neighbors)))
    if gridscore[1] < 0.6 or len(healthy_neighbors)<1:
        pass
    elif random.uniform(0,1)< 0.8:
        healthy_neighbors[a-1].infection = days

def global_infection(grid_scores):
    """
    This function defines the likelood of infection for all healthy plants following a windstorm under conditions of likely infection across clusters. This is the only means of spread between clusters. It can also be interpreted as the probability of transporting and depositing CLR via equipment
    """
    total_score = sum(x[1] for x in grid_scores)
    healthy = [x for x in myplants if x.infection < 0.0001]
    if len(healthy) > 100:
        if total_score < 0.5:
            pass
        else:
            a = random.randint(0,len(healthy)-1)
            b = random.randint(0,len(healthy)-1)
            c = random.randint(0,len(healthy)-1)
            healthy[a].infection = days
            healthy[b].infection = days
            healthy[c].infection = days
        

def each_day():
    """This function controls the whole program and runs it each day"""
    weather = weather_effects(day)
    inf_plants = [x for x in myplants if x.infection > 0.0001]
    [x.progression() for x in inf_plants]
    [x.define_infectivity() for x in inf_plants]
    if weather[0]:
        inf_grid = set([x.grid for x in inf_plants])
        grid_scores = []
        for i in inf_grid:
            grid_infection_score = within_cell_infection(i)
            grid_scores.append(grid_infection_score)
        if weather[1]:
            for i in grid_scores:
                neighbor_cell_infection(i)
            if weather[2]:
                global_infection(grid_scores)
    infectivity_score = sum([x.infectivity for x in myplants])
    infected_grid_cells = len(set(x.grid for x in myplants if x.infection > 0.001))
    infected_plants = len([x for x in myplants if x.infection > 0.001])
    results = [infectivity_score,infected_grid_cells,infected_plants,day]
    return results

def initial_infection():
    """
    Randomly select one plant and one plant in an an adjascent cell to become infected
    """
    a = random.randint(0,len(myplants))
    inf_plants_seed = myplants[a]
    inf_plants_seed.infection = days
    b = get_neighbors(inf_plants_seed.grid)
    c = random.randint(0,len(b)-1)
    neighbors = [x for x in myplants if x.grid in b]
    neighbors[c].infection = days

def save_intermediate_infected():
    """This function saves the intermediate spreads of CLR at day 0, 120, 240, 360"""
    infected = set([x.grid for x in myplants if x.infection > 0.0001])
    landscaped = landscape*1
    for index,row in landscaped.iterrows():
        column = 0
        while column < size:
            if (index,column) in infected:
                row[column] = 2
            column+=1
    landscaped.to_csv(F"{datadir}/map-{day}-{z}-{proportions}-{cluster}.csv")

# Put it all together

# make the landscape and identify the coffee / not-coffee cells
returns = []
runs = 10
for z in range(0,runs):
    landscape = make_landscape(size,cluster)
    cafe = []
    not_cafe = []
    for index,row in landscape.iterrows():
        c = []
        nc = []
        column = 0
        while column < size:
            if row[column]:
                c.append((index,column))
            else:
                nc.append((index,column))
            column+=1
        cafe.extend(c)
        not_cafe.extend(nc)
    
    # Create a user-specified number of instances of the Plant class for each cell with coffee in it
    
    myplants =[]
    for i in cafe:
        for j in range(plants_per_cell):
            myplants.append(Plant(grid = i, plant = j))
    
    # initialize infection
        
    initial_infection()     
    
    # Run code for each day       
    day = 0
    returns = []
    daily_results = []
    while day < 365:
        daily_results.append(each_day())
        if day%120==0:
            save_intermediate_infected()
            print(day)
        day+=1
    
    # organize data
    # harvest berries
    day = 0
    
    def calculate_returns():
        [x.get_production() for x in myplants]
        return sum([x.production for x in myplants])
    
    coffee_cherries = np.floor(calculate_returns())
    returns.append((coffee_cherries,runs))
    results = pd.DataFrame(daily_results)
    results.columns = ["infection_score","infected_cells",'infected_plants','day']
    results.to_csv(F"{datadir}/results-{z}-{proportions}-{cluster}.csv")
    datadir = "/home/tge/dev/rust-model/clr-landscape/data" 

b = pd.DataFrame(returns)
b.to_csv(F"{datadir}/returns-{proportions}-{cluster}.csv")