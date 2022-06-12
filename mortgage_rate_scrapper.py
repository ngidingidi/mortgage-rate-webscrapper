# -*- coding: utf-8 -*-
"""
Created on Fri May 20 18:15:16 2022

@author: sicelo
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from flask import Flask, render_template, send_from_directory
import json
import plotly
import plotly.express as px
import sqlite3


# Send HTTP request entire web page contents

response = requests.get('https://www.nerdwallet.com/mortgages/mortgage-rates')
if (response.status_code) == 200:
    print('----Successfully received HTTP response----------')
else:
    print('----Did not successfully receive HTTP response------')

# Parse the html from the webpage

soup = BeautifulSoup(response.text, 'html.parser')

# Inspect the webpage and find something unique about the data you want to pull

# Extract hyperlinks within a webpage

#print(soup.find_all('a'))

# Right click and inspect html page to extract div containers with corresponding class attribute

# Extract the datetime

for content in soup.findAll('time'):
        if content.has_attr('datetime'):
            page_listed_date_string = content['datetime']

page_listed_date = datetime.strptime(page_listed_date_string, "%Y-%m-%d")
print(page_listed_date)

rate_div = soup.find_all('div', class_='_13J6Bq')

# Remove the % sign after the published mortgage rate

for content in rate_div:
    rate = content.text[:5]
print(rate)

# Create dataframe 

data = {
  "date": [page_listed_date],
  "mortgage_rate": [rate]
}

#load data into a DataFrame object. Save to csv the first time you create it
table_rates = pd.DataFrame(data)
#table_rates.to_csv('mortgage_rates.csv', index=False)

# df = pd.read_csv("mortgage_rates.csv", parse_dates=["date"])

# Connect to SQLite database
conn = sqlite3.connect('mortgage_rate_database.db')

# Create a cursor object
cur = conn.cursor()
df = pd.read_sql('SELECT * FROM mortgage_rates',
            conn,
            parse_dates=["date"])
print(df.dtypes)

for index, row in df.iterrows():
  if (row["date"] == page_listed_date):
      print('The dataframe already contains the page listed date.')
      df.drop([index],axis='index', inplace=True)
      df_updated = pd.concat([df,table_rates])
      try:
          df_updated.drop('Unnamed: 0', axis=1, inplace=True)
      except:
          pass
      
  else:
      print('The dataframe does not contain the page listed date. We will add this date.')
      df_updated = pd.concat([df,table_rates])
      try:
          df_updated.drop('Unnamed: 0', axis=1, inplace=True)
      except:
          pass

# Save the updated dataframe
df_updated.to_csv('mortgage_rates.csv', index=False)
  
# Write the data to a sqlite table
df_updated.to_sql('mortgage_rates', conn, if_exists='replace', index=False)
  

# Fetch and display result
for row in cur.execute('SELECT * FROM mortgage_rates'):
    print(row)
    
# Close connection to SQLite database
conn.close()

# Begin flask app

app = Flask(__name__, static_folder='static')

@app.route('/', methods = ['GET'])
def index():
    """
    Returns graph showing mortgage rates trend
    """
    #df = pd.read_csv('mortgage_rates.csv', parse_dates=["date"])
    
    df = df_updated
    df['mortgage_rate'] = pd.to_numeric(df['mortgage_rate'],errors = 'coerce')
    df.sort_values(by='date', ascending=True, inplace=True)
    
    fig = px.scatter(df, 
                     x=df['date'], 
                     y=df['mortgage_rate'],
                     width=1000, height=580)
    print(df.shape)
    fig.update_xaxes(categoryorder='category ascending')
    fig.update_traces(mode='lines+markers', 
                      marker_line_width=2, marker_size=10)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('index.html', graphJSON=graphJSON)

@app.route('/table', methods = ['GET'])
def table():
    """
    Returns table showing mortgage rates over time
    """
    df = df_updated
    df['mortgage_rate'] = pd.to_numeric(df['mortgage_rate'],errors = 'coerce')
    df['mortgage_rate'] = df['mortgage_rate'].round(3)
    df.sort_values(by='date', ascending=True, inplace=True)
    
    return render_template('table_rates.html', table=df)

@app.route('/<path:file_path>')
def send_file(file_path):
    return send_from_directory(app.static_folder, file_path, as_attachment=False)


if __name__ == "__main__":
    app.run(debug=True)
