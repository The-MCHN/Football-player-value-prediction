import pandas as pd
import requests
from bs4 import BeautifulSoup

import clubcodes

headers = {'Accept-Language': "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7,fi;q=0.6,de;q=0.5",
           'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"}

club_codes_list = clubcodes.get_club_codes()

players_list = []
values_list = []
age_list = []
nationality_list = []
position_list = []

for code in club_codes_list:
    # url = "https://www.transfermarkt.com/fc-bayern-munchen/startseite/verein/27"
    url = f"https://www.transfermarkt.com/fc-paris-saint-germain/startseite/verein/{code}"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")



    players = soup.find_all(name="img", class_="bilderrahmen-fixed lazy lazy")
    age = soup.find_all(name="td", class_="zentriert")
    positions = soup.find_all(name="td", class_=["zentriert rueckennummer bg_Mittelfeld",
                                                 "zentriert rueckennummer bg_Sturm",
                                                 "zentriert rueckennummer bg_Torwart",
                                                 "zentriert rueckennummer bg_Abwehr"])

    nationality = soup.find_all(name="td", class_="zentriert")
    values = soup.find_all(name="td", class_="rechts hauptlink")

    # pprint(players)

    for i in players:
        name = str(i).split('" class="')[0].split('<img alt="')[1]
        players_list.append(name)

        # pprint(age)
    for i in range(1, len(players) * 3, 3):
        _age = str(age[i])[-8:-6]
        # print(_age)
        age_list.append(_age)

    # pprint(nationality)

    for i in nationality:
        if "flaggenrahmen" in str(i):
            k = str(i).split('" class="flaggenrahmen"')[0].split('alt="')[1]
            # print(k)
            nationality_list.append(k)

    # pprint(positions)
    for i in positions:
        k = str(i).split('"><div class="rn_nummer"')[0].split('" title="')[1].lower()
        position_list.append(k)

    # pprint(values)
    for i in range(len(values)):
        # currency_index = str(i).index("€")
        # k = str(i)[currency_index + 1:].split("</")[0]
        # print(k)
        # if k[-1] == 'm':
        #     k = float(k[:-1]) * 1_000_000
        # else:
        #     k = float(k[:-3]) * 1_000
        values_list.append(values[i].text)

df = pd.DataFrame({
    "player": players_list,
    "age": age_list,
    "nationality": nationality_list,
    "position": position_list,
    "value_euro": values_list
})

# print(df)

df.to_csv("./CreatingFootballersDataSet")
