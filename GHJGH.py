#Welcome to the new era, where data analyts don't have to write a single line of code
#%%
# Import packages
import numpy as np
import pandas as pd
import os
raw_data = pd.read_csv(os.path.join(os.getcwd(), 'cars.csv'))
# Dropping rows if it contains any NaN:
raw_data = raw_data.dropna()
# Export final data
raw_data = raw_data.to_csv(os.path.join(os.getcwd(),'final.csv'))
# The End