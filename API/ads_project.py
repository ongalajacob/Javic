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
import requests
import io  

from plotly.subplots import make_subplots


########################### Display text ###########################################
#Display text
#images
#from PIL import Image
#im = Image.open("https://github.com/ongalajacob/Javic/blob/main/API/images/logo.jpg")
#st.image(im, width=150)


student = 'https://raw.githubusercontent.com/ongalajacob/Javic/main/2021_data/student.csv'
class_session = 'https://raw.githubusercontent.com/ongalajacob/Javic/main/2021_data/class_session.csv'
classregister = 'https://raw.githubusercontent.com/ongalajacob/Javic/main/2021_data/classregister.csv'
invoice = 'https://raw.githubusercontent.com/ongalajacob/Javic/main/2021_data/invoice.csv'
employees = 'https://raw.githubusercontent.com/ongalajacob/Javic/main/2021_data/employees.csv'
fees = 'https://raw.githubusercontent.com/ongalajacob/Javic/main/2021_data/fees.csv'
exams = 'https://raw.githubusercontent.com/ongalajacob/Javic/main/2021_data/exams.csv'



def main():
    stud_df = pd.read_csv(student)
    session_df = pd.read_csv(class_session)
    classregister_df = pd.read_csv(classregister)
    invoice_df = pd.read_csv(invoice)
    employees_df = pd.read_csv(employees)
    fee_df = pd.read_csv(fees)
    exams_df = pd.read_csv(exams)

    session = pd.merge(left=session_df, right=employees_df[['id', 'name', 'Staff_ID', 'sex']], how='left', left_on='ClassTeacher', right_on='id')
    session.drop(["id_y","ClassTeacher"], axis=1, inplace=True)
    session.rename(columns = {'name':'ClassTeacher','id_x':'id', }, inplace = True)
    #session
    Register = pd.merge(left=classregister_df, right=session, how='left', left_on='Session', right_on='id')
    Register.drop(["id_y","Session"], axis=1, inplace=True)
    Register.rename(columns = {'id_x':'id', }, inplace = True)

    Register = pd.merge(left=Register, right=stud_df, how='left', left_on='student', right_on='ID')
    Register.drop(['ID','Mother', 'Father', 'Guadian',
        'Class_Admitted', 'PHONE1', 'PHONE2', 'PHONE3', 'DOA', 'address',
            'DateExit',"student",'Startdate','Enddate'], axis=1, inplace=True)
    Register.rename(columns = {'sex_x':'sex_teacher','sex_y':'sex_stud' ,'name':'name_stud' ,'Class_grd':'grade'  }, inplace = True)

    Register=pd.merge(left=Register, right=invoice_df, how='left', left_on='id', right_on='ClassRegisterID')
    Register.drop(["id_y"], axis=1, inplace=True)
    Register.rename(columns = {'id_x':'id', }, inplace = True)
    Register_df = Register.rename(columns=str.lower) 

    Register_df['tot_invoice']=Register_df['bal_bf']+Register_df['uniform']+Register_df['uniform_no']+(Register_df['transport']*Register_df['transport_months'])+ \
        (Register_df['lunch']*Register_df['lunch_months'])+Register_df['otherlevyindv']+Register_df['tutionfee']+Register_df['examfee']+ \
            Register_df['booklevy'] +Register_df['activityfee']+Register_df['otherlevies']
    Register_df= Register_df[['id', 'year', 'term',"classregisterid", 'grade', 'classteacher', 'staff_id', 'sex_teacher',
        'name_stud', 'adm', 'dob', 'sex_stud', 'enrolstatus', 'bal_bf', 'tot_invoice']]      
    Register_df["grade"].replace({"Baby1":'Baby','Class5':'Grade5',}, inplace=True)
    
    #Register_df.to_csv(r'API\data\Register_df.csv', index = False)
    #prepare fee data 
    fee_df[['Admission', 'Tuition',
        'Transport', 'Uniform', 'Lunch', 'Exams', 'BookLvy', 'Activity',
        'OtheLvy']] = fee_df[['Admission', 'Tuition',
        'Transport', 'Uniform', 'Lunch', 'Exams', 'BookLvy', 'Activity',
        'OtheLvy']].fillna(0)
    fee_df["total_paid"] =fee_df["Admission"] +fee_df["Tuition"] +fee_df["Transport"] +fee_df["Uniform"] \
        +fee_df["Lunch"] +fee_df["Exams"] +fee_df["BookLvy"] +fee_df["Activity"] +fee_df["OtheLvy"] 
    fee_df['id']=fee_df['id'].astype(object)
    fee_df['ReceiptNo']=fee_df['ReceiptNo'].astype(object)
    fee_df['DOP1']=pd.to_datetime(fee_df['DOP'] ,format = '%d/%m/%Y') 
    fee_df['DOP']=pd.to_datetime(fee_df['DOP']).dt.strftime('%d/%m/%Y')
    fees_df=pd.merge(left=fee_df, right=Register_df, how='left', left_on='ClassRegisterID', right_on='classregisterid')
    fees_df = fees_df.rename(columns=str.lower)
    fees_df.drop(["id_y",'classregisterid'], axis=1, inplace=True)
    fees_df.rename(columns = {'id_x':'id', }, inplace = True)
    fees_df=fees_df[['id', 'receiptno', 'dop', 'year', 'term', 'grade','adm','name_stud', 'enrolstatus', 'admission', 'tuition', 'transport',
        'uniform', 'lunch', 'exams', 'booklvy', 'activity', 'othelvy',  'total_paid','dop1']]
    fees_df["pay_year"] = fees_df.dop1.dt.year 
    fees_df["pay_month"] = fees_df.dop1.dt.month 
    fees_df["pay_day"] = fees_df.dop1.dt.day
    fees_df['pay_month']=  fees_df['pay_month'].apply(str)
    fees_df['pay_year']=  fees_df['pay_year'].apply(str)
    #fees_df["pay_month"].replace({1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'July',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec' }, inplace=True)
    

    fee_df1=fee_df.groupby(["ClassRegisterID"])["total_paid"].sum().reset_index(name='Total_collection')
    fees_bal_df=pd.merge(left=fee_df1, right=Register_df, how='left', left_on='ClassRegisterID', right_on='classregisterid')
    fees_bal_df["bal_cf"] =fees_bal_df["tot_invoice"] - fees_bal_df["Total_collection"] 
    fees_bal_df=fees_bal_df[['ClassRegisterID','year', 'term','grade',  'adm','name_stud','enrolstatus',  'bal_bf', 'tot_invoice', 'Total_collection','bal_cf']]
    fees_bal_df = fees_bal_df.rename(columns=str.lower)
    
    #Exams 
    exam_df=pd.merge(left=exams_df, right=Register_df, how='left', left_on='ClassRegisterID', right_on='classregisterid')
    exam_df.drop(["id_y",'classregisterid'], axis=1, inplace=True)
    exam_df.rename(columns = {'id_x':'id', }, inplace = True)
    exam_df=exam_df[['id', 'ClassRegisterID', 'ExamType', 'year', 'term', 'grade', 'classteacher','adm',   'name_stud', 'dob', 'sex_stud','enrolstatus',  'Maths', 'EngLan', 'EngComp',
        'KisLug', 'KisIns', 'Social', 'Creative', 'CRE', 'Science', 'HmScie',
        'Agric', 'Music', 'PE']]
    exam_df = exam_df.rename(columns=str.lower)
    exam_df['year'] = pd.to_numeric(exam_df['year'], errors='coerce')
    exam_df['adm'] = pd.to_numeric(exam_df['adm'], errors='coerce')

    selection = st.sidebar.selectbox('Select your analysis option:', 
        ('Background Information', 'Data Intergration', 'Descriptive Analysis', 'Machine Learning'))
    if selection == 'Background Information':
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
        #with col2:
        #st.image(im, width=150)

        st.markdown(html_temp2,unsafe_allow_html=True)
        #st.title('This is for a good design')
        st.markdown('<style>h1{color: red;}</style>', unsafe_allow_html=True)


        Infos="""
        Welcome to Javic Junior  School. This application will be used to monitor the the financial 
        management operations and academics of our students. For more information contact the director @
        javicjun@javicjuniorschool.co.ke  or Manager @  vogendo@javicjuniorschool.co.ke
        """
        st.markdown(Infos)
        

        st.markdown("**Project Problem Statement**")
        Problem="""
        Javic Junior School is a private primary and pre-primary school based in Kisumu, 
        Kenya. It is a partnership business between Dr. Jacob Ong'ala and Mrs. Vivian Awuor
        The two partners stay apart (in different Countries) but they participarte in the daily, 
        Operations of the school. And thefore the need for an automated online management 
        plattform 

        To make decisions as managers, they get alot of reference from the data that they collect 
        from School operations. In July 2020, Javic Junior School upgraded their data management system to a 
        web-based (www.javicjuniorschool.com). The system is hosted by a web company and is runing on MySQL laguange. 

        The management would like to use the data to make decision in aswering the following 
        following question a
        """

        st.markdown(Problem)
        st.markdown("* Study the student population (interm of gender, grade, term and year)")
        st.markdown("* Monitor fee collection  and establish fee balance status")
        st.markdown("* Report on students perormance ")
        st.markdown("* Monitor financial aspect for Lunch programss and transport programs  and advise on their viability")
        st.markdown("* Categorize students in their fee payment behaviors and academic perofmance to help in restructuring future admission creteria")


        st.markdown("**Methodology**")
        methods="""
        The database is hosted in a webhosting company but can be accessed in form of variou csv tables. They will 
        be exctracted from the database and saved github repository where the application can access them easily 
        for management and building model. 

        Since the table are from arelational relational database, they will be marged accordingly to form dataframe(s) which will be used in the 
        application building
        """
        st.markdown(methods)


    elif selection == 'Data Intergration':
        Register_df['grade'] = pd.Categorical(Register_df['grade'], ['Baby', 'PP1', 'PP2','Grade1',  'Grade2', 'Grade3', 'Grade4', 'Grade5'])        
        st.title("Cleaned/Merged Data")
        st.markdown("**Select the data set that you want to view**")
        if st.checkbox("Show Students Dataset"):
            #st.write('Students data')
            st.dataframe(Register_df[Register_df.enrolstatus=='In_Session'].head(5))
        if st.checkbox("Show Fee Collection Dataset"):
            #st.write('Feee data')
            st.dataframe(fees_df[fees_df.enrolstatus=='In_Session'][['receiptno', 'dop', 'grade', 'adm', 'name_stud',
            'admission', 'tuition', 'transport', 'uniform', 'lunch',
            'exams', 'booklvy', 'activity', 'othelvy', 'total_paid']])    
        if st.checkbox("Show Fee balances Dataset"):
            #st.write('Feee data')
            st.dataframe(fees_bal_df[fees_bal_df.enrolstatus=='In_Session'][['year', 'term', 'grade', 'adm', 'name_stud',
            'bal_bf', 'tot_invoice', 'total_collection', 'bal_cf']])   
        if st.checkbox("Show Academic Dataset"):
            #st.write('Feee data')
            st.dataframe(exam_df[exam_df.enrolstatus=='In_Session'][['examtype', 'year', 'term', 'grade',
            'adm', 'name_stud', 'maths', 'englan', 'engcomp', 'kislug', 'kisins', 'social', 'creative',
            'cre', 'science', 'hmscie', 'agric', 'music', 'pe']]) 
    
    elif selection == 'Descriptive Analysis':

        st.title("Descriptive Analysis")
        st.markdown("**Select statistics to view**")
        curent_pop=Register_df.drop_duplicates('adm').id.count()
        st.write("the current student population is ", curent_pop)

        if st.checkbox("Student Population by Class"):
            Register_df['grade'] = pd.Categorical(Register_df['grade'], ['Baby', 'PP1', 'PP2','Grade1',  'Grade2', 'Grade3', 'Grade4', 'Grade5'])    
            a = Register_df.groupby(["term",'grade', 'sex_stud'])["id"].count().reset_index(name='Number')
            fig = px.bar(a, x='grade', y='Number',color='term',barmode='group',hover_name='sex_stud')
            st.plotly_chart(fig)
            
        if st.checkbox("Student Population by Gender"):
            df = Register_df.groupby(["term",'sex_stud'])["id"].count().reset_index(name='Number')
            # Create subplots: use 'domain' type for Pie subplot
            fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
            fig.add_trace(go.Pie(labels=df[df.term== 'Term 2'].sex_stud.array, values=df[df.term== 'Term 2'].Number.array, name="Term 2"),
                        1, 1)
            fig.add_trace(go.Pie(labels=df[df.term== 'Term 3'].sex_stud.array, values=df[df.term== 'Term 3'].Number.array, name="Term 3"),
                        1, 2)
            fig.update_traces(hole=.4, hoverinfo="label+value+name")
            fig.update_layout(
                title_text="Population by gender",
                # Add annotations in the center of the donut pies.
                annotations=[dict(text='Term 2', x=0.18, y=0.5, font_size=20, showarrow=False),
                            dict(text='Term 3', x=0.82, y=0.5, font_size=20, showarrow=False)])
            st.plotly_chart(fig)
        if st.checkbox("Monthly Fee Collection"): 
            #fees_df['pay_year']= pd.Categorical(fees_df['pay_year'])
            #fees_df['pay_month'] = pd.Categorical(fees_df['pay_month'], ['Jan', 'Feb', 'Mar','Apr',  'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']) 

            st.dataframe(pd.crosstab(fees_df.pay_year,  fees_df.pay_month))
            a = fees_df.groupby(["pay_year",'pay_month'])["total_paid"].sum().reset_index(name='Monthl_fee_received')
            fig = px.bar(a, x='pay_month', y='Monthl_fee_received',color='pay_year',barmode='group')
            st.plotly_chart(fig)
if __name__ =='__main__':
    main() 


#@st.cache

#st.balloons()


