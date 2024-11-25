
---

# BRICS Economic Data Analysis

## Overview

This project provides an interactive analysis of economic indicators for the BRICS countries (Brazil, Russia, India, China, and South Africa) from 1970 to 2020. It uses data from various economic sources, such as government expenditure, GDP growth, and adjusted savings, to visualize historical trends and make predictive models for future growth. 

The project leverages **Streamlit** for building the web-based application and **Plotly** for interactive visualizations. It also incorporates **Prophet** for time-series forecasting of economic trends.

---

## Key Features

- **Country Selection**: Users can choose a BRICS country to explore its economic data.
- **Historical Data Visualization**: Display trends and insights for economic indicators (e.g., GDP, government expenditure) over time.
- **Predictive Modeling**: Future predictions (2024–2050) based on historical data using **Prophet**.
- **Interactive Charts**: Generate interactive charts that visualize data points and trends.
- **Economic Correlation**: Visualize the correlation between GDP and government expenditure for BRICS nations.
- **Country Facts**: Display interesting facts about the selected country (e.g., GDP size, exports, key industries).

---

## Technologies Used

- **Streamlit**: For building the interactive web application.
- **Plotly**: For interactive and customizable data visualizations.
- **Pandas & Numpy**: For data manipulation and processing.
- **Prophet**: For time-series forecasting of economic data.
- **Python**: The main programming language used for data analysis and visualization.

---

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/brics-economic-data-analysis.git
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the Streamlit application:
    ```bash
    streamlit run src/app.py
    ```

4. Visit `http://localhost:8501` in your browser to view the app.

---

## Data

The project uses economic data from multiple sources covering BRICS countries (Brazil, Russia, India, China, and South Africa). The dataset includes:

- **GDP growth** (annual growth rate of GDP)
- **Government consumption expenditure** (as a percentage of GDP)
- **Adjusted savings** (taking into account environmental and human capital depreciation)

The data spans from **1970 to 2020** and is stored in CSV files.

---

## Features to Explore

- **Select a Country**: Choose one of the BRICS countries to explore its historical data and predictions.
- **Economic Growth Trends**: View past and future growth projections for GDP and other economic metrics.
- **Interactive Charts**: Visualize the trends using interactive line charts.
- **Country-Specific Insights**: Learn more about the country’s economic facts, key exports, and challenges.

---

## Acknowledgments

- **Streamlit** and **Plotly** for creating excellent frameworks for data science applications and interactive visualizations.
- **Prophet** for providing an easy way to forecast time series data.
- **The data sources** Kaggle for making global economic data accessible.
