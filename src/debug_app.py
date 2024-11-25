import streamlit as st
import pandas as pd
import os

# Path to the folder containing the dataset files
folder_path = r'/src/data/transformed'

# Check if the folder exists
if not os.path.exists(folder_path):
    st.error("The specified folder path does not exist.")
    st.stop()

# Get a list of all files in the folder
file_list = os.listdir(folder_path)
st.write(f"Total files found: {len(file_list)}")

# Filter out non-CSV files
csv_files = [file for file in file_list if file.endswith('.csv')]
st.write(f"CSV files found: {len(csv_files)}")

if len(csv_files) == 0:
    st.error("No CSV files found in the directory.")
    st.stop()

# Read each CSV file and print its structure
data_frames = []
for i, file in enumerate(csv_files):
    file_path = os.path.join(folder_path, file)

    try:
        temp_data = pd.read_csv(file_path)
        st.write(f"File {i + 1}: {file}")
        st.write("Columns:", temp_data.columns)
        st.write("First few rows:")
        st.write(temp_data.head())

        # Check if 'Country' column exists
        if 'Country' not in temp_data.columns:
            st.error(f"Column 'Country' missing in file {file}")
        else:
            data_frames.append(temp_data)

    except Exception as e:
        st.error(f"Error reading file {file}: {e}")

# Combine all data if successful
if data_frames:
    data = pd.concat(data_frames, ignore_index=True)
    st.write("Combined DataFrame Preview:")
    st.write(data.head())
    st.write("Combined DataFrame Columns:", data.columns)

    # Check if 'Country' column exists in the final combined DataFrame
    if 'Country' in data.columns:
        st.write("Unique countries in combined data:", data['Country'].unique())
    else:
        st.error("No 'Country' column found in combined DataFrame.")
else:
    st.error("No data was loaded.")
