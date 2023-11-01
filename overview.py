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