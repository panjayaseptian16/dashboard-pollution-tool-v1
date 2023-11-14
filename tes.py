import pandas as pd
import streamlit as st
from prophet.plot import plot_plotly, plot_components_plotly, plot_cross_validation_metric
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
from statsmodels.tools.eval_measures import rmse
import sqlite3
from datetime import date
import holidays

# Judul dan deskripsi
st.title("Prediksi Indeks Kualitas Udara dengan Prophet")
st.subheader("Aplikasi ini menggunakan model Prophet untuk memprediksi nilai Indeks Kualitas Udara (AQI).")

# Membaca data dari database
conn = sqlite3.connect('pollution.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM daily_aqi WHERE indicator LIKE "%pm25%";')
rows = cursor.fetchall()
conn.close()

# Mengonversi data ke dalam DataFrame
df = pd.DataFrame(rows, columns=['date', 'country_code', 'city', 'indicator', 'count', 'min', 'max', 'median', 'variance'])
df = df[["date", "median"]]
df.columns = ['ds', 'y']
df['ds'] = pd.to_datetime(df['ds'])

# Kontrol untuk jangka waktu prediksi
forecast_period = st.slider("Pilih Periode Prediksi (dalam hari):", min_value=1, max_value=730, value=365)  # 730 hari untuk 2 tahun

st.line_chart(df.set_index('ds'), use_container_width=True)

# Buat DataFrame untuk hari libur
new_holidays = holidays.ID(years=[2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025], language="id")
holiday_dates = []
holiday_names = []
for dt, name in sorted(new_holidays.items()):
    holiday_dates.append(dt)
    holiday_names.append(name)
holiday_df = pd.DataFrame({'ds': pd.to_datetime(holiday_dates), 'holiday': holiday_names})

# Fit model
model = Prophet(holidays=holiday_df)
model.add_seasonality('semiannual', period=182.5, fourier_order=6)
model.fit(df)
future = model.make_future_dataframe(periods=forecast_period)
forecast = model.predict(future)

# Menampilkan grafik menggunakan plotly_chart di Streamlit
st.plotly_chart(plot_plotly(model, forecast))

# Menampilkan komponen-komponen grafik menggunakan plotly_chart di Streamlit
st.plotly_chart(plot_components_plotly(model, forecast))

# Cross-validation
df_cv = cross_validation(model, initial='730 days', period='180 days', horizon='365 days')

# Menampilkan plot Cross-Validation Metric
fig_cv_metric = plot_cross_validation_metric(df_cv, metric='mape')
st.subheader('Plot Cross-Validation Metric:')
st.plotly_chart(fig_cv_metric)

# Menghitung dan menampilkan RMSE di Streamlit
train = df.iloc[:len(df)-forecast_period]
test = df.iloc[len(df)-forecast_period:]
predictions = forecast.iloc[-forecast_period:]['yhat']
rmse_value = rmse(predictions, test['y'])
st.write(f"Root Mean Squared Error antara nilai aktual dan nilai prediksi: {rmse_value}")
st.write(f"Nilai Rata-rata dari Dataset Uji: {test['y'].mean()}")
