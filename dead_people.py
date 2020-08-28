# This script perfroms the analysis for the paper on dead people gases

# Importing required modules

import pandas as pd
import statsmodels.api as stats

# Loading the data

edata = pd.read_csv('C:/Users/User/Documents/Data/dead_people/NEC_NFR14.csv', sep = '\t')
cdata = pd.read_csv('C:/Users/User/Documents/Data/dead_people/international_data.csv', encoding = 'utf-8')
rdata = pd.read_csv('C:/Users/User/Documents/Data/dead_people/Religious Characteristics of States Dataset Project.csv')
wbdata = pd.read_csv('C:/Users/User/Documents/Data/dead_people/WBdata.csv')

# Subset for cremation data

edata = edata[edata.sector_name == 'Cremation'].reset_index(drop = True)

# Create a list of pollutants with cremation data

pollutants = list(sorted(edata.Pollutant_name.unique()))

# Subset data based on non-nan emissions data

idx = [row for row in range(len(edata)) if type(edata.Emissions[row]) != float]
edata = edata.loc[idx,:].reset_index(drop = True)

# Remove 'EU28' from set of nations to study

idx2 = [row for row in range(len(edata)) if edata.Country[row] != 'EU28']
edata = edata.loc[idx2,:].reset_index(drop = True)

# A dataframe of the number of observations for each pollutant

lens = [len(edata[edata.Pollutant_name == p]) for p in pollutants]
sum_stats = pd.DataFrame({'P':pollutants, 'L':lens})

# Merging cdata and edata

# A dictionary linking names in edata and cdata

ec = ['Austria', 'Belgium', 'Bulgaria', 'Cyprus', 'czechia', 'Germany',
       'Denmark', 'Estonia', 'Spain', 'Finland', 'France',
       'United Kingdom', 'Greece', 'Croatia', 'Hungary', 'Ireland',
       'Italy', 'Lithuania', 'Luxembourg', 'Latvia', 'Malta',
       'Netherlands', 'Poland', 'Portugal', 'Romania', 'Sweden',
       'Slovenia', 'Slovakia']

cc = ['AUSTRIA', 'BELGIUM', 'BULGARIA', 'CYPRUS', 'CZECH REPUBLIC',
      'GERMANY', 'DENMARK', 'ESTONIA', 'SPAIN', 'FINLAND', 'FRANCE',
      'UNITED KINGDOM', 'GREECE', 'CROATIA', 'HUNGARY', 'IRELAND',
      'ITALY', 'LITHUANIA', 'LUXEMBOURG', 'LATVIA', 'MALTA',
      'THE NETHERLANDS', 'POLAND', 'PORTUGAL', 'ROMANIA', 'SWEDEN',
      'SLOVENIA', 'SLOVAK REPUBLIC']

cdic = dict(zip(ec,cc))

# A dictionary linking names in rdata and cdata

iso = ['AUT', 'BEL', 'BGR', 'CYP', 'CZE', 'DEU', 'DNK', 'EST', 'ESP', 'FIN',
       'FRA', 'GBR', 'GRC', 'HRV', 'HUN', 'IRL', 'ITA', 'LTU', 'LUX', 'LVA',
       'MLT', 'NLD', 'POL', 'PRT', 'ROU', 'SWE', 'SVN', 'SVK']

isodic = dict(zip(iso,cc))

# A dictionary linking names in wbdata and cdata

wb = ['Austria', 'Belgium', 'Bulgaria', 'Cyprus', 'Czech Republic',
      'Germany', 'Denmark', 'Estonia', 'Spain', 'Finland', 'France',
      'United Kingdom', 'Greece', 'Croatia', 'Hungary', 'Ireland',
      'Italy', 'Lithuania', 'Luxembourg', 'Latvia', 'Malta',
      'Netherlands', 'Poland', 'Portugal', 'Romania', 'Sweden',
      'Slovenia', 'Slovak Republic']

wbdic = dict(zip(wb,cc))

# Creating a column in each dataframe for the join

c_add = [str(cdata.Country[i]) + str(cdata.Year[i]) for i in range(len(cdata))]
e_add = [str(cdic[edata.Country[i]]) + str(edata.Year[i]) for i in range(len(edata))]
r_add = [str(isodic[rdata.ISO3[i]]) + str(rdata.YEAR[i]) if rdata.ISO3[i] in isodic.keys() else 'NOPE' for i in range(len(rdata))]
wb_add = [str(wbdic[wbdata['Country Name'][i]]) + str(wbdata.Year[i]) if wbdata['Country Name'][i] in wbdic.keys() else 'NOPE' for i in range(len(wbdata))]

# Add the reference columns to the dataframes

cdata = pd.concat([pd.Series(c_add, name = 'Ref'), cdata], axis = 1)
edata = pd.concat([pd.Series(e_add, name = 'Ref'), edata], axis = 1)
rdata = pd.concat([pd.Series(r_add, name = 'Ref'), rdata], axis = 1)
wbdata = pd.concat([pd.Series(wb_add, name = 'Ref'), wbdata], axis = 1)

# Subset rdata for relevant columns

rdata = rdata[['Ref', 'CHRPC', 'CHRPP', 'MUSPC', 'MUSPP', 'JEWPC', 'JEWPP',
               'BUDPC', 'BUDPP', 'NREPC', 'NREPP', 'ATHPC', 'ATHPP']]

# Appending this data to the cremation data

data = edata.merge(cdata, left_on = 'Ref', right_on = 'Ref')
data = data.merge(rdata, left_on = 'Ref', right_on = 'Ref')
data = data.merge(wbdata, left_on = 'Ref', right_on = 'Ref')

# Run regressions for cremations

# Likely need to build a separate data set here -- can just find first instances of 'Ref'!






# Run regressions for each pollutant

for pollutant in data.Pollutant_name.unique():
    
    temp = data[data.Pollutant_name == pollutant]
    regdata = temp[['Country_x', 'Pollutant_name', 'Year_x', 'Emissions', 'Crematoria',
                    'Deaths', 'Cremations', 'Pct Cremations', 'CHRPC', 'MUSPC',
                    'BUDPC', 'JEWPC', 'NREPC', 'GDP per capita (constant 2010 US$)',
                    'Land area (sq. km)', 'Renewable energy consumption (% of total final energy consumption)',
                    'Alternative and nuclear energy (% of total energy use)',
                    'Energy use (kg of oil equivalent) per $1,000 GDP (constant 2011 PPP)']].dropna()
    Y = regdata.Emissions
    X = regdata[['Crematoria', 'Deaths', 'Cremations', 'Pct Cremations',
                 'CHRPC', 'MUSPC', 'BUDPC', 'JEWPC', 'NREPC',
                 'GDP per capita (constant 2010 US$)', 'Land area (sq. km)',
                 'Renewable energy consumption (% of total final energy consumption)',
                 'Alternative and nuclear energy (% of total energy use)',
                 'Energy use (kg of oil equivalent) per $1,000 GDP (constant 2011 PPP)']]
    X.Deaths = X.Deaths.str.replace(',', '').astype(float)
    X.Cremations = X.Cremations.str.replace(',', '').astype(float)
    


"""

run regressions for each (viable) pollutant

subset each pollutant, see what data is there

if its good, run regressions

if they're good, keep that pollutant in the project

"""








