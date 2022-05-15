#Welcome to the new era, where data analyts don't have to write a single line of code
#%%
# Import packages
import numpy as np
import pandas as pd
import os
raw_data = pd.read_csv(os.path.join(os.getcwd(), 'cars.csv'))
# Replace row 0, column Car from Chevrolet Chevelle Malibu to lalala
raw_data.loc[0,'Car'] = 'lalala'
# Export final data
raw_data = raw_data.to_csv(os.path.join(os.getcwd(),'final.csv'))
# The End