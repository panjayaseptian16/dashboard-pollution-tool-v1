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
            <h3 style="text-align: center;color:#1F4172;">Air Quality Realtime Monitoring</h3>
            """, unsafe_allow_html=True)

# Baca konten HTML dari berkas interactive_aqi_widget.html
tes_html = read_file("tes.html")

with st.container():
    html(tes_html, height=425)
    st.markdown(
    "<p style='margin-top:-25px; text-align: center; font-size: 14px; color:#1F4172;'>Air Quality Index (AQI) scale as defined by the US-EPA 2016 standard. Check details in <a href='https://aqicn.org/scale/'>here</a></p>",
    unsafe_allow_html=True)
st.markdown("""
            <h3 style="text-align: center;color:#1F4172;">Dashboard Pollution in Jakarta</h3>
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
            caption = "Air pollution in Jakarta is still a cause for concern, even though PM2.5 AQI has fluctuated from 2018 to 2023 and always decreased during the end and beginning of the year. The median PM2.5 AQI in Jakarta is still predominantly in the moderate and unhealthy range, which means that air pollution in Jakarta can still have a negative impact on the public. This implies that there hasn't been any effective policy or program to address this issue significantly."
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
            col3,col4 = st.columns([2,1],gap="small")
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