import requests
import pandas
from bs4 import BeautifulSoup

base_url = 'https://pythonizing.github.io/data/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s='

response = requests.get(base_url + '0.html')
content = response.content
soup = BeautifulSoup(content, 'html.parser')
page_number = int(soup.find_all('a', {'class': 'Page'})[-1].text)

list_of_estate_dicts = []

for page in range(0, page_number*10, 10):
    current_url = base_url + str(page) + '.html'
    response = requests.get(current_url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    all_estates = soup.find_all('div', {'class': 'propertyRow'})

    for item in all_estates:
        estate_dict = {}
        estate_dict['Address'] = item.find_all('span', {'class': 'propAddressCollapse'})[0].text
        try:
            estate_dict['Locality'] = item.find_all('span', {'class': 'propAddressCollapse'})[1].text
        except AttributeError:
            estate_dict['Locality'] = None
        estate_dict['Price'] = item.find('h4', {'class': 'propPrice'}).text.strip()
        try:
            estate_dict['Beds'] = item.find('span', {'class': 'infoBed'}).b.text
        except AttributeError:
            estate_dict['Beds'] = None

        try:
            estate_dict['Area'] = item.find('span', {'class': 'infoSqFt'}).b.text
        except AttributeError:
            estate_dict['Area'] = None

        try:
            estate_dict['Full Baths'] = item.find('span', {'class': 'infoValueFullBath'}).b.text
        except AttributeError:
            estate_dict['Full Baths'] = None

        try:
            estate_dict['Half Bath'] = item.find('span', {'class': 'infoValueHalfBath'}).b.text
        except AttributeError:
            estate_dict['Half Bath'] = None

        for column_group in item.find_all('div', {'class': 'columnGroup'}):
            for feature_group, feature_name in zip(column_group.find_all('span', {'class': 'featureGroup'}),
                                                   column_group.find_all('span', {'class': 'featureName'})):
                if 'Lot Size' in feature_group.text:
                    estate_dict['Lot Size'] = feature_name.text

        list_of_estate_dicts.append(estate_dict)

df = pandas.DataFrame(list_of_estate_dicts)
df.to_csv('Output.csv')
