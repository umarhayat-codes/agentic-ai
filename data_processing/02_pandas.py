# Pandas take value in arr, dic and show output in table form 
from matplotlib.dates import rrule
import pandas as pd



# Series: 1-D mean one axis of index axis and each index point one value 

# series = pd.Series([1,2,3,4,5],index=['a','b','c','d','e'])
# print(series)

# DataFrame
# A DataFrame is a two-dimensional (2D) data structure with two axes:
# Axis 0 (Horizontal) – Represents the rows, which can be accessed using the index.
# Axis 1 (Vertical) – Represents the columns, which can be accessed using the column names.

# data = {"Name":['umar','zain','ali'],"Age":[20,30,40]}
# df = pd.DataFrame(data)
# print(df)

# selection row
# print(df.loc[1])
# print(df.loc[df['Age'] < 40])

# selection column 
# print(df['Age']) 
# print(df[['Name',"Age"]])

# Read file
# df = pd.read_csv('data/student_data.csv')
# df = pd.read_json('data/employee_data.json')

# basic inspection
# print(df.head())
# print(df.tail())
# print(df.describe())
# print(df.shape)
# print(df.columns)
# print(df.dtypes)

# data manipulation
# add/remove column
# df['Bonus'] = df['Salary'] // 100
# print(df.drop("Bonus",axis=1,inplace=True))
# print(df.drop("Salary",axis=1,inplace=True))
# add/remove row
# df.loc[14] = ['umar','IT','AI',67890,'2020-04-09']
# print(df)
# print(df.drop(14,axis=0,inplace=True))
# print(df)
# sort
# print(df.sort_values('Salary',ascending=False,inplace=True))
# df.sort_values(['Name','Department'],ascending=True,inplace=True)
# print(df)


# Grouping and Aggregation
# a. Grouping Data

# Splitting
# Applying
# Combining
# group = df.groupby("Department")
# print(group["Salary"].mean())

# Aggregation function: helps in applying multiple aggregation functions to columns.
# print(group.agg({"Salary" : ["max","mean"]}))


#  Merging and Joining Data
# a. Concatenation it only concat such as stack
# df1 = pd.DataFrame({"ID": [1, 2, 3], "Name": ["A", "B", "C"]})
# df2 = pd.DataFrame({"ID": [4, 5, 6], "Name": ["D", "E", "F"]})
# result = pd.concat([df1,df2], ignore_index=True)
# print(result)
# b. Merging DataFrames it merge same value of column
# df1 = pd.DataFrame({"ID": [1, 2, 3], "Salary": [1000, 2000, 3000]})
# df2 = pd.DataFrame({"ID": [1, 2, 4], "Bonus": [100, 200, 400]})
# merge_df = df1.merge(df2,on="ID",how="inner") # merge and show value of ID which is same 
# merge_df = df1.merge(df2,on="ID",how="outer") # merge and show all value of ID which is same or not 
# print(merge_df)


# url = "https://huggingface.co/datasets/jahjinx/IMDb_movie_reviews/resolve/main/IMDB_test.csv"
# url = "https://huggingface.co/datasets/xinqiyang/tradingview_msn_financial_news_1k/resolve/main/tradingview_msn_financial_news_1k.csv"
# url = "https://huggingface.co/datasets/yymYYM/stock_trading_QA/resolve/main/stock_trading_qa_pairs_processed.csv"
# url = "https://huggingface.co/datasets/jyanimaulik/yahoo_finance_stock_market_news/resolve/main/final_formatted_data.csv"
# url = "https://huggingface.co/datasets/abhinavsarkar/delhi_air_quality_feature_store_unprocessed.csv/resolve/main/delhi_air_quality_feature_store_unprocessed.csv"

# url = "https://huggingface.co/datasets/antitheft159/_908_electricity_demands/resolve/main/electricity.csv"
# url = "https://huggingface.co/datasets/tablegpt/AppleStockData2025/resolve/main/apple_stock.csv"

#  Date      Open      High       Low     Close  Adj Close     Volume

import pandas as pd
import matplotlib.pyplot as plt

# URL of the dataset
url = "https://huggingface.co/datasets/Ammok/apple_stock_price_from_1980-2021/resolve/main/AAPL.csv"

# Read the dataset
df = pd.read_csv(url)
print(df)


# Convert the Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Set Date as the index
df.set_index('Date', inplace=True)

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(df['Close'], label="Closing Price", color='blue')

# Adding labels and title
plt.title("Apple Stock Prices")
plt.xlabel("Date")
plt.ylabel("Price (USD)")

# Show grid and legend
plt.grid(True)
plt.legend()

# Save the plot to a file (e.g., as a PNG image)
plt.savefig("apple_stock_plot_new.png")

# Optionally, you can also close the plot if you're done
plt.close()

df['50-day MA'] = df['Close'].rolling(window=50).mean()
df['200-day MA'] = df['Close'].rolling(window=200).mean()


plt.figure(figsize=(10,5))
plt.plot(df.index, df['Close'], label="Closing Price", color='blue', alpha=0.5)
plt.plot(df.index, df['50-day MA'], label="50-Day Moving Average", color='red')
plt.plot(df.index, df['200-day MA'], label="200-Day Moving Average", color='green')
plt.title("Apple Stock Price with Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid()
plt.savefig("apple_stock_plot_operation.png")
# df['Date'] = pd.to_datetime(df['Date'])
# df.set_index('Date',inplace=True)



# print(df.columns)
# print(df.describe)