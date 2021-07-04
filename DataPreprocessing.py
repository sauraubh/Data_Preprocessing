#!/usr/bin/env python
# coding: utf-8

# ## Analyzing borrowers’ risk of defaulting
# 
# Your project is to prepare a report for a bank’s loan division. You’ll need to find out if a customer’s marital status and number of children has an impact on whether they will default on a loan. The bank already has some data on customers’ credit worthiness.
# 
# Your report will be considered when building a **credit scoring** of a potential customer. A ** credit scoring ** is used to evaluate the ability of a potential borrower to repay their loan.

# ### Step 1. Open the data file and have a look at the general information. 

# In[2]:


import pandas as pd
df = pd.read_csv('/datasets/credit_scoring_eng.csv')
print('----Read CSV FILE----')
print(df.head())#read the csv file
print('--------')
import pandas as pd
df = pd.read_csv('/datasets/credit_scoring_eng.csv')
print('----Check General Info----')
df.info()
print('--------')
print('----check statastical summarry of data----')
df.describe()
print('--------')
print('----display function used to  display the table in a more readable format----')
df


#  Conclusion 

# Findings of the table:
# Table has various columns which gives an idea about customers of bank who took loan an by processing this data we can find out future scope for the bank in Marketing, Loan processing and Cleanical client service.
# I believe here the main important columns are: debt, total income, family status and purpose of loan.

# ### Step 2. Data preprocessing

# ### Processing missing values

# In[3]:


print('----look for missing values----')
print(df.isnull())
print('--------')
df['total_income'] = df.groupby('income_type')['total_income'].fillna(value = df['total_income'].median())
print('----fill missing values----')
print(df[df['total_income'].isnull()].count())
print('--------')


# ### Conclusion

# df.info()# check general info of the data such as data_type, rows, column
# df.describe() # used to check statastical summarry of data
# print(df.isnull())#looked for missing values
# print(df[df['total_income'].isnull()].count())#chose this column to find missing values and to replace it as it is important for further calculation.
# 
# Reason behind missing values is might be the slight difference between income type as many of bank customers might have retired or unfortunately lost their jobs which may affected and fluctuated their income. So, that is the reason we filled up missing values by considering income type as strong back point to fill it with mean of the data.

# ### Data type replacement

# In[4]:


df['total_income'] = pd.to_numeric(df['total_income'], errors='coerce')
df.info()
df.loc[df['children'] == -1,'children']= 1#as it seems unrealistick to have kids in negative value or more than 10 so we changed it by using loc
df.loc[df['children'] == 20,'children']= 2


# ### Conclusion

# 

# ### Processing duplicates

# In[5]:


print('----look for duplicates----')
print(df.duplicated().sum())

print('--------')
print('---- delete  duplicates----')
df = df.dropna().reset_index(drop = True)
df[df.duplicated()]
print('--------')
df


# ### Conclusion

# 

# ### Categorizing Data

# In[6]:


Kids_data = df['children'].unique()

def kids_cat(kids_data):
    if kids_data == 0:
        return 'Have Kids'
    else:
        return 'No Kids'
df['kids_data'] = df['children'].apply(kids_cat)

df['total_income'] = df['total_income'].astype('float')
 
def income_data(total_income):
    """
    The function returns the income category according to the total_income value, using the following rules:
Low-income - under 10,000
Lower-middle income - 10,001 - 20,000
Upper-middle income - 20,001 - 30,000
High income > 30,001
    """
 
    if total_income <= 10000:
        return 'low_income'
    if total_income <= 20000:
        return 'lower_mid_income'
    if total_income <= 30000:
        return 'upper_mid_income'
    return 'very_high_income'
 
df['income_data'] = df['total_income'].apply(income_data)
#print(df.head())
purpose_data = df['purpose'].unique().tolist()

def purpose_cat(purpose_data):
    if 'car' in purpose_data:
        return 'car'
    elif "hous" in purpose_data:
        return 'house'
    elif 'educ' in purpose_data:
        return "education"
    elif 'univers' in purpose_data:
        return 'education'
    elif 'wedding' in purpose_data:
        return 'wedding'
    elif 'real' in purpose_data:
        return 'real estate'
    elif 'estat' in purpose_data:
        return 'real estate'
    elif 'building' in purpose_data:
        return 'building'
    else:
        return 'other'
df['purpose_data'] = df['purpose'].apply(purpose_cat)
print('----Categorized data according to income level, purpose of loan and number of kids----')
df


# ### Conclusion

# 

# ### Step 3. Answer these questions

# - Is there a relation between having kids and repaying a loan on time?

# In[23]:



print('----created kids pivot table to answer first question----')
print('----total is number of percentage of debts from debt free loans----')
kids_data1= df.pivot_table(index = 'kids_data', values= 'debt', aggfunc = ['sum','count']).reset_index()
kids_data1['total'] = (kids_data1['sum'] / kids_data1['count'] * 100).round(2)
print(kids_data1)
print('--------')


# ### Conclusion

# As per output we got we can conclude the customer with no kids have more regular in loan payment than customer with kids:
# debt_data  kids_data  Not Regular  Regular      total  % of ratio
# 0          Have Kids         1063    13086   8.123185        8.12
# 1            No Kids          678     6698  10.122425       10.12

# - Is there a relation between marital status and repaying a loan on time?

# In[25]:


family_pivot = df.pivot_table(values="debt", index= "family_status", aggfunc= ['sum', 'count']) 
family_pivot['total'] = (family_pivot['sum'] / family_pivot['count'] * 100).round(2)
print('----created family pivot table to answer second question----')
print('----total is number of percentage of debts from debt free loans----')
print(family_pivot)
print('--------')


# ### Conclusion

# As per output we got we can conclude the customer with no marriage status and civil partnership status have more regular in loan payment than customer with other status:
# debt_data          Not Regular  Regular      total  % of ratio
# family_status                                                 
# civil partnership          388     3789  10.240169       10.24
# divorced                    85     1110   7.657658        7.66
# married                    931    11449   8.131715        8.13
# unmarried                  274     2539  10.791650       10.79
# widow / widower             63      897   7.023411        7.02
# 

# - Is there a relation between income level and repaying a loan on time?

# In[26]:


income_pivot = df.pivot_table(values="debt", index= "income_data", aggfunc= ['sum', 'count']) 
income_pivot['total'] = (income_pivot['sum'] / income_pivot['count'] * 100).round(2)
print('----created income pivot table to answer third question----')
print('----total is number of percentage of debts from debt free loans----')
print(income_pivot)
print('--------')


# Conclusion

# As per output we got we can conclude the customer with lower_mid_income status and upper_mid_income status have more regular in loan payment than customer with other status:
# debt_data          Not Regular  Regular      total  % of ratio
# debt_data       income_data  Not Regular  Regular     total  % of ratio
# 0                low_income           58      868  6.682028        6.68
# 1          lower_mid_income          550     5893  9.333107        9.33
# 2          upper_mid_income          697     7540  9.244032        9.24
# 3          very_high_income          436     5483  7.951851        7.95

# - How do different loan purposes affect on-time repayment of the loan?

# In[28]:


purpose_pivot = df.pivot_table(values="debt", index= "purpose_data", aggfunc= ['sum', 'count']) 
purpose_pivot['total'] = (purpose_pivot['sum'] / purpose_pivot['count'] * 100).round(2)
print('----created purpose pivot table to answer fourth question----')
print(purpose_pivot)
print('--------')


# ### Conclusion

# As per output we got we can conclude the customer with car loan purpose and education loan purpose have more regular in loan payment than customer with other status:
# debt_data purpose_data  Not Regular  Regular      total  % of ratio
# 0             building           54      566   9.540636        9.54
# 1                  car          403     3912  10.301636       10.30
# 2            education          370     3652  10.131435       10.13
# 3                house          256     3564   7.182941        7.18
# 4                other          136     1786   7.614782        7.61
# 5          real estate          336     4142   8.112023        8.11
# 6              wedding          186     2162   8.603145        8.60

# ### Step 4. General conclusion

# By Analysing all the data given in the file. we can add all our step by step conclusion and create uniform conclusion which is:
# The Customers who has taken loan on the basis of [purpose = car and eduction, income level = lower mid or upper mid] without married and civil relationship who is having No Kids are the most efficient customers regarding credit scoring.
# To evaluate more I have attached full code downwords in new cell by combining all the task please have look.

# ### Project Readiness Checklist
# 
# Put 'x' in the completed points. Then press Shift + Enter.

# - [x]  file open;
# - [x]  file examined;
# - [x]  missing values defined;
# - [x]  missing values are filled;
# - [x]  an explanation of which missing value types were detected;
# - [x]  explanation for the possible causes of missing values;
# - [x]  an explanation of how the blanks are filled;
# - [x]  replaced the real data type with an integer;
# - [x]  an explanation of which method is used to change the data type and why;
# - [x]  duplicates deleted;
# - [x]  an explanation of which method is used to find and remove duplicates;
# - [x]  description of the possible reasons for the appearance of duplicates in the data;
# - [x]  data is categorized;
# - [x]  an explanation of the principle of data categorization;
# - [x]  an answer to the question "Is there a relation between having kids and repaying a loan on time?";
# - [x]  an answer to the question " Is there a relation between marital status and repaying a loan on time?";
# - [x]   an answer to the question " Is there a relation between income level and repaying a loan on time?";
# - [x]  an answer to the question " How do different loan purposes affect on-time repayment of the loan?"
# - [x]  conclusions are present on each stage;
# - [x]  a general conclusion is made.
