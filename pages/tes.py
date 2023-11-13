import pandas as pd 
import streamlit as st   
import plotly.express as px
from prophet.plot import plot_plotly, plot_components_plotly
from prophet import Prophet
from statsmodels.tools.eval_measures import rmse
import sqlite3
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar

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
df = pd.DataFrame(rows,  columns=['date', 'country_code', 'city', 'indicator', 'count', 'min', 'max', 'median', 'variance'])
df = df[["date","median"]]
df.columns = ['ds','y']
df['ds'] = pd.to_datetime(df['ds'])

# Kontrol untuk jangka waktu prediksi
forecast_period = st.slider("Select Forecast Period (in days):", min_value=1, max_value=365, value=365)

# Menampilkan DataFrame
st.dataframe(df)

# Menampilkan line chart dengan opsi visualisasi
st.line_chart(df.set_index('ds'), use_container_width=True)

# Menentukan hari libur
cal = calendar()
holidays = cal.holidays(start=df['ds'].min(), end=df['ds'].max(), return_name=True)
holiday_df = pd.DataFrame(data=holidays, columns=['holiday'])
holiday_df = holiday_df.reset_index().rename(columns={'index': 'ds'})

# Menambahkan hari libur ke model Prophet
model = Prophet(holidays=holiday_df)
model.fit(df)
future = model.make_future_dataframe(periods=forecast_period)
forecast = model.predict(future)

# Menampilkan grafik menggunakan plotly_chart di Streamlit
st.plotly_chart(plot_plotly(model, forecast))

# Menampilkan komponen-komponen grafik menggunakan plotly_chart di Streamlit
st.plotly_chart(plot_components_plotly(model, forecast))

# Menghitung dan menampilkan RMSE di Streamlit
train = df.iloc[:len(df)-365]
test = df.iloc[len(df)-365:]
predictions = forecast.iloc[-365:]['yhat']
rmse_value = rmse(predictions, test['y'])
st.write(f"Root Mean Squared Error between actual and predicted values: {rmse_value}")
st.write(f"Mean Value of Test Dataset: {test['y'].mean()}")
