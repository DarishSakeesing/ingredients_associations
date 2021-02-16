# Ingredients Associations from 11 Different Cuisines.

## Introduction:
In this repository, there is the code that I wrote to collect recipe data from 11 different types of cuisines from yummly.com and analyze which ingredients had the strongest associations.

## Motivation:
This project comes at the end of the 'Data Analysis with Python' module at the NYC Datascience Academy. I aim to explore how supermarket chains such as Morton Williams stock their supplies based on the ethnicity of the market it is based in.
Therefore, I collected data on different cuisines such as America, Chinese, Indian and many more and looked at what ingredients were most popular for each of them or any combinations of them.

## Methodology:
After typing a query in the Yummly search bar, the query is incorporated into the url and a request is sent to the Yummly server. 
The data is then sent to your computer in the form of a JSON. I therefore, iteratively constructed multiple urls and sent requests 
to the yummly server in order to get the appropriate JSON file.

I transformed the data in the appropriate format and run an FPGrowth Algorithm on it that constructs the metrics needed.


