#Welcome to the new era, where data analyts don't have to write a single line of code
#%%
# Import packages
import numpy as np
import pandas as pd
import os
raw_data = pd.read_csv(os.path.join(os.getcwd(), 'cars.csv'))
# Replace row 0, column Displacement from 307.0 to 0.0
raw_data.loc[0,'Displacement'] = 0.0
# Replace row 0, column Car from Chevrolet Chevelle Malibu to rgsg
raw_data.loc[0,'Car'] = 'rgsg'
# Export final data
raw_data = raw_data.to_csv(os.path.join(os.getcwd(),'final.csv'))
# The End