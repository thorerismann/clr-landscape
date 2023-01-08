# -*- coding: utf-8 -*-

from dataclasses import dataclass
import pandas as pd
import numpy as np
import scipy
import random
from itertools import chain
import seaborn as sns


# what is the size of a typical smallholder coffee plantation? (how many plants)

# set parameters for number of plants, branches, leaves
plants_per_cell_min = 8
plants_per_cell_max = 12

branches_per_plant_min = 15
branches_per_plant_max = 20

leaves_per_branch_min = 20
leaves_per_branch_max = 30

# leaf ages
age_min = 0
age_max = 300

# varieties - now only "susc" for susceptible...

# production values
prod_factor = 1
berry_cost = 70
leaf_cost = 80
# branch cost = 1000

## virus parameters

# virus growth benchmarks (days)

# 4-7 week latency period in the field
benchmark_1 = 35
# spores are given off
benchmark_2 = 120
# dies from infection at day 150
benchmark_3 = 150

# virus spread to branches, plants, other plants (P success each infected leaf to each healthy leaf)
clr_b = 0.001
clr_p = 0.0001
clr_g = 0.00001

# chance of germination of spores
# modified significantly with climate / temp / humid / rainfall
germ_chance = 0.5

# leaf ages determine its health status 
# for now just productivity, will later help w/ infection
age_1 = 50
age_2 = 250
age_3 = 350

# make grid
grid_size = 2
x = np.arange(0,grid_size)
y = np.arange(0,grid_size)
tuples = []
for i in x:
    for j in y:
        tuples.append((i,j))
grid = tuples



lstatus = {'healthy':0,'latent':1,'spores':2,'dead':3}

# productivity of leaf goes from 0 to 10
#leaf.prod

@dataclass
class Leaf:
    """
    The leaf class is the basic element of infection, leaf and berry production
    """
    grid: tuple = (0,0)
    plant: int = 0
    branch: int = 0
    leaf: int = 0
    age: int = 0
    status: int = 0
    prod: int = 10
    idays: int = 0
    clr_germs: int = 0
    variety: str = 'susc'
    
    def aging(self):
        """
        Each turn the leaf ages by one day. Its base productivity is determined by its age.
        """
        if self.status < 3:
            self.age+=1
            if self.age > age_3:
                self.status = 3
            if self.age > age_2:
                self.prod = 7
            elif self.age > age_1:
                self.prod = 10
            else:
                self.prod = 5
        
    
    def clr_progression(self):
        """
        Each turn the coffee leaf rust infection in the leaf advances by one day and reduces leaf productivity
        """
        if (self.status == 1)|(self.status==2):
            self.idays += 1
            if self.idays < benchmark_1:
                self.prod = max(self.prod-2,0)
                self.status = 1
            elif self.idays < benchmark_2:
                self.prod = max(self.prod-5,0)
                self.status = 2
            elif self.idays < benchmark_3:
                self.prod = max(self.prod-8,0)
                self.status = 2
            else:
                self.status = 3
    
    def germ_rust(self):
        """
        Each turn the rust spores can germinate on the leaf
        """
        if self.status == 0:
            if self.clr_germs > 0:
                if np.random.binomial(self.clr_germs,germ_chance) > 0:
                    self.status = 1
                    self.idays = 1
            
    def leaf_death(self):
        """
        Each turn leaves that age past 350 years old or are infected for more than 150 days die.
        """
        if (self.idays >=benchmark_3):
            self.status = 3
        elif (self.age >= age_3):
            self.status = 3
        
            
# initiate leaves
mylist =[]
for i in grid:
    plants = random.randint(plants_per_cell_min,plants_per_cell_max)
    for j in range(plants):
        branches = random.randint(branches_per_plant_min,branches_per_plant_max)
        for k in range(branches):
            leaves = random.randint(leaves_per_branch_min,leaves_per_branch_max)
            for l in range(leaves):
                mylist.append(Leaf(grid=i,plant=j,branch=k,leaf=l,age=random.randint(age_min,age_max),status=0,prod=10,idays=0,clr_germs=0,variety = 'susc'))              
al = mylist       


@dataclass
class Branch:
    """
    Branches are where production of berries and leaves are defined and where the infection operations occur
    """
    leaves: list
    grid: tuple = (0,0)
    plant: int = 0
    branch: int = 0
    berries: int = 0
    leaf_prod: int = 0
    berry_prod: int = 0
    prod_factor: int = 0
    branch_status: int = 0
    inf_leaves: int = 0
    
    def production_l(self):
        """
        leaf production function
        """
        for i in self.leaves:
            if i.status<3:
                self.leaf_prod = self.leaf_prod + 0.1*getattr(i,'prod')
        a = int(np.floor(self.leaf_prod/leaf_cost))
        leaf_count = len(self.leaves)
        if a>0:
            for i in range(a):
                newleaf = Leaf(grid = self.grid,plant = self.plant, branch = self.branch,status = 0,leaf = leaf_count+a,age=0,prod=8,idays=0,clr_germs=0,variety='susc')
                self.leaves.append(newleaf)
                al.append(newleaf)
                self.leaf_prod = self.leaf_prod - a*leaf_cost
                
    def production_b(self):
        """
        berry production function
        """
        for i in self.leaves:
            if i.status <3:
                self.berry_prod = self.berry_prod + 0.1*getattr(i,'prod')
        a = int(np.floor(self.berry_prod/berry_cost))
        self.berries = self.berries + a
        self.berry_prod = self.berry_prod - a*berry_cost
    
    def branch_status(self):
        """
        update branch status (healthy infected dead)
        """
        pass
    
    def get_inf_leaves(self):
        infected = [x for x in self.leaves if x.status == 1]
        self.inf_leaves = len(infected)
    
    def infection(self):
        """
        Each turn the healthy leaves on the branch can get a spore from an infected leaf on the same branch, same plant or same grid cell.
        """
        # first infected leaves on the branch
        infected_branch = [x for x in self.leaves if x.status == 1]
        infected = len(infected_branch)
        healthy = [x for x in self.leaves if x.status == 0]
        if infected > 0:
            for i in healthy:
                i.clr_germs = np.random.binomial(infected,clr_b)
        
        # infected leaves on same plant different branch
        my_infected_plant = [x for x in ap if (x.grid == self.grid) & (x.plant ==self.plant)]
        infected_leaves_plant = my_infected_plant[0].infected
        infected = infected_leaves_plant - len(infected_branch)
        if infected > 0:
            for i in healthy:
                i.clr_germs = np.random.binomial(infected,clr_p) 
        
        # infected leaves on different plant same grid
        infected_grid = [x for x in ag if (x.grid == self.grid)]
        infected_leaves_grid = infected_grid[0].infected
        infected = infected_leaves_grid - infected_leaves_plant
        if infected > 0:
            for i in healthy:
                i.clr_germs = np.random.binomial(infected,clr_g) 

# create branch objects            
mylist = []
for i in grid:
    grid_ = [x for x in al if getattr(x,'grid')== i]
    a = set([x.plant for x in grid_])
    for j in a:
        plant_ = [x for x in grid_ if getattr(x,'plant')== j]
        b = set([x.branch for x in plant_])
        for k in b:
            branch_ = [x for x in plant_ if getattr(x,'branch')== k]
            mylist.append(Branch(leaves=branch_,grid=i,plant=j,branch=k,berries=0,leaf_prod=0,berry_prod=0,prod_factor=1,branch_status=0,inf_leaves=0))
ab = mylist    

@dataclass
class Plant:
    """
    The Plant class is where the properties of the leafs and branches are controlled
    The definition of the plant variety, its health status, climate impacts, occur here
    Treatments also occur here
    """
    branches: list
    grid: tuple
    plant: int
    infected: int    
    variety: str
    
    def get_inf_leaves(self):
        inf_leaves = 0
        for i in self.branches:
            inf_leaves += i.inf_leaves
        self.infected = inf_leaves
    
    def some_climate(self):
        """
        Modify the leaves/branches assigned to each plant based on climate factors
        """
        pass
    
    def some_health_status(self):
        """
        Modify the leaves/branches assigned to each plant based on plant health status
        """
        pass
    
    def variety_defs(self):
        """
        modify the leaves assigned to this plant based on the variety
        """
        pass
    
@dataclass
class Grid:
    """This class is primarily functional - could be removed if a 
    distance function is used."""
    plants: list
    grid: tuple
    infected: int
    
    def get_inf_leaves(self):
        inf_leaves = 0
        for i in self.plants:
            inf_leaves += i.infected
        self.infected = inf_leaves

# make plant objects

mylist = []
for i in grid:
    grid_ = [x for x in ab if getattr(x,'grid')== i]
    plants_ = set([x.plant for x in grid_])
    for j in plants_:
        branches_ = [x for x in grid_ if getattr(x,'plant')== j]
        mylist.append(Plant(branches=branches_,grid=i,plant=j,infected = 0,variety = 'susc'))
ap = mylist

# make grid objects

mylist = []
for i in grid:
    plants_ = [x for x in ap if getattr(x,'grid')==i]
    mylist.append(Grid(plants = plants_,grid = i,infected = 0))
ag = mylist


def make_frame_branches(branches,time):
    """
    This function summarizes the key branch level values for each time step as a dictionary.
    Used for data output
    """
    list_dict = []
    for i in branches:
        dead =  len([x for x in i.leaves if x.status == 3])
        infected = len([x for x in i.leaves if (x.status == 1) | (x.status ==2)])
        healthy = len([x for x in i.leaves if x.status == 0])
        list_dict.append({'dead':dead,'healthy':healthy,'infected':infected,
                          'plant':i.plant,'branch' : i.branch,'grid':i.grid,'berries' : i.berries,'time' : time})
    return list_dict
    


# start off with 2 infected leaves in 3 of 4 grid cells
toinfect = [x for x in al if (x.plant == 2) & (x.branch == 3) & ((x.leaf == 2) | (x.leaf == 3))&((x.grid == (0,0)) | (x.grid == (0,1)) | (x.grid == (1,1)))]
for i in toinfect:
    i.status = 1
    i.idays =1

# run code for 250 days
my_dict_list = []
time = 0
while time<250:
    [x.aging() for x in al]
    [x.clr_progression() for x in al]
    [x.leaf_death() for x in al]
    [x.get_inf_leaves() for x in ab]
    [x.get_inf_leaves() for x in ap]
    [x.get_inf_leaves() for x in ag]
    [x.production_l() for x in ab]
    [x.production_b() for x in ab]
    [x.germ_rust() for x in al]
    [x.infection() for x in ab]
    my_dict_list.append(make_frame_branches(ab,time))
    time+=1


# organize the data frame
df = pd.DataFrame(list(chain.from_iterable(my_dict_list)))
df.plant = df.plant.astype(str)
mylist = ["".join(str(x)) for x in df.grid]
mylist = [x[1]+x[4] for x in mylist]
df.grid = mylist
df['id_no'] = df.grid + df.plant
df.set_index('id_no',inplace=True,drop=True)
grouped_tg = df.groupby(['time','grid']).agg({'healthy':'mean','dead':'mean','infected':'mean','berries':'mean'})
grouped_tg.reset_index(inplace=True,drop=False)

#df.to_csv("branch_level_data.csv",sep=';')
#grouped_tg.to_csv("grouped_data_for_charts.csv",sep=';')

#sns.lineplot(data = grouped_tg,x = grouped_tg.time,y = grouped_tg.berries,hue=grouped_tg.grid)
#sns.lineplot(data = grouped_tg,x = grouped_tg.time,y = grouped_tg.infected,hue=grouped_tg.grid)
#sns.lineplot(data = grouped_tg,x = grouped_tg.time,y = grouped_tg.healthy,hue=grouped_tg.grid)

