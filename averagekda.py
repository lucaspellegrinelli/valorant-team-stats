import sys
import pandas as pd
import numpy as np

df = pd.read_csv("data/player-data.csv")

if len(sys.argv) > 1:
    df = df[df["player"] == sys.argv[1]]

df["season"] = 3 * df["episode"] + df["act"]
df["matches"] = df["wins"] + df["losses"]

maps = set(df["mapname"])
seasons = set(df["season"])

gb_mean = df.groupby(["season", "mapname", "player"]).mean().reset_index()
gb_sum = df.groupby(["season", "mapname", "player"]).sum().reset_index()

kdas_values = []
for mapname in maps:
    kdas = gb_mean[gb_mean["mapname"] == mapname]["kd"]
    matches = gb_sum[gb_sum["mapname"] == mapname]["matches"]
    kdas_values.append((
        mapname,
        np.sum(kdas * matches) / np.sum(matches)
    ))

kdas_values.sort(key=lambda wr: wr[1], reverse=True)
for mapname, kda in kdas_values:
    print(mapname, "=", round(kda, 2), "KD")