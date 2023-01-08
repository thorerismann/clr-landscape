#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 02:05:31 2022

@author: tge
"""

import pandas as pd

# search terms used
s1 = "coffee leaf rust model"
s2 = "hemileia vastatrix model"
s3 = "hemileia vastatrix modelling"
s4 = "coffee leaf rust modelling"
s5 = "coffee leaf rust prediction"
s6 = "coffea disease model"
s7 = "coffea rust model"

# load in search terms
s1_ = pd.read_excel("/home/tge/dev/clr-model/Coffee-Leaf-Rust/data/search-data/search1.xls")
s2_ = pd.read_excel("/home/tge/dev/clr-model/Coffee-Leaf-Rust/data/search-data/search2.xls")
s3_ = pd.read_excel("/home/tge/dev/clr-model/Coffee-Leaf-Rust/data/search-data/search3.xls")
s4_ = pd.read_excel("/home/tge/dev/clr-model/Coffee-Leaf-Rust/data/search-data/search4.xls")
s5_ = pd.read_excel("/home/tge/dev/clr-model/Coffee-Leaf-Rust/data/search-data/search5.xls")
s6_ = pd.read_excel("/home/tge/dev/clr-model/Coffee-Leaf-Rust/data/search-data/search6.xls")
s7_ = pd.read_excel("/home/tge/dev/clr-model/Coffee-Leaf-Rust/data/search-data/search7.xls")
# combine
searches = pd.concat([s1_,s2_,s3_,s4_,s5_,s6_,s7_],axis = 0)
# filter for useful columns and unique results
searches = searches [["Authors","Publication Type","Article Title","DOI","Abstract","Source Title","Publication Year"]]
searches.drop_duplicates(inplace=True)

# export as .csv to filter manually
searches.to_csv("all_searches.csv")

# reimport csv

# excluded from search: 
# genetics, identification of clr via machine vision, human health impact of coffee, other dieseases (e.g. coffee berry borer, brown leaf spot), pure climate modelling/downscaling, pure economic modelling/downscaling

# papers to read
