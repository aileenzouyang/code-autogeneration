#Welcome to the new era, where data analyts don't have to write a single line of code
#%%
# Import packages
import numpy as np
import pandas as pd
import os
raw_data = pd.read_csv(os.path.join(os.getcwd(), 'cars.csv'))
# Replace row 3, column Car from AMC Rebel SST to ery
raw_data.loc[3,'Car'] = 'ery'
# Dropping rows if it contains any NaN:
raw_data = raw_data.dropna()
# Include row if Cylinders == 4.0
raw_data = raw_data[(raw_data['Cylinders'] == 4.0)]
# Export final data
raw_data = raw_data.to_csv(os.path.join(os.getcwd(),'final.csv'))
# The End