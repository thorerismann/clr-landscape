#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 02:00:13 2022

@author: tge
"""

import pandas as pd
import numpy as np
import scipy
import seaborn as sns
import matplotlib.pyplot as plt
from dataclasses import dataclass
from random import Random as rand


@dataclass
class Plant:
    """
    The plant is the basic element of infection, leaf and berry production
    """
    grid: tuple = (0,0)
    plant_id: int = 0
    leaves: pd.DataFrame = pd.DataFrame(columns=['age','inf_days'])
    leaf_counter: int = 0
    bad_days: int = 0
    age: int = 400
    prod: int = 10
    variety: int = 0
    berries: int = 0
    
    def aging(self):
        """
        Each turn the plant and leaves age by one day.
        """
        # plant age
        self.age += 1
        
        #leaf age
        a = self.leaves
        a.age = a.age+1
        self.leaves = a
    
    def clr_progression(self):
        """
        Each turn the coffee leaf rust infection in the leaf advances by one day
        """
        a = self.leaves
        def check_inf(x):
            if x == 0:
                return 0
            else:
                return x+1
        a.inf_days = a.inf_days.apply(lambda x: check_inf(x))
        self.leaves = a
        
    def leaf_death(self):
        """
        Each turn leaves die as they age or are infected too long
        """
        a = self.leaves
        b = a[(a.age<350) & (a.inf_age < 120)]
        self.leaves = b
    def death(self):
        """
        If too many bad days happen in a row leaves and then berries start to die.
        Plant first lets leaves die then lets berries die. Leaves are removed starting from the first row
        """
        if len(self.leaves) > 0:
            if self.bad_days <= 10:
                pass
            elif (self.bad_days >10) & (self.bad_days <= 20):
                self.leaves = self.leaves.iloc[1:,:]
            elif (self.bad_days >20) & (self.bad_days <= 30):
                self.leaves = self.leaves.iloc[2:,:]
            else:
                self.leaves = self.leaves.iloc[3:,:]
        else:
            if self.bad_days <= 10:
                pass
            elif (self.bad_days >10) & (self.bad_days <= 20):
                self.berries = self.berris-1
            elif (self.bad_days >20) & (self.bad_days <= 30):
                self.berries = self.berries-2
            else:
                self.berries = self.beries-3
        
            
            
            
            

inf_status = [0]*500
age = list(np.random.randint(0,350,500))
leaf_info = list(zip(age,inf_status))
leafs = pd.DataFrame(leaf_info,columns = ['age','inf_days'])

myplant = Plant(leaves = leafs)

def production(plant):
    """
    production currently dependent only on health/infected status of leaves
    """
    ls = plant.leaves
    healthy = len(ls[ls.inf_days == 0])
    latent = len(ls[(ls.inf_days <= 20) & (ls.inf_days > 0)])
    inf_1 = len(ls[(ls.inf_days <= 90)&(ls.inf_days>20)])
    inf_2 = len(ls[ls.inf_days > 90])
    production = (healthy + 0.8*latent+ 0.6*inf_1+0.2*inf_2)*plant.prod
    return production

# berry ratio for starting
br = (2,1,0.5)
# daily cost of each berry
bc = 1
# cost of new leaf
lc = 10

def set_berries(plant,br):
    """
    Set the number of berries for the plant for the season based on the number of healthy, latent infected leaves.
    br = berry to leaf ratio tuple
    neeed to add the age variable in to account for biannual cycle + age effect
    """
    a = plant.leaves
    plant.berries = br[0]*len(a[a.inf_days < 1]) + br[1]*len(a[(a.inf_days > 1) & (a.inf_days < 31 )])+ +br[2]*len(a[a.inf_days > 30])

def excess_production(plant,bc):
    """
    Each day the berries cost a certain amount to maintain. If the cost is exceeded the excess is passed to leaf production. If the cost is not exceeded, berry growth halts for the day. If it halts for 5 consecutive days the berries start to fall from the tree
    """
    a = production(plant) - plant.berries*bc
    if a < 0:
        plant.bad_days = plant.bad_days +1
    return production(plant) - plant.berries*bc



def grow_leaves(excess,plant,bc,lc):
    if excess > 0:
        new_leaves = int(np.floor((plant.leaf_counter + excess)/lc))
        plant.leaf_counter = plant.leaf_counter + int((plant.leaf_counter + excess)%lc)
        while new_leaves >0:
            plant.leaves.append([1,0])
            new_leaves-1
        plant.leaf_counter = plant.leaf_counter + new_leaves
    else:
        pass

excess_prod = excess_production(myplant,bc)
grow_leaves(excess_prod,myplant,bc,lc)

def adjust_productivity_climate(self,climate = None):
    """
    adjust productivity based on age and infection
    """
    pass
    
def pruning():
    pass
def treatment():
    pass

# if wet season


# build year



















