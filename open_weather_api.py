import pandas as pd
import streamlit as st
import requests
from datetime import datetime, timezone

# Replace with your actual API key
API_key = "cdc2c6d95c0c0d6762d9fcc26ae895ef"

# Jakarta's coordinates
jakarta_lat = -6.1753942
jakarta_lon = 106.827183

# Convert start and end dates to Unix timestamps
start_date = "2013-01-01"
end_date = "2023-11-12"

# Function to convert date to Unix timestamp
def date_to_unix_time(date):
    dt_object = datetime.strptime(date, "%Y-%m-%d")
    unix_time = int(dt_object.replace(tzinfo=timezone.utc).timestamp())
    return unix_time

# Get Unix timestamps for start and end dates
start_unix_time = date_to_unix_time(start_date)
end_unix_time = date_to_unix_time(end_date)

# Check if Unix timestamps are obtained successfully
if start_unix_time is not None and end_unix_time is not None:
    # API endpoint
    api_url = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={jakarta_lat}&lon={jakarta_lon}&start={start_unix_time}&end={end_unix_time}&appid={API_key}"

    # Make the API request
    response = requests.get(api_url)

    # Get the JSON data
    json_data = response.json()

    # Extract relevant data for DataFrame
    data_list = json_data.get("list", [])

    # Create DataFrame
    df = pd.json_normalize(data_list)

    # Convert Unix timestamp to datetime
    df["dt"] = pd.to_datetime(df["dt"], unit="s")

    # Select relevant columns
    selected_columns = ["dt", "main.aqi", "components.co", "components.no", "components.no2", "components.o3", "components.so2", "components.pm2_5", "components.pm10", "components.nh3"]

    # Rename columns
    column_mapping = {
        "dt": "DateTime",
        "main.aqi": "AQI",
        "components.co": "CO",
        "components.no": "NO",
        "components.no2": "NO2",
        "components.o3": "O3",
        "components.so2": "SO2",
        "components.pm2_5": "PM2.5",
        "components.pm10": "PM10",
        "components.nh3": "NH3",
    }

    df = df[selected_columns].rename(columns=column_mapping)

    # Display DataFrame in Streamlit
    st.dataframe(df)

    # Save DataFrame to CSV
    df.to_csv("pollution_data.csv", index=False)
else:
    st.error("Error obtaining Unix timestamps.")
