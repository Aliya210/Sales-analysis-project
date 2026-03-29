#import libraries
import pandas as pd
#sqlite3 is ready made tool inside python,, to use other than sqlite3 we need external tools installed,for sqlite no setup headache
import sqlite3

#load data
df=pd.read_csv("sales.csv")
print(df["order_date"].head(10))

conn=sqlite3.connect("sales.db")
print("databse created")

#clean data by removing comma
df["sales"]=df["sales"].str.replace(",", "")

#converting sales string data to numeric data in order to perform mathematical operations
df["sales"]=pd.to_numeric(df["sales"])

#store data in sql,, store df (your data)in sales_table inside conn databse(sqlite3), index=false means dont store row numbers
df.to_sql("sales_table",conn, if_exists="replace", index=False)
print("Data stored in sql")

#run queries
query="select SUM(sales) as total_sales FROM sales_table"
result=pd.read_sql(query, conn)
print(result)

#to check the data type of sales column
print(df["sales"].dtype)

#identify top selling products upto 5 records(limit 5)
query="""select product_name, sum(sales) as total_sales from sales_table group by product_name order by total_sales desc limit 5"""
top_products=pd.read_sql(query, conn)
print(top_products)

df["order_date"]=pd.to_datetime(df["order_date"], format="mixed", dayfirst=True)
df.to_sql("sales_table", conn, if_exists="replace", index=False)
query="""select strftime('%m',order_date) as month, SUM(sales) as total_sales from sales_table group by month order by month"""
monthly_sales=pd.read_sql(query, conn)
print(monthly_sales)

#compared regional perfromance
query="""select region, sum(sales) as total_sales from sales_table group by region order by total_sales desc limit 1"""
r_performance=pd.read_sql(query, conn)
print(r_performance)

print("no of rows and cols:", df.shape)
print("no of columns:", len(df.columns))
print("no of rows:", len(df))
print(df)
print(df.columns)

import matplotlib.pyplot as plt

#DASHBOARD to create multiple graph in one screen we use subplots
# create figure
plt.figure(figsize=(12,5))

# 📈 1. Monthly Sales Trend
plt.subplot(1,2,1)   #rows*cols>=number of graphs
plt.plot(monthly_sales["month"], monthly_sales["total_sales"])
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")

# 🏆 2. Top Products
plt.subplot(1,2,2)
plt.bar(top_products["product_name"], top_products["total_sales"])
plt.title("Top 5 Products")
plt.xlabel("Product Name")
plt.ylabel("Sales")
plt.xticks(rotation=45)

# adjust layout
plt.tight_layout()

# show dashboard
plt.show()