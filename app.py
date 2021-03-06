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
    #raw_data = pd.read_csv(os.path.join(os.getcwd(),'input','cars.csv'))
    output_header = "Output Code: "
    #%%
    # Initialize a session
    if "filename" not in st.session_state:
        st.session_state.filename = "test.py"
        st.session_state.save_path = os.path.join(os.getcwd(),st.session_state.filename)
        #st.session_state.raw_data = pd.read_csv(os.path.join(os.getcwd(),'input','cars.csv'))
        #st.session_state.raw_data = pd.read_csv(os.path.join(os.getcwd(),'cars.csv'))
        st.session_state.raw_data = pd.DataFrame()
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
                "🧽 Data Cleaning",
                "🧮 Calculation",
                "🪄 Export"]

    page = sb.radio("", page_names, index=0)

    col1, col2 = st.columns([1, 1])

    if page == "🏠 Home":

        col1.subheader("FlashScript")
        lorem_ipsum = "Welcome, I am a python code generation bot to help you write data analytics script faster \
            I am still a working progress, so do let me know how I can improve to serve you better. \
            To begin, load a excel or csv file and hit the Display button: "
        col1.markdown(lorem_ipsum, unsafe_allow_html=True)

        #gb = GridOptionsBuilder.from_dataframe(st.session_state.raw_data)
        #gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
        #gb.configure_side_bar() #Add a sidebar
        #gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
        #gridOptions = gb.build()

        uploaded_file = col1.file_uploader("Upload an Excel or csv file: ", type = ["csv","xlsx"], accept_multiple_files=False, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False)
        confirm = col1.button("Click to Display Table")
        if confirm: 
            if uploaded_file.name.endswith('.csv'):
                st.session_state.raw_data = pd.read_csv(uploaded_file)
                st.session_state.file.write("raw_data = pd.read_csv(os.path.join(os.getcwd(), '{}'))\n".format(uploaded_file.name))
            if uploaded_file.name.endswith('.xlsx'):
                st.session_state.raw_data = pd.read_excel(uploaded_file)
                st.session_state.file.write("raw_data = pd.read_excel(os.path.join(os.getcwd(), '{}'))\n".format(uploaded_file.name))
            
        col2.subheader(output_header)

        st.session_state.file.close()
        st.session_state.file = open(st.session_state.save_path,"r")
        code =  st.session_state.file.read()
        st.session_state.file.close()
        st.session_state.file = open(st.session_state.save_path,"a")
        col2.code(code)
        st.dataframe(st.session_state.raw_data)

    elif page == "🧽 Data Cleaning":

        col1.subheader("Data Cleaning")

        methods = ["Manual Edits",
                    "Replace",
                    "Drop NA",
                    "Rename Columns",
                    "Remove First N Rows",
                    "Filter Rows",
                    "Select Columns",
                    "Promote Top Row to Header"]

        method = col1.selectbox("Action:", methods)  

        if method == "Remove First N Rows":

            n = col1.text_input("How many rows from the top would you like to remove: ")
            confirm2 = col1.button("Generate Code")
            if confirm2: 
                try: n = int(n)
                except: st.write("Please enter a integer.")
                else: 
                    if n >= 0 & n <= len(st.session_state.raw_data):
                        equation = "raw_data.drop(index=raw_data.index[:{}],inplace=True)".format(n)
                        string = "{}\n".format(equation)
                        execution_string = script_generation_from_equation(string)
                        try: exec(execution_string)
                        except: st.write("Not a valid function. ")
                        else: st.session_state.file.write(string)
                    else: st.write("Index out of Range.")

        elif method == "Manual Edits":

            row_ind = col1.selectbox("Replace row: ",(st.session_state.raw_data.index))      
            col_ind = col1.selectbox("column ",(st.session_state.raw_data.columns))  

            original_value = st.session_state.raw_data.loc[row_ind,col_ind]
            new_value = string = col1.text_input("with ")
            try: new_value = float(new_value)
            except: 
                col1.write("input recognized as a string")
            else: 
                col1.write("input recognized as a number")

            confirm = col1.button("Generate Code")

            if confirm: 
                st.session_state.file.write("# Replace row {}, column {} from {} to {}\n".format(row_ind, col_ind, original_value, new_value))
                if type(new_value) == str:
                    st.session_state.file.write("raw_data.loc[{},'{}'] = '{}'\n".format(row_ind, col_ind, new_value))
                else: st.session_state.file.write("raw_data.loc[{},'{}'] = {}\n".format(row_ind, col_ind, new_value))
                col1.write("Success!")
                st.session_state.raw_data.loc[row_ind,col_ind] = new_value
                confirm = False
        
        elif method == "Drop NA":
            # Ask user if they want to remove NaN
            options = col1.multiselect(
            'Drop rows if the following parameters are NA: ',
            st.session_state.raw_data.columns,
            st.session_state.raw_data.columns[0])
            q1 = "Would you like to remove the NaNs?"
            confirm = col1.button("Generate Code")

            if confirm: 
                st.session_state.file.write("# Dropping rows if {} is NaN:\n".format(options))
                equation = "for parameter in {}:\n    raw_data = raw_data[~(raw_data[parameter].isna())]".format(options)
                execution_string = script_generation_from_equation(equation)
                try: exec(execution_string)
                except: 
                    col1.write("Not a valid function.")
                    col1.write(execution_string)
                else: st.session_state.file.write("{}\n".format(equation))

        elif method == "Filter Rows":
            # Ask user if they want to create an if statement
            action_option = col1.selectbox("Action: ",("Include", "Exclude"))        
            print('Page refreshed.')

            column_option = col1.selectbox("row if ",(st.session_state.raw_data.columns))

            compare_option = col1.selectbox("Action: ",("contains (string)", ">=", "==", "<", "<=")) 
            string = col1.text_input(" ")
            confirm = col1.button("Generate Code")

            try: string = float(string)
            except: col1.write("input recognized as a string")
            else: col1.write("input recognized as a number")

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

                confirm = False
        elif method == "Select Columns":
            col1.subheader("Select Columns to Keep")
            options = col1.multiselect(
            'Select the columns you would like to keep: ',
            st.session_state.raw_data.columns,
            st.session_state.raw_data.columns[0])
            confirm = st.button("Select the columns above")
            if confirm:
                equation = "raw_data = raw_data[{}]".format(options)
                string = "{}\n".format(equation)
                execution_string = script_generation_from_equation(string)
                try: exec(execution_string)
                except: st.write("Not a valid function")
                else: st.session_state.file.write(string)
        
        elif method == "Replace":

            original_string = col1.text_input("Replace")
            replace_string = col1.text_input("with")
            replace_column_option = col1.multiselect("in",st.session_state.raw_data.columns,st.session_state.raw_data.columns[0])

            confirm = st.button("Generate Code")
            if confirm:
                equation = "for parameter in {}:\n  raw_data[parameter].replace({{'{}':'{}'}}, inplace = True)".format(replace_column_option,original_string,replace_string)
                string = "{}\n".format(equation)
                execution_string = script_generation_from_equation(string)
                try: 
                    exec(execution_string)
                    st.write(execution_string)
                except: 
                    st.write("Not a valid function")
                    st.write(execution_string)
                else: st.session_state.file.write(string)


        col2.subheader(output_header)
        st.session_state.file.close()
        st.session_state.file = open(st.session_state.save_path,"r")
        code =  st.session_state.file.read()
        st.session_state.file.close()
        st.session_state.file = open(st.session_state.save_path,"a")
        col2.code(code)
        st.dataframe(st.session_state.raw_data)        


    elif page == "🧮 Calculation":

        col1.subheader("Calculate New Columns")
        string = col1.text_input("Equation (e.g., A=B*3): ")
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
                col1.write("Success!")

        col2.subheader(output_header)

        st.session_state.file.close()
        st.session_state.file = open(st.session_state.save_path,"r")
        code =  st.session_state.file.read()
        st.session_state.file.close()
        st.session_state.file = open(st.session_state.save_path,"a")
        col2.code(code)

        st.dataframe(st.session_state.raw_data)


    elif page == "🪄 Export":
        filename = "autogenerated-code.py"

        confirm = col1.button("Add code to export final data")
        if confirm:
            st.session_state.file.write("# Export final data\n")
            #st.session_state.file.write("raw_data = raw_data.to_csv(os.path.join(os.getcwd(),output_header,'cars_final.csv'))\n")
            st.session_state.file.write("raw_data = raw_data.to_csv(os.path.join(os.getcwd(),'final.csv'))\n")
            st.session_state.file.write("# The End")
        
        st.session_state.file.close()
        st.session_state.file = open(os.path.join(os.getcwd(),st.session_state.filename),"r")
        col1.download_button('Download .py', st.session_state.file, filename) 
        
        col2.subheader(output_header)
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
# %%
