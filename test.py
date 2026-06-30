from data.loader import DataLoader

loader = DataLoader()

df = loader.from_yahoo()

print(df.tail())
