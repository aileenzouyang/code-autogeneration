#Welcome to the new era, where data analyts don't have to write a single line of code
#%%
# Import packages
import numpy as np
import pandas as pd
import os
raw_data = pd.read_csv(os.path.join(os.getcwd(), 'Admission Data.csv'))
for parameter in ['Name of University', 'GPA']:
  raw_data[parameter].replace({'':''}, inplace = True)
