# get streamlit 

#streamlitrun app.py   IN CONSOLE

from typing import Any
import streamlit as st 
import pandas as pd 
import altair as alt
import numpy as np
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
from bokeh.plotting import figure

import os
import seaborn as sns
import cufflinks as cf
import warnings
import cufflinks as cf
import plotly.express as px 
import plotly.graph_objects as go


########################### Display text ###########################################
#Display text
#images
from PIL import Image
im = Image.open("logo.jpg")
#st.image(im, width=150)


student = 'https://github.com/ongalajacob/Javic/blob/main/2021_data/student.csv'
class_session = 'https://github.com/ongalajacob/Javic/blob/main/2021_data/class_session.csv'
classregister = 'https://github.com/ongalajacob/Javic/blob/main/2021_data/classregister.csv'
invoice = 'https://github.com/ongalajacob/Javic/blob/main/2021_data/invoice.csv'
employees = 'https://github.com/ongalajacob/Javic/blob/main/2021_data/employees.csv'
fees = 'https://github.com/ongalajacob/Javic/blob/main/2021_data/fees.csv'
exams = 'https://github.com/ongalajacob/Javic/blob/main/2021_data/exams.csv'




stud_df = pd.read_csv (student, error_bad_lines=False)
session_df= pd.read_csv (class_session, error_bad_lines=False)
classregister_df= pd.read_csv (classregister, error_bad_lines=False)
invoice_df= pd.read_csv (invoice, error_bad_lines=False)
employees_df= pd.read_csv (employees, error_bad_lines=False)
fee_df= pd.read_csv (fees, error_bad_lines=False)
exams_df= pd.read_csv (exams, error_bad_lines=False)






html_temp1 = """
<div style="background-color:white;padding:1.5px">
<h1 style="color:black;text-align:center;">JAVIC JUNIOR SCHOOL </h1>
</div><br>"""

html_temp2 = """
<div style="background-color:white;padding:1.5px">
<h3 style="color:black;text-align:center;">Management Mornitoring Application </h3>
</div><br>"""
st.markdown(html_temp1,unsafe_allow_html=True)
_,_,_, col2, _,_,_ = st.beta_columns([1,1,1,2,1,1,1])
with col2:
 st.image(im, width=150)

st.markdown(html_temp2,unsafe_allow_html=True)
#st.title('This is for a good design')
st.markdown('<style>h1{color: red;}</style>', unsafe_allow_html=True)


Infos="""
Welcome to Javic Junior  School. This application will be used to monitor the the financial 
management operations and academics of our students. for more information contact the director @
javicjun@javicjuniorschool.co.ke  or Manager @  vogendo@javicjuniorschool.co.ke
"""
st.text(Infos)
 
def main():
   
    selection = st.sidebar.selectbox('Select your analysis option:', 
        ('Students', 'feeStatus'))
    
        

    if selection == 'Students':
        stud_data= st.file_uploader("Select Students data':", type = ["csv"])
        if stud_data is not None:
            stud_df = pd.read_csv(stud_data)
            st.title('Students Population')
            if st.checkbox("Show Students Dataset"):
                st.write("#### Enter the number of rows to view")
                stud_df=stud_df[stud_df.EnrolStatus=='In_Session']
                rows = st.number_input("", min_value=0,value=5, max_value=stud_df.ID.count())
                if rows > 0:
                    columns = stud_df.columns.tolist()
                    st.write("#### Select the columns to display:")
                    selected_cols = st.multiselect("", columns)
                    if len(selected_cols) > 0:
                        selected_df = stud_df[selected_cols]
                        st.dataframe(selected_df)
                       #st.dataframe(stud_df[stud_df.EnrolStatus=='In_Session'].head(rows))
            if st.checkbox("Show Admission Statistics"):
                st.subheader('Admission Statistics')
            #stud_df.drop(columns= 'DateExit' , axis=1, inplace=True)
                stud_df["Class"].replace({"Baby 1":'Baby1',  'Middle':'PP1','Pre-Unit':'PP2','Grade 1':'Grade1','Grade 2':'Grade2','Grade 3':'Grade3',
                        'Four':'Grade4','Class5':'Grade5','Grade 5':'Grade5'}, inplace=True)
            
                st.dataframe(stud_df.Class.value_counts(), )
                
            if st.checkbox("Curent Student Population"):
                st.write('The total population currently enrolled at Javic is' ,  stud_df.ID.count(), 'and they are agreegated as below')
                st.dataframe(stud_df[stud_df.EnrolStatus=='In_Session'].groupby(["sex"])["ID"].count().reset_index(name='Counts'))
                if st.checkbox("Show Pie Chart and Value Counts of Gender"):
                    fig, ax = plt.subplots(figsize=(2, 2))
                    stud_df.groupby('sex').size().plot(kind='pie', textprops={'fontsize': 20},
                                    colors=['violet', 'lime'], ax=ax)
                    st.pyplot(fig)
            stud_df = pd.read_csv(stud_data)

    elif selection == 'feeStatus':
        #st.title('Fee collection Information')
        fee_data = st.file_uploader("Select fee collection data':", type = ["csv"])
        if fee_data is not None:
            fee_df = pd.read_csv(fee_data)
            st.title('Fee collection Information')
            st.dataframe(fee_df.describe())
            st.dataframe(fee_df.head())

            st.subheader('Graphical display')
            stud_df = fee_df.groupby(['adm', 'stud_names']).size().reset_index(name='Freq')
            stud_df.drop("Freq", axis=1, inplace=True)
            pd.set_option('display.max_rows', None)
            monthly_sum=fee_df.groupby(["pay_year",'pay_month'])["total"].sum().reset_index(name='Total_collection')
            g= sns.catplot(x="pay_month", y="Total_collection", hue="pay_year", data=monthly_sum, kind="bar")
            plt.xlabel("Month of theyear", size=16)
            plt.ylabel("Total fee collected", size=16)
            plt.title("JAVIC JUNIOR SCHOOL \n Monthly fee collection", size=23)
            g.fig.set_figwidth(12)
            g.fig.set_figheight(8)
            st.pyplot(g)
            mothly_fee ="""
            The highest collection is experienced in January. There is anincreasing trend onmolty 
            collection  from 2019 to 2021. This can be seen in Jan, Feb and March. where data set 
            was complete for all the years 
            """
            st.write(mothly_fee)


            fee_df['Count'] = 1
            keys = [pair for pair, df in fee_df.groupby(['pay_day'])]
            fig = plt.figure()
            plt.plot(keys, fee_df.groupby(['pay_day']).count()['Count'])
            plt.xticks(keys)
            plt.xlabel('Day of the month')
            plt.ylabel('No of students')
            plt.title('JAVIC JUNIOR \n No of daily fee Payments',fontsize=18)
            plt.grid()
            fig.set_figwidth(15)
            fig.set_figheight(8)

            st.pyplot(fig)

            Termly_collection=fee_df.groupby(['year', 'term'])["total"].sum().reset_index(name='Total_collection')


            g1= sns.catplot(x="term", y="Total_collection", hue="year",data=Termly_collection, kind="bar" )
            plt.xlabel("Term", size=16)
            plt.ylabel('Total Collection in Millions', size=16)
            plt.title("JAVIC JUNIOR SCHOOL \n Termly fee collection", size=24)
            g1.fig.set_figwidth(12)
            g1.fig.set_figheight(8)

            st.pyplot(g1)

if __name__ =='__main__':
    main() 


#@st.cache

st.balloons()