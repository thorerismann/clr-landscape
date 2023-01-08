#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 23:11:45 2022

@author: tge
"""

import numpy as np

#all parameters in the Table 1

# recruitment of healthy branches / day (assumed LOL)
delta_d = 6
delta_w = 8

# germ effectiveness
w_d = 0.045
w_w = 0.055

# rate at which a spore covered branch turns into a latent branch
spore_germ_rate_dry = 0.2
spore_germ_rate_wet = 0.4

# rate at which a latent branch turns into a sporulating branch / day
latent_days_dry = 30
theta_d = 1/latent_days_dry
latent_days_wet = 21
theta_w = 1/latent_days_wet

# branch mortality rate (other causes) / days
mu_d = 0.0134
mu_w = 0.0034
# berry production rate healthy / day
delta_s_d = 0
delta_s_w = 0.7

# berry production rate latent / day
delta_l_d = 0
delta_l_w = 0.5

# berry production rate infected  / day
delta_i_d = 0
delta_i_w = 0.3

# berry production rate infected  / day
delta_j_d = 0
delta_j_w = 0.05

#sporulation period duration
spore_days = 150
alpha = 1/spore_days

# berry mortality rate / days (assumed)
mu_b = 0.0021

# disease mortality rate / day (assumed)
d = 0.056

# deposition rate ( in days)
v = 0.09

# diffusion coefficient ( m² / day)
e = 5000

# rate of production of spores ( in first simulation)
y = 1.5

# mortality rate of urediniospores (days)
mu_u = 0.015

# seasons ( cameroon seasons, just start with dry then wet follows)
dry = np.arange(0,145)
wet = np.arange(146,365)

# starting values
healthy = 100
latent = 0
infected = 0
meters = 100
spores = 2000*(np.sin((np.pi/100)))**2
# x is one square meter (?)
x = np.ones(meters) 



def each_time(healthy,latent,infected,dead,berries,spores,time):
    if time in dry:
        healthy_ = delta_d - ((w_d*v*spores)/sum([healthy,latent,infected,dead]))*healthy - mu_d*healthy
        latent_ = ((w_d*v*spores)/sum([healthy,latent,infected,dead]))*healthy - (theta_d + mu_d)*latent
        infected_ = theta_d*latent - (alpha + d + mu_d)*infected
        dead_ = alpha*latent -mu_d*dead
        spores_ = e*spores + y*infected - (v + mu_u)*spores
    
    else:
        berries_ = delta_s_w*healthy + delta_l_w*latent + delta_i_w*infected + delta_j_w*dead - mu_b*berries
        healthy_ = delta_w - ((w_w*v*spores)/sum([healthy,latent,infected,dead]))*healthy - mu_w*healthy
        latent_ = ((w_w*v*spores)/sum([healthy,latent,infected,dead]))*healthy - (theta_w + mu_w)*latent
        infected_ = theta_w*latent - (alpha + d + mu_w)*infected
        dead_ = alpha*latent -mu_w*dead
        spores_ = spores + 
        if time == 365: 
            harvested = berries
        
time = 365
def the_function():
    np.sum()
    
    each_time(,time)
    return y + starting_branches
















