# Pandas take value in arr, dic and show output in table form 
import pandas as pd



# Series: 1-D mean one axis of index axis and each index point one value 

series = pd.Series([1,2,3,4,5],index=['a','b','c','d','e'])
print(series)

# DataFrame
# A DataFrame is a two-dimensional (2D) data structure with two axes:
# Axis 0 (Horizontal) – Represents the rows, which can be accessed using the index.
# Axis 1 (Vertical) – Represents the columns, which can be accessed using the column names.

data = {"Name":['umar','zain','ali'],"Age":[20,30,40]}
df = pd.DataFrame(data)
# print(df)

# selection row
print(df.loc[1])
print(df.loc[df['Age'] < 40])

# selection column 
print(df['Age']) 
print(df[['Name',"Age"]])

# Read file
df = pd.read_csv('data/student_data.csv')
df = pd.read_json('data/employee_data.json')

# basic inspection
print(df.head())
print(df.tail())
print(df.describe())
print(df.shape)
print(df.columns)
print(df.dtypes)

# data manipulation
# add/remove column
df['Bonus'] = df['Salary'] // 100
print(df.drop("Bonus",axis=1,inplace=True))
print(df.drop("Salary",axis=1,inplace=True))
# add/remove row
df.loc[14] = ['umar','IT','AI',67890,'2020-04-09']
print(df)
print(df.drop(14,axis=0,inplace=True))
print(df)
# sort
print(df.sort_values('Salary',ascending=False,inplace=True))
df.sort_values(['Name','Department'],ascending=True,inplace=True)
print(df)


# Grouping and Aggregation
# a. Grouping Data

# Splitting
# Applying
# Combining
group = df.groupby("Department")
print(group["Salary"].mean())

# Aggregation function: helps in applying multiple aggregation functions to columns.
print(group.agg({"Salary" : ["max","mean"]}))

