# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 20:18:50 2023

@author: Jason
"""

import pandas as pd
import matplotlib.pyplot as plt

# create a list of random book topics
random_book_topics = ['Coffee', 'Nutrition', 'National Parks', 'Yoga', 'Beer']

# create empty lists to hold the counts of "Yes" and "No" values for each file
yes_counts = []
no_counts = []

# loop through each file and read in the Excel file as a DataFrame
for i in range(1, 6):
    filename = f'amazon_book_info_search_page_{i}ex.xlsx'
    df = pd.read_excel(filename)
    # count the number of "Yes" and "No" values in the "Plausible" column
    yes_count = df['Plausible'].value_counts()['Yes']
    no_count = df['Plausible'].value_counts()['No']
    # append the counts to the respective lists
    yes_counts.append(yes_count)
    no_counts.append(no_count)

# create a bar graph of what was found
x_labels = random_book_topics
x = list(range(len(x_labels))) # convertthe range to list
width = 0.35
fig, ax = plt.subplots()
rects1 = ax.bar([i - width/2 for i in x], yes_counts, width, label='Yes') # subtract width/2 from each element of x
rects2 = ax.bar([i + width/2 for i in x], no_counts, width, label='No') # add width/2 to each element of x
ax.set_xlabel('Book Topic')
ax.set_ylabel('Yes or No')
ax.set_title('Plausible Counts by Book Topic')
ax.set_xticks(x)
ax.set_xticklabels(x_labels)
ax.legend()

# add a horizontal line at y=5
ax.axhline(y=5, color='gray', linestyle='--')

# save the figure as a PDF file
plt.savefig('yes and no bar graph.pdf')

plt.show()



