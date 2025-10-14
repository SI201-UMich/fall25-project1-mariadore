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
import kagglehub
import os

def read_csv_file(filename):
    #reads dataset and returns list of dictionaries
    data= []
    with open(filename,'r', encoding='utf-8') as f:
        reader=csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data
              

def calculate_average_profit(data):
    #calculation 1: average profit per category in each region
    results={}
    for row in data:
        region=row['Region']
        category= row['Category']
        profit= float(row['Profit'])

        if region not in results:
            results[region]={}
        if category not in results[region]:
            results[region][category]=[]
        results[region][category].append(profit)
    
    avg_results={}
    for region, categories in results.items():
        avg_results[region]={}
        for category, profits in categories.items():
            avg_results[region][category]= sum(profits)/len(profits)
    return avg_results


def calculate_shipping_percentage(data):
    #calculation 2: r=percentage of orders shipped with 'second class' and sales> 500
    total_orders= 0
    qualifying_orders=0

    for row in data:
        total_orders += 1
        if row['Ship Mode'].strip().lower() == 'second class' and float(row['Sales'])>500:
            qualifying_orders+=1

    if total_orders == 0:
        return 0
    return (qualifying_orders / total_orders) *100
    

def write_to_file(results, filename):
    #writes results to a csv file
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Region', 'Category', 'Average Profit'])
        for region, categories in results.items():
            for category, avg_profit in categories.items():
                writer.writerow([region, category, round(avg_profit, 2)])


path = kagglehub.dataset_download("bravehart101/sample-supermarket-dataset")
print("Path to dataset files:", path)

print("Files in dataset folder:", os.listdir(path))
csv_file=os.path.join(path, "SampleSuperstore.csv")
data=read_csv_file(csv_file)
avg_profit_results = calculate_average_profit(data)
shipping_percentage = calculate_shipping_percentage(data)

# Save and display results
write_to_file(avg_profit_results, "results.csv")
print("Results written to results.csv")
print("Second Class orders with Sales > 500:", round(shipping_percentage, 2), "%")

import unittest
class TestProject1(unittest.TestCase):
    def test_calculate_average_profit_normal(self):
        data= [
            {'Region': 'East', 'Category': 'Furniture', 'Profit': '100'},
            {'Region': 'East', 'Category': 'Furniture', 'Profit': '200'},
            {'Region': 'West', 'Category': 'Technology', 'Profit': '300'}
        ]
        result= calculate_average_profit(data)
        self.assertAlmostEqual(result['East']['Furniture'], 150.0)
        self.assertAlmostEqual(result['West']['Technology'], 300.0)

    def test_calculate_average_profit_multiple_categories(self):
        data = [
            {'Region': 'South', 'Category': 'Furniture', 'Profit': '50'},
            {'Region': 'South', 'Category': 'Office Supplies', 'Profit': '150'}
        ]            
        result = calculate_average_profit(data)
        self.assertAlmostEqual(result['South']['Furniture'], 50.0)
        self.assertAlmostEqual(result['South']['Office Supplies'], 150.0)

    def test_calculate_agerage_profit_empty(self):
        data=[]
        result= calculate_average_profit(data)
        self.assertEqual(result, {})

    def test_calculate_average_profit_negative_profit(self):
        data = [
            {'Region': 'Central', 'Category': 'Furniture', 'Profit': '-100'},
            {'Region': 'Central', 'Category': 'Furniture', 'Profit': '0'}
        ]
        result = calculate_average_profit(data)
        self.assertAlmostEqual(result['Central']['Furniture'], -50.0)

    def test_calculate_shipping_percentage_normal(self):
        data = [
            {'Ship Mode': 'Second Class', 'Sales': '600'},
            {'Ship Mode': 'First Class', 'Sales': '400'},
            {'Ship Mode': 'Second Class', 'Sales': '550'}
        ]
        result = calculate_shipping_percentage(data)
        self.assertAlmostEqual(round(result, 2), 66.67, places=1)

    def test_calculate_shipping_percentage_no_qualifying(self):
        data = [
            {'Ship Mode': 'Second Class', 'Sales': '300'},
            {'Ship Mode': 'Standard Class', 'Sales': '700'}
        ]
        result = calculate_shipping_percentage(data)
        self.assertEqual(result, 0)

    def test_calculate_shipping_percentage_empty(self):
        result = calculate_shipping_percentage([])
        self.assertEqual(result, 0)

    def test_calculate_shipping_percentage_case_insensitive(self):
        data = [
            {'Ship Mode': 'SECOND CLASS', 'Sales': '600'}
        ]
        result = calculate_shipping_percentage(data)
        self.assertEqual(result, 100.0)

    def test_write_to_file_creates_file(self):
        test_data= {'East': {'Furniture': 50.5}}
        write_to_file(test_data, 'test_results.csv')
        with open('test_results.csv') as f:
            content= f.read()
        self.assertIn('East', content)
        self.assertIn('Furniture', content)
        os.remove('test_results.csv')

    def test_write_to_multiple_entries(self):
        test_data={
            'East': {'Furniture': 100.0, 'Office Supplies': 200.0},
            'West': {'Technology': 300.0}
        }
        write_to_file(test_data, 'test_results.csv')
        with open('test_results.csv') as f:
            lines=f.readlines()
            self.assertGreater(len(lines), 2)
            os.remove('test_results.csv')

if __name__ == '__main__':
    unittest.main()