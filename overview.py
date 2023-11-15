import streamlit as st
from streamlit.components.v1 import html
import requests
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from st_pages import show_pages_from_config, add_page_title

st.set_page_config(
    layout="wide",
    initial_sidebar_state="auto")



# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar
show_pages_from_config()


# Adding a sidebar with the required elements
#with st.sidebar:
#    st.subheader("Created by : ")
#    st.markdown("""<h3 style='text-align:center;'>Septian Panjaya</h3>""", unsafe_allow_html=True)
#    col3, col4 = st.columns(2)
#    with col3:
#        st.markdown("[![Linkedin](https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg)](https://www.linkedin.com/in/septian-panjaya)")

#st.markdown(
#    """
#    <style>
 #   .sidebar .sidebar-content {
 #       position: fixed;
  #      max-width: 220px;
   #     padding: 2rem;
    #}
    #</style>
    #""",
#    unsafe_allow_html=True,
#)


st.markdown("""
          <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome! Pollution Ranger</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f3f3f3;
            font-family: 'Arial', sans-serif;
        }

        .text-container {
            text-align: center;
            position: relative;
            top: 50%;
            transform: translateY(-50%);
        }

        .text {
            font-size: 3rem;
            white-space: nowrap;
            overflow: hidden;
            border-right: 0.15em solid;
            animation: animate-text 5s infinite;
            transition: all 0.3s ease;
        }

        .text:hover {
            color: #ff9900;
            transform: scale(1.2);
        }

        @keyframes animate-text {
            0% {
                color: #ff0000;
            }
            10% {
                color: #ff7f00;
            }
            20% {
                color: #ffff00;
            }
            30% {
                color: #00ff00;
            }
            40% {
                color: #00ff7f;
            }
            50% {
                color: #00ffff;
            }
            60% {
                color: #007fff;
            }
            70% {
                color: #0000ff;
            }
            80% {
                color: #7f00ff;
            }
            90% {
                color: #ff00ff;
            }
            100% {
                color: #ff0000;
            }
        }
    </style>
</head>
<body>
    <div class="text-container">
        <h1 class="text">Welcome! Pollution Ranger</h1>
    </div>
</body>
</html>
""", unsafe_allow_html=True
)

from streamlit_lottie import st_lottie

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

about_project = load_lottieurl("https://lottie.host/096edf35-97f9-402a-ab07-13438c3190a2/O6iG18SZ9B.json")
features = load_lottieurl("https://lottie.host/6ef5a986-33d7-4dcc-8920-d473e3b2db36/bTb56aUDUm.json")
st.empty()
col1, col2 = st.columns([1.5, 1], gap="small")

with col1:
    st.markdown("<h3 style='text-align: center;color: #008080;'>About Our Project</h3>", unsafe_allow_html=True)
    st.markdown(
    """
    <p style='text-align: center;'>Air pollution is a <span style='color: #008080; font-weight: bold;'>persistent threat</span> in Jakarta, with the air quality consistently at unhealthy levels for the past 5 years.</p>
    <p style='text-align: center;'>Our mission is to <span style='color: #008080; font-weight: bold;'>raise awareness</span> and prompt action. Through our website, we provide real-time air quality data and temperature monitoring, empowering individuals to track their contributions to pollution.</p>
    <p style='text-align: center;'>Recognizing the urgency, we foster a community-driven effort through the <span style='color: #008080; font-weight: bold;'>Pollution Ranger task force</span>. These dedicated individuals monitor and address air pollution within their communities, advocating for change and inspiring others to join the cause.</p>
    """, unsafe_allow_html=True)
with col2:
    st_lottie(about_project, speed=1, reverse=False, loop=True, height=300)

col3,col4 = st.columns([1,3],gap="small")
with col4: 
    st.markdown("<h3 style='text-align: center;color: #4169E1;'>Features</h3>", unsafe_allow_html=True)
    st.markdown(':chart_with_upwards_trend: :blue[Dashboard] : Real-time monitoring of AQI (Air Quality Index) and temperature, along with visualization of pollution conditions in Jakarta.')
    st.markdown(':male-detective: :green[Deep Analysis] : Advanced analysis of pollution data that includes recommendations and ideas for improvement.')
    st.markdown(":ballot_box_with_check: :rainbow[Knowledge Check] : A feature to assess the user's knowledge about air pollution, including statistics (Developer only).")
    st.markdown(":bookmark: :orange[Personal Pollution Tracker] : A calculator to measure or track the amount of pollution or emissions generated in daily activities, including statistics (Developer only).")
    st.caption("*NOTE : It is highly recommended to use a desktop or laptop web browser. However, if you prefer using a smartphone, make sure to enable desktop mode (in Chrome) and use it in landscape orientation.*")
with col3: 
    st_lottie(features, speed=1, reverse=False, loop=True, height=300)

with st.container():
    st.markdown("<h3 style='text-align: center;color: #FF6347;'>Our Team</h3>", unsafe_allow_html=True)
    col5,col6,col7,col8,col9 = st.columns(5, gap="small")
    with col6:
       st.markdown("""
            <style>
                .our-team {
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: center;
                }

                .profile {
                    margin: 20px;
                    padding: 20px;
                    text-align: center;
                    background-color: #F0FFFF;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    width: 200px;
                    transition: background-color 0.3s;
                }

                .profile:hover {
                    background-color: #AFEEEE;
                }

                .profile img {
                    width: 120px;
                    height: 120px;
                    border-radius: 50%;
                    object-fit: cover;
                    margin-bottom: 15px;
                }

                .profile h3 {
                    font-size: 15px;
                    margin-bottom: 10px;
                }

                .profile a button {
                    background-color: #f08080;
                    color: #fff;
                    border: none;
                    padding: 8px 12px;
                    border-radius: 5px;
                    cursor: pointer;
                    transition: background-color 0.3s;
                }

                .profile a button:hover {
                    background-color: #2980b9;
                }
            </style>
            """,unsafe_allow_html=True)
       st.markdown("""
            <h3 style='text-align:center;font-size:20px;'> Team Leader </h3>
            <div class="our-team">
                <div class="profile">
                    <img src="https://drive.google.com/uc?export=view&id=1S2YdHLmzTA-m6qCHvbsFeQSfNg1_S7Uc" alt="">
                    <h3 style='color:#183D3D;'>Septian Panjaya</h3>
                    <a href="https://www.linkedin.com/in/septian-panjaya"><button>LinkedIn</button></a>
                </div>
            </div>
            """,unsafe_allow_html=True)
    with col8: 
       st.markdown("""
            <style>
                .our-team {
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: center;
                }

                .profile {
                    margin: 20px;
                    padding: 20px;
                    text-align: center;
                    background-color: #F0FFFF;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    width: 200px;
                    transition: background-color 0.3s;
                }

                .profile:hover {
                    background-color: #AFEEEE;
                }

                .profile img {
                    width: 120px;
                    height: 120px;
                    border-radius: 50%;
                    object-fit: cover;
                    margin-bottom: 15px;
                }

                .profile h3 {
                    font-size: 15px;
                    margin-bottom: 10px;
                }

                .profile a button {
                    background-color: #f08080;
                    color: #fff;
                    border: none;
                    padding: 8px 12px;
                    border-radius: 5px;
                    cursor: pointer;
                    transition: background-color 0.3s;
                }

                .profile a button:hover {
                    background-color: #2980b9;
                }
            </style>
            """,unsafe_allow_html=True)
       st.markdown("""
            <h3 style='text-align:center;font-size:20px;'> Team Member </h3>
            <div class="our-team">
                <div class="profile">
                    <img src="https://drive.google.com/uc?export=view&id=1cP4zUoHT6XjW_imoDDFDvnLJn37OKr8o" alt="">
                    <h3 style='color:#183D3D;'>Katon Bagaskara</h3>
                    <a href="https://www.linkedin.com/in/katonbk"><button>LinkedIn</button></a>
                </div>
            </div>
            """,unsafe_allow_html=True)
    col10,col11,col12,col13,col14 = st.columns(5, gap="small")
    with col12:
        st.markdown("""
            <style>
                .our-team {
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: center;
                }

                .profile {
                    margin: 20px;
                    padding: 20px;
                    text-align: center;
                    background-color: #F0FFFF;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    width: 200px;
                    transition: background-color 0.3s;
                }

                .profile:hover {
                    background-color: #AFEEEE;
                }

                .profile img {
                    width: 120px;
                    height: 120px;
                    border-radius: 50%;
                    object-fit: cover;
                    margin-bottom: 15px;
                }

                .profile h3 {
                    font-size: 18px;
                    margin-bottom: 10px;
                }

                .profile a button {
                    background-color: #f08080;
                    color: #fff;
                    border: none;
                    padding: 8px 12px;
                    border-radius: 5px;
                    cursor: pointer;
                    transition: background-color 0.3s;
                }

                .profile a button:hover {
                    background-color: #2980b9;
                }
            </style>
            """,unsafe_allow_html=True)
        st.markdown("""
            <h3 style='text-align:center;font-size:20px;'> Team Coach </h3>
            <div class="our-team">
                <div class="profile">
                    <img src="https://drive.google.com/uc?export=view&id=151O1cYGzt7IavTX8j2r4XlB0Q-g-tkWV" alt="">
                    <h3 style='color:#183D3D;'>I Wayan Nadiantara</h3>
                    <a href="https://www.linkedin.com/in/nadiantara"><button>LinkedIn</button></a>
                </div>
            </div>
            """,unsafe_allow_html=True)

st.markdown(
    """
    <style>
        hr.rainbow {
            height: 1px;
            border: 0;
            background: linear-gradient(to right, violet, indigo, blue, green, yellow, orange, red);
        }
    </style>
    """,
    unsafe_allow_html=True)

st.markdown("<hr class='rainbow'>", unsafe_allow_html=True)