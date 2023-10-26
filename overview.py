import streamlit as st
from streamlit.components.v1 import html
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from streamlit_folium import folium_static
import folium


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

def read_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content

tes_html = read_file("map1.html")

col1, col2 = st.columns([4,1],gap='medium')
with col1:
        html(tes_html, height=425)
with col2:
        m = folium.Map(location=[-6.2088, 106.8456], zoom_start=11, control_scale=True)
        folium.TileLayer('openstreetmap').add_to(m)
        waqi_tile_layer = folium.TileLayer(
                tiles='https://tiles.aqicn.org/tiles/usepa-aqi/{z}/{x}/{y}.png?token=3f5ba5c57e7bbe5460dda6475203d0e5e91fb9b8',
                attr='Air Quality',
                name='Air Quality',
                overlay=True,
                control=True
            )
        waqi_tile_layer.add_to(m)
        folium.LayerControl().add_to(m)
        # Display the map in Streamlit
        folium_static(m)
        if col2.button('Reset'):
            m.location = [-6.2088, 106.8456]
            m.zoom_start = 11
