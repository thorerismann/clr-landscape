# clr-landscape
Simple Coffee Leaf Rust model

This project was created for the graduate seminar in Economics of Biodiversity course at the University of Bern.

The goal of this project is to build a flexible model that can explore how changing likelihoods in CLR dispersal impact output, and how this can be related to both choice of inputs to increase coffee reistance and to changing weather patterns. This is accomplished with a flexible model that allows one to adjust the cost of each plant, its maximum berry production, its resistance to infection, and weather impacts on CLR propogation. This flexibility comes at a cost of model speed, particularly when higher levels of infection are "achieved".

The nlmpy package is used to generate a neutral landscape model of a coffee/forest matrix that is common for smallholder coffee farmers. Each coffee grid cell is assigned a number of coffee plants and infection randomly starts in two coffee plants in adjascent grid cells. The model runs for 365 days, at which point it is assumed the owner harvests the berries and uses fungicide to remove the CLR for the start of next year's growth.

The data folder contains the data from sample runs testing some parameter combinations to test the robustness of the model. The figures folder contains the figures needed to visualize this data.

See the main paper here: :)


Thi following packages are required:
- nlmpy
- numpy
- pandas
- seaborn

*Note: it is recomended to install numbpy and numpy via conda-forge channel prior to installing nlmpy as some of the package dependencies did not load correctly without this.*
