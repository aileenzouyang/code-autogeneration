import pandas as pd
import numpy as np
import os

def script_generation_from_equation(script):

    execution_script = script.replace("raw_data", "st.session_state.raw_data")
    
    return execution_script


