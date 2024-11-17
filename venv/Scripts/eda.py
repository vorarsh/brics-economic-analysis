import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set(style="whitegrid")
data_path = 'C:/Users/ARSH/brics-economic-analysis/venv/data/processed'
files = os.listdir(data_path)

def load_data(files, data_path):
    data_dict = {}
    for file in files:
        file_path = os.path.join(data_path, file)
        try:
            df = pd.read_csv(file_path)
            data_dict[file] = df
        except Exception as e:
            print(f"Error loading {file}: {e}")
    return data_dict

def basic_exploration(df):
    print(df.head())
    print(df.info())
    print(df.describe())

def plot_trends(df, column, title):
    plt.figure(figsize=(10,6))
    sns.lineplot(x="Year", y=column, data=df)
    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel(column)
    plt.tight_layout()
    plt.show()

data_dict = load_data(files, data_path)

gdp_data = data_dict['Economy_Data_1_Adjusted_net_national_income__annual___growth_.csv']
basic_exploration(gdp_data)

plot_trends(gdp_data, 'Value', 'GDP Growth for India')


def plot_correlation(data):
    correlation_matrix = data.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    plt.show

gdp_data = data_dict['Economy_Data_1_Adjusted_net_national_income__annual___growth_.csv']
gov_expenditure_data = data_dict['Economy_Data_76_Final_consumption_expenditure__current_US__.csv']
merged_data = pd.merge(gdp_data, gov_expenditure_data, on=['CountryName', 'Year'], how='inner')
plot_correlation(merged_data[['Value_x', 'Value_y']])
plt.savefig('visualizations/gdp_growth_india.png')  # Save the plot to the visualizations folder
