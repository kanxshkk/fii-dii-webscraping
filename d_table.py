import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import mysql.connector
from mysql.connector import Error
import re
import sqlalchemy

url = "https://www.cdslindia.com/publications/FIIDailyData.aspx"

r = requests.get(url)

print(r) # if the response is 403 then it means we are not able to access the html content of the page ;respone-> 200
html = r.text
soup=bs(html,"html.parser")


# Find the table body
derivatives_table = soup.find_all('tbody')[1]


derivative_table_values = []
for i in derivatives_table.find_all("tr")[1:]:
    td_tags = i.find_all("td")
    td_val = [y.text for y in td_tags] 
    derivative_table_values.append(td_val)


derivative_table_values = derivative_table_values[1:-1]

for i in range(len(derivative_table_values)):
    derivative_table_values[i][0]=derivative_table_values[0][0]
print(derivative_table_values)

new_column_names = [
    'Reporting Date',
    'Derivative Products',
    'Buy No. of Contracts',
    'Buy Amount in Crore',
    'Sell No. of Contracts',
    'Sell Amount in crore',
    'Open Interest at the end of the date No. of Contracts',
    'Open Interest at the end of the date Amount in Crore'
]

df_derivatives = pd.DataFrame(derivative_table_values,columns = new_column_names)
df_derivatives['Reporting Date'] = pd.to_datetime(df_derivatives['Reporting Date'], format='%d-%b-%Y').dt.strftime('%Y-%m-%d')

print(df_derivatives)

engine = sqlalchemy.create_engine('mysql+pymysql://root:root@localhost:3306/mydb')


try:
    df_derivatives.to_sql("Daily Trends in FII / FPI Derivative Trades", engine, if_exists='append', index=False)
    print("Data inserted successfully!")
except Error as e:
    print(f"Error inserting data into MySQL table: {e}")
    # Handle the error condition

