# This script scrapes the international cremation data from cremation.org/uk

# Importing required modules

import pandas as pd
import urllib
from bs4 import BeautifulSoup as bs

# Creating a list of the webpages from which data is harvested

base = 'https://www.cremation.org.uk/international-statistics-'
pages = [base + str(yr) for yr in range(1996,2018)]
pages.append('https://www.cremation.org.uk/international-cremation-statistics-2018')

# Initializing lists for storage

list0 = []
list1 = []
list2 = []
list3 = []
list4 = []
list5 = []
list6 = []
list7 = []
listyrs = []

# Harvesting the data from each page

for page in pages:

    print('Harvesting international cremation data for ' + page[len(page)-4:] + '.......')
    page_raw = urllib.request.Request(page, headers = {'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(page_raw)
    soup = bs(response, 'html.parser')
    entries = soup.find_all('tr')
    
    for entry in entries:
        
        rows = entry.find_all('td')
        
        if len(rows) == 8:
            
            c = -1
            listyrs.append(str(page)[len(str(page))-4:])
            
            for row in rows:
                
                c += 1
                a = str(row).find('<font size="1">')
                b = str(row).find('</font>')
                content = str(row)[a+15:b]
                content = content.replace('*','')
                content = content.strip()
                
                # Fixes country names
                
                if '<' in content:
                    
                    q = content.find('>')
                    r = content.find('</a')
                    content = content[q+1:r]

                # Fixes issues with remaining data
                    
                if content == '-':
                    
                    content = ''
                    
                if 'Â¯' in content:
                    
                    content = ''
                    
                if '±' in content:
                    
                    content = ''
                    
                if '\xa0' in content:
                    
                    content = ''
                    
                if content == 'COMMONWEALTH OF<br/>\n\t\t\tINDEPENDENT STATES' or content == 'CONFEDERATION OF<br/>\n\t\t\tINDEPENDENT STATES':
                    
                    content = 'CONFEDERATION OF INDEPENDENT STATES'
                    
                if content == 'TRINIDAD &amp; TOBAGO':
                    
                    content = 'TRINIDAD & TOBAGO'
                    
                if content == 'GREAT BRITAIN':
                    
                    content = 'UNITED KINGDOM'
                    
                if content == 'EIRE':
                    
                    content = 'IRELAND'
                    
                if c == 0:
                    
                    list0.append(content)
                    
                elif c == 1:
                    
                    list1.append(content)
                
                elif c == 2:
                    
                    list2.append(content)
                    
                elif c == 3:
                    
                    list3.append(content)
                    
                elif c == 4:
                    
                    list4.append(content)
                    
                elif c == 5:
                    
                    list5.append(content)
                    
                elif c == 6:
                    
                    list6.append(content)
                    
                elif c == 7:
                    
                    list7.append(content)
                
# With all of the data harvested and stored in lists, we just create a df and write to file

df = pd.DataFrame({'Country':list0 , 'Year':listyrs, 'Crematoria':list1, 'Deaths':list2, 'Cremations':list3, 'Pct Cremations':list4})
df.to_csv('C:/Users/User/Documents/Data/dead_people/international_data.csv', index = False)

