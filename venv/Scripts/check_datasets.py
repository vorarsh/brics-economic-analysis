import os
import pandas as pd

data_folder = r"C:\Users\ARSH\brics-economic-analysis\venv\data\transformed"

files = os.listdir(data_folder)

log_file = open("dataset_issues_log.txt", "w")

for file in files:
    file_path = os.path.join(data_folder, file)

    try:
        data = pd.read_csv(file_path)

        if 'Country' not in data.columns:
            log_file.write(f"Missing 'Country' column in file: {file}\n")
            print(f"Missing 'Country' column in file: {file}")
        else:
            print(f"File '{file}' loaded successfully with 'Country' column.")
            print(data.head())

    except Exception as e:
        log_file.write(f"Error loading file {file}: {e}\n")
        print(f"Error loading file {file}: {e}")

log_file.close()

print("\nCheck 'dataset_issues_log.txt' for details on problematic files.")
