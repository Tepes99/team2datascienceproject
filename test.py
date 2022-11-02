import plotly.express as px
import pandas as pd

df = pd.read_csv("data\RFF_Carbon_Price.csv")
df = pd.melt(df, id_vars="Year", value_vars=df.columns[1:])
df.columns = ["Year", "Policy", "$ Price Per Metric Ton CO2"]
df = df.set_index("Year")
df.to_csv("data\RFF_Carbon_Price.csv")
print(df)
