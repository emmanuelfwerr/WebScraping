from bs4 import BeautifulSoup
import requests


def get_strain_names(soup):

    return strain_names


def get_strain_data(strain_names):

    return strain_data



def main():

    source = requests.get('https://www.leafly.com/strains').text
    soup = BeautifulSoup(source, 'lxml')

    # returns list with all strains from Leafly
    strain_names = get_strain_names(soup)

    # iterate through each strain name to get url for next strain and scrape
    for i in strain_names:
        # missing: replace ' ' with '-' for each string
        new_source = 'https://www.leafly.com/strains/{}'.format(strain_names[i])
        # missing: pandas DataFrame
        strain_data = get_strain_data(new_source)

if __name__ == "__main__":
    main()
