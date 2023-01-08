#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 00:05:25 2022

@author: tge
"""

import pandas as pd
import numpy as np
import scipy
import seaborn as sns
import matplotlib.pyplot as plt

# each grid has 
# set parameters for number of plants, branches, leaves
number_cells = 100

plants_per_cell = 100

branches_per_plant = 15

leaves_per_branch = 40

starting_age = 100

time = 0

leaf_status = {'healthy':0,'latent':1,'infected':2}

age_max = 250
age_inf_max = 120

# healthy leaf growth factor
alpha = 1

# latent leaf growth factor
beta = 0.7

# infected leaf growth factor
delta = 0.1

# index 0 = grid, index 1 = plant, index 2 = branch, index 3 = healthy/infected, index 4 = leaf-age
# make array of ones as placeholders
leaves = np.ones((number_cells,plants_per_cell,branches_per_plant,3,leaves_per_branch))
# set all infected, latent leaves to 0 days of age (none infected yet)
leaves[:,:,:,1] = 0
leaves[:,:,:,2] = 0

# set all healthy leaves to an age drawn from the uniform distribution between age_max and 1
leaves[:,:,:,0] = np.random.randint(1,age_max,size = (number_cells,plants_per_cell,branches_per_plant,leaves_per_branch))

#increment age of (infected + healthy) leaves by one day
leaves = leaves + 1

#increment time by 1
time = time + 1

# 4-7 week latency period in the field
benchmark_1 = 35
# spores are given off until day 90
benchmark_2 = 90
# dies from infection at day 150
benchmark_3 = 120

# daily progress in infection
clr_growth_dict = {'no-growth':0,'low-growth':1,'high-growth':2}
hg_1 = 1/50
hg_2 = 1/25
hg_0 = 0 

# daily spore production = lifetime number of spores divided by number of days in
# spore producitn period citation : https://www.sciencedirect.com/science/article/abs/pii/S0261219419303849
spore_dict = {'no-spore': 0, 'low-spore':1, 'high-spore':2}
spores_0 = 0
spores_1 = np.random.randint(low=300000,high = 750000)/55
spores_2 = np.random.randint(low=750000,high = 2000000)/55

# daily value that determines whether or not the spores have the proper conditions to germinate
# will be replaced by a climate-defined thing based on data
germ_dict = {'no-germ': 0, 'low-germ': 1, 'high-germ': 2}

germ_cond_wet = np.random.choice(a = (0,1,2),size= 182)
spore_cond_dry = np.random.choice(a = (0,1),size= 182)


def check_inf_age(leaves):
    return leaves[:,:,:,0] < age_inf_max

def check_healthy_age(leaves):
    return leaves[:,:,:,0] < age_max

def plant_prod(plant):
    inf_prod =  beta*leaves[:,:,:,0]
    healthy_prod = alpha*leaves[:,:,:,1]
    pass
    
def get_inf_prod(leaves):
    return alpha*leaves[:,:,:,0]
    

def remove_old(leaves):
    a = check_healthy_age(leaves)
    b = check_inf_age(leaves)
    pass
    
def make_leaves(l):
    a = get_inf_prod()
    pass
    
    


