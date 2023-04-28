# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 11:03:24 2023

@author: Jason
"""
#This code finds the amount of sales each booksells based off of the rank
#This code does it for any amount of files/ book topics
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import numpy as np
import subprocess



# Loop through all CSV files
for i in range(5): # change the range as per your requirement
    # set up the chrome options
    chrome_options = Options()
    #Only option needed is the extension for a pop-up blocker
    chrome_options.add_extension('cjpalhdlnbpafiamejdnhcphjbkeiagm.crx') #adds the extension for the pop-up blocker

    # apply all of the options and executable path
    driver = webdriver.Chrome(options=chrome_options)

    # This is the URL it will go to
    #this website takes ranks and gives the amount of books sold based off the rank
    driver.get("https://www.tckpublishing.com/amazon-book-sales-calculator/")
    filename = f'amazon_book_info_search_page_{i+1}.csv'
    # read the CSV file created in previous script
    df = pd.read_csv(filename)

    # calculate estimated sales for each rank
    estimated_sales = []
    for rank in df['Rank']:
        #find where to type in the rank
        number_input = driver.find_element(By.ID, "brpbsr-bsr")
        number_input.clear()
        #get the column titled 'rank;
        number_input.send_keys(rank)
        #find where to input whether it is a book or ebook
        number_input = driver.find_element(By.ID, "brpbsr-type")
        #enter in book since we are only looking at books
        number_input.send_keys("Book")
        #Find the button to run the sales estimator
        submit_button = driver.find_element(By.ID, "cf-submitted")
        #click the button
        submit_button.click()
        #find the text output section
        text_output = driver.find_element(By.ID, "brpbsr-month-sales")
        # get the exact output text
        text = text_output.get_attribute("value")
        #append sales per month
        estimated_sales.append(text)


    #add in a column header to the data found
    df['Estimated Sales'] = estimated_sales
    
    # save data found and header to the CSV file
    df.to_csv(f'amazon_book_info_search_page_{i}.csv', index=False)
    
    #calculate the monthly revenue by multiplying monthly sales by cost of book
    df['Monthly revenue'] = df['Estimated Sales'].astype(float) * df['Price'].astype(float)
    df.to_csv(f'amazon_book_info_search_page_{i}.csv', index=False)
    

# Run the analyze_data.py script which analyzes the data
#subprocess.run(["python", "analyze_data.py"])
