# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 17:23:42 2015

@author: Laetitia
"""

import pandas as pd
import seaborn as sns
from datetime import datetime
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from matplotlib.figure import Figure

train_df=pd.read_csv("train.csv")

train_df.head()

## Dictionary by Marie-Laura 
# aggregate crimes into several categories : it is an arbitrary choice but still very useful
crime_dict = {
    'THEFT':['LARCENY/THEFT','VEHICLE THEFT','STOLEN PROPERTY','RECOVERED VEHICLE'],
    'ROBBERY':['ROBBERY'],
    'DRUGS':['DRUG/NARCOTIC'],
    'ALCOHOL':['DRUNKENNESS', 'DRIVING UNDER THE INFLUENCE','LIQUOR LAWS',],
    'VIOLENCE':['WEAPON LAWS','ASSAULT', 'OTHER OFFENSES','FAMILY OFFENSES'],
    'FRAUD':['FRAUD', 'FORGERY/COUNTERFEITING','EMBEZZLEMENT', 'BAD CHECKS'], 
    'DEATH':['SUICIDE'], 
    'VANDALISM':['VANDALISM'],
    'FIRE':['ARSON'],
    'PROPERTY': ['WARRANTS', 'TRESPASS','BURGLARY', 'TREA'],
    'SEX':['PORNOGRAPHY/OBSCENE MAT', 'PROSTITUTION','SEX OFFENSES FORCIBLE'],
    'MISSING':['MISSING PERSON', 'KIDNAPPING', 'RUNAWAY'],
    'MISCONDUCT':['LOITERING', 'DISORDERLY CONDUCT', 'SEX OFFENSES NON FORCIBLE', 'SUSPICIOUS OCC'],
    'CORRUPTION':['BRIBERY'],
    'OTHER':['GAMBLING','SECONDARY CODES','EXTORTION'],
    'NON-CRIMINAL':['NON-CRIMINAL']
    }


# get list of categories of crimes
crime_values = []
for i in range(len(crime_dict.keys())):
    crime_values += list(crime_dict.values())[i]
print(crime_values) 
print(len(crime_values))

## We have gathered all the 39 categories in the dictionary
len(train_df['Category'].unique())

# Crime dictionary inverse
crime_dict_inv={}
for key in list(crime_dict.keys()):
    for value in crime_dict[key]:
        crime_dict_inv[value]=key

# add column to data frame
train_df['agg_Category'] = train_df['Category'].map(crime_dict_inv)

# add year, month, day, hour column
def parse_date(date):
    d=datetime.strptime(date,"%Y-%m-%d %H:%M:%S")
    year=d.year
    month=d.month
    day=d.day
    hour=d.hour
    return year, month, day, hour

train_df['year'], train_df['month'], train_df['day'], train_df['hour']=zip(*train_df['Dates'].apply(parse_date))


# Plot 1
fig = Figure()
ax = fig.add_axes([0.1, 0.1, 0.5, 0.5])
sns.set_palette("hls", 16)

for i, c in enumerate(crime_dict.keys()):
    df = train_df[train_df['agg_Category']==c].groupby('year').count()['Category']
    df=df[df.index<2015]
    df[:2015].plot(label=c)
    
ax.set_title('Number of crimes per category')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()

# Plot 2
fig = Figure(figsize=(8,6))
ax=fig.add_subplot(1,1,1)
sns.set_palette("hls", 7)

for i, c in enumerate(crime_dict.keys()):
    df = train_df[train_df['agg_Category']==c].groupby('year').count()['Category']
    if df.mean()>2500:
        df=df[df.index<2015]
        df[:2015].plot(label=c)

ax.set_title('Number of crimes per category for the 7 most frequent categories')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()

# Plot 3
df=pd.DataFrame()
for i, c in enumerate(crime_dict.keys()):
    df[c] = train_df[train_df['agg_Category']==c].groupby('PdDistrict').count()['Category']

fig = Figure(figsize=(8,6))
ax=fig.add_subplot(1,1,1)
sns.set_palette("hls", 16)
df.plot(kind='bar', stacked=True)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()
