# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 14:42:23 2023

@author: Jason
"""

from reportlab.pdfgen import canvas
import pandas as pd

random_book_topics = ['Coffee', 'Nutrition', 'National Parks', 'Yoga', 'Beer']

# create a new PDF file
pdf_file = canvas.Canvas("correlations.pdf")

# create a list of file names
file_names = [f'amazon_book_info_search_page_{i}ex.xlsx' for i in range(1, 6)]

# set the line spacing
line_spacing = 1

# loop through each file
for i, file_name in enumerate(file_names):
    # read in the Excel file as a DataFrame
    df = pd.read_excel(file_name, engine='openpyxl')
    # calculate the correlation coefficient between "Monthly revenue" and "Reviews"
    corr = df['Monthly revenue'].corr(df['Reviews'])
    # write the results to the PDF file
    pdf_file.setFont("Helvetica", 8)
    pdf_file.drawString(100, 800-i*50, f"Correlation for {random_book_topics[i]}:")
    pdf_file.drawString(120, 780-i*50, f"{corr:.1f}")

# save and close the PDF file
pdf_file.save()

