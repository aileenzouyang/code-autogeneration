#%%
# Import packages
import streamlit as st
import pandas as pd
import numpy as np
import os
import re
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from script_generation import *
#https://towardsdatascience.com/make-dataframes-interactive-in-streamlit-c3d0c4f84ccb

raw_data = pd.read_csv(os.path.join(os.getcwd(),'input','cars.csv'))
#%%
# Initialize a session
if "filename" not in st.session_state:
    st.session_state.filename = "test.py"
    st.session_state.save_path = os.path.join(os.getcwd(),st.session_state.filename)
    st.session_state.raw_data = pd.read_csv(os.path.join(os.getcwd(),'input','cars.csv'))
    st.session_state.file = open(st.session_state.save_path,"w")
    st.session_state.file.write("#Welcome to the new era, where data analyts don't have to write a single line of code\n")
    st.session_state.file.write("#%%\n")
    st.session_state.file.write("# Import packages\n")
    st.session_state.file.write("import numpy as np\n")
    st.session_state.file.write("import pandas as pd\n")
    st.session_state.file.write("import os\n")
    st.session_state.file.write("raw_data = pd.read_csv(os.path.join(os.getcwd(),'input','cars.csv'))\n")
    
#%%
########################################################
# Sidebar section
########################################################
sb = st.sidebar # defining the sidebar

sb.markdown("🛰️ **Navigation**")

page_names = ["🏠 Home", 
            "🧽 Data Cleaning - Manual Edits",
            "🧽 Data Cleaning - Conditional Selection",
            "🧮 Calculation",
            "🪄 Export"]

page = sb.radio("", page_names, index=0)

if page == "🏠 Home":

    st.subheader("Awesome MVP")
    st.subheader("What is Awesome MVP?")
    lorem_ipsum = "Awesome MVP autogenerates python script based on user requirement. \
        In this example we will be curating, summarizing, analyzing, and visualizing the folloing data table."

    st.markdown(lorem_ipsum, unsafe_allow_html=True)

    gb = GridOptionsBuilder.from_dataframe(st.session_state.raw_data)
    gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
    gb.configure_side_bar() #Add a sidebar
    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
    gridOptions = gb.build()

    AgGrid(raw_data)

elif page == "🧽 Data Cleaning - Manual Edits":
    st.subheader("Awesome MVP")
    st.subheader("Data Cleaning")


    # Ask user if they want to create an if statement
    row_ind = st.selectbox("Replace row: ",(st.session_state.raw_data.index))      
    col_ind = st.selectbox("column ",(st.session_state.raw_data.columns))  

    original_value = st.session_state.raw_data.loc[row_ind,col_ind]
    new_value = string = st.text_input("with ")
    confirm = st.button("Generate")

    if confirm: 
        st.session_state.file.write("# Replace row {}, column {} from {} to {}\n".format(row_ind, col_ind, original_value, new_value))
        st.session_state.file.write("raw_data.loc[{},'{}'] = '{}'\n".format(row_ind, col_ind, new_value))
        st.write("Success!")
        st.session_state.raw_data.loc[row_ind,col_ind] = new_value
        confirm = False

    AgGrid(st.session_state.raw_data)

elif page == "🧽 Data Cleaning - Conditional Selection":

    st.subheader("Awesome MVP")
    st.subheader("Data Cleaning")

    # Ask user if they want to remove NaN
    q1 = "Would you like to remove the NaNs?"
    removena = st.button(q1)

    if removena: 
        st.session_state.file.write("# Dropping rows if it contains any NaN:\n")
        st.session_state.file.write("raw_data = raw_data.dropna()\n")
        st.session_state.raw_data = st.session_state.raw_data.dropna()

    # Ask user if they want to create an if statement
    action_option = st.selectbox("Action: ",("Include", "Exclude"))        
    print(action_option)
    print(action_option == "Include")

    column_option = st.selectbox("row if ",(st.session_state.raw_data.columns))
    string = st.text_input("contains: ")
    confirm = st.button("Generate")

    if confirm: 
        st.session_state.file.write("# {} row if {} contains {}\n".format(action_option, column_option, string))
        if action_option == "Include": 
            st.session_state.file.write("raw_data = raw_data[{}raw_data['{}'].str.contains('{}') ]\n".format("", column_option,string))
            st.session_state.raw_data = st.session_state.raw_data[st.session_state.raw_data[column_option].str.contains(string)]
        if action_option == "Exclude": 
            st.session_state.file.write("raw_data = raw_data[{}raw_data['{}'].str.contains('{}') ]\n".format("~", column_option,string))
            st.session_state.raw_data = st.session_state.raw_data[~st.session_state.raw_data[column_option].str.contains(string)]

        st.write("Success!")
        confirm = False
    AgGrid(st.session_state.raw_data)

elif page == "🧮 Calculation":

    st.subheader("Awesome MVP")
    st.subheader("Calculation")
    string = st.text_input("Equation: ")
    confirm = st.button("Generate")
    if confirm: 
        print(string)

        # Create a temporary string: 
        string_temp = string

        # Identify all elements
        try: elements = re.split('=',string_temp)
        except: st.write("Not a valid function")
        if len(elements) == 2:
            new_var = "raw_data['{}']".format(elements[0])
            equation = elements[1]
            columns = sorted(st.session_state.raw_data.columns,key=len, reverse = True)
            for element in columns:
                equation = equation.replace(element, "raw_data['{}']".format(element))
            final_equation = new_var + "=" + equation
            execution_string = script_generation_from_equation(final_equation)
        try:
            exec(execution_string)
        except:
            st.write("Not a valid function.")
        else:
            st.session_state.file.write("# Calculatiion \n")
            st.session_state.file.write("{} \n".format(final_equation))

    AgGrid(st.session_state.raw_data)



elif page == "🪄 Export":
    filename = st.text_input("Enter the filename: ")
    filename = filename + ".py"

    confirm = st.button("Confirm")

    if confirm: 
        st.session_state.filename = filename
    download = st.button("Download")
    if download:
        print(st.session_state.save_path)
        st.write("Success! File {} has been downloaded".format([st.session_state.filename]))
        st.session_state.file.write("# Export final data\n")
        st.session_state.file.write("raw_data = raw_data.to_csv(os.path.join(os.getcwd(),'output','cars_final.csv'))\n")
        st.session_state.file.write("# The End")
        st.session_state.file.close()
        os.rename(st.session_state.save_path, os.path.join(os.getcwd(),st.session_state.filename))
# %%
