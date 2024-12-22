#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 14:33:05 2023

@author: tge
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import seaborn as sns
from pathlib import Path

datadir = Path.cwd() / 'data'
figdir = Path.cwd() / 'figures'

proportions_used = [[0.1,0.9],[0.25,0.75],[0.4,0.6]]
cluster_used = [0.2,0.3,0.4]

# plot run 5 of cluster = 0.3,
# proportions_used = [0.25]

fig1 = np.genfromtxt(F'{datadir}/map-0-5-[0.25, 0.75]-0.3.csv', delimiter=',')
fig2 = np.genfromtxt(F'{datadir}/map-120-5-[0.25, 0.75]-0.3.csv', delimiter=',')
fig3 = np.genfromtxt(F'{datadir}/map-240-5-[0.25, 0.75]-0.3.csv', delimiter=',')
fig4 = np.genfromtxt(F'{datadir}/map-360-5-[0.25, 0.75]-0.3.csv', delimiter=',')

# plot run 5
# Make classified colour map
cmapClas = mpl.colors.ListedColormap(['#8dd3c7', '#ffffb3', '#bebada'])
bounds=[-1,0.9,1.9,2.9]
norm = mpl.colors.BoundaryNorm(bounds, cmapClas.N)

for i in proportions_used:
    for j in cluster_used:
        for z in range(0,10):
            fig1 = np.genfromtxt(F'{datadir}/map-0-{z}-{i}-{j}.csv', delimiter=',')
            fig2 = np.genfromtxt(F'{datadir}/map-120-{z}-{i}-{j}.csv', delimiter=',')
            fig3 = np.genfromtxt(F'{datadir}/map-240-{z}-{i}-{j}.csv', delimiter=',')
            fig4 = np.genfromtxt(F'{datadir}/map-360-{z}-{i}-{j}.csv', delimiter=',')
            figs = [fig1,fig2,fig3,fig4]
            fig, axs = plt.subplots(4, 1)
            axs[0].imshow(figs[0], interpolation='none', aspect=1, cmap=cmapClas, norm=norm)
            axs[0].set_yticklabels([])
            axs[0].set_xticklabels([])
            axs[0].set_title(F'{i}, {j}')
            axs[1].imshow(figs[1], interpolation='none', aspect=1, cmap=cmapClas, norm=norm)
            axs[1].set_yticklabels([])
            axs[1].set_xticklabels([])
            axs[2].imshow(figs[2], interpolation='none', aspect=1, cmap=cmapClas, norm=norm)
            axs[2].set_yticklabels([])
            axs[2].set_xticklabels([])
            axs[3].imshow(figs[3], interpolation='none', aspect=1, cmap=cmapClas, norm=norm)
            axs[3].set_yticklabels([])
            axs[3].set_xticklabels([])
            plt.savefig(F'{figdir}/infection_progression_{z}_{i}_{j}.png')
            plt.show()

# read in daily data for all runs
for z in proportions_used:
    for k in cluster_used:
        for i in range(0,10):
            a = pd.read_csv(F"{datadir}/results-{i}-{z}-{k}.csv")
            a.set_index("day",inplace=True)
            a = a[['infection_score', 'infected_cells', 'infected_plants']]
            a["run"] = i
            if i == 0:
                final = a
            else:
                final = pd.concat([final,a],axis = 0)

        sns.lineplot(data = final, x = "day",y = "infected_cells",hue = "run")
        plt.title(F"{z}, {k}")
        plt.savefig(F'{figdir}/infected-cells-{z}-{k}.png')
        plt.show()
        sns.lineplot(data = final, x= "day",y = "infection_score",hue = "run")
        plt.title(F"{z}, {k}")
        plt.savefig(F'{figdir}/infection-score-{z}-{k}.png')
        plt.show()
        sns.lineplot(data = final, x= "day",y = "infected_plants",hue = 'run')
        plt.title(F"{z}, {k}")
        plt.savefig(F'{figdir}/infected-plants-{z}-{k}.png')
        plt.show()



mylist = []
for i in proportions_used:
    for j in cluster_used:
        for z in range(0,10):
            data = np.genfromtxt(F'{datadir}/map-360-{z}-{i}-{j}.csv', delimiter=',')
            unique, counts = np.unique(data, return_counts=True)
            mydata = dict(zip(unique, counts))
            trees = mydata[0]-2
            uninfected = mydata[1]-2
            infected = mydata[2]-2
            total_cafe = infected+uninfected
            infected_percent = infected/total_cafe
            uninfected_percent = uninfected/total_cafe
            tree_percent = trees/1600
            total_cafe_percent = total_cafe/1600
            mylist.append([trees,uninfected,infected,total_cafe,infected_percent,uninfected_percent,tree_percent,total_cafe_percent,i[0],j,z])

df = pd.DataFrame(mylist)
df.columns = ["trees","uninfected","infected","total_cafe","infected_percent","uninfected_percent","tree_percent","total_cafe_percent","proportions","clustering","run"]
grouped_mean = df.groupby(["proportions", "clustering"])[["uninfected_percent", "total_cafe_percent"]].mean().reset_index()
grouped_min = df.groupby(["proportions", "clustering"])[["uninfected_percent"]].min().reset_index()
grouped_max = df.groupby(["proportions", "clustering"])[["uninfected_percent"]].max().reset_index()

bottom = df.sort_values("uninfected_percent", ascending=True).head(10)
bottom = (bottom[["uninfected_percent","tree_percent","infected_percent","proportions","clustering"]]).round(2)
bottom.to_csv(F'{datadir}/bottom.csv')
top = df.sort_values("uninfected_percent", ascending=False).head(10)
top = (top[["uninfected_percent","tree_percent","infected_percent","proportions","clustering"]]).round(2)
top.to_csv(F'{datadir}/top.csv')

