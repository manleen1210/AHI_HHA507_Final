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
import matplotlib.pyplot as plt


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

# Merging Datasets 

hospital_info['provider_id'] = hospital_info['provider_id'].astype(str)
outpatient2015['provider_id'] = outpatient2015['provider_id'].astype(str)
inpatient2015['provider_id'] = inpatient2015['provider_id'].astype(str)

st.header('Hospital/Outpatient Merged Data')
df_merge_outpt = outpatient2015.merge(hospital_info, how = 'left', left_on = 'provider_id', right_on = 'provider_id')
st.dataframe(df_merge_outpt)

st.header('Hospital/Inpatient Merged Data')
df_merge_inpt = inpatient2015.merge(hospital_info, how = 'left', left_on = 'provider_id', right_on = 'provider_id')
df_merge_inpt_preview = df_merge_inpt.sample(20)
st.dataframe(df_merge_inpt_preview)

st.subheader('Stonybrook Data Hospital/Outpatient')
# Stony brook data for Hospital/outpatient merged dataset
sb_merge_outpt = df_merge_outpt[df_merge_outpt['provider_id'] == '330393']
st.dataframe(sb_merge_outpt)

st.subheader('Non Stonybrook Data Hospital/Outpatient')
# Non Stony Brook Data for Hospital/Outpatient merged dataset
nonsb_merge_outpt = df_merge_outpt[df_merge_outpt['provider_id'] != '330393']
st.dataframe(nonsb_merge_outpt)

st.subheader('Stonybrook Data Hospital/Inpatient')
# Stony brook data for Hospital/Inpatient merged dataset
sb_merge_inpt = df_merge_inpt[df_merge_inpt['provider_id'] == '330393']
sb_merge_inpt_preview = sb_merge_inpt.sample(20)
st.dataframe(sb_merge_inpt_preview)

st.subheader('Non Stonybrook Data Hospital/Inpatient')
# Non Stony Brook Data for Hospital/Inpatient merged dataset
nonsb_merge_inpt = df_merge_inpt[df_merge_inpt['provider_id'] != '330393']
nonsb_merge_inpt_preview = nonsb_merge_inpt.sample(20)
st.dataframe(nonsb_merge_inpt_preview)


# Question 1
st.subheader('Question 1')
st.write('Question1: How does the data for Stony Brook compare to other outpatient facilities for the most expensive APCs?')
st.markdown('Based on the two pivot tables here, we can see that the most expensive outpatient APC at Stonybrook is 0074 - Level IV Endoscopy Upper Airway. The most expensive outpatient APC in non Stonybrook facilities is also 0074 - Level IV Endoscopy Upper Airway, however the average total payment for this APC at Stonybrook is $2307.21 whereas outside of Stonybrook the average total payment is $2783.802785')

# Stony Brook -> Most expensive outpatient APCs
st.subheader('StonyBrook Outpatient APCs Pivot Table')
SB_Outpatient_APCs_pivot = sb_merge_outpt.pivot_table(index=['provider_id','apc'],values=['average_total_payments'])
SB_Outpatient_APCs_pivot_desc = SB_Outpatient_APCs_pivot.sort_values(['average_total_payments'], ascending=False)
st.dataframe(SB_Outpatient_APCs_pivot_desc)

st.subheader('Non-StonyBrook Outpatient APCs Pivot Table')
NonSB_Outpatient_APCs_pivot = nonsb_merge_outpt.pivot_table(index=['provider_id','apc'],values=['average_total_payments'])
NonSB_Outpatient_APCs_pivot_desc = NonSB_Outpatient_APCs_pivot.sort_values(['average_total_payments'], ascending=False)
st.dataframe(NonSB_Outpatient_APCs_pivot_desc)

# Question 2
st.subheader('Question 2')
st.write('Question2: How does the data for Stony Brook compare to other inpatient facilities for the most expensive DRGs?')
st.markdown('Based on the pivot tables shown below, at StonyBrook 003 - ECMO OR TRACH W MV >96 HRS OR PDX EXC FACE, MOUTH & NECK W MAJ O.R.	with an average total payment of $216636.88 is the most expensive inpatient DRG whereas 001 - HEART TRANSPLANT OR IMPLANT OF HEART ASSIST SYSTEM W MCC with an average total payment of $449486.11 is the most expensive DRG at non StonyBrook inpatient facilities ')

# Stony Brook -> Most expensive inpatient DRGs
st.subheader('StonyBrook Inpatient DRGs Pivot Table')
SB_Inpatient_DRGs_pivot = sb_merge_inpt.pivot_table(index=['provider_id','drg_definition'],values=['average_total_payments'])
SB_Inpatient_DRGs_pivot_desc = SB_Inpatient_DRGs_pivot.sort_values(['average_total_payments'], ascending=False)
st.dataframe(SB_Inpatient_DRGs_pivot_desc)

st.subheader('Non-StonyBrook Inpatient DRGs Pivot Table')
NonSB_Inpatient_DRGs_pivot = nonsb_merge_inpt.pivot_table(index=['provider_id','drg_definition'],values=['average_total_payments'])
NonSB_Inpatient_DRGs_pivot_desc = NonSB_Inpatient_DRGs_pivot.sort_values(['average_total_payments'], ascending=False)
st.dataframe(NonSB_Inpatient_DRGs_pivot_desc)


# All NY data except Stonybrook 

st.subheader('All NY data except StonyBrook (Outpatient)')
NY_nonsb_merge_outpt = nonsb_merge_outpt[nonsb_merge_outpt['provider_state'] == 'NY']
NY_nonsb_merge_outpt_preview = NY_nonsb_merge_outpt.sample(10)
st.dataframe(NY_nonsb_merge_outpt_preview)

st.subheader('All NY data except StonyBrook (Inpatient)')
NY_nonsb_merge_inpt = nonsb_merge_inpt[nonsb_merge_inpt['provider_state'] == 'NY']
NY_nonsb_merge_inpt_preview = NY_nonsb_merge_inpt.sample(10)
st.dataframe(NY_nonsb_merge_inpt_preview)

#Cleaning columns of interest
NY_nonsb_merge_outpt_nonull = NY_nonsb_merge_outpt[~NY_nonsb_merge_outpt['mortality_national_comparison'].isnull()]
NY_nonsb_merge_inpt_nonull = NY_nonsb_merge_inpt[~NY_nonsb_merge_inpt['mortality_national_comparison'].isnull()]
readmission_hospital_nonull = hospital_info[~hospital_info['readmission_national_comparison_footnote'].isnull()]
effectiveness_hospital_nonull = hospital_info[~hospital_info['effectiveness_of_care_national_comparison_footnote'].isnull()]


# Question 3
st.subheader('Question 3')
st.write('Question3: How does the data for Stony Brook compare to other NY outpatient facilities when looking at the mortality national comparison and outpatient services?')
st.markdown('The pivot tables here show that the Mortality rate for Stony Brook is Above the National Average whereas majority of NY hospitals rank the Same as national average in mortality and their average number of outpatient services (986.006) is much higher than that of Stonybrook (307.538)')

# Stony Brook -> NY (mortality national comparison (MNC)) (Outpatient)
st.subheader('Stonybrook Outpatient Mortality National Comparison Pivot Table')
SB_Outpatient_MNCs_pivot = sb_merge_outpt.pivot_table(index=['provider_id','mortality_national_comparison'],values=['outpatient_services'])
st.dataframe(SB_Outpatient_MNCs_pivot)

st.subheader('Non Stonybrook NY Outpatient Mortality National Comparison Pivot Table')
NY_NonSB_Outpatient_MNCs_pivot = NY_nonsb_merge_outpt_nonull.pivot_table(index=['provider_id','mortality_national_comparison'],values=['outpatient_services'])
st.dataframe(NY_NonSB_Outpatient_MNCs_pivot)
NY_NonSB_Outpatient_MNCs = NY_nonsb_merge_outpt_nonull['mortality_national_comparison'].value_counts().reset_index()
MNC_fig1 = px.bar(NY_NonSB_Outpatient_MNCs, x='index', y='mortality_national_comparison')
st.plotly_chart(MNC_fig1)

Avg_outpt_NY_Services = NY_NonSB_Outpatient_MNCs_pivot['outpatient_services'].mean()
st.header('Total Count of Services from Outpatient: ' )
st.markdown(float(Avg_outpt_NY_Services))

# Question 4
st.subheader('Question 4')
st.write('Question4: How does the data for Stony Brook compare to other NY inpatient facilities when looking at the mortality national comparison and total discharges?')
st.markdown('StonyBrook facilities fall in the Above national average in the mortality comparison and majority of other inpatient NY facilities fall in the Same as national average for mortality rates. The total discharges for Stonybrook (40.2890) is higher than the NY average (35.178)')

# Stony Brook -> NY (mortality national comparison (MNC)) (Inpatient)
st.subheader('StonyBrook Inpatient Mortality National Comparison Pivot Table')
SB_Inpatient_MNCs_pivot = sb_merge_inpt.pivot_table(index=['provider_id','mortality_national_comparison'],values=['total_discharges'])
st.dataframe(SB_Inpatient_MNCs_pivot)

st.subheader('Non Stonybrook NY Inpatient Mortality National Comparison Pivot Table')
NY_NonSB_Inpatient_MNCs_pivot = NY_nonsb_merge_inpt_nonull.pivot_table(index=['provider_id','mortality_national_comparison'],values=['total_discharges'])
st.dataframe(NY_NonSB_Inpatient_MNCs_pivot)
NY_NonSB_Inpatient_MNCs = NY_nonsb_merge_inpt_nonull['mortality_national_comparison'].value_counts().reset_index()
MNC_fig2 = px.bar(NY_NonSB_Inpatient_MNCs, x='index', y='mortality_national_comparison')
st.plotly_chart(MNC_fig2)

Avg_inpt_NY_Discharges = NY_NonSB_Inpatient_MNCs_pivot['total_discharges'].mean()
st.header('Total Count of Discharges from Inpatient Captured: ' )
st.markdown(float(Avg_inpt_NY_Discharges))


# Question 5
st.subheader('Question 5')
st.write('Question5: What is the correlation between effectiveness of care compared to the readmission national comparison?')
st.markdown('Based on the scatterplot, it is difficult to see a direct correlation between effectiveness of care and readmission national comparison data')
st.subheader('Effectiveness of care vs Readmission Comparison Pivot Table')
readmission_pivot = readmission_hospital_nonull.pivot_table(index=['state', 'effectiveness_of_care_national_comparison'],values=['readmission_national_comparison_footnote'])
st.dataframe(readmission_pivot)

# Attempted to create a chart to show the comparison between the two main variables but cannot make it work on Streamlit
df_Chart1 = readmission_hospital_nonull[['effectiveness_of_care_national_comparison', 'readmission_national_comparison_footnote']]
st.dataframe(df_Chart1)
df_Chart1.plot.scatter(x='effectiveness_of_care_national_comparison', y = 'readmission_national_comparison_footnote')


#Question 6 
st.subheader('Question 6')
st.write('Question6: What is the correlation between effectiveness of care compared to the safety of care national comparison?')
st.markdown('Based on the scatterplot, it is difficult to see a direct correlation between effectivesness of care and safety of care national comparison data')
st.subheader('Effectiveness of care vs Safety of Care Pivot Table')
Care_effectiveness_pivot = effectiveness_hospital_nonull.pivot_table(index=['state', 'safety_of_care_national_comparison'],values=['effectiveness_of_care_national_comparison_footnote'])
st.dataframe(Care_effectiveness_pivot)

# Attempted to create a chart to show the comparison between the two main variables but cannot make it work on Streamlit
df_Chart2 = effectiveness_hospital_nonull[['safety_of_care_national_comparison', 'effectiveness_of_care_national_comparison_footnote']]
st.dataframe(df_Chart2)
df_Chart2.plot.scatter(x='safety_of_care_national_comparison', y = 'effectiveness_of_care_national_comparison_footnote')


