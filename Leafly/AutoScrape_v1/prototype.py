import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from bs4 import BeautifulSoup, Comment
import requests

class Page(QWebEnginePage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()


def get_urls(link):
    page = Page(link)
    soup = BeautifulSoup(page.html, 'html.parser')
    page_strains = soup.find('ul', {'class': 'row w-full'})

    # Extract urls from Soup and append to url_extensions[]
    url_extensions = []
    for i in page_strains.findAll('a', href=True):
        url_extensions.append(i['href'])

    # Create list of
    parent_link = 'https://www.leafly.com'
    strain_links = []
    for i in url_extensions:
        strain_links.append(parent_link + '{}'.format(i))

    return(strain_links)

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import collections

def get_strain_data(strain_links):
    '''
    Accesses each strain link and collects individual strain data

    input: List of strain links in page
    ouput: DataFrame containing individual strain data for strains in page
    '''
    cannabis_info = []
    headers = ['strain', 'type', 'potency', 'rating', 'review_count', 'reports']
    cannabis_effects_df = pd.DataFrame()
    for link in strain_links:
        # Progress tracker (debugging)
        print(link)

        # Request HTML for each link
        source = requests.get(link).text
        soup = BeautifulSoup(source, 'lxml')

        try:
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
            cannabis_info.append([strain, type, potency, rating, review_count, reports])

            effect_ratios = {}
            for i in range(len(ratios)):
                effect_ratios[effects[i].text] = [ratios[i].text]
                effect_ratios = collections.OrderedDict(sorted(effect_ratios.items()))

            cannabis_effects_df = cannabis_effects_df.append(effect_ratios, ignore_index=True)

        except Exception as e:
            print(e)
            '''
            *runtz is Leafly Strain of the Year
            *
            '''

def main():
    '''

    '''
    # Manufacture List of all page links
    all_pages = ['https://www.leafly.com/strains']
    parent_page = 'https://www.leafly.com/strains?page='
    for i in range(2,156):
        all_pages.append(parent_page + '{}'.format(i))

    #
    df_allstrains = pd.DataFrame()

    #
    for page in all_pages:
        strain_links = get_urls(page)
        df_strains_perpage = get_strain_data(strain_links)
        df_allstrains = df_allstrains.append(df_strains_perpage, ignore_index=True)

#    return(df_allstrains)

if __name__ == "__main__":
    main()
