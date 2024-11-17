import pandas as pd
import os

data_path = 'C:/Users/ARSH/brics-economic-analysis/venv/data/processed'
output_path = 'C:/Users/ARSH/brics-economic-analysis/venv/data/transformed'

if not os.path.exists(output_path):
    os.makedirs(output_path)

def process_files(data_path):
    files = os.listdir(data_path)
    for file in files:
        file_path = os.path.join(data_path, file)
        try:
            df = pd.read_csv(file_path)

            if 'Value' not in df.columns:
                print(f"Skipping {file} due to missing 'Value' column.")
                continue
            df.dropna(subset=['Value'], inplace=True)
            df['Value_Change'] = df['Value'].pct_change()*100
            df['5yr_Rolling_Avg'] = df['Value'].rolling(window=5).mean()
            df['Cumulative_Sum'] = df['Value'].cumsum()

            output_file = os.path.join(output_path, file)
            df.to_csv(output_file, index=False)
            print(f"Processed and saved: {file}")

        except Exception as e:
            print(f"Error processing: {file}: {e}")

process_files(data_path)

