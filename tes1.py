import pandas as pd
import streamlit as st
import plotly.express as px
from prophet.plot import plot_plotly, plot_components_plotly
from prophet import Prophet
from statsmodels.tools.eval_measures import rmse
import sqlite3
from datetime import date
import holidays
from sklearn.metrics import mean_absolute_error

# Judul dan deskripsi
st.title("Air Quality Index Prediction with Prophet")
st.subheader("This application uses the Prophet model to predict Air Quality Index (AQI) values.")

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
forecast_period = st.slider("Select Forecast Period (in days):", min_value=1, max_value=730, value=365)  # 730 days for 2 years

# Menampilkan DataFrame
st.dataframe(df)

# Menampilkan line chart dengan opsi visualisasi
st.line_chart(df.set_index('ds'), use_container_width=True)

# Buat DataFrame untuk hari libur baru
new_holidays = holidays.ID(years=[2018, 2019, 2020, 2021, 2022, 2023], language="id")
holiday_dates = []
holiday_names = []
for dt, name in sorted(new_holidays.items()):
    holiday_dates.append(dt)
    holiday_names.append(name)
holiday_df = pd.DataFrame({'ds': pd.to_datetime(holiday_dates), 'holiday': holiday_names})

# Menambahkan hari libur ke model Prophet
model = Prophet(holidays=holiday_df,interval_width=0.95)
model.fit(df)
future = model.make_future_dataframe(periods = forecast_period)
forecast = model.predict(future)

# Menampilkan grafik menggunakan plotly_chart di Streamlit
st.plotly_chart(plot_plotly(model, forecast),theme=None, use_container_width=True)

# Menampilkan komponen-komponen grafik menggunakan plotly_chart di Streamlit
st.plotly_chart(plot_components_plotly(model, forecast),theme=None, use_container_width=True)

# Menghitung dan menampilkan RMSE di Streamlit
train = df.iloc[:len(df)-forecast_period]
test = df.iloc[len(df)-forecast_period:]
predictions = forecast.iloc[-forecast_period:]['yhat']
rmse_value = rmse(predictions, test['y'])
mae_value = mean_absolute_error(predictions, test['y'])
st.write(f"Mean Absolute Error between actual and predicted values: {mae_value}")
st.write(f"Root Mean Squared Error between actual and predicted values: {rmse_value}")
st.write(f"Mean Value of Test Dataset: {test['y'].mean()}")

