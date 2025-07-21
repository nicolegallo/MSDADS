#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import packages needed for calculations
import pandas as pd
from scipy.stats import kruskal
from scipy.stats import ttest_ind
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Read in the Excel file
df=pd.read_excel('Health_Insurance_Dataset.xlsx')


# In[2]:


# Keep only the first 1,339 rows (Python is 0-based)
df = df.iloc[:1339]


# In[3]:


# Convert BMI and Charges to numeric data types for calculations
df['bmi'] = pd.to_numeric(df['bmi'])
df['charges'] = pd.to_numeric(df['charges'])


# In[4]:


df.head()


# In[5]:


# Drop rows with missing smoker, bmi, or charges data
df_clean = df.dropna(subset=['smoker', 'bmi', 'charges'])


# In[6]:


df_clean.shape


# In[7]:


# Print the stats for Charges column
df['charges'].describe()


# In[8]:


# Display a histogram of Charges
sns.histplot(data=df, x='charges')


# In[9]:


# Print the stats for BMI column
df['bmi'].describe()


# In[10]:


# Display a histogram of BMI
sns.histplot(data=df, x='bmi')


# In[11]:


# Count values in Smoker column
df.value_counts('smoker')


# In[12]:


# Display a barchart for non-smokers vs smokers
sns.countplot(data=df, x='smoker')


# In[13]:


# Count values in Region column
df.value_counts('region')


# In[14]:


# Display a barchart for count of individuals in each region
sns.countplot(data=df, x='region')


# In[15]:


# Scatterplot to show correlation between BMI and charges
sns.regplot(data=df, x='bmi', y='charges')


# In[16]:


# Calculate Pearson correlation between 'bmi' and 'charges'
correlation = df['bmi'].corr(df['charges'])

# Print the correlation
print("Correlation between BMI and Charges:", correlation)


# In[17]:


# Boxplot to show comparison data between smoker and charges
sns.boxplot(data=df, x='smoker', y='charges')


# In[18]:


# Boxplot to show comparison data between region and charges
sns.boxplot(data=df, x='region', y='charges')


# In[19]:


# Boxplot to show comparison data between smoker and bmi
sns.boxplot(data=df, x='smoker', y='bmi')


# In[20]:


# Boxplot to show comparison data between smoker and bmi
sns.boxplot(data=df, x='smoker', y='charges')


# In[21]:


# Split into smoker and non-smoker groups
smokers = df[df['smoker'] == 'yes']['charges']
non_smokers = df[df['smoker'] == 'no']['charges']


# In[22]:


# Run independent samples t-test (Welch’s t-test for unequal variances)
t_stat, p_value = ttest_ind(smokers, non_smokers, equal_var=False)


# In[23]:


# Output results
print("T-statistic:", t_stat)
print("P-value:", p_value)


# In[ ]:





# In[24]:


# Ensure 'charges' is numeric and drop rows with missing values
df['charges'] = pd.to_numeric(df['charges'])
df = df.dropna(subset=['charges', 'region'])


# In[25]:


# Group charges by region
regions = df['region'].unique()
grouped_charges = [df[df['region'] == region]['charges'] for region in regions]


# In[26]:


# Run the Kruskal-Wallis H-test
h_stat, p_value = kruskal(*grouped_charges)


# In[27]:


# Print results
print("Kruskal-Wallis H-statistic:", h_stat)
print("P-value:", p_value)

