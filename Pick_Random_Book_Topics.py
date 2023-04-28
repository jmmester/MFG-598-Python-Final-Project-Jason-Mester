# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 09:22:31 2023

@author: Jason
"""

import pandas as pd
import random
import subprocess

# Load the Excel file into a pandas dataframe
book_topics_df = pd.read_excel('Book_Topics.xlsx')

# Get the list of book topics from the 'Topic' column of the dataframe
book_topics_list = book_topics_df['Topic'].tolist()

# Randomly select 5 book topics from the list
random_book_topics = random.sample(book_topics_list, k=5)

# Print the selected book topics
print(random_book_topics)

#subprocess.run(["python", "get_all_info_from_search_page.py"])
