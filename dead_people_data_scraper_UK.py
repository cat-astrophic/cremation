# This script scrapes the international cremation data from cremation.org/uk

# Downloaded pdfs are stored in C:/Users/User/Documents/Data/dead_people/pdfs/

# Importing required modules

import os
import pandas as pd
import tabula

# Make the following directory for storing raw tables

os.mkdir('C:/Users/User/Documents/Data/dead_people/tables')

# A list of pages to collect data from for each pdf

p = ['1-7', '1-6', '1-7', '1-7', '1-7', '1-7', '1-7', '1-7', '1-7',
     '1-7', '1-7', '1-7', '1-7', '1-7', '1-7', '1-7', '1-15', '1-5']

# Scraping data from pdfs

for yr in range(2002,2020):
    
    print('Scraping data from pdf for ' + str(yr) + '.......')
    df = tabula.read_pdf('C:/Users/User/Documents/Data/dead_people/pdfs/' + str(yr) + '.pdf', pages = p[yr-2002])
    count = 0
    
    for d in df:
        
        count += 1
        d = pd.DataFrame(d)
        d.to_csv('C:/Users/User/Documents/Data/dead_people/tables/' + str(yr) + '_table_' + str(count) + '_of_' + str(len(df)) + '.csv', index = False)

