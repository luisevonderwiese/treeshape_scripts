import pandas as pd
df = pd.read_csv("results.csv")

df = df[(df["lwr_max"] + df["lwr_max_2"]) > 0.5]
df = df[df["d"] > 1.0]
df = df[df["lwr_max"] < 0.9]
print(df)
