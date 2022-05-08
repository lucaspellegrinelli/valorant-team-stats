import time
import json
import pandas as pd
from statsgrabber import StatsGrabber

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

full_output = []
for account in accounts:
    for episode in [3, 4]:
        for act in [1, 2, 3]:
            time.sleep(0.25)
            player, acc = account
            print(player, acc, episode, act)
            grabber = StatsGrabber(player, acc, episode, act)
            maps = grabber.grab()
            for map_data in maps:
                full_output.append(map_data.__dict__)

df = pd.DataFrame(full_output)
df["winrate"] = df["winrate"].str.rstrip("%").astype("float") / 100.0
df["hs"] = df["hs"].str.rstrip("%").astype("float") / 100.0
df.to_csv("data/player-data.csv", index=False)