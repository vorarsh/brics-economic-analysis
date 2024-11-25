import os
import pandas as pd

data_folder = r"C:\Users\ARSH\brics-economic-analysis\venv\data\transformed"

files = os.listdir(data_folder)

log_file = open("../venv/Scripts/dataset_issues_log.txt", "w")

country_files = {}

for file in files:
    file_path = os.path.join(data_folder, file)

    try:
        data = pd.read_csv(file_path)

        if 'CountryName' not in data.columns:
            log_file.write(f"Missing 'CountryName' column in file: {file}\n")
            print(f"Missing 'CountryName' column in file: {file}")
        else:
            print(f"File '{file}' loaded successfully with 'CountryName' column.")
            print(f"Columns in '{file}': {list(data.columns)}\n")
            log_file.write(f"File '{file}' loaded successfully with 'CountryName' column.\n")
            log_file.write(f"Columns in '{file}': {list(data.columns)}\n\n")

            for country in data['CountryName'].unique():
                if country not in country_files:
                    country_files[country] = []
                country_files[country].append(file)

    except Exception as e:
        log_file.write(f"Error loading file {file}: {e}\n")
        print(f"Error loading file {file}: {e}")

for country, files in country_files.items():
    log_file.write(f"\nCountry: {country}\nFiles: {files}\n")
    print(f"\nCountry: {country}\nFiles: {files}\n")

log_file.close()

print("\nCheck 'dataset_issues_log.txt' for details on problematic files.")

data_path = '/src/data/raw'
file_name = 'WorldExpenditures.csv'

file_path = os.path.join(data_path, file_name)
df = pd.read_csv(file_path)

unique_countries = df['Country'].unique()
print("Unique countries in the dataset:")
print(unique_countries)
