import sqlite3
import pandas as pd
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
df = pd.DataFrame(rows,  columns=['date', 'country_code', 'city', 'indicator', 'count', 'min', 'max', 'median', 'variance'])

# Ubah format data tanggal
df['date'] = pd.to_datetime(df['date'])

df = df.sort_values(by='date')

df = df[df['indicator']=='pm25'] 

# Tambahkan kolom tahun, bulan, dan hari
df['year'] = df['date'].dt.year

median_pm25_per_year = df.groupby('year')['median'].median()

st.dataframe(median_pm25_per_year)