#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np


# In[3]:


# Read in the CSV file
df=pd.read_csv('Employee_Turnover_Dataset.csv')


# In[4]:


# Count how many duplicates in dataset
df.duplicated().sum()


# In[5]:


df = df.drop_duplicates()


# In[6]:


# Count how many duplicates in dataset; after running df.drop_duplicates()
df.duplicated().sum()


# In[7]:


for col in df.select_dtypes(include='object').columns:
    print(col)
    print(df[col].value_counts(dropna=False))


# In[8]:


print(df['JobRoleArea'].value_counts(dropna=False))


# In[9]:


df['JobRoleArea'] = df['JobRoleArea'].str.strip().str.title()


# In[10]:


# Replace inconsistent entries with standardized versions
df['JobRoleArea'] = df['JobRoleArea'].replace({
    'Humanresources': 'Human Resources',
    'Human_Resources': 'Human Resources',
    'Information_Technology': 'Information Technology',
    'Informationtechnology': 'Information Technology'
})


# In[11]:


for col in df.select_dtypes(include='object').columns:
    print(col)
    print(df[col].value_counts(dropna=False))


# In[12]:


# Count how many missing values in dataset
df.isnull().sum()


# In[13]:


# Use .fillna() to insert a median value into missing values
df['NumCompaniesPreviouslyWorked'] = df['NumCompaniesPreviouslyWorked'].fillna(df['NumCompaniesPreviouslyWorked'].median())

# Check missing values
df.isnull().sum()


# In[14]:


# Use .fillna() to insert a median value into missing values
df['AnnualProfessionalDevHrs'] = df['AnnualProfessionalDevHrs'].fillna(df['AnnualProfessionalDevHrs'].median())

# Check missing values
df.isnull().sum()


# In[15]:


# Use .fillna() to insert a mode value into missing values
df['TextMessageOptIn'] = df['TextMessageOptIn'].fillna(df['TextMessageOptIn'].mode()[0])

# Check missing values
df.isnull().sum()


# In[16]:


# Show negative DrivingCommuterDistance data
df[df['DrivingCommuterDistance'] < 0]


# In[17]:


# Change negative DrivingCommuterDistance to positive with .abs()
df['DrivingCommuterDistance'] = df['DrivingCommuterDistance'].abs()

# Count negative DrivingCommuterDistance data; should now be 0
((df['DrivingCommuterDistance']) < 0).sum()


# In[18]:


# Show negative DrivingCommuterDistance data
df[df['DrivingCommuterDistance'] < 0]


# In[19]:


# Show 'HourlyRate' with $ and whitespace
print(df['HourlyRate '])

# Strip whitespace from column names
df.columns = df.columns.str.strip()


# In[20]:


# Clean HourlyRate
df['HourlyRate'] = df['HourlyRate'].astype(str).str.replace(r'[^0-9.]', '', regex=True).astype(float)

# Show 'HourlyRate' after cleaning
print(df['HourlyRate'])


# In[21]:


# Annual Salary showing negative values
df[df['AnnualSalary'] < 0]


# In[22]:


# Only recalculate for hourly employees
hourly_mask = df['CompensationType'].str.lower() == 'salary'
df.loc[hourly_mask, 'AnnualSalary'] = df.loc[hourly_mask, 'HourlyRate'] * df.loc[hourly_mask, 'HoursWeekly'] * 52

# Round to 2 decimal places
df['AnnualSalary'] = df['AnnualSalary'].round(2)

# Print pay metrics to confirm changes
print(df[['CompensationType', 'HourlyRate', 'HoursWeekly', 'AnnualSalary']].head(10))


# In[23]:


# Print any negative Annual Salary after fixing calculation
df[df['AnnualSalary'] < 0]


# In[24]:


# Print PaycheckMethod before standardizing
print(df['PaycheckMethod'].value_counts())


# In[25]:


# Convert to lowercase and strip whitespace to catch all variations
df['PaycheckMethod'] = df['PaycheckMethod'].str.strip().str.lower()


# In[26]:


# Replace inconsistent entries with standardized versions
df['PaycheckMethod'] = df['PaycheckMethod'].replace({
    'mailed check': 'Mail Check',
    'mail_check': 'Mail Check',
    'mailedcheck': 'Mail Check',
    'mail check': 'Mail Check',
    'directdeposit': 'Direct Deposit',
    'direct_deposit': 'Direct Deposit',
    'direct deposit': 'Direct Deposit'
})


# In[27]:


# Print PaycheckMethod with standardized version
print(df['PaycheckMethod'].value_counts())


# In[28]:


for col in df.select_dtypes(include='object').columns:
    print(col)
    print(df[col].value_counts(dropna=False))


# In[29]:


# Use IQR to find outliers in DrivingCommuterDistance
Q1 = df['DrivingCommuterDistance'].quantile(0.25)
Q3 = df['DrivingCommuterDistance'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Print lower and upper bounds to see range
print("Lower bound is: ", lower_bound)
print("Upper bound is: ", upper_bound)

# Show outlier rows
df[(df['DrivingCommuterDistance'] < lower_bound) | (df['DrivingCommuterDistance'] > upper_bound)]


# In[30]:


# Outlier capping using .clip()
df['DrivingCommuterDistance'] = df['DrivingCommuterDistance'].clip(lower=lower_bound, upper=upper_bound)


# In[31]:


# Show outlier rows after .clip() method
df[(df['DrivingCommuterDistance'] < lower_bound) | (df['DrivingCommuterDistance'] > upper_bound)]


# In[32]:


# Print lower and upper bounds & Min and Max to see range after .clip() method
print("Lower bound is: ", lower_bound)
print("Upper bound is: ", upper_bound)

print("Min:", df['DrivingCommuterDistance'].min())
print("Max:", df['DrivingCommuterDistance'].max())


# In[33]:


# Save cleaned dataset
df.to_csv("Employee_Turnover_Cleaned.csv", index=False)

