import streamlit as st
from streamlit.components.v1 import html

def read_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content

tes_html = read_file("tracker.html")
html(tes_html, height=1500)
