from bs4 import BeautifulSoup
import pandas as pd
import requests
from io import StringIO

#url = "https://pokemondb.net/location/sinnoh-route-204"
print('Find the URL to the PokeDB location guide here: https://pokemondb.net/location/')
url = input('What is the URL of the PokeDB location page that you would like to scrape?')

def scrape(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    def h2_and_p(tag):
        return (tag.name == 'p' and tag.has_attr('class')) or tag.name == 'h2'

    tables = soup.find_all("table", "data-table")

    to_decompose = soup.find_all("small", "text-muted")
    [small.decompose() for small in to_decompose]

    descriptions = soup.find_all(h2_and_p)

    j = -1

    for i, table in enumerate(tables):
        j += 1
        print(descriptions[j].string)

        if descriptions[j].name == 'h2':
            j += 1
            print(descriptions[j].string)

        df = pd.read_html(StringIO(str(table)))[0]

        df = df.drop(columns=['Games', 'Games.1', 'Rarity', 'Details'])

        cols_to_drop = ['Times', 'Games.2', 'Games.3', 'Seasons']
        for col in cols_to_drop:
            if col in df:
                df = df.drop(columns=[col])
        
        df = df.drop_duplicates()

        trash_values = ['Hoenn Sound', 'Sinnoh Sound', 'Swarm', 'Alternate S.O.S. encounters', 'Shaking/Bubbling spots', 'Double Grass', 'Alternate S.O.S. encounters, Shaking/Bubbling spots', 'Island Scan', 
                        'All Weather', 'Snowstorm', 'Normal Weather', 'Overcast', 'Heavy Fog', 'Raining', 'Sandstorm', 'Snowing', 'Intense Sun', 'Thunderstorm', 'Horde encounter', 'Purple flower patch', 'Red flower patch', 
                        'Yellow flower patch', 'Tall grass', "Water's edge", 'Any Pokémon game in GBA slot','Pokémon Emerald in GBA slot',
                        'Pokémon Ruby in GBA slot','Pokémon Sapphire in GBA slot','Pokémon FireRed in GBA slot','Pokémon LeafGreen in GBA slot']
        trash_row_index = []
        
        for value in trash_values:
            if value in df.values:
                trash_row_index.append(df.index[df['Pokémon'] == value].item())


        if len(trash_row_index) > 0:
            df = df.drop(index=trash_row_index)
        
        df = df.dropna(axis=0, how='all')
        df = df.dropna(axis=1)

        df = df.reset_index(drop=True)
        

        print (df)

scrape(url)