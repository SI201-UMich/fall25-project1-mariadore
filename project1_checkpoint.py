# Project 1 Checkpoint
#  Name: Maria Dore
# Student ID: 9490 5426
# Email: mdore@umich.edu
#Used Chat GPT to help with structure and general debugging
# Dataset: Sample Superstore Dataset
# Columns: Category, Region, Profit, Sales, Ship Mode
# Calculations:
# 1. Average Profit per Category in each Region
# 2. Percentage of orders shipped with "Second Class" that had Sales > 500

import csv

def read_csv_file(filename):
    #reads dataset and returns list of dictionaries
    data= []
    with open(filename,'r') as f:
        reader=csv.Dictreader(f)
        for row in reader:
            data.append(row)
    return data
              

def calculate_average_profit(data):
    #calculation 1: average profit per category in each region
    pass

def calculate_shipping_percentage(data):
    #calculation 2: r=percentage of orders shipped with 'second class' and sales> 500
    pass

def write_to_file(results, filename):
    #writes results to a csv file
    pass