import glob
import pandas as pd

filename = glob.glob("data/*.xlsx")

df = pd.read_excel(filename[0])
print(df)