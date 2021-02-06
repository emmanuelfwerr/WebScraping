from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import collections
from CustomTools import get_urls, get_strain_data


def main():
    '''
    Orchestrator
    '''
    # Input page link
    #page = 'https://www.leafly.com/strains'
    page = 'https://www.leafly.com/strains?page=69'

    #
    df_allstrains = pd.DataFrame()

    #
    strain_links = get_urls(page)
    df_strains_perpage = get_strain_data(strain_links)
    df_allstrains = df_allstrains.append(df_strains_perpage, ignore_index=True)

    #
    df_allstrains.to_csv('page69_strain_data.csv', index=False)

if __name__ == "__main__":
    main()
