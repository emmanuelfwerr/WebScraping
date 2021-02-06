import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEnginePage
#
from bs4 import BeautifulSoup, Comment
import requests
import pandas as pd
import numpy as np
import collections

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
        except Exception as e:
            '''
            *runtz is Leafly Strain of the Year
            '''
            strain = 'Unavailable'
            print('NAME_NOT_FOUND')

        try:
            potency = soup.find('span', {'class':'text-xs bg-deep-green-20 py-sm px-sm rounded'}).text
        except Exception as e:
            '''
            *many strains dont list potency
            '''
            potency = 'Unavailable'
            print('POTENCY_NOT_FOUND')

        try:
            type = soup.find('span', {'class':'text-xs bg-leafly-white py-sm px-sm rounded'}).text
        except Exception as e:
            '''
            *some strains dont list type
            '''
            type = 'Unavailable'
            print('TYPE_NOT_FOUND')

        try:
            rating = soup.find('span', {'class':'pr-xs'}).text
            review_count = soup.find('span', {'class':'pl-xs'}).text
        except Exception as e:
            '''
            *many strains dont list reported effects
            '''
            rating = 'Unavailable'
            review_count = 'Unavailable'
            print('NO_REVIEWS_SUBMITTED')

        try:
            #Extract Effects Reported
            reports = soup.find('div', {'class':'flex items-center font-mono text-xs'}).text
        except Exception as e:
            '''
            *many strains dont list reported effects
            '''
            reports = 'Unavailable'
            print('NO_EFFECTS_REPORTED')

        ratios = soup.findAll('span', {'class':'font-mono text-grey text-xs'})
        effects = soup.findAll('span', {'class':'font-bold font-headers text-sm'})

        effect_ratios = {}
        for i in range(len(ratios)):
            effect_ratios[effects[i].text] = [ratios[i].text]
            effect_ratios = collections.OrderedDict(sorted(effect_ratios.items()))

        cannabis_effects_df = cannabis_effects_df.append(effect_ratios, ignore_index=True)

        # Fill cannabis_info[]
        cannabis_info.append([strain, type, potency, rating, review_count, reports])

    # Create and fill DataFrame
    cannabis_info_df = pd.DataFrame(cannabis_info, columns = headers)
    all_info_df = pd.concat([cannabis_info_df, cannabis_effects_df], axis=1)

    return(all_info_df)
