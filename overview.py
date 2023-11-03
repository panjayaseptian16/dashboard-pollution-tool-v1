import streamlit as st
from streamlit.components.v1 import html
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


# Adding a sidebar with the required elements
with st.sidebar:
    st.subheader("Created by : ")
    st.markdown("""<h3 style='text-align:center;'>Septian Panjaya</h3>""", unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("[![Linkedin](https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg)](https://www.linkedin.com/in/septian-panjaya)")

st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        position: fixed;
        max-width: 220px;
        padding: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
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


import streamlit as st

html_code = """
<!DOCTYPE html>
<html>
<head>
    <title>AirVisual Widget</title>
</head>
<body>
    <div name="airvisual_widget" key="654518acce379fa31df00fae"></div>
    <script type="text/javascript" src="https://widget.iqair.com/script/widget_v3.0.js"></script>
</body>
</html>
"""

html(html_code, height=500)

import streamlit as st

html_code1 = """
<!DOCTYPE html>
<html>
<head>
    <title>WeatherAPI Widget</title>
</head>
<body>
    <div id="weatherapi-weather-widget-4"></div>
    <script type='text/javascript' src='https://www.weatherapi.com/weather/widget.ashx?loc=3026315&wid=4&tu=1&div=weatherapi-weather-widget-4' async></script><noscript><a href="https://www.weatherapi.com/weather/q/jakarta-3026315" alt="Hour by hour Jakarta weather">10 day hour by hour Jakarta weather</a>
    </noscript></body>
</html>
"""

html(html_code1, height=500)
