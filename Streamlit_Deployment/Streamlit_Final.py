# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 00:52:53 2021

@author: manle

Streamlit Deployment
"""


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import time
from janitor import clean_names, remove_empty


@st.cache
def load_hospitals():
    hospital_info = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_hospital_2.csv')
    return hospital_info

@st.cache
def load_outpatient():
    outpatient2015 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_outpatient_2.csv')
    return outpatient2015

@st.cache
def load_inpatient():
    inpatient2015 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_inpatient_2.csv')
    return inpatient2015




st.title('Medicare — Expenses - National')

 

st.write('Hello, *World!* :sunglasses:') 
  
# Load the data:     
hospital_info = load_hospitals()
outpatient2015 = load_outpatient()
inpatient2015 = load_inpatient()


# Preview the dataframes 
st.header('Hospital Data Preview')
st.dataframe(hospital_info)

st.header('Outpatient Data Preview')
st.dataframe(outpatient2015)

st.header('Inpatient Data Preview')
st.dataframe(inpatient2015)

# Cleaning the data
df_hospital = clean_names(hospital_info)
df_hospital = remove_empty(hospital_info)

df_inpatient = clean_names(inpatient2015)
df_inpatient = remove_empty(inpatient2015)

df_outpatient = clean_names(outpatient2015)
df_outpatient = remove_empty(outpatient2015)

# Merging Datasets 
st.header('Hospital/Outpatient Merged Data')
df_merge_outpt = df_outpatient.merge(df_hospital, how = 'left', left_on = 'provider_id', right_on = 'provider_id')
st.dataframe(df_merge_outpt)

st.header('Hospital/Inpatient Merged Data')
df_merge_inpt = df_inpatient.merge(df_hospital, how = 'left', left_on = 'provider_id', right_on = 'provider_id')
st.dataframe(df_merge_outpt)




# Quickly creating a pivot table 
st.subheader('Hospital Data Pivot Table')
dataframe_pivot = df_hospital_2.pivot_table(index=['state','city'],values=['effectiveness_of_care_national_comparison_footnote'],aggfunc='mean')
st.dataframe(dataframe_pivot)



hospitals_ny = df_hospital_2[df_hospital_2['state'] == 'NY']


#Bar Chart
st.subheader('Hospital Type - NY')
bar1 = hospitals_ny['hospital_type'].value_counts().reset_index()
st.dataframe(bar1)

st.markdown('The majority of hospitals in NY are acute care, followed by psychiatric')


st.subheader('With a PIE Chart:')
fig = px.pie(bar1, values='hospital_type', names='index')
st.plotly_chart(fig)



st.subheader('Map of NY Hospital Locations')

hospitals_ny_gps = hospitals_ny['location'].str.strip('()').str.split(' ', expand=True).rename(columns={0: 'Point', 1:'lon', 2:'lat'}) 	
hospitals_ny_gps['lon'] = hospitals_ny_gps['lon'].str.strip('(')
hospitals_ny_gps = hospitals_ny_gps.dropna()
hospitals_ny_gps['lon'] = pd.to_numeric(hospitals_ny_gps['lon'])
hospitals_ny_gps['lat'] = pd.to_numeric(hospitals_ny_gps['lat'])

st.map(hospitals_ny_gps)


#Timeliness of Care
st.subheader('NY Hospitals - Timelieness of Care')
bar2 = hospitals_ny['timeliness_of_care_national_comparison'].value_counts().reset_index()
fig2 = px.bar(bar2, x='index', y='timeliness_of_care_national_comparison')
st.plotly_chart(fig2)

st.markdown('Based on this above bar chart, we can see the majority of hospitals in the NY area fall below the national\
        average as it relates to timeliness of care')



#Drill down into INPATIENT and OUTPATIENT just for NY 
st.title('Drill Down into INPATIENT data')


inpatient_ny = df_inpatient_2[df_inpatient_2['provider_state'] == 'NY']
total_inpatient_count = sum(inpatient_ny['total_discharges'])

st.header('Total Count of Discharges from Inpatient Captured: ' )
st.header( str(total_inpatient_count) )





##Common D/C 

common_discharges = inpatient_ny.groupby('drg_definition')['total_discharges'].sum().reset_index()


top10 = common_discharges.head(10)
bottom10 = common_discharges.tail(10)



st.header('DRGs')
st.dataframe(common_discharges)


col1, col2 = st.beta_columns(2)

col1.header('Top 10 DRGs')
col1.dataframe(top10)

col2.header('Bottom 10 DRGs')
col2.dataframe(bottom10)




#Bar Charts of the costs 

costs = inpatient_ny.groupby('provider_name')['avsterage_total_payments'].sum().reset_index()
costs['average_total_payments'] = costs['average_total_payments'].astype('int64')


costs_medicare = inpatient_ny.groupby('provider_name')['average_medicare_payments'].sum().reset_index()
costs_medicare['average_medicare_payments'] = costs_medicare['average_medicare_payments'].astype('int64')


costs_sum = costs.merge(costs_medicare, how='left', left_on='provider_name', right_on='provider_name')
costs_sum['delta'] = costs_sum['average_total_payments'] - costs_sum['average_medicare_payments']


st.title('COSTS')

bar3 = px.bar(costs_sum, x='provider_name', y='average_total_payments')
st.plotly_chart(bar3)
st.header("Hospital - ")
st.dataframe(costs_sum)


#Costs by Condition and Hospital / Average Total Payments
costs_condition_hospital = inpatient_ny.groupby(['provider_name', 'drg_definition'])['average_total_payments'].sum().reset_index()
st.header("Costs by Condition and Hospital - Average Total Payments")
st.dataframe(costs_condition_hospital)



# hospitals = costs_condition_hospital['provider_name'].drop_duplicates()
# hospital_choice = st.sidebar.selectbox('Select your hospital:', hospitals)
# filtered = costs_sum["provider_name"].loc[costs_sum["provider_name"] == hospital_choice]
# st.dataframe(filtered)










