# python-webscraping-sqlite-database-flask-mortgage-rates

Mortgage rates have been increasing at an alarming pace since the beginning of 2022. I have been following them quite closely and watching the trends pretty much on a daily basis. I wanted to build a program/script which fetches mortage interest rates from the internet and visualize them on a webpage. 

I decided to use python to accomplish this task since I have some background on the language.

In this demonstration, I use python to extract mortgage interest rates from a webpage (webscraping), then store the results in an sqlite database, and visualize trends on a webpage using python Flask. I also scrape the S & P index and visualize it's trend just below the mortgage rate trend to see how they correlate. I used the plotly python library for visualization since it provides interactive plots which make for an improved user experience.

I scrape the mortgage rates from this website:
https://www.nerdwallet.com/mortgages/mortgage-rates

I use this website to get the S & P index:
https://fred.stlouisfed.org/series/SP500

This is what the visualization looks like:

![My Image](static/img/picture_rate_trend.PNG)
![My Image](static/img/picture_snp_trend.PNG)