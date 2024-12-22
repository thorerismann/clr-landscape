#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLR-Landscape Model

This script simulates Coffee Leaf Rust (CLR) infection spread in a neutral landscape
composed of coffee and non-coffee cells. It models infection progression, daily weather
effects on transmission, and ultimately calculates coffee berry yields.
"""

from nlmpy import nlmpy
import pandas as pd
from dataclasses import dataclass
import random
import numpy as np
from pathlib import Path
from typing import List, Tuple

# -------------------------------------------------------------------------------------
# Global Parameters
# -------------------------------------------------------------------------------------

# Data directory path
datadir: Path = Path.cwd() / "data"
datadir.mkdir(exist_ok=True)

# Grid parameters
size: int = 40  # The x,y size of the grid.
cluster: float = 0.4  # Clustering parameter (0-1) for the neutral landscape model.
proportions: List[float] = [0.4, 0.6]  # Proportions of coffee vs. non-coffee in the landscape.
plants_per_cell: int = 8  # Number of plants placed in each coffee cell.

# Plant production parameters
max_production: int = 4000  # Typical production of coffee beans per plant.
resistance: float = 1.0  # Base resistance of the plant (1 = no extra resistance).
production: float = 1.0  # Base production percentage (1 = 100% production).

# Weather parameters affecting infection
weather_within_cell_dry: float = 0.2  # Probability of infection within the same cell in dry conditions.
weather_within_cell_wet: float = 0.7  # Probability of infection within the same cell in wet conditions.
weather_adj: float = 0.6  # Probability that infection spreads to adjacent cells.
weather_cluster: float = 0.05  # Probability that infection spreads beyond adjacent cells (clusters).

# Infection progression parameters
days: float = 1 / 365  # Days used for infection progression speed (1/365 for daily).
progression_cutoff: List[int] = [20, 40, 60, 120]  # Infection progression cutoffs in days.
progression_scaling: List[int] = [1, 4, 8, 16]  # Scaling factors for infection progression at cutoffs.

#######################################
# make landscape
#######################################

def make_landscape(size: int, cluster: float) -> pd.DataFrame:
    """
    Generate a neutral landscape model using randomClusterNN and classify cells
    into coffee (True) vs. non-coffee (False) based on specified proportions.

    Parameters
    ----------
    size : int
        Size of the grid (x and y dimensions).
    cluster : float
        Clustering parameter (0 to 1).

    Returns
    -------
    pd.DataFrame
        DataFrame with boolean values indicating coffee (True) or non-coffee (False).
    """
    landscape = nlmpy.randomClusterNN(size, size, cluster, "8-neighbourhood")
    landscape = pd.DataFrame(nlmpy.classifyArray(landscape, proportions))
    landscape = landscape.astype(bool)
    return landscape

@dataclass
class Plant:
    """
    Represents a coffee plant in a specific grid cell, tracking infection level,
    production, resistance, and infectivity over time.

    Attributes
    ----------
    grid : tuple
        Location of plant in grid cell (row, column).
    plant : int
        ID of plant in grid cell.
    infection : float
        Level of infection (0 < infection < 1).
    infectivity : float
        Level of infectivity based on infection.
    production : float
        Production multiplier (0 < production < 1) modifies the output relative to max berry output based on infection level.
    resistance : float
        Resistance to CLR slows spread of the virus.
    cost : int
        Cost associated with the plant.
    """
    grid: Tuple[int, int] = (0, 0)  # location of plant in grid cell
    plant: int = 0  # id of plant in grid cell
    infection: float = 0.0  # level of infection 0 < infection < 1
    infectivity: float = 0.0  # level of infectivity based on infection
    production: float = 1.0  # 0 < production < 1 modifies the output relative to max berry output based on infection level
    resistance: float = 1.0  # resistance to CLR slows spread of the virus
    cost: int = 100

    def progression(self) -> None:
        """
        Progress the infection level based on defined cutoffs and scaling factors.
        Caps infection at 1.
        """
        if 0 < self.infection < 1:
            for cutoff, scaling in zip(progression_cutoff, progression_scaling):
                if self.infection < cutoff * days:
                    self.infection += scaling * days * self.resistance
                    break
            else:
                self.infection += 20 * days * self.resistance
        if self.infection > 1:
            self.infection = 1.0

    def get_production(self) -> None:
        """
        Calculate the production of coffee berries based on infection level.
        Production decreases with higher infection.
        """
        self.production = (1 - 0.5 * self.infection) * max_production

    def define_infectivity(self) -> float:
        """
        Defines infectivity based on the infection level and a latency period.

        Returns
        -------
        float
            Updated infectivity value.
        """
        if self.infection < 20 * days:
            self.infectivity = 0.0
        else:
            self.infectivity = self.infection
        return self.infectivity


def get_harvest(myplants: List[Plant]) -> float:
    """
    Calculate the total coffee berries harvested based on plant production.

    Parameters
    ----------
    myplants : List[Plant]
        List of all Plant instances in the simulation.

    Returns
    -------
    float
        Total coffee berries harvested.
    """
    total_berries: float = 0.0
    for plant in myplants:
        total_berries += max_production * plant.production
    return total_berries


def weather_effects(day: int) -> List[bool]:
    """
    Define whether weather conditions are favorable for spreading infection on a given day.
    Returns three booleans indicating:
    1. Within-cell infection possibility.
    2. Adjacent cell infection possibility.
    3. Global infection possibility across clusters.

    Parameters
    ----------
    day : int
        Current day of the simulation.

    Returns
    -------
    List[bool]
        [within_cell, adjacent, global]
    """
    if day < 180:
        cell = random.uniform(0, 1) < weather_within_cell_dry
    else:
        cell = random.uniform(0, 1) < weather_within_cell_wet
    cluster = False
    grid = False

    # if it is, is weather ok to spread further to neighboring grids (small wind, normal conditions)
    if cell:
        cluster = random.uniform(0, 1) < weather_adj
        # if it is, is weather ok to spread to other clusters (e.g. wind and rain)
        if cluster and cell:
            grid = random.uniform(0, 1) < weather_cluster
            return [cell, cluster, grid]
        else:
            return [cell, cluster, grid]
    else:
        return [cell, cluster, grid]


def get_neighbors(grid: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Compute the list of 8-neighbors around a given grid cell.

    Parameters
    ----------
    grid : tuple
        (row, column) coordinates.

    Returns
    -------
    list of tuples
        Coordinates of the 8 surrounding cells.
    """
    possible: List[Tuple[int, int]] = [
        (grid[0] + 1, grid[1] + 1),
        (grid[0], grid[1] + 1),
        (grid[0] - 1, grid[1] + 1),
        (grid[0] - 1, grid[1]),
        (grid[0] - 1, grid[1] - 1),
        (grid[0], grid[1] - 1),
        (grid[0] + 1, grid[1] - 1),
        (grid[0] + 1, grid[1])
    ]
    return possible


def get_gridscore(gridsquare: Tuple[int, int], myplants: List[Plant]) -> float:
    """
    Calculate the total infectivity score of a given grid cell.

    Parameters
    ----------
    gridsquare : tuple
        Grid cell coordinates (row, column).
    myplants : List[Plant]
        List of all Plant instances in the simulation.

    Returns
    -------
    float
        Sum of infectivity values for all infected plants in the grid cell.
    """
    return sum(x.infectivity for x in myplants if x.grid == gridsquare)


def within_cell_infection(gridsquare: Tuple[int, int], myplants: List[Plant]) -> Tuple[Tuple[int, int], float]:
    """
    Determine if a healthy plant within the same cell gets infected based on infection score.

    Parameters
    ----------
    gridsquare : tuple
        Grid cell coordinates.
    myplants : List[Plant]
        List of all Plant instances in the simulation.

    Returns
    -------
    Tuple[Tuple[int, int], float]
        (Grid cell coordinates, infection score).
    """
    infection_score: float = get_gridscore(gridsquare, myplants)
    plants_in_cell_healthy: List[Plant] = [x for x in myplants if (x.infection < 0.001) and (x.grid == gridsquare)]
    if len(plants_in_cell_healthy) > 0:
        if infection_score < 0.4:
            pass
        else:
            plants_in_cell_healthy[0].infection = days
            pass
    return (gridsquare, infection_score)


def neighbor_cell_infection(gridscore: Tuple[Tuple[int, int], float], myplants: List[Plant]) -> None:
    """
    Infect one additional plant in an adjacent grid cell based on infection score.

    Parameters
    ----------
    gridscore : Tuple[Tuple[int, int], float]
        (Grid cell coordinates, infection score).
    myplants : List[Plant]
        List of all Plant instances in the simulation.
    """
    neighbors  = get_neighbors(gridscore[0])
    healthy_neighbors = [x for x in myplants if (x.grid in neighbors) and (x.infection < 0.0001)]
    a = max(1,random.randint(0, len(healthy_neighbors)))
    if gridscore[1] < 0.6 or len(healthy_neighbors)<1:
        pass
    elif random.uniform(0,1)< 0.8:
        healthy_neighbors[a-1].infection = days

def global_infection(grid_scores: List[Tuple[Tuple[int, int], float]], myplants: List[Plant]) -> None:
    """
    Spread infection globally across the landscape under extreme weather conditions.

    Parameters
    ----------
    grid_scores : List[Tuple[Tuple[int, int], float]]
        List of (grid cell, infection score).
    myplants : List[Plant]
        List of all Plant instances in the simulation.
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
        

def each_day(myplants: List[Plant], day: int) -> List[float]:
    """
    Control the simulation for a single day: progress infections, spread based on weather.

    Parameters
    ----------
    myplants : List[Plant]
        List of all Plant instances in the simulation.
    day : int
        Current day number.

    Returns
    -------
    List[float]
        [infectivity_score, infected_cells, infected_plants, day_number]
    """
    weather = weather_effects(day)
    inf_plants = [x for x in myplants if x.infection > 0.0001]
    [x.progression() for x in inf_plants]
    [x.define_infectivity() for x in inf_plants]
    if weather[0]:
        inf_grid = set([x.grid for x in inf_plants])
        grid_scores = []
        for i in inf_grid:
            grid_infection_score = within_cell_infection(i, myplants)
            grid_scores.append(grid_infection_score)
        if weather[1]:
            for i in grid_scores:
                neighbor_cell_infection(i, myplants)
            if weather[2]:
                global_infection(grid_scores, myplants)
    infectivity_score = sum([x.infectivity for x in myplants])
    infected_grid_cells = len(set(x.grid for x in myplants if x.infection > 0.001))
    infected_plants = len([x for x in myplants if x.infection > 0.001])
    results = [infectivity_score,infected_grid_cells,infected_plants,day]
    return results


def initial_infection(myplants: List[Plant]) -> None:
    """
    Randomly select one plant and one plant in an adjacent cell to become infected.

    Parameters
    ----------
    myplants : List[Plant]
        List of all Plant instances in the simulation.
    """
    a = random.randint(0,len(myplants))
    inf_plants_seed = myplants[a]
    inf_plants_seed.infection = days
    b = get_neighbors(inf_plants_seed.grid)
    c = random.randint(0,len(b)-1)
    neighbors = [x for x in myplants if x.grid in b]
    neighbors[c].infection = days

def save_intermediate_infected(myplants: List[Plant], landscape: pd.DataFrame, day: int, z: int) -> None:
    """
    Save intermediate infection maps to CSV at specified days (0, 120, 240, 360).

    Parameters
    ----------
    myplants : List[Plant]
        List of all Plant instances in the simulation.
    landscape : pd.DataFrame
        DataFrame representing the landscape grid.
    day : int
        Current day number.
    z : int
        Simulation run identifier.
    """
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
    print(f"Starting run {z}")
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
    
    plants =[]
    for i in cafe:
        for j in range(plants_per_cell):
            plants.append(Plant(grid = i, plant = j))
    
    # initialize infection
        
    initial_infection(plants)
    
    # Run code for each day       
    day = 0
    returns = []
    daily_results = []
    while day < 365:
        daily_results.append(each_day(plants, day))
        if day%120==0:
            save_intermediate_infected(plants, landscape, day, z)
            print(f"reached day {day}")
        day+=1
    
    # organize data
    # harvest berries
    day = 0
    
    def calculate_returns(myplants):
        [x.get_production() for x in myplants]
        return sum([x.production for x in myplants])
    
    coffee_cherries = np.floor(calculate_returns(plants))
    returns.append((coffee_cherries,runs))
    results = pd.DataFrame(daily_results)
    results.columns = ["infection_score", "infected_cells", 'infected_plants', 'day']
    results.to_csv(F"{datadir}/results-{z}-{proportions}-{cluster}.csv")

b = pd.DataFrame(returns)
b.to_csv(F"{datadir}/returns-{proportions}-{cluster}.csv")
