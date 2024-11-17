
import pandas as pd
import os

data_path = 'C:/Users/ARSH/brics-economic-analysis/venv/data/raw'

files = os.listdir(data_path)
print(f"Total files: {len(files)}")

sample_file = os.path.join(data_path, files[0])
df = pd.read_csv(sample_file)

print("Sample Data:")
print(df.head())
print("\nColumns:",df.columns)
