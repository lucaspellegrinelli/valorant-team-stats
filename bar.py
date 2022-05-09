import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse

plt.style.use("seaborn-dark")

parser = argparse.ArgumentParser()
parser.add_argument("-x", required=True)
parser.add_argument("-y", required=True)
parser.add_argument("-p", "--player", required=False)
parser.add_argument("-m", "--metric", default="mean", required=False)
args = parser.parse_args()

df = pd.read_csv("player-data.csv")

if args.player:
    df = df[df["player"] == args.player]

print(f"Matches found {len(df)}")
df["season"] = 3 * df["episode"] + df["act"]
df["winrate"] = (df["rounds_won"] > df["rounds_lost"]).astype(int)
df["matches"] = 1

group_by_items = [args.x]
if args.player:
    group_by_items.append("player")

gb = df.groupby(group_by_items)
gb = getattr(gb, args.metric)().reset_index()

gb = gb.sort_values(args.y, ascending=False)
gb.plot.bar(x=args.x, y=args.y, rot=0)

plt.axhline(y=df[args.y].mean(), color="r", linestyle="-")

title_str = f"{args.y} x {args.x}"
if args.player:
    title_str += f" - {args.player}"
plt.title(title_str)
plt.ylabel(args.y)
plt.tight_layout()
plt.show()