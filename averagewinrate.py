import pandas as pd
import numpy as np

df = pd.read_csv("data/player-data.csv")

df["season"] = 3 * df["episode"] + df["act"]
df["matches"] = df["wins"] + df["losses"]

maps = set(df["mapname"])

gb = df.groupby(["mapname", "player"]).mean().reset_index()
winrates = []
for mapname in maps:
    winrates.append((mapname, np.mean(gb[gb["mapname"] == mapname]["winrate"])))

winrates.sort(key=lambda wr: wr[1], reverse=True)
for mapname, wr in winrates:
    print(mapname, f"{round(wr * 100, 2)}%")
