import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
plt.style.use("seaborn-dark")

df = pd.read_csv("data/player-data.csv")

if len(sys.argv) > 1:
    df = df[df["player"] == sys.argv[1]]

df["season"] = 3 * df["episode"] + df["act"]
df["matches"] = df["wins"] + df["losses"]

gb = df.groupby(["mapname"]).sum().reset_index()

figure = plt.gcf()

x = np.linspace(0, 1, 1000)
for index, row in gb.iterrows():
    r = row["wins"]
    n = row["wins"] + row["losses"]
    wr = round(r / n * 100, 1)
    distribution = stats.binom.pmf(r, n, x)
    distribution *= n
    distribution /= np.sum(distribution)
    plt.plot(x, distribution, label=f"{row['mapname']} ({wr}% / {n})")

plt.ylabel("P(P(X))")
plt.xlabel("P(X) where X = us winning the map")
plt.legend()
figure.set_size_inches(8, 4)
plt.tight_layout()
# plt.show()
plt.savefig("plots/map-binomial.png")