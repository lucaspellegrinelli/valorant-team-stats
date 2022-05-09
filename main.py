import pandas as pd
from pagescraper import PageScraper

accounts = [
    ("Pelle", "pll#moc"),
    ("Pelle", "Poseidon#aerf"),
    ("Douglas", "Dobakay#BR1"),
    ("Douglas", "NGL Jambaloso#2508"),
    ("DCS", "DCS#DCSTv"),
    ("DCS", "SmurfDcs#BR1"),
    ("Taffarel", "Conqer#BR1"),
    ("Taffarel", "Conquito#emo24"),
    ("Joao", "NGL Jambalaia#BR01"),
    ("Hugo", "Desculp ser Omen#0001")
]

scraper = PageScraper(load_wait=10)

full_output = []
for player, account in accounts:
    for episode in [3, 4]:
        for act in [1, 2, 3]:
            acc_name = account.split("#")[0]
            acc_tag = account.split("#")[1]
            full_output += [s.__dict__ for s in scraper.scrap(player, acc_name, acc_tag, episode, act)]

df = pd.DataFrame(full_output)
df.to_csv("player-data.csv", index=False)