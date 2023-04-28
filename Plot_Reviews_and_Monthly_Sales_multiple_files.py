# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 20:28:21 2023

@author: Jason
"""
#This code plots all the reviews and revenue for each book that is in the list
import pandas as pd
import matplotlib.pyplot as plt

# Set up a new figure with a larger size
fig = plt.figure(figsize=(9, 17))

#book topics are here for the title of each plot
random_book_topics = ['Coffee', 'Nutrition', 'National Parks', 'Yoga', 'Beer']

# Loop over the five files and create subplots for each graph
for i in range(1, 6):
    # Read in the data
    filename = f'amazon_book_info_search_page_{i}ex.xlsx'
    df = pd.read_excel(filename)
    
    # Select the columns to plot
    reviews = df['Reviews']
    revenue = df['Monthly revenue']
    
    # Create a new subplot with two y-axes
    ax = fig.add_subplot(5, 1, i)
    ax2 = ax.twinx()
    
    # Plot the data on the two axes
    ax.plot(reviews, label='Reviews', color='b')
    ax2.plot(revenue, label='Monthly Revenue', color='r')
    
    # Add horizontal lines at 100 reviews and $500 monthly revenue
    ax.axhline(y=100, color='gray', linestyle='--')
    ax2.axhline(y=500, color='gray', linestyle='--')
    
    # Set the labels and title
    ax.set_xlabel('Book Number')
    ax.set_ylabel('Reviews', color='b')
    ax2.set_ylabel('Monthly Revenue', color='r')
    ax.set_title(random_book_topics[i-1])
    
    # Show the legend
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    lines = lines1 + lines2
    labels = labels1 + labels2
    ax2.legend(lines, labels, loc='center left', bbox_to_anchor=(1.1, 0), handlelength=1)#This is where the location of the legend is stated

# Adjust spacing between subplots
fig.subplots_adjust(hspace=1)

# Save the figure as a PDF
fig.savefig('plots of reviews and revenue.pdf', dpi=300, bbox_inches='tight')
