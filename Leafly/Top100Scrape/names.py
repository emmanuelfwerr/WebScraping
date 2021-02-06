from bs4 import BeautifulSoup, Comment
import requests

def strain_names_list():
    # Extract HTML for Top 100 Strains
    source = requests.get('https://www.leafly.com/news/strains-products/top-100-marijuana-strains').text
    soup = BeautifulSoup(source, 'html5lib')
    names = soup.findAll('h2')

    # Extract name from HTML as well as string transformations
    for i in range(len(names)):
        names[i] = names[i].text
        names[i] = names[i].replace(' ', '-')
        names[i] = names[i].replace(' No. ', '-')
        names[i] = names[i].replace("\'", '-')
        names[i] = names[i].lower()

    # Manually remove discrepancies
    for i in range(4):
        out = [-2, -1, 0, 0]
        names.pop(out[i])
    # Special cases
    names.pop(-3)
    names[16] = 'chemdawg'
    names[29] = 'g-13'
    names[39] = 'herojuana'
    names[49] = 'lamb-s-bread'
    names[79] = 'skunk-1'
    names[80] = 'snoop-s-dream'
    names[87] = 'sunset-sherbert'

    return names

def strain_links(names):
    parent_link = 'https://www.leafly.com/strains/'

    strain_link = []
    for i in range(len(names)):
        strain_link.append(parent_link + '{}'.format(names[i]))

    return strain_link

#source = requests.get('https://www.leafly.com/strains').text
#soup = BeautifulSoup(source, 'html5lib')

#names = soup.findAll('li')
#print(names)

#place = soup.find(string=lambda tag: isinstance(tag, Comment))
#print(place)
