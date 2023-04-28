# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 07:27:27 2023

@author: Jason
"""

# This code gets the HTML from Amazon and then goes through it and gets all the information of the books
#This code will get all the information for any amount of books
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import re
import subprocess
import pandas as pd
import random

# Sets the executable path (Chrome)
webdriver_service = ChromeService(executable_path='path/to/chromedriver')

# Set the options for how Chrome will be run
chrome_options = ChromeOptions()
#This could run in headless mode and go faster but in order to run the extensions it can't run in headless mode
#chrome_options.add_argument("--headless")  # runs through python
chrome_options.add_argument("--disable-gpu")  
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36") #runs through my Chrome user agent
chrome_options.add_extension('jkompbllimaoekaogchhkmkdogpkhojg.crx') #This is the file for the ranking extension extension

# apply all of the options and executable path
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

#Below is a way to pick random book topics and run the code for them
#It works but for simplicity sake I picked 5 "random topics"

# Load the Excel file into a pandas dataframe
#book_topics_df = pd.read_excel('Book_Topics.xlsx')

# Get the list of book topics from the 'Topic' column of the dataframe
#book_topics_list = book_topics_df['Topic'].tolist()

# Randomly select 5 book topics from the list
#random_book_topics = random.sample(book_topics_list, k=5)
#gives 5 'random' book topics
#have it set up for non random
random_book_topics = ['Coffee', 'Nutrition', 'National Parks', 'Yoga', 'Beer']

category = "books"

html_list = []  # list to store all the HTMLs

#for every book topic in the random book topics list this code will find all of the html and save it
for topic in random_book_topics:
    # Set the search keyword
    search_keyword = topic

    # make the URL
    search_url = f"https://www.amazon.com/s?k={search_keyword}&i={category}"

    # Go to search page
    driver.get(search_url)
    time.sleep(10)  # add a pause in order for the ranks to load

    # Extract the HTML of the search results page
    html = driver.page_source
    time.sleep(3)  # Add a pause

    # This saves the html file that was pulled from the website
    file_path = f"C:/Users/Jason/OneDrive/Documents/ASU/EGR 598 Python/Final Project/{search_keyword}_html.html"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

    html_list.append(html)  # append the HTML to the list

driver.quit()  # end the driver

# loop through all the saved HTMLs
for i, html in enumerate(html_list):
    #This uses Beautiful Soup to parse out the html
    soup = BeautifulSoup(html, 'html.parser')

    #Creates a csv and applies the column names
    csv_headers = ['Book', 'Reviews', 'Price', 'Author', 'Rank']
    file_name = f'amazon_book_info_search_page_{i+1}.csv'  # Name the file with a different number for each HTML file
    with open(file_name, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)

    # Looks for a div that has a data-asin with a length of 10
    # This is looking for the number associated with each book that has all of the propper information from it
    books = soup.find_all("div",  {"data-asin": lambda x: x and len(x) == 10})

    # for every book in books so for every 10 digit number get all of the below information
    for book in books:
    
        #Find Title
        # look for a span class that includes 'a-color-base a-text-normal'
        # Sometimes it returns 'None' so as long as its not 'None' then copy the text and that is the title
        title = book.find('span', {'class': lambda x: x and 'a-color-base a-text-normal' in x})
        if title is not None:
            title_text = title.text
        else:
            continue
    
        #Find Reviews
        # look for the span class with 'a-size-base s-underline-text'
        # Sometimes it returns 'None' so as long as its not 'None' then copy the text
        reviews = book.find('span', class_='a-size-base s-underline-text')
        if reviews is not None:
            reviews_text = reviews.text
            reviews_text = reviews_text.replace(',', '') # removes commas
            reviews_text_no_par =re.sub(r"\(|\)", "", reviews_text) # removes parenthesis from number
        else:
            continue
        
        #This is how the rank is found
        rank = book.find('span', class_='extension-rank')
        if rank is not None:
            rank_text = rank.text
            rank_text = rank_text.replace(',', '') # removes commas
            rank_text = rank_text.replace('#', '') # removes pound sign
        else:
            continue
    
        
        #Find Price
        # look for the span class with 'a-size-base a-link-normal s-underline-text s-underline-link-text s-link-style a-text-bold'
        # if the text in it is "Paperback" then go to the next div and find the span class titled "a-offscreen" and pull that text as the price
        # if it doesn't find "Paperback" then check for "Hardcover"
        # if it finds "Hardcover" then go to the next div and find the span class titled "a-offscreen" and pull that text as the price
        # if it doesn't find "Hardcover" then set price_text to an empty string
        price_text = ""
        price_tags = book.find_all('a', class_='a-size-base a-link-normal s-underline-text s-underline-link-text s-link-style a-text-bold')
        if len(price_tags) > 0:
            for tag in price_tags:
                if 'Paperback' in tag.text:
                    price = tag.find_next('span', class_='a-offscreen')
                    if price is not None:
                        price_text = price.text
                        price_text = price_text.replace('$', '')
                    break
                elif 'Hardcover' in tag.text:
                    price = tag.find_next('span', class_='a-offscreen')
                    if price is not None:
                        price_text = price.text
                        price_text = price_text.replace('$', '')
                    break
                else:
                    price = tag.find_next('span', class_='a-offscreen')
                    if price is not None:
                        price_text = price.text
                        price_text = price_text.replace('$', '')
                    break
        print(price_text)
    
    
            
        #Find author
        # look for the span class with 'a-price-whole'
        # Sometimes it returns 'None' so as long as its not 'None' then copy the text
        author = book.find('a', class_='a-size-base a-link-normal s-underline-text s-underline-link-text s-link-style')
        if author is not None:
            author_text = author.text   
        else:
            continue
    
        
        # For every book it saves all of the above to the csv that was created
        with open(f'amazon_book_info_search_page_{i+1}.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([title_text, reviews_text_no_par, price_text, author_text, rank_text])

    
    # call for the next code
    #subprocess.run(["python", "find_all_sales_per_month.py"])
    


