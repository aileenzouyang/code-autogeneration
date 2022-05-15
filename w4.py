#Welcome to the new era, where data analyts don't have to write a single line of code
#%%
# Import packages
import numpy as np
import pandas as pd
import os
raw_data = pd.read_csv(os.path.join(os.getcwd(), 'cars.csv'))
# Replace row 1, column Car from Buick Skylark 320 to wer
raw_data.loc[1,'Car'] = 'wer'
# Dropping rows if it contains any NaN:
raw_data = raw_data.dropna()
# Exclude row if MPG >= 15.0
raw_data = raw_data[~(raw_data['MPG'] >= 15.0)]
# Calculatiion 
raw_data['mode']=raw_data['Cylinders']>2 
# Export final data
raw_data = raw_data.to_csv(os.path.join(os.getcwd(),'final.csv'))
# The End