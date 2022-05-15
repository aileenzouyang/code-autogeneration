#%%
# Import packages
import streamlit as st
import pandas as pd
import numpy as np
import os
import re
#from st_st.dataframe import GridOptionsBuilder, st.dataframe, GridUpdateMode, DataReturnMode
from script_generation import *
from pathlib import Path
#https://towardsdatascience.com/make-dataframes-interactive-in-streamlit-c3d0c4f84ccb

def main():
    raw_data = pd.read_csv(os.path.join(os.getcwd(),'input','cars.csv'))
    #%%
    # Initialize a session
    if "filename" not in st.session_state:
        st.session_state.filename = "test.py"
        st.session_state.save_path = os.path.join(os.getcwd(),st.session_state.filename)
        #st.session_state.raw_data = pd.read_csv(os.path.join(os.getcwd(),'input','cars.csv'))
        st.session_state.raw_data = pd.read_csv(os.path.join(os.getcwd(),'cars.csv'))
        st.session_state.file = open(st.session_state.save_path,"w")
        st.session_state.file.write("#Welcome to the new era, where data analyts don't have to write a single line of code\n")
        st.session_state.file.write("#%%\n")
        st.session_state.file.write("# Import packages\n")
        st.session_state.file.write("import numpy as np\n")
        st.session_state.file.write("import pandas as pd\n")
        st.session_state.file.write("import os\n")
        #st.session_state.file.write("raw_data = pd.read_csv(os.path.join(os.getcwd(),'input','cars.csv'))\n")
        
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

    col1, col2 = st.columns([1, 1])

    if page == "🏠 Home":

        col1.subheader("Awesome MVP")
        col1.subheader("What is Awesome MVP?")
        lorem_ipsum = "Awesome MVP autogenerates python script based on user requirement. \
            In this example we will be curating, summarizing, analyzing, and visualizing the folloing data table."
        col1.markdown(lorem_ipsum, unsafe_allow_html=True)

        #gb = GridOptionsBuilder.from_dataframe(st.session_state.raw_data)
        #gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
        #gb.configure_side_bar() #Add a sidebar
        #gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
        #gridOptions = gb.build()

        uploaded_file = col1.file_uploader("Upload an Excel or csv file: ", type = ["csv","xlsx"], accept_multiple_files=False, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False)
        confirm = col1.button("Display")
        if confirm: 
            if uploaded_file.name.endswith('.csv'):
                st.session_state.raw_data = pd.read_csv(uploaded_file)
                st.session_state.file.write("raw_data = pd.read_csv(os.path.join(os.getcwd(), '{}'))\n".format(uploaded_file.name))
            if uploaded_file.name.endswith('.xlsx'):
                st.session_state.raw_data = pd.read_excel(uploaded_file)
                st.session_state.file.write("raw_data = pd.read_excel(os.path.join(os.getcwd(), '{}'))\n".format(uploaded_file.name))
            
            col2.subheader('Output')

            st.session_state.file.close()
            st.session_state.file = open(st.session_state.save_path,"r")
            code =  st.session_state.file.read()
            st.session_state.file.close()
            st.session_state.file = open(st.session_state.save_path,"a")
            col2.code(code)
            st.dataframe(st.session_state.raw_data)

    elif page == "🧽 Data Cleaning - Manual Edits":
        col1.subheader("Awesome MVP")
        col1.subheader("Data Cleaning")


        # Ask user if they want to create an if statement
        row_ind = col1.selectbox("Replace row: ",(st.session_state.raw_data.index))      
        col_ind = col1.selectbox("column ",(st.session_state.raw_data.columns))  

        original_value = st.session_state.raw_data.loc[row_ind,col_ind]
        new_value = string = col1.text_input("with ")
        confirm = col1.button("Generate")

        if confirm: 
            st.session_state.file.write("# Replace row {}, column {} from {} to {}\n".format(row_ind, col_ind, original_value, new_value))
            st.session_state.file.write("raw_data.loc[{},'{}'] = '{}'\n".format(row_ind, col_ind, new_value))
            col1.write("Success!")
            st.session_state.raw_data.loc[row_ind,col_ind] = new_value
            confirm = False
        
        col2.subheader('Output')

        st.session_state.file.close()
        st.session_state.file = open(st.session_state.save_path,"r")
        code =  st.session_state.file.read()
        st.session_state.file.close()
        st.session_state.file = open(st.session_state.save_path,"a")
        col2.code(code)

        st.dataframe(st.session_state.raw_data)


    elif page == "🧽 Data Cleaning - Conditional Selection":

        col1.subheader("Awesome MVP")
        col1.subheader("Data Cleaning")

        # Ask user if they want to remove NaN
        q1 = "Would you like to remove the NaNs?"
        removena = col1.button(q1)

        if removena: 
            st.session_state.file.write("# Dropping rows if it contains any NaN:\n")
            equation = "raw_data = raw_data.dropna()"
            col1.write(equation)
            st.session_state.file.write("{}\n".format(equation))
            execution_string = script_generation_from_equation(equation)
            try: exec(execution_string)
            except: col1.write("Not a valid function.")

        # Ask user if they want to create an if statement
        action_option = col1.selectbox("Action: ",("Include", "Exclude"))        
        print('Page refreshed.')

        column_option = col1.selectbox("row if ",(st.session_state.raw_data.columns))

        compare_option = col1.selectbox("Action: ",("contains (string)", ">=", "==", "<", "<=")) 
        string = col1.text_input(" ")
        confirm = col1.button("Generate")

        if confirm: 
            if compare_option == "contains (string)":
                st.session_state.file.write("# {} row if {} contains {}\n".format(action_option, column_option, string))
                if action_option == "Include": 
                    st.session_state.file.write("raw_data = raw_data[{}raw_data['{}'].str.contains('{}') ]\n".format("", column_option,string))
                    st.session_state.raw_data = st.session_state.raw_data[st.session_state.raw_data[column_option].str.contains(string)]
                if action_option == "Exclude": 
                    st.session_state.file.write("raw_data = raw_data[{}raw_data['{}'].str.contains('{}') ]\n".format("~", column_option,string))
                    st.session_state.raw_data = st.session_state.raw_data[~st.session_state.raw_data[column_option].str.contains(string)]
            
            elif compare_option in [">=", "==", "<", "<="]:
                try: string = float(string)
                except: col1.write("Please enter a number")
                else:
                    st.session_state.file.write("# {} row if {} {} {}\n".format(action_option, column_option, compare_option, string))
                    if action_option == "Include": 
                        equation = "raw_data = raw_data[{}(raw_data['{}'] {} {})]".format("", column_option,compare_option,string)
                    if action_option == "Exclude": 
                        equation = "raw_data = raw_data[{}(raw_data['{}'] {} {})]".format("~", column_option,compare_option,string)

                    execution_string = script_generation_from_equation(equation)
                    try: exec(execution_string)
                    except: col1.write("Not a valid equation: {}".format(execution_string))
                    else: st.session_state.file.write("{}\n".format(equation))

            col1.write("Success!")
            confirm = False
        
        col2.subheader('Output')

        st.session_state.file.close()
        st.session_state.file = open(st.session_state.save_path,"r")
        code =  st.session_state.file.read()
        st.session_state.file.close()
        st.session_state.file = open(st.session_state.save_path,"a")
        col2.code(code)

        st.dataframe(st.session_state.raw_data)

    elif page == "🧮 Calculation":

        col1.subheader("Awesome MVP")
        col1.subheader("Calculation")
        string = col1.text_input("Equation: ")
        confirm = col1.button("Generate")
        if confirm: 
            print(string)

            # Create a temporary string: 
            string_temp = string

            # Identify all elements
            try: elements = re.split('=',string_temp)
            except: col1.write("Not a valid function")
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
                col1.write("Not a valid function.")
            else:
                st.session_state.file.write("# Calculatiion \n")
                st.session_state.file.write("{} \n".format(final_equation))

        col2.subheader('Output')

        st.session_state.file.close()
        st.session_state.file = open(st.session_state.save_path,"r")
        code =  st.session_state.file.read()
        st.session_state.file.close()
        st.session_state.file = open(st.session_state.save_path,"a")
        col2.code(code)

        st.dataframe(st.session_state.raw_data)



    elif page == "🪄 Export":
        filename = col1.text_input("Enter the filename: ")
        filename = filename + ".py"

        confirm = col1.button("Confirm")

        if confirm: 
            st.session_state.filename = filename
        download = col1.button("Download")
        if download:
            print(st.session_state.save_path)
            col1.write("Success! File {} has been downloaded".format([st.session_state.filename]))
            st.session_state.file.write("# Export final data\n")
            #st.session_state.file.write("raw_data = raw_data.to_csv(os.path.join(os.getcwd(),'output','cars_final.csv'))\n")
            st.session_state.file.write("raw_data = raw_data.to_csv(os.path.join(os.getcwd(),'final.csv'))\n")
            st.session_state.file.write("# The End")
            if st.session_state.file.closed:
                print('file is closed')
            else: st.session_state.file.close()

            os.rename(st.session_state.save_path, os.path.join(os.getcwd(),st.session_state.filename))
        
            col2.subheader('Output')

            st.session_state.file.close()
            st.session_state.file = open(os.path.join(os.getcwd(),st.session_state.filename),"r")
            code =  st.session_state.file.read()
            st.session_state.file.close()
            st.session_state.file = open(os.path.join(os.getcwd(),st.session_state.filename),"a")
            col2.code(code)

        st.dataframe(st.session_state.raw_data)


# Run main()

if __name__ == '__main__':
    main()