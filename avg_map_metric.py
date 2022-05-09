import sys
import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--metric", required=True)
parser.add_argument("-p", "--player", required=False)
args = parser.parse_args()

df = pd.read_csv("data/player-data.csv")

if args.player:
    df = df[df["player"] == args.player]

df["season"] = 3 * df["episode"] + df["act"]
df["matches"] = df["wins"] + df["losses"]

maps = set(df["mapname"])
seasons = set(df["season"])

df["metric_match"] = df[args.metric] * df["matches"]
gb = df.groupby(["season", "mapname", "player"]).sum().reset_index()

metric_values = []
for mapname in maps:
    sum_df = gb[gb["mapname"] == mapname].copy()
    sum_df = sum_df.groupby(["mapname", "player"]).sum().reset_index()
    sum_df["mean_metric"] = sum_df["metric_match"] / sum_df["matches"]
    metric_values.append((mapname, np.mean(sum_df["mean_metric"])))

metric_values.sort(key=lambda wr: wr[1], reverse=True)
for mapname, metric in metric_values:
    print(mapname, "=", round(metric, 3))