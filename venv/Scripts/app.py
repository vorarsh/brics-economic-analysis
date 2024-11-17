import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
from modeling import build_prophet_model, prepare_data_for_prophet

DATA_PATH = r'C:\Users\ARSH\brics-economic-analysis\venv\data\transformed'
NUMERICAL_COLUMNS = ['Value']

st.set_page_config(page_title='BRICS Economic Data Analysis', layout='centered')
st.title('🌍 BRICS Economic Data Analysis')
st.markdown("""
Analyze economic indicators of BRICS countries from 1970 to 2020.
Use the filters to explore trends for Brazil, Russia, India, China, and South Africa.
""")

def load_data(folder_path):
    file_list = os.listdir(folder_path)
    csv_files = [file for file in file_list if file.endswith('.csv')]
    data = pd.DataFrame()
    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        temp_data = pd.read_csv(file_path)
        data = pd.concat([data, temp_data], ignore_index=True)
    return data

def clean_data(data):
    data.columns = data.columns.str.strip()
    data['Year'] = data['Year'].astype(int)
    data['Value'] = data['Value'].apply(lambda x: np.nan if x < 0 else x)
    return data

def aggregate_data(data, column):
    aggregated_data = data.groupby(['Year'])[column].mean().reset_index()
    return aggregated_data

data = load_data(DATA_PATH)
data = clean_data(data)
st.write("Loaded data:", data.head())

if 'Value' not in data.columns:
    st.error("No 'Value' column found in the dataset.")
    st.stop()
if 'CountryName' not in data.columns:
    st.error("No 'CountryName' column found in the dataset.")
    st.stop()

st.sidebar.header('Filter Data')
selected_country = st.sidebar.selectbox('Select Country:', data['CountryName'].unique())

year_min = data['Year'].min()
year_max = data['Year'].max()
selected_year_range = st.sidebar.slider('Select Year Range', min_value=year_min, max_value=year_max,
                                        value=(year_min, year_max))

filtered_data = data[(data['CountryName'] == selected_country) &
                     (data['Year'] >= selected_year_range[0]) &
                     (data['Year'] <= selected_year_range[1])]

aggregated_data = aggregate_data(filtered_data, 'Value')
aggregated_data = aggregated_data.dropna(subset=['Value'])
st.write("Aggregated data:", aggregated_data.head())

prophet_data = prepare_data_for_prophet(aggregated_data)
forecast = build_prophet_model(prophet_data)
forecast = forecast.rename(columns={'ds': 'Year', 'yhat': 'Value'})
forecast = forecast[forecast['Year'].dt.year > 2023]  # Filter future years

st.subheader(f"📊 Value for {selected_country} (Past Growth)")
fig_past = px.line(aggregated_data, x='Year', y='Value', title=f'Value Trend for {selected_country} (Past Growth)', markers=True)
if not aggregated_data['Value'].isna().all():
    max_value_row = aggregated_data.loc[aggregated_data['Value'].idxmax()]
    min_value_row = aggregated_data.loc[aggregated_data['Value'].idxmin()]
    fig_past.add_scatter(x=[max_value_row['Year']], y=[max_value_row['Value']], mode='markers+text',
                         text=['Max Value'], textposition='top center', marker=dict(color='green', size=10))
    fig_past.add_scatter(x=[min_value_row['Year']], y=[min_value_row['Value']], mode='markers+text',
                         text=['Min Value'], textposition='bottom center', marker=dict(color='red', size=10))
st.plotly_chart(fig_past)

st.subheader(f"📊 Value for {selected_country} (Predictive Growth)")
fig_predictive = px.line(forecast, x='Year', y='Value', title=f'Value Predicted Trend for {selected_country} (2024-2050)', markers=True)
st.plotly_chart(fig_predictive)

if not aggregated_data['Value'].isna().all():
    st.markdown(f"📈 **Highest Value**: {max_value_row['Value']} in {max_value_row['Year']}")
    st.markdown(f"📉 **Lowest Value**: {min_value_row['Value']} in {min_value_row['Year']}")

st.markdown("---")
st.markdown("""
👨‍💻 **Developed by Arsh Vora**  
📅 **Data Source**: BRICS Economic Dataset (1970-2020)
""")
