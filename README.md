# CLR-Landscape Model

**Simple Coffee Leaf Rust (CLR) Model**  
*Created for the graduate seminar in Economics of Biodiversity at the University of Bern.*

This project simulates the spread of Coffee Leaf Rust (CLR) across a patchwork landscape of coffee and non-coffee cells. It allows the user to explore how weather patterns and plant resistance parameters affect infection rates and final coffee yields.

## Overview

1. **Neutral Landscape Generation**  
   Uses the `nlmpy` package to create a patchwork of coffee (True) and non-coffee (False) cells in a grid.  
2. **Plant and Infection Dynamics**  
   Each coffee cell hosts a specified number of coffee plants. An initial infection starts in two adjacent coffee plants. The model then progresses day by day, allowing infection to spread within and between cells based on weather conditions and plant parameters.  
3. **Harvest and Returns**  
   After 365 days, the model calculates the total coffee berry yield and writes outputs (including intermediate infection maps and daily infection stats) to the `data/` directory.

## Required Packages

- **nlmpy**
- **numpy**
- **pandas**
- **seaborn** (recommended for plotting results)
- **numba** (optional, but recommended to optimize some dependencies)

> **Note:** It is often helpful to install `numba` and `numpy` via the `conda-forge` channel prior to installing `nlmpy`, because some dependencies may not load correctly otherwise.

## Usage

1. **Install Dependencies**  
   - Recommended approach (e.g., via Conda):  
     ```bash
     conda create -n clr_env python=3.9 -y
     conda activate clr_env
     conda install -c conda-forge numpy numba
     pip install nlmpy pandas seaborn
     ```
2. **Run the Script**  
   - Place this script in a directory with a `data/` folder (for saving outputs).
   - Execute:
     ```bash
     python clr_landscape.py
     ```
   - Results (CSV files for daily infection stats and final returns) will appear in the `data/` folder.

3. **Analyze and Plot**  
   - Use `seaborn` or any other plotting library to visualize outputs in Jupyter notebooks or Python scripts.
   - Sample figures can be found in the `figures/` folder.

## Main Paper

A more detailed discussion of the model and results is in the accompanying paper in this repository.

---
