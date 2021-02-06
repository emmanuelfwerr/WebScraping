from names import strain_names_list, strain_links
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import collections

# Compile list of links to scrape
names = strain_names_list()
strain_links = strain_links(names)

# Initializing list of lists for DataFrame
cannabis_info = []
headers = ['strain', 'type', 'potency', 'rating', 'review_count', 'reports']
cannabis_effects_df = pd.DataFrame()

# Extract cannabis info from each page
for i in range(len(strain_links)):
    # Request HTML for each link
    source = requests.get(strain_links[i]).text
    soup = BeautifulSoup(source, 'lxml')
    # Extract Strain ID Card
    strain = soup.find('div', {'class':'py-sm'}).h1.text
    type = soup.find('span', {'class':'text-xs bg-leafly-white py-sm px-sm rounded'}).text
    potency = soup.find('span', {'class':'text-xs bg-deep-green-20 py-sm px-sm rounded'}).text
    rating = soup.find('span', {'class':'pr-xs'}).text
    review_count = soup.find('span', {'class':'pl-xs'}).text

    #Extract Effects Reported
    reports = soup.find('div', {'class':'flex items-center font-mono text-xs'}).text
    ratios = soup.findAll('span', {'class':'font-mono text-grey text-xs'})
    effects = soup.findAll('span', {'class':'font-bold font-headers text-sm'})

    # Fill cannabis_info[]
    temporary_strain_data = [strain, type, potency, rating, review_count, reports]
    cannabis_info.append(temporary_strain_data)

    effect_ratios = {}
    for i in range(len(ratios)):
        effect_ratios[effects[i].text] = [ratios[i].text]
        effect_ratios = collections.OrderedDict(sorted(effect_ratios.items()))

    cannabis_effects_df = cannabis_effects_df.append(effect_ratios, ignore_index=True)

# Create and fill DataFrame
cannabis_info_df = pd.DataFrame(cannabis_info, columns = headers)
all_info_df = pd.concat([cannabis_info_df, cannabis_effects_df], axis=1)

# Export df to .csv file
all_info_df.to_csv('top100strains.csv', index=False)
