import pandas as pd
import os
from prophet import Prophet
import matplotlib.pyplot as plt

transformed_path = 'C:/Users/ARSH/brics-economic-analysis/venv/data/transformed'
files = os.listdir(transformed_path)

def load_transformed_data(files, path):
    data_dict = {}
    for file in files:
        file_path = os.path.join(path, file)
        try:
            df = pd.read_csv(file_path)
            data_dict[file] = df
        except Exception as e:
            print(f"Error loading {file}: {e}")
    return data_dict


data_dict = load_transformed_data(files, transformed_path)

for file, df in data_dict.items():
    print(f"\nData from {file}")
    print(df.head())

def prepare_data_for_prophet(df):
    df = df[['Year', 'Value']].dropna()
    df = df.rename(columns={'Year': 'ds', 'Value': 'y'})
    df['ds'] = pd.to_datetime(df['ds'], format='%Y')
    return df


sample_file = 'Economy_Data_9_Adjusted_net_savings__including_particulate_emission_damage____of_GNI_.csv'  # Example file
gdp_data = data_dict[sample_file]
prophet_data = prepare_data_for_prophet(gdp_data)


def build_prophet_model(df):
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=30, freq='Y')
    forecast = model.predict(future)
    fig = model.plot(forecast)
    plt.title("Forecast using Prophet")
    plt.xlabel("Year")
    plt.ylabel("Value")
    plt.grid(True)
    plt.show()
    return forecast

forecast = build_prophet_model(prophet_data)
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30))
