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

soup=bs(r.text,"html.parser")

br_tags = soup.find_all('br')
# Remove <br/> tags
for br_tag in br_tags:
    br_tag.unwrap()

# Get the modified HTML string
modified_html = str(soup)


investments_table=soup.find("table")
row_headers=[]
r_head = investments_table.find_all("tr",class_ = "head")

row_head=r_head[0].text
print(row_head,type(row_head))

row_headers=row_head.strip().split("\n")

for i in range(len(row_headers)):
    row_headers[i]=row_headers[i].strip()
    row_headers[i]=row_headers[i].rstrip("\r")
    if row_headers[i]=="GrossPurchases" or row_headers[i]=="GrossSales":
        row_headers[i]+="(Rs Crore)"
row_headers[-2]+=row_headers[-1]
row_headers[-4]+=row_headers[-3]
row_headers[-6]+=row_headers[-5]
    

final_row_headers = [i for i in row_headers if (i != "(Rs Crore)" and i != 'US($) million' and i != "(1 USD TO INR)*"  )]


print("final_row_headers:",final_row_headers)

investments_table_values = []
for i in investments_table.find_all("tr")[1:]:
    td_tags = i.find_all("td")
    td_val = [y.text for y in td_tags] 
    investments_table_values.append(td_val)


investments_table_values = investments_table_values[:-1]
for i in investments_table_values:
    print(i)

final_investment_table_values = []
for i in investments_table_values:
    if len(i)==8:
        date,d_e,data,conv=i[0:1],i[1:2],i[2:-1],i[-1:]
    elif len(i)==6:
        d_e=i[0:1]
        data=i[1:]
    elif len(i)==5:
        data=i
    final_investment_table_values.append(date+d_e+data)

date=list(date)
conv=list(conv)
print(date,conv)
conv_table = {
    "Reporting Date": date,
    "Conversion(1 USD TO INR)*": conv
}

df_investments = pd.DataFrame(final_investment_table_values,columns = final_row_headers[:-1])
df_conversion = pd.DataFrame(conv_table)
print(df_investments)
print(df_conversion)

engine = sqlalchemy.create_engine('mysql+pymysql://root:root@localhost:3306/mydb')
df_investments['Reporting Date'] = pd.to_datetime(df_investments['Reporting Date'], format='%d-%b-%Y').dt.strftime('%Y-%m-%d')
df_conversion['Reporting Date'] = pd.to_datetime(df_conversion['Reporting Date'], format='%d-%b-%Y').dt.strftime('%Y-%m-%d')

try:
    df_investments.to_sql("Daily Trends in FII / FPI Investments", engine, if_exists='append', index=False)
    df_conversion.to_sql("Conversion value",engine, if_exists='append', index=False)
    print("Data inserted successfully!")
except Error as e:
    print(f"Error inserting data into MySQL table: {e}")
    # Handle the error condition

