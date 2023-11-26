import requests
import streamlit as st
from streamlit_lottie import st_lottie
from deta import Deta

# Inisialisasi objek Deta dan Deta Base
deta = Deta(st.secrets["data_key"])
db = deta.Base("db_test2")  # Ganti dengan nama database yang sesuai

st.set_page_config(
    page_title="Feedback & Suggestion",
    page_icon="📣",
    layout="centered",
    initial_sidebar_state="auto"
)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def on_submit(name, organization, message, rating):
    data = {
        "name": name,
        "organization": organization,
        "message": message,
        "rating": rating
    }
    db.put(data)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

lottie_hello = load_lottieurl("https://lottie.host/974f9f98-21ed-4e87-b8c7-77f0b9e59828/hmNqyLXK1s.json")

with st.container():
    col1, col2 = st.columns([1, 5], gap="small")
    with col1:
        st.lottie(lottie_hello, height=100, width=-20)
    with col2:
        st.markdown("""
                    <h1 style="margin-bottom: 0x; color:#FFFD8C; font-family: monospace;"> Get in touch With Us </h1>""", unsafe_allow_html=True)
        
with st.form("feedback_form"):
    name = st.text_input("Your name", value=None, max_chars=50, placeholder="Please insert your name")
    organization = st.text_input("Your organization (optional)", placeholder="Optional: Company, School, etc.")
    message = st.text_area("Your feedback or suggestions (please be as specific as possible)", value=None, placeholder="Share your thoughts...")

    st.markdown("Rate Our Project:")
    rating = st.radio("Select your rating:", options=[1, 2, 3, 4, 5], index=None, horizontal=True)

    submit_button = st.form_submit_button("Send")

    if submit_button:
        if not name or not message or not rating:
            st.error("Please fill out the form completely.")
        else:
            on_submit(name, organization, message, rating)
            st.success("Thanks for your support! 🔥")
