import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import sqlite3
import base64
from prophet.plot import plot_plotly, plot_components_plotly
from prophet import Prophet
import holidays

st.set_page_config(
    page_title="Dashboard and Realtime Monitoring",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="auto",
)

#@st.cache_resource
def read_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content


with st.sidebar: 
    file_ = open("us_epa.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    gif_url = "https://aqicn.org/scale/"
    st.markdown(
    f'<div style="text-align:left;">'
    f'<a href="{gif_url}" target="_blank">'
    f'<img src="data:image/gif;base64,{data_url}" alt="cat gif" style="max-width:100%; cursor: pointer;">'
    f'</a></div>',
    unsafe_allow_html=True)
    st.markdown("<p style='margin-top:10px; text-align: center; font-size: 14px; color:#FFFD8C;'>Air Quality Index (AQI) scale as defined by the US-EPA 2016 standard. Check details in <a href='https://aqicn.org/scale/'>here</a></p>",
        unsafe_allow_html=True)


st.markdown("""
            <h3 style="text-align: center;color:#FFFD8C;">Air Quality Realtime Monitoring</h3>
            """, unsafe_allow_html=True)

# Baca konten HTML dari berkas interactive_aqi_widget.html
tes_html = read_file("tes.html")

with st.container():
    tab1,tab2,tab3 = st.tabs(['Widget', 'Alternative', 'Weather'])
    with tab1: 
        with st.container():
            html(tes_html, height=425)
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

st.divider()
st.markdown("""
            <h3 style="text-align: center;color:#FFFD8C;">Pollution Dashboard in Jakarta</h3>
            """, unsafe_allow_html=True)

st.markdown("##")
st.subheader("Air Quality Index")
st.caption("*NOTE : When the index value increases, it means air quality is decreasing, and vice versa.*")
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
    tab1, tab2, tab3, tab4,tab5 = st.tabs(["Median AQI PM2.5 (2018-2023)", "Daily Statistics", "Monthly Statistics", "Yearly Statistics", "Forecast using Prophet"])
    # Buat tab kedua
    with tab1: 
        col1,col2 = st.columns([2,1],gap="small")
        with col1:
            # Add a Streamlit date range slider
            date_range = st.date_input('Select Date Range:', (datetime.date(2018, 1, 1), datetime.date(2023, 10, 29)),datetime.date(2018, 1, 1), datetime.date(2023, 10, 29))

            # Check if both start_date and end_date are provided
            if len(date_range) == 2 and date_range[0] and date_range[1]:
                # Convert date_range values to Pandas datetime objects
                start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])

                # Filter the DataFrame based on the selected date range
                filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

                # Create the Plotly figure with the filtered DataFrame
                fig = px.line(filtered_df, x='date', y=['median'], title='Median AQI PM2.5 (2018-2023)')
                fig.update_traces(line=dict(width=2, dash='solid'))

                # Add your layout and annotations here (as in your existing code)
                fig.update_layout(yaxis_range=[0, 169], xaxis_title='Date', yaxis_title='AQI', title_x=0.3, width=950, height=500, xaxis_showgrid=False, yaxis_showgrid=False)
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
                fig.add_hrect(y0=0, y1=50, fillcolor=px.colors.qualitative.Set3[0], opacity=0.1, line_width=0.2, annotation_text="<b>Good</b>")
                fig.add_hrect(y0=50, y1=100, fillcolor=px.colors.qualitative.Set3[1], opacity=0.1, line_width=0.2, annotation_text="<b>Moderate</b>")
                fig.add_hrect(y0=100, y1=df['median'].max(), fillcolor=px.colors.qualitative.Set3[3], opacity=0.1, line_width=0.2, annotation_text="<b>Unhealthy</b>")
                fig.add_vrect(x0=datetime.datetime(2018, 7, 1), x1=datetime.datetime(2018, 12, 31),fillcolor="lightgrey", opacity=1, line_width=0.3)

                # Finally, display the Plotly chart in the Streamlit app
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)

            else:
                # Display an error message if the user didn't provide both start and end dates
                st.error("Please provide both start and end dates.")

            
        with col2:
           caption = "Air pollution in Jakarta is still a cause for concern, even though AQI has fluctuated from 2018 to 2023 and always decreased during the end and beginning of the year. The median of AQI in Jakarta is still predominantly in the <span style='color:red;font-weight:bold;'>Unhealthy</span> and <span style='color:yellow;font-weight:bold;'>Moderate</span> level, which means that air pollution in Jakarta can still have a negative impact on the public. This implies that there hasn't been any effective policy or program to address this issue significantly."
           st.markdown(f"<p style='text-align: center; margin-top: 25%;'>{caption}</p>", unsafe_allow_html=True)

    # Buat tab kedua
    with tab2:
        year_filter = st.slider("Select Year", min_value=int(df['year'].min()), max_value=int(df['year'].max()), value=(int(df['year'].min()), int(df['year'].max())))
        df_filtered = df[(df['year'] >= year_filter[0]) & (df['year'] <= year_filter[1])]
        use_stack_bar = st.checkbox("Show Stack Bar (with min & max)", value=False)

        if use_stack_bar:
            col16,col17 = st.columns([2,1],gap="small")
            with col16 :
                df_day_stacked = df_filtered.groupby('day').agg({'min': 'median', 'median': 'median', 'max': 'median'}).reset_index()
                fig2 = px.bar(df_day_stacked, x='day', y=['min', 'median', 'max'], title='Min, Median, and Max AQI by Day of Week', barmode='group')
                fig2.update_layout(xaxis_title='Day of Week', yaxis_title='AQI',width=950, height=500, title_x=0.4, xaxis={'categoryorder':'array', 'categoryarray':['Mon','Tue','Wed','Thu','Fri','Sat','Sun']}, xaxis_showgrid=False, yaxis_showgrid=False)
                fig2.update_yaxes(range=[0, 180])
                fig2.add_hrect(y0=0, y1=50, fillcolor=px.colors.qualitative.Set3[0], opacity=0.3, line_width=0.2, annotation_text="<b>Good</b>")
                fig2.add_hrect(y0=50, y1=100, fillcolor=px.colors.qualitative.Set3[1], opacity=0.3, line_width=0.2, annotation_text="<b>Moderate</b>")
                fig2.add_hrect(y0=100, y1=180, fillcolor=px.colors.qualitative.Set3[3], opacity=0.3, line_width=0.2, annotation_text="<b>Unhealthy</b>")
                st.plotly_chart(fig2,use_container_width=True)
            with col17:
                caption2 =  "When we delve deeper, it turns out that every day there are moments when the AQI reaches higher <span style='color:red;font-weight:bold;'>Unhealthy</span> levels and also times when the AQI touches the <span style='color:green;font-weight:bold;'>Good</span> level."
                st.markdown(f"<p style='text-align: center; margin-top: 25%;'>{caption2}</p>", unsafe_allow_html=True)
            
        else:
            col3,col4 = st.columns([2,1],gap="medium")
            with col3:
                df_day = df_filtered.groupby('day').agg({'median': 'median'}).reset_index()
                fig2 = px.bar(df_day, x='day', y='median', title='Air Quality Index by Day Of Week', barmode='stack')
                fig2.update_layout(xaxis_title='Day of Week', yaxis_title='AQI',width=850, height=500, title_x=0.4, xaxis={'categoryorder':'array', 'categoryarray':['Mon','Tue','Wed','Thu','Fri','Sat','Sun']}, xaxis_showgrid=False, yaxis_showgrid=False)
                fig2.update_yaxes(range=[0, 120])
                fig2.add_hrect(y0=0, y1=50, fillcolor=px.colors.qualitative.Set3[0], opacity=0.3, line_width=0.2, annotation_text="<b>Good</b>")
                fig2.add_hrect(y0=50, y1=100, fillcolor=px.colors.qualitative.Set3[1], opacity=0.3, line_width=0.2, annotation_text="<b>Moderate</b>")
                fig2.add_hrect(y0=100, y1=120, fillcolor=px.colors.qualitative.Set3[3], opacity=0.3, line_width=0.2, annotation_text="<b>Unhealthy</b>")
                st.plotly_chart(fig2,use_container_width=True)
            with col4:
                caption2 = "From Monday to Saturday, the AQI remains in the same range, classified as <span style='color:yellow;font-weight:bold;'>Moderate</span>, while on Sunday, it reaches the <span style='color:red;font-weight:bold;'>Unhealthy</span> level."
                st.markdown(f"<p style='text-align: center; margin-top: 25%;'>{caption2}</p>", unsafe_allow_html=True)
                
    # Buat tab ketiga
    with tab3:
        year_filter1 = st.slider("Select Year", min_value=int(df['year'].min()), max_value=int(df['year'].max()), value=(int(df['year'].min()), int(df['year'].max())), key='slider_tab3')
        df_filtered1 = df[(df['year'] >= year_filter1[0]) & (df['year'] <= year_filter1[1])]
        use_stack_bar_tab3 = st.checkbox("Show Stack Bar (with min & max)", value=False, key='stack_bar_tab3')
        col18,col19 = st.columns([2,1], gap="medium")
        if use_stack_bar_tab3:
            col18,col19 = st.columns([2,1], gap="medium")
            with col18:
                df_bulan_stacked = df_filtered1.groupby('month').agg({'min': 'median', 'median': 'median', 'max': 'median'}).reset_index()
                fig3 = px.bar(df_bulan_stacked, x='month', y=['min', 'median', 'max'], title='Air Quality Index per Month', barmode='group')
                fig3.update_layout(xaxis_title='Month',yaxis_title='AQI', width=850, height=500, title_x=0.4, xaxis={'categoryorder':'array', 'categoryarray':['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']}, xaxis_showgrid=False, yaxis_showgrid=False)
                fig3.update_yaxes(range=[0, 185])
                fig3.add_hrect(y0=0, y1=50, fillcolor=px.colors.qualitative.Set3[0], opacity=0.3, line_width=0.2, annotation_text="<b>Good</b>")
                fig3.add_hrect(y0=50, y1=100, fillcolor=px.colors.qualitative.Set3[1], opacity=0.3, line_width=0.2, annotation_text="<b>Moderate</b>")
                fig3.add_hrect(y0=100, y1=185, fillcolor=px.colors.qualitative.Set3[3], opacity=0.3, line_width=0.2, annotation_text="<b>Unhealthy</b>")
                st.plotly_chart(fig3,use_container_width=True)
            with col19:
                caption3 = "In June and July, only the minimum AQI values have reached the <span style='color:yellow;font-weight:bold;'>Moderate</span> level, while the others remain at the <span style='color:green;font-weight:bold;'>Good</span> level."
                st.markdown(f"<p style='text-align: center; margin-top: 25%;'>{caption3}</p>", unsafe_allow_html=True)
        else:
            col20, col21 = st.columns([2,1], gap="medium")
            with col20:
                df_bulan = df_filtered1.groupby('month')['median'].median().reset_index()
                fig3 = px.bar(df_bulan, x='month', y='median', title='Air Quality Index per Month')
                fig3.update_layout(xaxis_title='Month',yaxis_title='AQI', width=850, height=500, title_x=0.4, xaxis={'categoryorder':'array', 'categoryarray':['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']}, xaxis_showgrid=False, yaxis_showgrid=False)
                fig3.update_yaxes(range=[0, 160])
                fig3.add_hrect(y0=0, y1=50, fillcolor=px.colors.qualitative.Set3[0], opacity=0.3, line_width=0.2, annotation_text="<b>Good</b>")
                fig3.add_hrect(y0=50, y1=100, fillcolor=px.colors.qualitative.Set3[1], opacity=0.3, line_width=0.2, annotation_text="<b>Moderate</b>")
                fig3.add_hrect(y0=100, y1=160, fillcolor=px.colors.qualitative.Set3[3], opacity=0.3, line_width=0.2, annotation_text="<b>Unhealthy</b>")
                st.plotly_chart(fig3,use_container_width=True)
            with col21:
                caption3 = "From May to October, the AQI consistently reaches <span style='color:red;font-weight:bold;'>Unhealthy</span> levels, with the peak occurring in June and July. Conversely, January has the lowest AQI levels, even though it falls within the <span style='color:yellow;font-weight:bold;'>Moderate</span> category."
                st.markdown(f"<p style='text-align: center; margin-top: 25%;'>{caption3}</p>", unsafe_allow_html=True)

    # Buat tab keempat
    with tab4:
        col22,col23 = st.columns([2,1], gap="medium")
        with col22:
            df_tahun = df.groupby(df['year'])['median'].median().reset_index()
            fig4 = px.line(df_tahun, x='year', y='median', title='Air Quality Index per Year', markers=True)
            fig4.update_layout(xaxis_title='Year', yaxis_title='Air Quality Index',width=850, height=500, title_x = 0.4, xaxis_showgrid=False, yaxis_showgrid=False)
            fig4.add_hrect(y0=0, y1=50, fillcolor=px.colors.qualitative.Set3[0], opacity=0.3, line_width=0.2, annotation_text="<b>Good</b>")
            fig4.add_hrect(y0=50, y1=100, fillcolor=px.colors.qualitative.Set3[1], opacity=0.3, line_width=0.2, annotation_text="<b>Moderate</b>")
            fig4.add_hrect(y0=100, y1=df['median'].max(), fillcolor=px.colors.qualitative.Set3[3], opacity=0.3, line_width=0.2, annotation_text="<b>Unhealthy</b>")
            fig4.add_vrect(x0=2020, x1=2022, fillcolor="lightgrey", opacity=0.7, line_width=0.2)
            fig4.add_annotation(text="Period of COVID-19 (PSBB/PPKM)", x=2021, y=110, showarrow=False, font=dict(family="monospace", size=16, color="black"))
            st.plotly_chart(fig4,use_container_width=True)
        with col23:
            caption4 = "The Air Quality Index tended to increase during the COVID-19 pandemic and started to declined again in 2023, reaching <span style='color:red;font-weight:bold;'>Unhealthy</span> levels."
            st.markdown(f"<p style='text-align: center; margin-top: 25%;'>{caption4}</p>", unsafe_allow_html=True)
    with tab5:
        with st.container():
            col9,col10 = st.columns([3,1])
            with col9:
                df = df[["date", "median"]]
                df.columns = ['ds', 'y']
                df['ds'] = pd.to_datetime(df['ds'])

                # Kontrol untuk jangka waktu prediksi
                forecast_period = st.slider("Choose Prediction Period (in days):", min_value=1, max_value=730, value=365)  # 730 hari untuk 2 tahun

                # Buat DataFrame untuk hari libur
                new_holidays = holidays.ID(years=[2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025], language="id")
                holiday_dates = []
                holiday_names = []
                for dt, name in sorted(new_holidays.items()):
                    holiday_dates.append(dt)
                    holiday_names.append(name)
                holiday_df = pd.DataFrame({'ds': pd.to_datetime(holiday_dates), 'holiday': holiday_names})

                # Fit model
                model = Prophet(holidays=holiday_df,changepoint_prior_scale=0.5)
                model.fit(df)
                
                future = model.make_future_dataframe(periods=forecast_period)
                forecast = model.predict(future)

                # Menampilkan grafik menggunakan plotly_chart di Streamlit
                st.plotly_chart(plot_plotly(model, forecast),use_container_width=True)
            with col10:
                caption5 = "Based on forecast using Prophet, air quality index (AQI) in Indonesia is expected to fall in 2024, despite a steady increase in AQI in Dec 2023 and Jan 2024."
                st.markdown(f"<p style='text-align: center; margin-top: 60%;'>{caption5}</p>", unsafe_allow_html=True)
            col11,col12 = st.columns([3,1])
            with col11:
                st.subheader("Prophet Components")
                # Menampilkan komponen-komponen grafik menggunakan plotly_chart di Streamlit
                st.plotly_chart(plot_components_plotly(model, forecast),theme=None,use_container_width=True)
            with col12:
                caption6 = "In the holidays chart, we can observe that Waisak Day is a public holiday, during which the AQI actually decreases compared to other holidays"
                st.markdown(f"<p style='text-align: center; margin-top: 70%;'>{caption6}</p>", unsafe_allow_html=True)

st.divider()
st.subheader("By Pollutant Composition")
col5,col6 = st.columns(2, gap="medium")

with col5:
    df = pd.read_csv("pollution_data.csv")

    # Bar chart for pollutant composition using Plotly
    selected_pollutants = ["CO", "NO", "NO2", "O3", "SO2", "PM2.5", "PM10", "NH3"]

    # Create a new DataFrame for selected pollutants
    df_selected_pollutants = df[selected_pollutants]

    # Sum the selected pollutants
    total_concentration = df_selected_pollutants.sum()

    # Plotly bar chart
    fig = px.bar(total_concentration, x=total_concentration.index, y=total_concentration.values, labels={'y':'Total Concentration (µg/m³)'},color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_traces(marker_color=px.colors.qualitative.Set3)
    fig.update_layout(
        title='Total Pollutant Composition (2020-2023)',
        xaxis_title='Pollutants',
        yaxis_title='Total Concentration (µg/m³)',
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Set transparent background
        plot_bgcolor='rgba(0, 0, 0, 0)',   # Set transparent background for the plot area
    )

    # Display Plotly chart in Streamlit
    st.plotly_chart(fig,use_container_width=True)
with col6 :
    # Convert the "DateTime" column to datetime type
    df['DateTime'] = pd.to_datetime(df['DateTime'])

    # Extract the hour from the "DateTime" column
    df['Hour'] = df['DateTime'].dt.hour

    # Group data by hour and sum the concentrations
    df_hourly = df.groupby('Hour')[selected_pollutants].mean()

    # Convert the index (hour) to custom format
    df_hourly.index = df_hourly.index.map(lambda x: f'{x} AM' if x < 12 else '12 PM' if x == 12 else f'{x-12} PM')

    # Line chart for hourly pollution levels using Plotly
    fig = px.line(df_hourly, x=df_hourly.index, y=df_hourly.columns, labels={'value':'Concentration (µg/m³)'}, 
                title='Average Hourly Pollution Composition',
                line_shape='linear', render_mode='svg', color_discrete_sequence=px.colors.qualitative.Set3)

    # Update layout for a more appealing appearance
    fig.update_layout(
        xaxis_title='Hour of the Day',
        yaxis_title='Concentration (µg/m³)',
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Set transparent background
        plot_bgcolor='rgba(0, 0, 0, 0)',   # Set transparent background for the plot area
    )

    # Display Plotly chart in Streamlit
    st.plotly_chart(fig,use_container_width=True)

col7,col8 = st.columns(2,gap="medium")
with col7 : 
    df['DateTime'] = pd.to_datetime(df['DateTime'])

    # Extract the day of the week from the "DateTime" column
    df['DayOfWeek'] = df['DateTime'].dt.day_name()

    # Define the desired order of days of the week
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Convert the "DayOfWeek" column to a categorical data type with the specified order
    df['DayOfWeek'] = pd.Categorical(df['DayOfWeek'], categories=day_order, ordered=True)

    # Group data by day of the week and sum the concentrations
    df_daily = df.groupby('DayOfWeek')[selected_pollutants].mean()

    # Bar chart for daily pollution levels using Plotly
    fig = px.bar(df_daily, x=df_daily.index, y=df_daily.columns, labels={'value':'Concentration (µg/m³)'}, 
                title='Average Daily Pollution Composition',
                color_discrete_sequence=px.colors.qualitative.Set3)

    # Update layout for a more appealing appearance
    fig.update_layout(
        xaxis_title='Day of the Week',
        yaxis_title='Concentration (µg/m³)',
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Set transparent background
        plot_bgcolor='rgba(0, 0, 0, 0)',   # Set transparent background for the plot area
    )

    # Display Plotly chart in Streamlit
    st.plotly_chart(fig,use_container_width=True)
with col8 : 
    df['DateTime'] = pd.to_datetime(df['DateTime'])

    # Extract the month from the "DateTime" column
    df['Month'] = df['DateTime'].dt.strftime('%B')  # %B returns the full month name

    # Define the desired order of months
    month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    # Convert the "Month" column to a categorical data type with the specified order
    df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)

    # Group data by month and sum the concentrations
    df_monthly = df.groupby('Month')[selected_pollutants].mean()

    # Bar chart for monthly pollution levels using Plotly
    fig = px.bar(df_monthly, x=df_monthly.index, y=df_monthly.columns, labels={'value':'Concentration (µg/m³)'}, 
                title='Average Monthly Pollution Composition',
                color_discrete_sequence=px.colors.qualitative.Set3)

    # Update layout for a more appealing appearance
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Concentration (µg/m³)',
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Set transparent background
        plot_bgcolor='rgba(0, 0, 0, 0)',   # Set transparent background for the plot area
    )

    # Display Plotly chart in Streamlit
    st.plotly_chart(fig,use_container_width=True)
col13,col14 = st.columns(2)
with col13:
    df['Year'] = df['DateTime'].dt.year

    # Group data by year and sum the concentrations
    df_yearly = df.groupby('Year')[selected_pollutants].sum()

    # Bar chart for yearly pollution levels using Plotly
    fig = px.bar(df_yearly, x=df_yearly.index, y=df_yearly.columns, labels={'value':'Concentration (µg/m³)'}, 
                title='Total Yearly Pollution Composition (Nov 2020 - Nov 2023)',
                color_discrete_sequence=px.colors.qualitative.Set3)

    # Update layout for a more appealing appearance
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Concentration (µg/m³)',
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Set transparent background
        plot_bgcolor='rgba(0, 0, 0, 0)',   # Set transparent background for the plot area

    )

    # Display Plotly chart in Streamlit
    st.plotly_chart(fig,use_container_width=True)
with col14:
    st.markdown("""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <style>
                        table {
                            width: 70%;
                            border-collapse: collapse;
                            margin-top: 20px;
                            margin-left: 25px
                        }

                        th, td {
                            border: 1px solid #dddddd;
                            text-align: center;
                            padding: 12px;
                            transition: background-color 0.3s ease, color 0.3s ease;
                        }

                        th {
                            background-color: #f2f2f2;
                        }

                        .id {
                            color: #FFFD8C;
                            text-decoration: none;
                            font-weight: bold;
                            font-size: 14px;
                            transition: color 0.3s ease;
                        }

                        .id:hover {
                            text-decoration: underline;
                            color: #ff4500;
                        }

                        tr:hover {
                            background-color: #f5f5f5;
                        }
                    </style>
                </head>
                <body>
                    <table>
                        <tr>
                            <th style='color:#183D3D;'>Insights</th>
                        </tr>
                        <tr>
                            <td><p class="id" >CO, or carbon monoxide, is the primary pollutant contributing to air pollution.</p></td>
                        </tr>
                        <tr>
                            <td><p class="id">Between 4 am and 9 am, pollutant levels significantly decrease, only to peak again between 2 pm and 5 pm.</p></td>
                        </tr>
                        <tr>
                            <td><p class="id">On Saturdays and Sundays, the overall pollutant levels tend to be lower compared to other days.</p></td>
                        </tr>
                        <tr>
                            <td><p class="id">The highest pollutant levels occur in June, while the lowest levels are observed at the beginning and end of the year, namely in January and December</p></td>
                        </tr>
                    </table>
                </body>
                </html>""",unsafe_allow_html=True)

st.divider()
st.subheader("Correlation")
with st.container():
    col24,col25 = st.columns(2)
    with col24:
        df = pd.read_csv('jakarta.csv')

        # Mengubah kolom 'time_code' menjadi tipe data datetime
        df['time_code'] = pd.to_datetime(df['time_code'], format='%Y%m%d %H:%M')

        # Menambahkan kolom baru 'date' yang berisi tanggal
        df['date'] = df['time_code'].dt.date

        # Melakukan pengelompokan (group by) berdasarkan tanggal dan menghitung median AQI
        result = df.groupby('date')['value'].median().reset_index()
        result = result.rename(columns={'value': 'TCI'})

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
        result_df['Air Quality Index'] = result_df['median']
        result_df['Traffic Congestion Index'] = result_df['TCI']
        # Create a correlation matrix
        correlation_matrix = result_df[['Traffic Congestion Index', 'Air Quality Index']].corr()

        fig = px.imshow(correlation_matrix,
                x=['TCI', 'AQI'],
                y=['TCI', 'AQI'],
                labels=dict(color='Correlation'),
                title='Correlation Heatmap between Traffic Congestion Index and Air Quality Index',
                )
        fig.update_traces(hovertemplate='Correlation: %{z:.2f}')
        # Update layout for a more appealing appearance
        fig.update_layout(
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Set transparent background
            plot_bgcolor='rgba(0, 0, 0, 0)',   # Set transparent background for the plot area
        )

        # Show the plot
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('**Conclusion**: The correlation between Traffic Congestion Index and Air Quality Index is :blue[0.06]. While there is a :blue[positive correlation], the strength is considered :red[very weak].')
    with col25:
        # Ambil data dari database
        conn = sqlite3.connect('pollution.db')
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT
                a.date,
                a.median AS dew,
                b.median AS humidity,
                d.median AS aqi,
                e.median AS pressure,
                f.median AS temperature,
                g.median AS wind_gust,
                h.median AS wind_speed
            FROM
                daily_aqi a
            JOIN daily_aqi b ON a.date = b.date
            JOIN daily_aqi c ON a.date = c.date
            JOIN daily_aqi d ON a.date = d.date
            JOIN daily_aqi e ON a.date = e.date
            JOIN daily_aqi f ON a.date = f.date
            JOIN daily_aqi g ON a.date = g.date
            JOIN daily_aqi h ON a.date = h.date
            WHERE
                a.indicator = 'dew'
                AND b.indicator = 'humidity'
                AND d.indicator = 'pm25'
                AND e.indicator = 'pressure'
                AND f.indicator = 'temperature'
                AND g.indicator = 'wind-gust'
                AND h.indicator = 'wind-speed'
            order by a.date 
            '''
        )
        rows = cursor.fetchall()
        # Menutup koneksi
        conn.close()

        aqi_df = pd.DataFrame(rows, columns=['date', 'dew', 'humidity', 'aqi', 'pressure', 'temp', 'wind_gust', 'wind_speed'])

        heatmap_data = aqi_df.drop(columns=['date'])
        
        # Create a heatmap using Plotly
        fig = px.imshow(heatmap_data.corr(),
                        x=heatmap_data.columns,
                        y=heatmap_data.columns,
                        labels=dict(color='Correlation'),
                        title='Correlation Heatmap between Air Quality Index and Weather Parameters',
                        )

        # Customize hover text to display correlation values
        fig.update_traces(hovertemplate='Correlation: %{z:.2f}')
        aqi_indices = [heatmap_data.columns.get_loc(col) for col in heatmap_data.columns if 'aqi' in col]

        # Update layout to focus on columns related to 'aqi'
        fig.update_layout(
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Set transparent background
            plot_bgcolor='rgba(0, 0, 0, 0)',   # Set transparent background for the plot area
            shapes=[
                dict(
                    type='rect',
                    xref='x',
                    yref='y',
                    x0=min(aqi_indices) - 0.5,
                    y0=min(aqi_indices) - 0.5,
                    x1=max(aqi_indices) + 0.5,
                    y1=max(aqi_indices) + 0.5,
                    line=dict(color='red', width=2),
                    fillcolor='rgba(255, 0, 0, 0.1)',  # Set the fill color to red with transparency
                )
            ],
            xaxis=dict(range=[min(aqi_indices) - 0.5, max(aqi_indices) + 0.5]),
            yaxis=dict(range=[min(aqi_indices) - 0.5, max(aqi_indices) + 0.5]),
        )
        # Show the plot
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('**Conclusion:** The correlation between Dew, Humidity, Wind Gust, and Wind Speed with AQI indicates a :red[negative relationship], while **Pressure (0.21)** and **Temperature (0.24)** show a :blue[positive correlation].')
    col26,col27,col28 = st.columns([1,2,1])
    with col27: 
        df = pd.read_csv('pollution_data.csv')

        # Mengubah kolom 'DateTime' menjadi tipe data datetime
        df['DateTime'] = pd.to_datetime(df['DateTime'])

        # Menambahkan kolom 'Date' yang berisi tanggal saja
        df['date'] = df['DateTime'].dt.date

        # Mengelompokkan berdasarkan tanggal dan menghitung median untuk setiap kolom
        result = df.groupby('date')[['CO', 'NO', 'NO2', 'O3', 'SO2', 'PM2.5', 'PM10', 'NH3']].median().reset_index()

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

        # Melakukan inner join dengan hasil sebelumnya berdasarkan kolom 'date'
        result_df = pd.merge(result, median_df, on='date', how='inner')

        # Mengganti nama kolom 'median' pada median_df menjadi 'aqi'
        result_df = result_df.rename(columns={'median': 'aqi'})
        # Menghapus kolom 'date' dari result_df
        result_df = result_df.drop(columns=['date'])

        # Membuat heatmap menggunakan Plotly
        fig = px.imshow(result_df.corr(),
                        x=result_df.columns,
                        y=result_df.columns,
                        labels=dict(color='Correlation'),
                        title='Correlation Heatmap between Air Quality Index & Pollutant Composition',
                        )

        # Customize hover text to display correlation values
        fig.update_traces(hovertemplate='Correlation: %{z:.2f}')

        # Update layout for a more appealing appearance
        fig.update_layout(
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Set transparent background
            plot_bgcolor='rgba(0, 0, 0, 0)',   # Set transparent background for the plot area
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**Conclusion** : The analysis reveals :blue[positive correlations], with **NO2** showing the :blue[strongest association (0.60)]. **PM2.5 and PM10** also exhibit a notable correlation of 0.52. **O3** has a lower positive correlation at 0.14.")


st.divider()
st.subheader("Health Impacts")
with st.container():
    col29,col30 = st.columns(2)
    with col29: 
        data = {
                'Disease Cause': ['Cardiovascular', 'Respiratory'],
                'PM2.5': [3043, 455],
                'O3': [1357, 182]
                    }
        df = pd.DataFrame(data)
        # Plot
        fig = px.bar(df, 
                     x='Disease Cause', 
                     y=['PM2.5', 'O3'], 
                     barmode='group', 
                     labels={'value': 'Number of Cases a Year', 'variable': 'Attributable Indicator'},
                     title='Number Cases of Disease by Attributable Indicators (Short Term)',
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Set transparent background
            plot_bgcolor='rgba(0, 0, 0, 0)',   # Set transparent background for the plot area
        )

        # Streamlit App
        st.plotly_chart(fig, use_container_width=True)
    with col30 :
       data = {
    'Health Outcome': ['Infant Deaths', 'Stunting', 'Low Birth Weight', 'Preterm Births', 'Mortality'],
    'Number of Cases': [327, 6153, 680, 62, 9692],
            }
       df = pd.DataFrame(data)
       fig = px.bar(df, x='Health Outcome', y='Number of Cases', barmode='group',
                    labels={'value': 'Number of Cases', 'variable': 'Air Pollution Attributable Indicator'},
                    title='Number of Cases by Health Outcomes (Long-Term)', color_discrete_sequence=px.colors.qualitative.Set2)
       fig.update_layout(
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Set transparent background
            plot_bgcolor='rgba(0, 0, 0, 0)',   # Set transparent background for the plot area
        )
        # Streamlit App
       st.plotly_chart(fig,use_container_width=True)
       with st.expander("see details") :
           st.markdown("Source: [International Journal of Enviromental Research and Public Healtj](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9963985/pdf/ijerph-20-02916.pdf)")
           rates_data = {
                "Infant Deaths": "2 per 1000 births",
                "Stunting": "7 per 1000 children under 5",
                "Low Birth Weight": "5 per 1000 births",
                "Preterm Births": "4 per 10,000 births",
                "Mortality (2019)": "88 per 100,000 population"
            }
           st.subheader("Rates:")
           for key, value in rates_data.items():
                st.write(f"{key}: {value}") 
st.subheader("Economic Impacts")
with st.container():
    col31,col32 = st.columns([1.5,1])
    with col31:
        categories = ['Infant Deaths', 'Stunting', 'Adverse Birth', 'Mortality', 'Hospitalizations']
        economic_cost = [92.93, 0.79, 1.10, 2842.41, 6.19]

        # Create DataFrame
        data = pd.DataFrame({'Categories': categories, 'Economic Cost (Million USD)': economic_cost})

        # Plotly bar chart
        fig = px.bar(data, x='Categories', y='Economic Cost (Million USD)',
                    title='Annual Economic Cost of Health Impact Due to Air Pollution',
                    color_discrete_sequence=px.colors.qualitative.Set2,
                    text='Economic Cost (Million USD)')
        fig.update_layout(
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Set transparent background
            plot_bgcolor='rgba(0, 0, 0, 0)',   # Set transparent background for the plot area
        )
        fig.update_yaxes(showgrid=False,showticklabels=False)
        # Display the chart
        st.plotly_chart(fig,use_container_width=True)
    with col32:
        st.markdown("""

1. **Short-Term Health Impact:**
   - Cardiovascular diseases show a higher number of cases than respiratory diseases due to PM2.5 and O3.

2. **Long-Term Health Impact:**
   - Stunting and mortality present notably high numbers of cases, emphasizing the chronic health burden of air pollution.

3. **Economic Consequences:**
   - The economic cost chart reveals substantial financial burdens, with notable contributions from infant deaths and mortality.
""")    
st.divider()
with st.container():
    st.subheader("Public Perception")
    st.caption("Source : Breathing in Jakarta by @Internews - 2022")
    col33,col34 = st.columns(2)
    with col33:
        # Data
        categories = [
            "Health Impact",
            "Ecological Impact",
            "Economic Impact",
            "Air Pollution Data",
            "High Pollution Notifications",
            "Prevention and Decrease",
            "Efforts to Improve Air Quality",
            "Causes of Pollution",
            "Others"
        ]
        percentages = [63.3, 28.1, 7.6, 33.3, 45.7, 35.7, 23.8, 19.5, 0.5]

        # Create DataFrame
        data = pd.DataFrame({'Categories': categories, 'Percentages': percentages})

        # Plotly horizontal bar chart
        fig = px.bar(data, x='Percentages', y='Categories', orientation='h',
                    labels={'Percentages': 'Percentage (%)', 'Categories': 'Information Categories'},
                    title='User Preferences on Air Pollution Information',
                    color='Percentages', color_continuous_scale='Viridis',
                    category_orders={"Categories": sorted(categories, key=lambda x: percentages[categories.index(x)], reverse=True)})

        # Display the chart
        st.plotly_chart(fig, use_container_width=True)
    with col34:
        challenges = [
        "Have No Time to Access Information",
        "Information is Difficult to Understand",
        "Have No Access to TV/Radio",
        "Have No Access to the Internet",
        "Do Not Trust the Information",
        "Have No Access to Local Authority",
        "No Available Information",
        "Lack of Knowledge of Information Sources",
        "Not Interested",
        "Others"
        ]
        percentages = [34.0, 19.1, 2.1, 0.0, 4.3, 20.2, 26.6, 57.4, 2.1, 7.4]

        # Create DataFrame
        data = pd.DataFrame({'Challenges': challenges, 'Percentages': percentages})

        # Plotly horizontal bar chart
        fig = px.bar(data, x='Percentages', y='Challenges', orientation='h',
                    labels={'Percentages': 'Percentage (%)', 'Challenges': 'Challenges'},
                    title='Challenges in Obtaining Information on Air Pollution',
                    color='Percentages', color_continuous_scale='Viridis',
                    category_orders={"Challenges": sorted(challenges, key=lambda x: percentages[challenges.index(x)], reverse=True)})

        # Plotly horizontal bar chart with y-axis on the right
        
        st.plotly_chart(fig, use_container_width=True)
    col35,col36 = st.columns(2)
    with col35: 
        st.markdown("**Conclusion 1: User Preferences on Air Pollution Information**\n\n"
            "The majority prioritize 'Health Impact' (63.3%) and 'High Pollution Notifications' (45.7%), "
            "indicating a strong concern for personal well-being and timely awareness of pollution levels. "
            "This insight can guide tailored communication strategies.")
    with col36:
        st.markdown("**Conclusion 2: Challenges in Obtaining Information**\n\n"
            "The top challenges include 'Lack of Knowledge of Information Sources' (57.4%) and "
            "'Have No Time to Access Information' (34.0%). Addressing these issues can improve accessibility "
            "and ensure that information is delivered in a way that fits into users' schedules.")
st.divider()