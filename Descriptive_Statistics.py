# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 14:36:42 2023

@author: Jason
"""

from reportlab.pdfgen import canvas
import pandas as pd
from statistics import median, mode, stdev

# create a new PDF file
pdf_file = canvas.Canvas("Mean Median and SD.pdf")

random_book_topics = ['Coffee', 'Nutrition', 'National Parks', 'Yoga', 'Beer']

# create a list of file names
file_names = [f'amazon_book_info_search_page_{i}ex.xlsx' for i in range(1, 6)]

# set the line spacing
line_spacing = 1

for i, file_name in enumerate(file_names):
    # read in the Excel file as a DataFrame
    df = pd.read_excel(file_name, engine='openpyxl')
    # get the mean, median, mode, and standard deviation of the "Reviews" column
    reviews_mean = round(df['Reviews'].mean(), 1)
    reviews_median = round(median(df['Reviews']), 1)
    reviews_mode = round(mode(df['Reviews']), 1)
    reviews_std_dev = round(stdev(df['Reviews']), 1)
    # get the mean, median, mode, and standard deviation of the "Monthly revenue" column
    revenue_mean = round(df['Monthly revenue'].mean(), 1)
    revenue_median = round(median(df['Monthly revenue']), 1)
    revenue_mode = round(mode(df['Monthly revenue']), 1)
    revenue_std_dev = round(stdev(df['Monthly revenue']), 1)
    # write the results to the PDF file
    pdf_file.setFont("Helvetica", 10)
    pdf_file.drawString(100, 800-i*100, f"Results for {random_book_topics[i]}:")
    pdf_file.drawString(120, 780-i*100, f"Reviews:")
    pdf_file.drawString(140, 760-i*100, f"Mean: {reviews_mean}, Median: {reviews_median}, SD: {reviews_std_dev}")
    pdf_file.drawString(120, 740-i*100, f"Monthly Revenue:")
    pdf_file.drawString(140, 720-i*100, f"Mean: ${revenue_mean}, Median: ${revenue_median}, SD: {revenue_std_dev}")

# save and close the PDF file
pdf_file.save()


