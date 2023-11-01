import json
import requests  # pip install requests
import streamlit as st  # pip install streamlit
from streamlit_lottie import st_lottie

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
    
lottie_linkedin = load_lottieurl("https://lottie.host/dd1c4c17-53c0-4286-aafb-6f8bd0fcf325/ostEkHil72.json")
lottie_hello = load_lottieurl("https://lottie.host/974f9f98-21ed-4e87-b8c7-77f0b9e59828/hmNqyLXK1s.json")

container = st.container()
col1, col2 = container.columns([1,5],gap="small")
with col1:
    st.lottie(lottie_hello, height=100, width=-20)
with col2:
    st.markdown("""
                <h1 style="margin-bottom: 0x; color:#1F4172; font-family: monospace;"> Get in touch With Us </h1>""", unsafe_allow_html=True)

def on_submit():
    st.success('Thank You for the feedback', icon="✅")

contact_form = """
<form action="https://formsubmit.co/panjayaseptian@gmail.com" method="POST">
     <input type="text" minlength=5 name="name" placeholder="Your name" required>
     <input type="text" name="organization" placeholder="Your organization (optional, but it would be helpful to know)">
     <textarea name="message" minlength=5 placeholder="Your feedback or suggestions (please be as specific as possible)" required></textarea>
     <input type="hidden" name="_captcha" value="false">
     <input type="hidden" name="_template" value="table">
     <input type="hidden" name="_next">
     <p>Rate Our Project:</p>
    <fieldset class="rating">
        <input type="radio" id="star5" name="rating" value="5" /><label class = "full" for="star5" title="Awesome - 5 stars"></label>
        <input type="radio" id="star4" name="rating" value="4" /><label class = "full" for="star4" title="Pretty good - 4 stars"></label>
        <input type="radio" id="star3" name="rating" value="3" /><label class = "full" for="star3" title="Meh - 3 stars"></label>
        <input type="radio" id="star2" name="rating" value="2" /><label class = "full" for="star2" title="Kinda bad - 2 stars"></label>
        <input type="radio" id="star1" name="rating" value="1" /><label class = "full" for="star1" title="Terrible - 1 star"></label>
    </fieldset>
     <button type="submit">Send</button>
</form> 
"""
st.markdown(contact_form, unsafe_allow_html=True)

def on_submit():
    st.success('Terima kasih atas masukannya', icon="✅")

def local_css(file_name):
    with open(file_name) as f:
        container.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/style.css")