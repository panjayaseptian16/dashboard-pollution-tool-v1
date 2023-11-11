import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import sqlite3


#@st.cache_resource
def read_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content

st.set_page_config(
    page_title="Dashboard and Realtime Monitoring",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.markdown("""
            <h3 style="text-align: center;color:#FFFD8C;">Air Quality Realtime Monitoring</h3>
            """, unsafe_allow_html=True)

# Baca konten HTML dari berkas interactive_aqi_widget.html
tes_html = read_file("tes.html")

tab1,tab2,tab3 = st.tabs(['Widget', 'Alternative', 'Weather'])
with tab1: 
    with st.container():
        html(tes_html, height=425)
        st.markdown(
        "<p style='margin-top:-25px; text-align: center; font-size: 14px; color:#1F4172;'>Air Quality Index (AQI) scale as defined by the US-EPA 2016 standard. Check details in <a href='https://aqicn.org/scale/'>here</a></p>",
        unsafe_allow_html=True)
with tab2:
    html_code = """
        <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AirVisual Widget</title>
        <style>
            div[name="airvisual_widget"] {
                position: absolute;
                top: 20%;
                left: 50%;
                transform: translate(-50%, -50%);
                transition: transform 0.3s;
            }
            div[name="airvisual_widget"]:hover {
                transform: translate(-50%, -50%) scale(1.1);
            }
        </style>
        <script type="text/javascript">
            window.onload = function() {
                var widget = document.querySelector('div[name="airvisual_widget"]');
                widget.addEventListener('click', function(event) {
                    event.preventDefault(); // Mencegah tindakan default
                    event.stopPropagation(); // Mencegah penyebaran event
                });
            };
        </script>
    </head>
    <body>
        <div name="airvisual_widget" key="654518acce379fa31df00fae"></div>
        <script type="text/javascript" src="https://widget.iqair.com/script/widget_v3.0.js"></script>
    </body>
    </html>
    """
    html(html_code, height=500)

with tab3: 
    html_code1 = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>WeatherAPI Widget</title>
            <style>
                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
                #weatherapi-weather-widget-4 {
                    width: 320px; /* Sesuaikan lebar sesuai kebutuhan Anda */
                    transition: transform 0.3s;
                }
                #weatherapi-weather-widget-4:hover {
                    transform: scale(1.1);
                }
            </style>
        </head>
        <body>
            <div id="weatherapi-weather-widget-4"></div>
            <script type='text/javascript' src='https://www.weatherapi.com/weather/widget.ashx?loc=3026315&wid=4&tu=1&div=weatherapi-weather-widget-4' async></script><noscript><a href="https://www.weatherapi.com/weather/q/jakarta-3026315" alt="Hour by hour Jakarta weather">10 day hour by hour Jakarta weather</a>
            </noscript></body>
        </html>
        """
    html(html_code1, height=500)


st.markdown("""
            <h3 style="text-align: center;color:#FFFD8C;">Dashboard Pollution in Jakarta</h3>
            """, unsafe_allow_html=True)

# Perform query
#df = pd.read_csv("daily-aqi.csv", sep=',', names=["date","country","city","indicator","count","min","max","median","variance"])

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
df['month'] = df['date'].dt.month_name().str.slice(0, 3)
df['day'] = df['date'].dt.day_name().str.slice(0, 3)

with st.container():
    # Buat tab pertama
    tab1, tab2, tab3, tab4 = st.tabs(["Median AQI PM2.5 (2018-2023)", "Daily Statistics", "Monthly Statistics", "Yearly Statistics"])
    # Buat tab kedua
    with tab1: 
        col1,col2 = st.columns([2,1],gap="small")
        with col1:
            # Plot data menggunakan Plotly
            fig = px.line(df, x='date', y=['median'], title='Median AQI PM2.5 (2018-2023)')
            fig.update_layout(yaxis_range=[0, 169], xaxis_title='Date', yaxis_title='Median AQI', title_x=0.3, width=950, height=500, xaxis_showgrid=False, yaxis_showgrid=False)
            fig.update_layout(annotations=[
            dict(
                x="2018-10-01",
                y=0.5,
                xref="x",
                yref="paper",
                text="No Data",
                showarrow=False,
                font=dict(
                    family="Arial",
                    size=16,
                    color="black"
                ))])
            fig.add_hrect(y0=0, y1=50, fillcolor="green", opacity=0.2, line_width=0, annotation_text="<b>Good</b>")
            fig.add_hrect(y0=50, y1=100, fillcolor="yellow", opacity=0.2, line_width=0, annotation_text="<b>Moderate</b>")
            fig.add_hrect(y0=100, y1=df['median'].max(), fillcolor="red", opacity=0.2, line_width=0, annotation_text="<b>Unhealthy</b>")
            fig.add_vrect(x0=datetime.datetime(2018, 7, 1), x1=datetime.datetime(2018, 12, 31),fillcolor="lightgrey", opacity=0.8, line_width=0)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        with col2:
           caption = "Air pollution in Jakarta is still a cause for concern, even though PM2.5 AQI has fluctuated from 2018 to 2023 and always decreased during the end and beginning of the year. The median PM2.5 AQI in Jakarta is still predominantly in the <span style='color:red;font-weight:bold;'>unhealthy</span> and <span style='color:yellow;font-weight:bold;'>moderate</span> level, which means that air pollution in Jakarta can still have a negative impact on the public. This implies that there hasn't been any effective policy or program to address this issue significantly."
           st.markdown(f"<p style='text-align: center; margin-top: 25%;'>{caption}</p>", unsafe_allow_html=True)

    # Buat tab kedua
    with tab2:
        year_filter = st.slider("Select Year", min_value=int(df['year'].min()), max_value=int(df['year'].max()), value=(int(df['year'].min()), int(df['year'].max())))
        df_filtered = df[(df['year'] >= year_filter[0]) & (df['year'] <= year_filter[1])]
        use_stack_bar = st.checkbox("Show Stack Bar (with min & max)", value=False)

        if use_stack_bar:
            df_day_stacked = df_filtered.groupby('day').agg({'min': 'median', 'median': 'median', 'max': 'median'}).reset_index()
            fig2 = px.bar(df_day_stacked, x='day', y=['min', 'median', 'max'], title='Min, Median, and Max PM2.5 per Day', barmode='stack')
            fig2.update_layout(width=850, height=500, title_x=0.4, xaxis={'categoryorder':'array', 'categoryarray':['Mon','Tue','Wed','Thu','Fri','Sat','Sun']}, xaxis_showgrid=False, yaxis_showgrid=False)
            fig2.add_hrect(y0=0, y1=50, fillcolor="green", opacity=0.2, line_width=0, annotation_text="<b>Good</b>")
            fig2.add_hrect(y0=50, y1=100, fillcolor="yellow", opacity=0.2, line_width=0, annotation_text="<b>Moderate</b>")
            fig2.add_hrect(y0=100, y1=df['max'].max(), fillcolor="red", opacity=0.2, line_width=0, annotation_text="<b>Unhealthy</b>")
            st.plotly_chart(fig2)
        else:
            col3,col4 = st.columns([2,1],gap="medium")
            with col3:
                df_day = df_filtered.groupby('day').agg({'median': 'median'}).reset_index()
                fig2 = px.bar(df_day, x='day', y='median', title='Median PM2.5 per Day', barmode='stack')
                fig2.update_layout(width=850, height=500, title_x=0.4, xaxis={'categoryorder':'array', 'categoryarray':['Mon','Tue','Wed','Thu','Fri','Sat','Sun']}, xaxis_showgrid=False, yaxis_showgrid=False)
                fig2.add_hrect(y0=0, y1=50, fillcolor="green", opacity=0.2, line_width=0, annotation_text="<b>Good</b>")
                fig2.add_hrect(y0=50, y1=100, fillcolor="yellow", opacity=0.2, line_width=0, annotation_text="<b>Moderate</b>")
                fig2.add_hrect(y0=100, y1=df_day['median'].max(), fillcolor="red", opacity=0.2, line_width=0, annotation_text="<b>Unhealthy</b>")
                st.plotly_chart(fig2)
            with col4:
                caption1 =  "apaam"
                st.markdown(f"<p style='text-align: center; margin-top: 25%;'>{caption1}</p>", unsafe_allow_html=True)
            
    # Buat tab ketiga
    with tab3:
        year_filter1 = st.slider("Select Year", min_value=int(df['year'].min()), max_value=int(df['year'].max()), value=(int(df['year'].min()), int(df['year'].max())), key='slider_tab3')
        df_filtered1 = df[(df['year'] >= year_filter1[0]) & (df['year'] <= year_filter1[1])]
        use_stack_bar_tab3 = st.checkbox("Show Stack Bar (with min & max)", value=False, key='stack_bar_tab3')

        if use_stack_bar_tab3:
            df_bulan_stacked = df_filtered1.groupby('month').agg({'min': 'median', 'median': 'median', 'max': 'median'}).reset_index()
            fig3 = px.bar(df_bulan_stacked, x='month', y=['min', 'median', 'max'], title='Min, Median, and Max PM2.5 per Month', barmode='stack')
            fig3.update_layout(width=850, height=500, title_x=0.4, xaxis={'categoryorder':'array', 'categoryarray':['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']}, xaxis_showgrid=False, yaxis_showgrid=False)
            fig3.add_hrect(y0=0, y1=50, fillcolor="green", opacity=0.2, line_width=0, annotation_text="<b>Good</b>")
            fig3.add_hrect(y0=50, y1=100, fillcolor="yellow", opacity=0.2, line_width=0, annotation_text="<b>Moderate</b>")
            fig3.add_hrect(y0=100, y1=df['max'].max(), fillcolor="red", opacity=0.2, line_width=0, annotation_text="<b>Unhealthy</b>")
        else:
            df_bulan = df_filtered1.groupby('month')['median'].median().reset_index()
            fig3 = px.bar(df_bulan, x='month', y='median', title='Median PM2.5 per Month')
            fig3.update_layout(width=850, height=500, title_x=0.4, xaxis={'categoryorder':'array', 'categoryarray':['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']}, xaxis_showgrid=False, yaxis_showgrid=False)
            fig3.add_hrect(y0=0, y1=50, fillcolor="green", opacity=0.2, line_width=0, annotation_text="<b>Good</b>")
            fig3.add_hrect(y0=50, y1=100, fillcolor="yellow", opacity=0.2, line_width=0, annotation_text="<b>Moderate</b>")
            fig3.add_hrect(y0=100, y1=df_bulan['median'].max(), fillcolor="red", opacity=0.2, line_width=0, annotation_text="<b>Unhealthy</b>")
        st.plotly_chart(fig3)


    # Buat tab keempat
    with tab4:
        df_tahun = df.groupby(df['year'])['median'].median().reset_index()
        fig4 = px.line(df_tahun, x='year', y='median', title='Median PM2.5 per Year', markers=True)
        fig4.update_layout(width=850, height=500, title_x = 0.4, xaxis_showgrid=False, yaxis_showgrid=False)
        fig4.add_hrect(y0=0, y1=50, fillcolor="green", opacity=0.2, line_width=0, annotation_text="<b>Good</b>")
        fig4.add_hrect(y0=50, y1=100, fillcolor="yellow", opacity=0.2, line_width=0, annotation_text="<b>Moderate</b>")
        fig4.add_hrect(y0=100, y1=df['median'].max(), fillcolor="red", opacity=0.2, line_width=0, annotation_text="<b>Unhealthy</b>")
        fig4.add_vrect(x0=2020, x1=2022, fillcolor="lightgrey", opacity=0.5, line_width=0)
        fig4.add_annotation(text="Period of COVID-19 (PSBB/PPKM)", x=2021, y=110, showarrow=False, font=dict(family="monospace", size=16, color="black"))
    
        st.plotly_chart(fig4)

conn = sqlite3.connect('pollution.db')
cursor = conn.cursor()
cursor.execute(
    '''
    SELECT date, temperature, tmax, tmin
    FROM temperature
    '''
)
rows1 = cursor.fetchall()
# Menutup koneksi
conn.close()
# Mengonversi data ke dalam DataFrame
df1 = pd.DataFrame(rows1, columns=['date','temperature', 'tmax', 'tmin'])
df1['date'] = pd.to_datetime(df1['date'])
df1 = df1.groupby('date')[['temperature', 'tmax','tmin']].mean().reset_index()

temperature = df1.sort_values(by='date')
pm25 = df.loc[:, ["date", "median"]]
pm25 = pm25.rename(columns={"median": "pm25"})

result = pd.merge(temperature, pm25, on='date', how='inner')
result = result.sort_values(by='date')

st.dataframe(result)
result = result.drop('date', axis=1)
result = result.rename(columns={"temperature": "tavg"})

st.dataframe(result)

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

corr_matrix = result.corr()

plt.figure(figsize=(3, 2))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
st.pyplot(plt.gcf())  # Use plt.gcf() to get the current figure

# Menampilkan nilai korelasi
st.write("Heatmap Korelasi:")
st.write(corr_matrix)

# testing
conn = sqlite3.connect('pollution.db')
cursor = conn.cursor()
cursor.execute(
    '''
    select pm10.date,
       pm10.median as pm10,
       dew.median as dew,
       humidity.median as humidity,
       pm25.median as pm25,
       pressure.median as pressure, 
       temperature.median as temperature,
       wind_gust.median as wind_gust,
       wind_speed.median as wind_speed
from 
    (select date, median 
     from daily_aqi
     where indicator LIKE '%pm10%') as pm10
join 
    (select date, median 
     from daily_aqi
     where indicator LIKE '%dew%') as dew
on pm10.date = dew.date
join (select date, median 
     from daily_aqi
     where indicator LIKE '%humidity%') as humidity
on dew.date = humidity.date
join (select date, median 
     from daily_aqi
     where indicator LIKE '%pm25%') as pm25
on humidity.date = pm25.date
join (select date, median 
     from daily_aqi
     where indicator LIKE '%pressure%') as pressure
on pm25.date = pressure.date
join (select date, median 
     from daily_aqi
     where indicator LIKE '%temperature%') as temperature
on pressure.date = temperature.date
join (select date, median 
     from daily_aqi
     where indicator LIKE '%wind-gust%') as wind_gust
on temperature.date = wind_gust.date
join (select date, median 
     from daily_aqi
     where indicator LIKE '%wind-speed%') as wind_speed
on wind_gust.date = wind_speed.date
order by pm10.date
    '''
)
rows2 = cursor.fetchall()
# Menutup koneksi
conn.close()

df2 = pd.DataFrame(rows2, columns=['date','pm10', 'dew', 'humidity', 'pm25', 'pressure', 'temperature', 'wind-gust', 'wind-speed'])
df2 = df2.sort_values(by='date')
df2 = df2.drop('date', axis=1)
corr_matrix1 = df2.corr()

plt.figure(figsize=(3, 2))
sns.heatmap(corr_matrix1, annot=True, cmap='coolwarm', linewidths=0.5)
st.pyplot(plt.gcf())
st.write("Heatmap Korelasi:")
st.write(corr_matrix1)