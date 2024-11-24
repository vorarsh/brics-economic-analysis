import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
from modeling import build_prophet_model, prepare_data_for_prophet
from correlation_chart import plot_gdp_expenditure_correlation

DATA_PATH = r'C:\Users\ARSH\brics-economic-analysis\venv\data\transformed'
NUMERICAL_COLUMNS = ['Value']

st.set_page_config(page_title='BRICS Economic Data Analysis', layout='wide')


st.title('🌍 BRICS Economic Data Analysis')
st.markdown("""
Analyze economic indicators of BRICS countries from 1970 to 2020.
Click on the flags below to explore trends for Brazil, Russia, India, China, and South Africa.
""")

st.image("venv/images/Brics.jpg", use_container_width=True)

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

if 'Value' not in data.columns:
    st.error("No 'Value' column found in the dataset.")
    st.stop()
if 'CountryName' not in data.columns:
    st.error("No 'CountryName' column found in the dataset.")
    st.stop()

country_flags = {
    "Brazil": {"emoji": "🇧🇷", "image": "venv/flags/brazil-flag.png"},
    "Russian Federation": {"emoji": "🇷🇺", "image": "venv/flags/russia.png"},
    "India": {"emoji": "🇮🇳", "image": "venv/flags/india.png"},
    "China": {"emoji": "🇨🇳", "image": "venv/flags/china.png"},
    "South Africa": {"emoji": "🇿🇦", "image": "venv/flags/south-africa.png"}
}

if "selected_country" not in st.session_state:
    st.session_state["selected_country"] = "Brazil"  # Default country

st.markdown("""
    <style>
    body {
        background-image: url("venv/images/abstract-bg.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .stButton>button {
        border: none;
        background-color: transparent;
        color: white;
        font-size: 40px;
        font-weight: bold;
        padding: 10px;
        width: 100%;
        text-align: left;
    }
    .stButton>button:hover {
        background-color: #444444;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("### Select a Country:")

for country in country_flags:
    col1, col2 = st.columns([5, 1])  # First column for button, second column for flag
    with col1:
        if st.button(f"{country}"):
            st.session_state["selected_country"] = country
    with col2:
        st.image(country_flags[country]["image"], width=50)  # Display flag next to button

selected_country = st.session_state["selected_country"]

st.markdown(f"### Selected Country: {country_flags[selected_country]['emoji']} {selected_country}")

filtered_data = data[data['CountryName'] == selected_country]

aggregated_data = aggregate_data(filtered_data, 'Value')
aggregated_data = aggregated_data.dropna(subset=['Value'])

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

st.subheader("GDP and Expenditure Correlation for BRICS Nations")
if st.button("Generate GDP vs Expenditure Chart"):
    plot_gdp_expenditure_correlation(DATA_PATH, selected_country)

country_facts = {
    "Brazil": {
        "Capital": "Brasília",
        "Official Language": "Portuguese",
        "Population": "213 million (2021)",
        "Area": "8.5 million km²",
        "Economy": "Largest economy in South America",
        "Famous Landmark": "Christ the Redeemer statue",
        "GDP (2023)": "$2.08 trillion",
        "Projections for 2028": "$2.75 trillion (8th largest economy)",
        "Amazon Rainforest": "Home to more than 60% of the Amazon rainforest",
        "Agriculture": "Leading exporter of coffee, soybeans, corn, sugar, meat, and ethanol",
        "Challenges": "Struggles with political issues, inflation, and income inequality",
        "Average GDP Growth": "0.6% over the past decade",
    },
    "Russian Federation": {
        "Capital": "Moscow",
        "Official Language": "Russian",
        "Population": "146 million (2021)",
        "Area": "17.1 million km²",
        "Economy": "World's 11th largest economy by GDP",
        "Famous Landmark": "The Kremlin",
    },
    "India": {
        "Capital": "New Delhi",
        "Official Language": "Hindi, English",
        "Population": "1.38 billion (2021)",
        "Area": "3.29 million km²",
        "Economy": "World's 6th largest economy by nominal GDP",
        "Famous Landmark": "Taj Mahal"
    },
    "China": {
        "Capital": "Beijing",
        "Official Language": "Mandarin",
        "Population": "1.41 billion (2021)",
        "Area": "9.6 million km²",
        "Economy": "World's 2nd largest economy",
        "Famous Landmark": "Great Wall of China"
    },
    "South Africa": {
        "Capital": "Pretoria (administrative), Cape Town (legislative), Bloemfontein (judicial)",
        "Official Language": "11 official languages, including Zulu, Xhosa, and Afrikaans",
        "Population": "60 million (2021)",
        "Area": "1.22 million km²",
        "Economy": "Most industrialized country in Africa",
        "Famous Landmark": "Table Mountain"
    }
}

st.markdown(f"### Interesting Facts about {selected_country}")
facts = country_facts.get(selected_country, {})
for fact, value in facts.items():
    st.markdown(f"**{fact}:** {value}")

st.markdown("---")
st.markdown("""
👨‍💻 **Developed by Arsh Vora**  
📅 **Data Source**: BRICS economic indicators data (1970-2020)  
""")
