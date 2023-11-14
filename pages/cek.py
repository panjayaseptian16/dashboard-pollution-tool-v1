import streamlit as st
import pandas as pd
import sqlite3
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt

# Membaca data dari file CSV
file_path = 'jakarta.csv'
df = pd.read_csv(file_path)

# Mengubah kolom 'time_code' menjadi tipe data datetime
df['time_code'] = pd.to_datetime(df['time_code'], format='%Y%m%d %H:%M')

# Menambahkan kolom baru 'date' yang berisi tanggal
df['date'] = df['time_code'].dt.date

# Melakukan pengelompokan (group by) berdasarkan tanggal dan menghitung median AQI
result = df.groupby('date')['value'].median().reset_index()
result = result.rename(columns={'value': 'median_aqi'})

# Ambil data dari database
conn = sqlite3.connect('pollution.db')
cursor = conn.cursor()
cursor.execute(
    '''
    SELECT * FROM daily_aqi WHERE indicator LIKE '%pm25%';
    '''
)
rows = cursor.fetchall()
# Menutup koneksi
conn.close()

# Mengonversi data ke dalam DataFrame
aqi_df = pd.DataFrame(rows, columns=['date', 'country_code', 'city', 'indicator', 'count', 'min', 'max', 'median', 'variance'])

# Mengubah format tanggal pada DataFrame dari database SQLite agar sesuai
aqi_df['date'] = pd.to_datetime(aqi_df['date']).dt.date

# Memilih hanya kolom yang diperlukan
median_df = aqi_df[['date', 'median']]

# Melakukan inner join dengan hasil sebelumnya
result_df = pd.merge(result, median_df, on='date', how='inner')

# Perform hypothesis testing (e.g., Pearson correlation)
correlation, p_value = stats.pearsonr(result_df['median_aqi'], result_df['median'])

# Set the significance level (alpha)
alpha = 0.05

# Display the results of the hypothesis test
st.write("Results of Hypothesis Testing:")
st.write(f"Null Hypothesis (H0): There is no significant relationship between Air Quality Index and Traffic Congestion Index.")
st.write(f"Alternative Hypothesis (H1): There is a significant relationship between Air Quality Index and Traffic Congestion Index.")
st.write(f"Pearson Correlation Coefficient: {correlation}")
st.write(f"P-value: {p_value}")

# Check if the p-value is less than alpha to decide whether to reject the null hypothesis
if p_value < alpha:
    st.write("Result: Reject the Null Hypothesis. There is a significant relationship between Air Quality Index and Traffic Congestion Index.")
else:
    st.write("Result: Fail to reject the Null Hypothesis. There is no significant relationship between Air Quality Index and Traffic Congestion Index.")

# Visualization: Scatter plot and regression line
fig_scatter, ax_scatter = plt.subplots(figsize=(10, 6))
sns.regplot(x='median_aqi', y='median', data=result_df, ax=ax_scatter)
ax_scatter.set_title('Scatter Plot and Regression Line')
ax_scatter.set_xlabel('Median AQI')
ax_scatter.set_ylabel('Traffic Congestion Index (Median)')
st.pyplot(fig_scatter)