import pandas as pd
import os

data_path = 'C:/Users/ARSH/brics-economic-analysis/venv/data/raw'
files = os.listdir(data_path)

data_dict = {}


def clean_dataframe(df):
    """
    Clean a DataFrame by:
    - Dropping columns with all missing values.
    - Filling missing numerical values with 0
    - Converting columns to appropriate data types.
    """
    df.dropna(axis=1, how='all', inplace=True)

    if 'Value' not in df.columns:
        if 'ColumnX' in df.columns:
            df['Value'] = df['ColumnX']
        else:
            print(f"Warning: No 'Value' or equivalent column found in {df.columns}")

    df['Value'] = df['Value'].fillna(0)
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce', downcast='integer')
    return df


def clean_and_save_world_expenditures(data_path, processed_path, countries_of_interest):
    file_name = 'WorldExpenditures.csv'
    file_path = os.path.join(data_path, file_name)

    try:
        df = pd.read_csv(file_path)
        filtered_data = df[df['Country'].isin(countries_of_interest)]

        processed_file_path = os.path.join(processed_path, 'Cleaned_WorldExpenditures.csv')
        filtered_data.to_csv(processed_file_path, index=False)

        print(f"Filtered data saved to {processed_file_path}")
    except Exception as e:
        print(f"Error processing {file_name}: {e}")


for file in files:
    file_path = os.path.join(data_path, file)
    try:
        df = pd.read_csv(file_path, delimiter=';')
        df = clean_dataframe(df)
        data_dict[file] = df
        print(f"Cleaned {file} with shape {df.shape}")
    except Exception as e:
        print(f"Error processing {file}: {e}")

countries_of_interest = ['Brazil', 'India', 'China', 'Russian Federation', 'South Africa']

cleaned_data_path = 'C:/Users/ARSH/brics-economic-analysis/venv/data/processed'
os.makedirs(cleaned_data_path, exist_ok=True)
clean_and_save_world_expenditures(data_path, cleaned_data_path, countries_of_interest)

for key, df in data_dict.items():
    cleaned_file_path = os.path.join(cleaned_data_path, key)
    df.to_csv(cleaned_file_path, index=False)
    print(f"Saved cleaned data: {cleaned_file_path}")
