import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st


def plot_gdp_expenditure_correlation(directory_path, selected_country):
    all_data = []
    for file in os.listdir(directory_path):
        if file.endswith('.csv'):
            file_path = os.path.join(directory_path, file)
            df = pd.read_csv(file_path)
            all_data.append(df)

    combined_data = pd.concat(all_data, ignore_index=True)

    country_data = combined_data[combined_data['CountryName'] == selected_country]

    gdp_data = country_data[country_data['SeriesName'].str.contains('GDP', case=False)]
    expenditure_data = country_data[country_data['SeriesName'].str.contains('expenditure', case=False)]

    if gdp_data.empty or expenditure_data.empty:
        st.error(f"GDP or Expenditure data is not available for {selected_country}.")
        return

    gdp_data = gdp_data[['Year', 'Value']].rename(columns={'Value': 'GDP'})
    expenditure_data = expenditure_data[['Year', 'Value']].rename(columns={'Value': 'Expenditure'})

    gdp_data = gdp_data.groupby('Year', as_index=False).mean()
    expenditure_data = expenditure_data.groupby('Year', as_index=False).mean()

    merged_data = pd.merge(gdp_data, expenditure_data, on='Year', how='inner')

    plt.figure(figsize=(12, 8))

    sns.lineplot(
        data=merged_data,
        x='Year',
        y='GDP',
        label='GDP (in USD)',
        marker='o',
        linestyle='-',
    )
    sns.lineplot(
        data=merged_data,
        x='Year',
        y='Expenditure',
        label='Expenditure (% of GDP)',
        marker='s',
        linestyle='--',
    )

    plt.title(f"GDP and Expenditure Trends Over Years for {selected_country}")
    plt.xlabel("Year")
    plt.ylabel("Value (USD for GDP and % for Expenditure)")

    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    st.pyplot(plt)
