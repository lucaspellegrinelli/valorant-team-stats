import sys
import pandas as pd
import numpy as np

df = pd.read_csv("data/player-data.csv")

if len(sys.argv) > 1:
    df = df[df["player"] == sys.argv[1]]

df["season"] = 3 * df["episode"] + df["act"]
df["matches"] = df["wins"] + df["losses"]

maps = set(df["mapname"])

gb = df.groupby(["mapname", "player"]).mean().reset_index()
winrates = []
for mapname in maps:
    winrates.append((
        mapname,
        np.sum(gb[gb["mapname"] == mapname]["wins"]),
        np.sum(gb[gb["mapname"] == mapname]["losses"])
    ))

winrates.sort(key=lambda wr: wr[1], reverse=True)
for mapname, wins, losses in winrates:
    wr = wins / (wins + losses)
    print(mapname, f"{round(wr * 100, 2)}%")
