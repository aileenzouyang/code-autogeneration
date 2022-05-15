#Welcome to the new era, where data analyts don't have to write a single line of code
#%%
# Import packages
import numpy as np
import pandas as pd
import os
raw_data = pd.read_csv(os.path.join(os.getcwd(), cars.csv))
# Replace row 2, column Car from Plymouth Satellite to Bread
raw_data.loc[2,'Car'] = 'Bread'
# Dropping rows if it contains any NaN:
raw_data = raw_data.dropna()
# Exclude row if Origin contains Europe
raw_data = raw_data[~raw_data['Origin'].str.contains('Europe') ]
# Calculatiion 
raw_data['C2']=raw_data['Cylinders']*2 
# Export final data
raw_data = raw_data.to_csv(os.path.join(os.getcwd(),'final.csv'))
# The End