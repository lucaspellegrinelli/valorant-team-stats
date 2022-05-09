import argparse
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--metric", required=True)
args = parser.parse_args()

df = pd.read_csv("data/player-data.csv")

df["season"] = 3 * df["episode"] + df["act"]
df["matches"] = df["wins"] + df["losses"]

maps = set(df["mapname"])
seasons = set(df["season"])

gb = df.groupby(["player"]).sum().reset_index()
gb[f"{args.metric}_per_match"] = gb[args.metric] / gb["matches"]

print(gb[["player", f"{args.metric}_per_match"]])